
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      subroutine cycle(month, cancvr, bgwfunc) 

      implicit none
      include 'comput.inc'
      include 'const.inc'
      include 'dovars.inc'
      include 'param.inc'
      include 'parcp.inc'
      include 'parfx.inc'
      include 'plot1.inc'
      include 'plot2.inc'
      include 'plot3.inc'
      include 'seq.inc'
      include 'wth.inc'

c ... Argument declarations
      integer month
      real    cancvr, bgwfunc

c ... Determine relative water content, available water, and
c ... decomposition factor related to temperature and water.
c ... Initialize mineralization accumulators.  Compute potential
c ... production.

c ... Function declarations
      real     anerob, irrigt, pevap, tcalc
      external anerob, irrigt, pevap, tcalc

c ... Local variables
      integer      ii, iel, lyr
      real         amelt, co2val, rprpet,
     &             tfunc, agwfunc
      character*80 string

c ... Call schedl to determine scheduling options for this month
      call schedl()

c ... Initialize production accumulators
c ... For crops, annual accumulation starts at the month of planting.
c ... For grass, annual accumulation starts at the beginning of
c ... the growing season.
c ... For forest, annual accumulation starts at the beginning
c ... of the growing season.
c ... This call moved to the sched subroutine, cak - 05/20/03
c      if ((dofrst .or. doplnt .or. dofone) .or.
c     &    (month .eq. 1)) then
c        call inprac
c      endif

c ... Average air temperature at 2 meters
      tave = (maxtmp(month) + mintmp(month)) / 2.0

c ... Calculate RAIN for an output variable
      rain = prcurr(month)

c ... If irrigating, determine actual amount of irrigation, irract
      if (doirri) then
        irract = irrigt(month)
      else
        irract = 0
      endif

c ... If planting or growing month, calculate growing season precipitation
      if (doplnt .or. dofrst) then
        call prcgrw(month)
      endif

c ... Initialize the mineralization accumulators for each element.
      do 30 iel = 1, MAXIEL
        do 25 lyr = 1, 2
          strmnr(lyr,iel) = 0.0
          metmnr(lyr,iel) = 0.0
          s1mnr(lyr,iel) = 0.0
25      continue
        s2mnr(iel) = 0.0
        s3mnr(iel) = 0.0
        gromin(iel) = 0.0
        w1mnr(iel) = 0.0
        w2mnr(iel) = 0.0
        w3mnr(iel) = 0.0
30    continue

c ... ************************************************************************
c ... If the system is a microcosm, skip the rest of the routine
      if (micosm .eq. 1) then

        pet = 15.
        anerb = anerob(aneref, drain, rprpet, pet, micosm)

        if (docult) then
          do 32 ii = 1, 4
            cltfac(ii) = clteff(ii)
32        continue
        else
          do 33 ii = 1, 4
            cltfac(ii) = 1.0
33        continue
        endif

        goto 999

      endif
c ... ************************************************************************

c ... Potential production
      call potprod(cancvr)

c ... Determine co2 effect on transpiration, pass to h2olos
      if (cursys .eq. SAVSYS) then
        if (aglivc + rleavc .eq. 0.0) then
          co2val = 1.0
        else
          co2val = (co2ctr(CRPSYS)*aglivc + co2ctr(FORSYS)*rleavc) /
     &             (aglivc + rleavc)
        endif
      else
        co2val = co2ctr(cursys)
      endif

      pet = pevap(month)

c ... Compute the ratio of precipitation to PET.
c ... If there is snow melt use the amelt value returned from the h2olos
c ... subroutine to determine how much snow is melting into the ground,
c ... cak - 10/21/02
      if (amelt .gt. 0.0) then
c ..... amelt represents the amount of water draining into the soil when
c ..... there is snow on the ground, both precipitation and irrigation
c ..... amounts have been taken into account in the snow calculations,
c ..... cak - 12/13/02
c        rprpet = (amelt + irract) / pet
        rprpet = amelt / pet
		print *, 'rprpet=', rprpet
      else
        rprpet = (avh2o(3) + prcurr(month) + irract) / pet
      endif

      call h2olos(month,aglivb,sfclit,stdead,co2val,amelt)

c ... Average surface temperature
c ... Added check for snow  -rm 8/91
      if (snow .gt. 0.0) then
        stemp = 0.0
      endif

c ... Effect of temperature on decomposition
      tfunc = tcalc(stemp, teff)

c ... Effect of moisture on decomposition
c ... Option selection for wfunc depending on idef
c ...   idef = 1 for linear option
c ...   idef = 2 for ratio option
c ... Changed coefficients in both wfunc equations  -rm 6/91
c ... Relative water content -- rwcf

      if (idef .eq. 1) then
c ..... Check added to handle underflow potential in exp intrinsic
        if (rwcf(1) .gt. 1.) then
          agwfunc = 1.
        else
          agwfunc = 1./(1. + 10.0 * exp(-6.0*rwcf(1)))
        endif

      else if (idef .eq. 2) then
c ..... Check added to handle underflow potential in exp intrinsic
        if (rprpet .gt. 9) then
          agwfunc = 1.
        else
          agwfunc = 1./(1. + 30.0 * exp(-8.5 * rprpet))
        endif

      else
        call message(' ')
        string = '   IDEF may be either 1 or 2, but is currently: ' //
     &           char(ichar(char(idef)) + ichar('0'))
        call message(string)
        call message('   You must reset it and restart the run.')
        call message(' ')
        STOP
      endif
      if (agwfunc .ge. 1.0) then
        agwfunc = 1.0
      endif
      bgwfunc = agwfunc

c ... Calculate the effect impact of anerobic conditions on decomposition
      anerb = anerob(aneref, drain, rprpet, pet, micosm)

c ... Combined effects of temperature and moisture
      agdefac=tfunc*agwfunc
      bgdefac=tfunc*bgwfunc
c ... Bound defac to >= 0.0 12/21/92
      if (agdefac .lt. 0.0) agdefac = 0.0
      agdefacm(month)=agdefac
      if (bgdefac .lt. 0.0) bgdefac = 0.0
      bgdefacm(month)=bgdefac

c ... Effect of cultivation on decomposition (used in decomp routine)
c ... Determine effect of cultivation on decomposition. vk 03-13-91
c ... cltfac is this month's effect of cultivation on decomposition
c ... of som1, som2, som3, and structural.  It is set to clteff
c ... in months when cultivation occurs; otherwise it equals 1.
c ... clteff is the effect of cultivation on decomposition read from
c ... the cult.100 file

      if (docult) then
        do 34 ii = 1, 4
          cltfac(ii) = clteff(ii)
34      continue
      else
        do 35 ii = 1, 4
          cltfac(ii) = 1.0
35      continue
      endif

999   continue

      return
      end
