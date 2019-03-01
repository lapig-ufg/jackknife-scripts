
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      subroutine simsom()

      implicit none
      include 'comput.inc'
      include 'const.inc'
      include 'doubles.inc'
      include 'dovars.inc'
      include 'fertil.inc'
      include 'ligvar.inc'
      include 'param.inc'
      include 'parfs.inc'
      include 'parfx.inc'
      include 'pheno.inc'
      include 'plot1.inc'
      include 'plot2.inc'
      include 'plot3.inc'
      include 'seq.inc'
      include 'site.inc'
      include 't0par.inc'
      include 'timvar.inc'
      include 'wth.inc'
      include 'zztim.inc'

c ... Simulate flow of carbon, nitrogen, phosphorous, and sulfur.
c ... This routine is executed each time step.  It calls the decomposition
c ... submodel and a producer submodel.  It also includes a bunch of
c ... N fixation stuff that needs to be rewritten and put in its own routine.
c ...
c ... Added new local variable FSOL.  Added calls to new function FSFUNC
c ... to calculate the amount of mineral P that is in solution.  Added
c ... call to new subroutine PSCHEM, which calculates and schedules the
c ... Phosophorus and Sulfur flows during decomposition.  Previously
c ... this was calculated in the DECOMP routine.  -rm 6/91

c ... Fortran to C prototype
      INTERFACE

        SUBROUTINE daylen(month, sitlat, tmplen)
          !MS$ATTRIBUTES ALIAS:'_daylen' :: daylen
          INTEGER month
          REAL    sitlat
          REAL    tmplen
        END SUBROUTINE daylen

        SUBROUTINE flow(from, to, when, howmuch)
          !MS$ATTRIBUTES ALIAS:'_flow' :: flow
          REAL from
          REAL to
          REAL when
          REAL howmuch
        END SUBROUTINE flow

        SUBROUTINE flowup(time)
          !MS$ATTRIBUTES ALIAS:'_flowup' :: flowup
          REAL time
        END SUBROUTINE flowup

        SUBROUTINE flowup_double(time)
          !MS$ATTRIBUTES ALIAS:'_flowup_double' :: flowup_double
          REAL time
        END SUBROUTINE flowup_double

        SUBROUTINE flowup_double_in(time)
          !MS$ATTRIBUTES ALIAS:'_flowup_double_in' :: flowup_double_in
          REAL time
        END SUBROUTINE flowup_double_in

        SUBROUTINE flowup_double_out(time)
          !MS$ATTRIBUTES ALIAS:'_flowup_double_out' :: flowup_double_out
          REAL time
        END SUBROUTINE flowup_double_out

      END INTERFACE

c ... Function declarations
      real      fsfunc
      external  fsfunc

c ... Local variables
      integer   iel, kts, lyr, iso
      real      basf, biof, cancvr, cmn
      real      frlech(MAXIEL), fsol, fwdfx, fxbiom
      real      satm, sirr, stot, tbiom, texeff, tmplen
      real      wdbmas, wdfnp, wdfxm, bgwfunc

c ... Initialize local variables
      cancvr = 0.0

c ... Added below for savanna model (rm)
      if (cursys .eq. SAVSYS ) then
        wdbmas = (fbrchc + rlwodc) * 2.0
c ..... Can get a divide by zero error when there is no wood biomass,
c ..... add a minimum wood biomass so that trees can grow from nothing,
c ..... cak - 10/08/02
        if (wdbmas .le. 0.0) then
          wdbmas = 50
        endif
c ..... Change the way that tree basal area is calculated,
c ..... cak 12/19/01
c        trbasl = wdbmas / basfct
        basf = (wdbmas/(0.88 * ((wdbmas * 0.01)**0.635)))
        if (basf .lt. 250.0) then
          basf = basf * basfct
        endif
        trbasl = wdbmas / basf
        cancvr = 1 - exp(-0.064 * trbasl)
        if (trbasl .le. 1.0E-6) then
c          trbasl = 0.1
          trbasl = 0.3
        endif
      endif

