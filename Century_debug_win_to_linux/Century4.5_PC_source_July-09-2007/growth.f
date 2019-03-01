
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      subroutine growth()

      implicit none
      include 'comput.inc'
      include 'const.inc'
      include 'dovars.inc'
      include 'fertil.inc'
      include 'isovar.inc'
      include 'param.inc'
      include 'parcp.inc'
      include 'parfx.inc'
      include 'plot1.inc'
      include 'plot2.inc'
      include 'potent.inc'
      include 'seq.inc'
      include 'site.inc'
      include 'zztim.inc'

c ... Simulate production for the month.

c ... Fortran to C prototype
      INTERFACE
        SUBROUTINE flow(from, to, when, howmuch)
          !MS$ATTRIBUTES ALIAS:'_flow' :: flow
          REAL from
          REAL to
          REAL when
          REAL howmuch
        END SUBROUTINE flow
      END INTERFACE

c ... Function declarations
      real      fsfunc, rtimp
      external  fsfunc, rtimp

c ... Local variables
      integer   iel, lyr
      real      accum(ISOS)
      real      agfrac, amt, availm(MAXIEL),
     &          bgfrac, calcup, cfrac(CPARTS),
     &          euf(CPARTS), fsol,
     &          gnfrac, mcprd(CPARTS), rimpct,
     &          tm, uptake(4,MAXIEL), toler,
     &          mrspFlowShoots, mrspFlowRoots, mrspTempEffect
      real      cropNfix

      if (tave .le. -999.0) then
        write(*,*) 'Error in growth, tave = ', tave
        STOP
      endif

      toler = 1.0E-30

c ... Initialize monthly production and uptake variables
      do  5 iel = 1, nelem
        uptake(ESTOR,iel) = 0.0
        uptake(ESOIL,iel) = 0.0
        uptake(ENFIX,iel) = 0.0
        uptake(EFERT,iel) = 0.0
5     continue

      accum(UNLABL) = 0.0
      accum(LABELD) = 0.0

      mcprd(ABOVE) = 0.0
      mcprd(BELOW) = 0.0
      mrspflow(CRPSYS) = 0.0

c ... Determine actual production values, restricting the C/E ratios
      if (crpgrw .eq. 1 .and. pcropc .gt. 0.0 .and. .not. dosene)
     &    then

c ..... Calculate impact of root biomass on available nutrients
        rimpct = rtimp(riint, rictrl, bglivc)

c ..... Calculate carbon fraction in each part
        cfrac(ABOVE) = agp / tgprod
        cfrac(BELOW) = 1.0 - cfrac(ABOVE)

c ..... Determine nutrients available to plants for growth.
        do 10 iel = 1, nelem
          availm(iel) = 0.0
c ....... Nutrients available to grasses/crops are in the top claypg layers,
c ....... cak 01/29/03
c          do 15 lyr = 1, nlayer
          do 15 lyr = 1, claypg
            availm(iel) = availm(iel) + minerl(lyr, iel)
15        continue
10      continue

c ..... Calculate savanna available fractions
        if (cursys .eq. SAVSYS) then
          tm = MIN(availm(N), 1.5)
          gnfrac = exp(-1.664*exp(-.00102*tm*sitpot)*basfc2*trbasl)
c ....... Bound GNFRAC between 0 and 1
          gnfrac = MIN(gnfrac, 1.0)
          gnfrac = MAX(gnfrac, 0.0)
          do 70 iel = 1, nelem
            availm(iel) = availm(iel) * gnfrac
70        continue
        endif

c ..... Determine actual production values, restricting the C/E ratios
        call restrp(elimit, nelem, availm, cercrp, CPARTS, cfrac,
     &              pcropc, rimpct, crpstg, snfxmx(CRPSYS), cprodc,
     &              eprodc, uptake, crop_a2drat, cropNfix, relyld)

c ..... If growth occurs...
        if (cprodc .gt. 0.) then

c ....... Calculations for symbiotic N fixation accumulators moved
c ....... from nutrlm subroutine, cak - 10/17/02
c ....... Compute N fixation which actually occurs and add to the
c ....... N fixation accumulator.
          nfix = nfix + cropNfix
          snfxac(CRPSYS) = snfxac(CRPSYS) + cropNfix
c ....... Add computation for nfixac -mdh 1/16/02
          nfixac = nfixac + cropNfix

c ....... Update accumulators for N, P, and S uptake
          do 20 iel = 1, nelem
            eupacc(iel) = eupacc(iel) + eprodc(iel)
c ......... eup(ABOVE) is the fraction of element allocated to aboveground
c ......... eup(BELOW) is the fraction of element allocated to belowground
            eupaga(iel) = eupaga(iel) + eup(ABOVE,iel)
            eupbga(iel) = eupbga(iel) + eup(BELOW,iel)
20        continue

c ....... C/N ratio for production
          tcnpro = cprodc/eprodc(N)

c ....... Added maintenance respiration (mrspflow) calculation. -mdh 2/99
c ....... Growth of shoots
          agfrac = agp/tgprod
          mcprd(ABOVE) = cprodc * agfrac
          mrspFlowShoots = mcprd(ABOVE) * kmrsp(CRPSYS)
          mrspflow(CRPSYS) = mrspflow(CRPSYS) + mrspFlowShoots
          call csched(mcprd(ABOVE),cisofr,1.0,
     &                csrsnk(UNLABL),aglcis(UNLABL),
     &                csrsnk(LABELD),aglcis(LABELD),
     &                1.0,agcisa)

