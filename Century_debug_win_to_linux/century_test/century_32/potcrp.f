
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      subroutine potcrp (month,cancvr)

      implicit none
      include 'comput.inc'
      include 'const.inc'
      include 'dovars.inc'
      include 'param.inc'
      include 'parcp.inc'
      include 'parfx.inc'
      include 'plot1.inc'
      include 'plot3.inc'
      include 'potent.inc'
      include 'seq.inc'
      include 'site.inc'
      include 'wth.inc'

c ... Argument declarations
      integer month
      real    cancvr

c ... Compute monthly production potential based upon montly precip
c ... and restrict potential production based upon method specified
c ... by grzeff.

c ... Function declarations
      real     gpdf, pevap, pprdwc, shwave
      external gpdf, pevap, pprdwc, shwave

c ... Local variables
      real     agprod, aisc, bgp, bgprod, bio, bioc, biof,
     &         bioprd, ctemp, fracrc, potprd, ratlc, rtsh, sdlng,
     &         shdmod, subcan, temp1, temp2, temp3, tmns, tmxs

c ... Compute shading modifier for savanna
      if (cursys .eq. SAVSYS) then
        if (cancvr .le. 0.001) then
          aisc = 0.
        else
          aisc = 5 * exp(-.0035 * (rleavc*2.5)/cancvr)
        endif
        subcan = aisc/(aisc + 1.)
        shdmod = (1.0-cancvr) + (cancvr*subcan)
      else
        shdmod = 1.0
      endif

c ... Value for potential plant production is now calculated from the
c ... equation of a line whose intercept changes depending on water
c ... content based on soil type.  The function PPRDWC contains the
c ... equation for the line.

      pet = pevap(month)
      if (pet .ge. .01) then
        h2ogef(1) = (avh2o(1) + prcurr(month) + irract)/pet
      else
        h2ogef(1) = 0.01
      endif

      h2ogef(1) = pprdwc(wc,h2ogef(1),pprpts)

c ... Estimate plant production:
      if (stemp .gt. 0.0) then

c ..... Calculate temperature effect on growth

c ..... Removal of litter effects on soil temperature as it 
c ..... drives plant production (keith paustian)
        bio = aglivc * 2.5
        bio = min(bio,pmxbio)

c ..... Maximum temperature
        tmxs=maxtmp(month)+(25.4/(1.+18.*exp(-.20*maxtmp(month))))*
     &       (exp(pmxtmp*bio)-.13)

c ..... Minimum temperature
        tmns=mintmp(month)+pmntmp*bio-1.78

c ..... Average surface temperature
        ctemp=(tmxs+tmns)/2.

        potprd = gpdf(ctemp, ppdf(1,1), ppdf(2,1), ppdf(3,1), 
     &                ppdf(4,1))

c ..... Calculate biof
        if (bioflg .eq. 1) then

c ....... Calculate maximum potential effect of standing dead on plant growth
c ....... (the effect of physical obstruction of litter and standing dead)
          bioc = stdedc + .1*strucc(SRFC)
          if (bioc .le. 0.) then
            bioc = .01
          endif

          if (bioc .gt. pmxbio) then
            bioc = pmxbio
          endif
          bioprd = 1. - (bioc/(biok5+bioc))

c ....... Calculate the effect of the ratio of live biomass to dead biomass
c ....... on the reduction of potential growth rate.  The intercept of this 
c ....... equation ( highest negative effect of dead plant biomass ) is equal
c ....... to bioprd when the ratio is zero.
          temp1 = (1. - bioprd)
          temp2 = temp1*0.75
          temp3 = temp1*0.25
          ratlc = aglivc/bioc 
          if (ratlc .le. 1.0) then
            biof = bioprd+(temp2*ratlc)
          endif
          if (ratlc .gt. 1.0 .and. ratlc .le. 2.0) then
            biof = (bioprd+temp2)+temp3*(ratlc-1.)
          endif
          if (ratlc .gt. 2.0) then
            biof = 1.0
          endif
        else
          biof = 1.0
        endif

c ..... Restriction on seedling growth
c ..... sdlng is the fraction that prdx is reduced
        if (aglivc .gt. fulcan) then
          seedl = 0
        endif

        if (seedl .eq. 1) then
          sdlng = min(1.0, pltmrf + aglivc*(1-pltmrf) /fulcan)
        else
          sdlng = 1.0
        endif

c ..... Add call to new subroutine for calculating photo period effect
c ..... on growth, in the fall, when the day length is decreasing,
c ..... growth will slow down.  The definition of PRDX(1) has been
c ..... changed, it now represents the coefficient for calculating the
c ..... potential aboveground monthly production as a function of
c ..... solar radiation outside of the atmosphere.  cak - 08/26/02
c ..... Calculate potential production (biomass)
c        agprod = shwave(month,sitlat) * prdx(1) * potprd * h2ogef(1) *
c     &           biof * shdmod * sdlng * co2cpr(CRPSYS)
c ..... Compute total production, cak - 08/22/03
        tgprod = shwave(month,sitlat) * prdx(1) * potprd * h2ogef(1) *
     &           biof * shdmod * sdlng * co2cpr(CRPSYS)

c ..... Dynamic carbon allocation routines for crop/grsss, used to compute
c ..... root/shoot ratio, cak - 07/01/02
c ..... Do not call the dynamic carbon allocation routine when there is no
c ..... production, cak - 09/09/02
        if (tgprod .gt. 0.0) then
          call cropDynC(rtsh, fracrc)
        else
          tgprod = 0.0
          agp = 0.0
          pcropc = 0.0
          goto 40
        endif

cc ..... Change root/shoot ratio if burning occurs
c        if (dofire(CRPSYS).or.dofire(SAVSYS)) then
c          rtsh = rtsh + frtsh
c        endif

c ..... Change root/shoot ratio by effect of CO2
        rtsh = rtsh * co2crs(CRPSYS)

c ..... Use the fraction of carbon allocated to the roots rather than
c ..... root to shoot ratio to determine amount of aboveground and
c ..... belowground production, cak - 08/22/03
c        bgprod = agprod * rtsh
        bgprod = tgprod * fracrc
        agprod = tgprod - bgprod

        agp = agprod
        bgp = bgprod
        tgprod = agp + bgp
      else
c ..... No production this month
        tgprod = 0.0
        agp = 0.0
        pcropc = 0.0
        goto 40
      endif

c ... Determine if grazing occurs
      if (dograz) then
        call grazrst(agp, bgp, flgrem, gremb, grzeff, rtsh, tgprod)
      endif

c ... Update accumulators & compute potential C production
      ptagc = ptagc + agp/2.5
      ptbgc = ptbgc + bgp/2.5
      pcropc = tgprod / 2.5

40    continue

      return
      end