c ... Set aminrl for use in routines called from decomp
      do 10 iel = 1, nelem
        if (iel .eq. P) then
          fsol = fsfunc(minerl(1,P), pslsrb, sorpmx)
        else
          fsol = 1.0
        endif
        aminrl(iel) = minerl(1,iel) * fsol
10    continue

c ... Determine decomposition factor and initialize accumulators
c ... Added CANCVR to argument list.  -rm 6/91
      call cycle(month, cancvr, bgwfunc)

c ... N Fixation
c ... Does not take into account the effect of irrigation
      if (nsnfix .eq. 1 .and. nelem .ge. P) then

c ..... Compute mineral N:P ratio for N-Fixation (use suface layer only)
c ..... rnpml1 is used to control soil N-fixation using a regression
c ..... equation based on Kansas data. This ratio is used only if nelem = 2.
c ..... rnpml1 is flagged if either minerl(1,1) or minerl(1,2) is zero.

        rnpml1 = minerl(1,N)/minerl(1,P)*
     &           fsfunc(minerl(1,P),pslsrb,sorpmx)

c ..... Wet-dry fixation of nitrogen -- monthly flow
c ..... Atmospheric fixation is split between monthly dry fall and
c ..... wdfnp is the N:P ratio control function for non-symbiotic
c ..... soil fixation.
c ..... Both wdfnp and fxbiom are relative functions
c ..... which vary from 0 to 1.
c ..... wdfnp computed as a negative natural log of rnpml1
c ..... symnfx is the symbiotic N fixation by legumes derived from Cole and
c ..... Heil (1981) using data from Walker et al. 1959.
        if (rnpml1 .eq. 0) then
          wdfnp = 1.
        else
          wdfnp = min(1., ((-alog(rnpml1))/fxnpb)-.2)
        endif

c ..... The definitions of fxmca and fxmcb originally refered to water,
c ..... not biomass. (Alister 11/91)
        tbiom = aglivc+stdedc+strucc(SRFC)
        biof  = fxmca + tbiom * fxmcb
        fxbiom = 1 - biof
        fxbiom = min(1.,fxbiom)
        if (wdfnp .lt. 0 .or. fxbiom .lt. 0 .or. stemp .lt. 7.5) then
          fwdfx = 0.0
        else
          fwdfx = wdfnp * fxbiom
        endif

c ..... Compute N-fixation for the month

c ..... Wet fall depending on the monthly precipitation (wdfxma)
c ..... Add an optional multiplier on N deposition, cak - 04/05/04
        if (Ninput .eq. 2 .or. Ninput .eq. 3) then
          wdfxma = baseNdep * prcurr(month)/prcann * Nscalar(month)
        else
          wdfxma = baseNdep * prcurr(month)/prcann
        endif
        wdfxms = fxmxs * fwdfx
        wdfxm  = wdfxma + wdfxms

c ..... Compute annual N-fixation accumulators for atmosphere and soils
        wdfxas = wdfxas + wdfxms
        wdfxaa = wdfxaa + wdfxma
        call flow(esrsnk(N),minerl(1,N),time,wdfxm)
c ..... nfixac should accumulate SYMBIOTIC N-fixation -mdh 11/16/01
c        nfixac = nfixac+wdfxm

c ... Monthly N-fixation based on annual parameters
      else
c ..... USE PRCURR/PRCANN INSTEAD OF DT
        wdfxms = wdfxs * prcurr(month)/prcann
c ..... Add an optional multiplier on N deposition, cak - 04/05/04
        if (Ninput .eq. 2 .or. Ninput .eq. 3) then
          wdfxma = baseNdep * prcurr(month)/prcann * Nscalar(month)
        else
          wdfxma = baseNdep * prcurr(month)/prcann
        endif
        wdfxas = wdfxas + wdfxms
        wdfxaa = wdfxaa + wdfxma
        wdfxm = wdfxma + wdfxms
        call flow(esrsnk(N),minerl(1,N),time,wdfxm)
c ..... nfixac should accumulate SYMBIOTIC N-fixation -mdh 11/16/01
c        nfixac = nfixac + wdfxm
      endif

c ... Accumulate values for annual N deposition output variables,
c ... cak - 04/05/04
      wdfx = wdfx + wdfxma
      wdfxa = wdfxa + wdfxma