c ....... Growth of roots
          bgfrac = 1.0 - agfrac
          mcprd(BELOW) = cprodc * bgfrac
          mrspFlowRoots = mcprd(BELOW) * kmrsp(CRPSYS)
          mrspflow(CRPSYS) = mrspflow(CRPSYS) + mrspFlowRoots
          call csched(mcprd(BELOW),cisofr,1.0,
     &                csrsnk(UNLABL),bglcis(UNLABL),
     &                csrsnk(LABELD),bglcis(LABELD),
     &                1.0,bgcisa)

c ....... Added maintenance respiration (mrspflow) flow. -mdh 2/99
c ....... Maintenance respiration flows are added to maintenance
c ....... respiration storge pool, mdh - 7/6/01
          call csched(mrspflow(CRPSYS),cisofr,1.0,
     &                csrsnk(UNLABL),mrspstg(CRPSYS,UNLABL),
     &                csrsnk(LABELD),mrspstg(CRPSYS,LABELD),
     &                1.0,accum)

c ....... Maintenance respiration fluxes reduce maintenance respiration
c ....... storage pool, mdh - 9/4/01
          mrspTempEffect = 0.1 * exp(0.07 * tave)
c ....... Bound maintenance respiration temperature effect between 0.0 and 1.0,
c ....... cak - 09/16/02
          mrspTempEffect = min(1.0, mrspTempEffect)
          mrspTempEffect = max(0.0, mrspTempEffect)
          cmrspflux(ABOVE) = ckmrspmx(ABOVE) * mrspTempEffect * aglivc
          cmrspflux(BELOW) = ckmrspmx(BELOW) * mrspTempEffect * bglivc
          mrspann(CRPSYS) = mrspann(CRPSYS) + cmrspflux(ABOVE) +
     &                      cmrspflux(BELOW)
          call csched(cmrspflux(ABOVE),cisofr,1.0,
     &                mrspstg(CRPSYS,UNLABL),csrsnk(UNLABL),
     &                mrspstg(CRPSYS,LABELD),csrsnk(LABELD),
     &                1.0,accum)
          call csched(cmrspflux(BELOW),cisofr,1.0,
     &                mrspstg(CRPSYS,UNLABL),csrsnk(UNLABL),
     &                mrspstg(CRPSYS,LABELD),csrsnk(LABELD),
     &                1.0,accum)

c ....... Actual uptake
          do 40 iel = 1, nelem
            euf(ABOVE) = eup(ABOVE,iel) /eprodc(iel)
            euf(BELOW) = eup(BELOW,iel) /eprodc(iel)

c ......... Take up nutrients from internal storage pool
c ......... Don't allow uptake from storage if crpstg is negative,
c ......... cak 07/21/03
            if (crpstg(iel) .gt. 0.0) then
              amt = uptake(ESTOR,iel) * euf(ABOVE)
              call flow(crpstg(iel),aglive(iel),time,amt)
              amt = uptake(ESTOR,iel) * euf(BELOW)
              call flow(crpstg(iel),bglive(iel),time,amt)
            endif

c ......... Take up nutrients from soil
c ......... Nutrients for uptake are available in the top claypg layers,
c ......... cak 01/29/03
c            do 30 lyr = 1, nlayer
            do 30 lyr = 1, claypg
              if (minerl(lyr,iel) .gt. toler) then
                fsol = 1.0
                if (iel .eq. P) then
                  fsol = fsfunc(minerl(SRFC,P), pslsrb, sorpmx)
                endif
                calcup = uptake(ESOIL,iel) *
     &                   minerl(lyr,iel) * fsol / availm(iel)
                amt = calcup * euf(ABOVE)
                call flow(minerl(lyr,iel),aglive(iel),time,amt)
                amt = calcup * euf(BELOW)
                call flow(minerl(lyr,iel),bglive(iel),time,amt)
              endif
30          continue

c ......... Take up nutrients from nitrogen fixation
            if (iel .eq. N .and. cropNfix .gt. 0) then
              amt = uptake(ENFIX,iel) * euf(ABOVE)
              call flow(esrsnk(iel),aglive(iel),time,amt)
              amt = uptake(ENFIX,iel) * euf(BELOW)
              call flow(esrsnk(iel),bglive(iel),time,amt)
            endif

c ......... Take up nutrients from fertilizer
            if (aufert .ne. 0 .and. uptake(EFERT,iel) .gt. 0.0) then

c ........... Automatic fertilizer added to plant pools
              amt = uptake(EFERT,iel) * euf(ABOVE)
              call flow(esrsnk(iel),aglive(iel),time,amt)
              amt = uptake(EFERT,iel) * euf(BELOW)
              call flow(esrsnk(iel),bglive(iel),time,amt)

c ........... Automatic fertilizer added to mineral pool
              amt = uptake(EFERT,iel) * (1./favail(iel) - 1.)  
              fertot(iel) = fertot(iel) + uptake(EFERT,iel) + amt
              fertac(iel) = fertac(iel) + uptake(EFERT,iel) + amt
              call flow(esrsnk(iel),minerl(SRFC,iel),time,amt)
            endif
40        continue
        endif

c ... Else no production this month
      else
        cprodc = 0.0
        do 50 iel = 1, nelem
          eprodc(iel) = 0.0
50      continue
      endif

      return
      end