c ... Monthly atmospheric S deposition
      if (nelem .eq. S) then
        satm = satmt * prcurr(month) / prcann
        satmac = satmac + satm
        if (doirri) then
          sirr = sirri * irract * 0.01
        else
          sirr = 0
        endif
        sirrac = sirrac + sirr
        stot = satm + sirr
        call flow(esrsnk(S),minerl(SRFC,S),time,stot)
      endif

c ... -----------------------------------------------------------

c ... Decomposition Submodel

c ... Determine  whether cultivation occurs this month.
c ... Removed this call from DECOMP and put it here -rm 2/91
c ... Removed it from here and put it in CYCLE.  -vk 3/91

c ... Initialize stream variables for organic leaching (they are
c ... monthly output).  -rm 3/92
      do 20 kts = 5, 8
        stream(kts) = 0.0
20    continue
      strm5l = 0.0
      strm5u = 0.0

c ... Initialize monthly co2 accumlators (10/92)
      do 25 iso = 1, 2
        st1c2(iso) = 0.0
        st2c2(iso) = 0.0
        mt1c2(iso) = 0.0
        mt2c2(iso) = 0.0
        s11c2(iso) = 0.0
        s21c2(iso) = 0.0
        s2c2(iso)  = 0.0
        s3c2(iso)  = 0.0
        wd1c2(iso) = 0.0
        wd2c2(iso) = 0.0
        wd3c2(iso) = 0.0
25    continue

c ... Initialize monthly accumulator for volatilization of N during
c ... harvest, senescence, and return from grazing animal waste,
c ... cak 01/02
      volpl = 0.0

c ... Initialize monthly accumulator for symbiotic N fixation to track
c ... fixation for both grasses and trees as necessary, cak - 10/15/02
      nfix = 0.0

c ... Scale pH values if necessary, cak - 10/17/05
      if (phsys .gt. 0) then
        ph = phstart * pHscalar(month)
      endif

c ... Call decomp routines ntspm times per month.
c ... Removed the P and S chemistry from decomp and created the
c ... subroutine pschem.  -rm  6/91
      do 40 kts = 1, ntspm
        call decomp(decodt,decsys)
        if (nelem .ge. P) then
          call pschem(decodt)
        endif

c ..... Update decomposition and nitrogen fixation flows.
        call flowup(time)
        call flowup_double(time)
        call flowup_double_in(time)
        call flowup_double_out(time)
        call sumcar

c ..... Update the occlud and secndy single precision variables using
c ..... the values from the double precision variables, cak - 03/20/02
        occlud = real(occlud_double)
        secndy(1) = real(secndy_double(1))
        secndy(2) = real(secndy_double(2))
        secndy(3) = real(secndy_double(3))

c ..... aminrl contains the average amount of N, P, and S
c ..... available in the top layer for the time period covered by
c ..... dt/ntspm.  minerl contains the current value of mineral N,
c ..... P, and S by layer.
        do 30 iel = 1, nelem
          if (iel .eq. P) then
            fsol = fsfunc(minerl(SRFC,P), pslsrb, sorpmx)
          else
            fsol = 1.0
          endif
          aminrl(iel) = (aminrl(iel) + minerl(SRFC,iel)*fsol)/2.0
30      continue
40    continue

c ... Annual co2 accumulators (10/92)
      amt1c2 = amt1c2 + mt1c2(UNLABL) + mt1c2(LABELD)
      amt2c2 = amt2c2 + mt2c2(UNLABL) + mt2c2(LABELD)
      as11c2 = as11c2 + s11c2(UNLABL) + s11c2(LABELD)
      as2c2 = as2c2 + s2c2(UNLABL) + s2c2(LABELD)
      as3c2 = as3c2 + s3c2(UNLABL) + s3c2(LABELD)
      ast1c2 = ast1c2 + st1c2(UNLABL) + st1c2(LABELD)
      as21c2 = as21c2 + s21c2(UNLABL) + s21c2(LABELD)
      ast2c2 = ast2c2 + st2c2(UNLABL) + st2c2(LABELD)

c ... Volatilization loss of nitrogen as a function of
c ... gross mineralization
      volgm = vlossg*gromin(1)
      minerl(SRFC,N) = minerl(SRFC,N) - volgm
      esrsnk(N) = esrsnk(N) + volgm

c ... Set frlech to leaching fraction vek june90
c ... Compute normal value for frlech.  Recompute in flood routine
c ... if flooding occurs.
      texeff = fleach(1) + fleach(2) * sand
      do 50 iel = 1, nelem
        if (iel .eq. P) then
          fsol = fsfunc(minerl(SRFC,P), pslsrb, sorpmx)
        else
          fsol = 1.0
        endif
        frlech(iel) = texeff * fleach(iel+2) * fsol
50    continue

c ... Soil erosion
      if (doerod) then
        call erosn(psloss,bulkd,edepth,enrich,lhzci,lhze,nelem)
      else
        scloss = 0.0
      endif

c ... Fertilization option
      if (dofert) then
        do 60 iel = 1, nelem
          if (iel .eq. N) then
            if (Ninput .eq. 1 .or. Ninput .eq. 3) then
              esrsnk(iel) = esrsnk(iel)-feramt(iel)*Nscalar(month)
              minerl(SRFC,iel) = minerl(SRFC,iel)+feramt(iel)*
     &                           Nscalar(month)
              fertot(iel) = fertot(iel) + feramt(iel)*Nscalar(month)
              fertac(iel) = fertac(iel) + feramt(iel)*Nscalar(month)
            else
              esrsnk(iel) = esrsnk(iel)-feramt(iel)
              minerl(SRFC,iel) = minerl(SRFC,iel)+feramt(iel)
              fertot(iel) = fertot(iel) + feramt(iel)
              fertac(iel) = fertac(iel) + feramt(iel)
            endif
          else
            esrsnk(iel) = esrsnk(iel)-feramt(iel)
            minerl(SRFC,iel) = minerl(SRFC,iel)+feramt(iel)
            fertot(iel) = fertot(iel) + feramt(iel)
            fertac(iel) = fertac(iel) + feramt(iel)
          endif
60      continue
      endif

c ... Available nutrients
c ... tminrl is the total amount of each element available in
c ... mineral form.
      do 80 iel = 1, nelem
        tminrl(iel) = 0.
        if (iel .eq. P) then
          fsol = fsfunc(minerl(SRFC,P), pslsrb, sorpmx)
        else
          fsol = 1.0
        endif

        do 70 lyr = 1, nlayer

c ....... Plants can only uptake from a layer with a positive
c ....... value, so only the positive layers are summed here.
          if (minerl(lyr,iel) .gt. 0.)  then
            tminrl(iel) = tminrl(iel) + minerl(lyr,iel) * fsol
          endif
70      continue
80    continue

c ... Compute the fraction of labile (non-sorbed) P in the surface
c ... layer available to plants
      favail(2) = max(favail(4),
     &                min(favail(4) + minerl(SRFC,N)*
     &                   (favail(5) - favail(4)) / favail(6),
     &                    favail(5)))

c ... Add to fallow rain
      if (falprc .eq. 1 .and. .not. dohrvt) then
        prcfal = prcfal + prcurr(month)
      endif

c ... Call the producer submodel

c ... Compute daylength for use in phenology of trees
      call daylen(month, sitlat, tmplen)

c ... Determine if daylength is increasing or decreasing
      if (tmplen .lt. dayhrs) then
        hrsinc = .FALSE.
      else if (tmplen .gt. dayhrs) then
        hrsinc = .TRUE.
      endif

      dayhrs = tmplen

c ... Crop and Forest removal options - moved here from CROP
c ... and TREES so the mineral pools are not radically changed
c ... between the growth routines. - rm 7/94

      if (cursys .eq. CRPSYS) then
        call crop(time, bgwfunc)
c ..... Burning of aboveground live, standing dead, and litter layer
c ..... or grazing
        if (dofire(CRPSYS) .or. dograz) then
          call grem()
        endif

      else if (cursys .eq. FORSYS) then
        call trees(bgwfunc)
c!! Code for Victor
c        write(99,9) time, rleavc, rleave(1), rleave(2), rleave(3),
c     &              frootc, froote(1), froote(2), froote(3)
c9       format(f7.2, 2x, f8.2, 2x, 3(f6.3, 2x), f8.2, 2x, 3(f6.3, 2x))
c!! End of code change for Victor
        if (dotrem) then
c ....... Burning of live wood or cutting events
          call frem()
        endif
        if (dofire(FORSYS)) then
c ....... Burning of dead wood and litter layer, cak - 08/23/02
          call grem()
        endif

      else if (cursys .eq. SAVSYS) then
        call crop(time, bgwfunc)
        call trees(bgwfunc)
c!! Code for Victor
c        write(99,9) time, rleavc, rleave(1), rleave(2), rleave(3),
c     &              frootc, froote(1), froote(2), froote(3)
c!! End of code change for Victor
        if (dotrem) then
c ....... Burning of live wood or cutting events
          call frem()
        endif
        if (dofire(SAVSYS) .or. dograz) then
c ....... Burning of aboveground live, standing dead, litter layer, and
c ....... dead wood or grazing
          call grem()
        endif
      endif

c ... Update state variables and accumulators and sum carbon isotopes.
      call flowup(time)
      call flowup_double(time)
      call flowup_double_in(time)
      call flowup_double_out(time)
      call sumcar

c ... Harvest may be performed after updating flows.  Put here for
c ... consistency with the Savanna model - moved calls to flowup, 
c ... sumcar and harvst from CROP routine to here. -rm 7/94

      if (dohrvt) then
        call harvst(month,pltlig)
      endif

c ... Leaching
      call leach(amov, nelem, nlayer, minerl, minlch, frlech, stream,
     &           basef, stormf)

c ... Update state variables and accumulators and sum carbon isotopes.
      call flowup(time)
      call flowup_double(time)
      call flowup_double_in(time)
      call flowup_double_out(time)
      call sumcar

c ... Accumulate leached C,N,P,S
      csrsnk(UNLABL) = csrsnk(UNLABL) + strm5u
      csrsnk(LABELD) = csrsnk(LABELD) + strm5l
      stream(5) = strm5u + strm5l
      do 90 iel = 1, nelem
        esrsnk(iel) = esrsnk(iel) + stream(iel+1) + stream(iel+5)
90    continue

c ... Volatilization loss as a function of the mineral n which
c ... remains after uptake by plants
      if (minerl(SRFC,N) .gt. 0.0) then
        volex = vlosse*minerl(SRFC,N)*dt
        minerl(SRFC,N) = minerl(SRFC,N) - volex
        esrsnk(N) = esrsnk(N) + volex
      endif

c ... Volatilization
      volgma = volgma+volgm
      volexa = volexa+volex
      volgac = volgac+volgm
      voleac = voleac+volex

c ... Production
      cproda = cproda + cprodc + cprodf

c ... Net Mineralization
      do 100 iel = 1, nelem

c ..... Net mineralization for the mineralizing compartments
c ..... The structural component of litter and the wood compartments
c ..... are not mineralizers.  They should not be added into cmn or
c ..... sumnrs.
        cmn = metmnr(SRFC,iel) + metmnr(SOIL,iel) +
     &        s1mnr(SRFC,iel) + s1mnr(SOIL,iel) +
     &        s2mnr(iel) + s3mnr(iel)
        sumnrs(iel) = sumnrs(iel) + cmn

c ..... soilnm is net mineralization in the soil.
        soilnm(iel) = soilnm(iel) + s1mnr(SOIL,iel) +
     &                s2mnr(iel) + s3mnr(iel) +
     &                metmnr(SOIL,iel) + strmnr(SOIL,iel) + w3mnr(iel)

c ..... Total net mineralization
        tnetmn(iel) = tnetmn(iel) + cmn + 
     &                strmnr(SRFC,iel) + strmnr(SOIL,iel) +
     &                w1mnr(iel) + w2mnr(iel) + w3mnr(iel)
100   continue

c ... Stream flow accumulators, cak - 04/08/03
      do 105 kts = 1, 8
        strmac(kts) = strmac(kts) + stream(kts)
105   continue

c ... Compute output variables for printing or plotting.
      call savarp

      return
      end
