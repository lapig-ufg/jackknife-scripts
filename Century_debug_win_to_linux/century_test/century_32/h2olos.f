
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      subroutine h2olos(month, aliv, alit, adead, co2val, amelt)

      implicit none
      include 'const.inc'
      include 'param.inc'
      include 'parfs.inc'
      include 'parfx.inc'
      include 'plot1.inc'
      include 'plot3.inc'
      include 'seq.inc'

c ... Argument declarations
      integer month
      real    aliv, alit, adead, amelt, co2val

c ... Water Submodel for Century - written by Bill Parton
c ... Updated from Fortran 4 - rm 2/92
c ... Rewritten by Bill Pulliam - 9/94

c ... Function declarations
      real      line
      external  line

c ... Local Variables
      integer   jj
      real      abs, add, afl, aint, asimx, avhsm,
     &          avinj, avw, awwt(MAXLYR), base, evl,
     &          evlos, evmt, fwlos, inputs,
     &          petrem, pevp, rwc1, sd, strm,
     &          tot, tot2, trap, trl, winputs
      real      croplai, treelai, totlai

c ... Description of variables
c ...
c ... adead       the average monthly standing dead biomass(gm/m..2)
c ... adep        depth of the ith soil layer(cm)
c ... afiel       the field capacity of the ith soil layer(fraction)
c ... alit        the average monthly litter biomass(gm/m..2)
c ... aliv        the average monthly live plant biomass(gm/m..2)
c ... amelt       the amount of water from snowmelt draining into the snow
c ...             (cm h2o)
c ... amov        the index for water movement(0-no flow,1-saturated flow)
c ... asmos       the soil water content of the ith soil layer(cm h2o)
c ... asnow       the snow pack water contint(cm-h2o)
c ... avh2o (1)   water available to plants for growth
c ... avh2o (2)   water available to plants for survival
c ...             (available water in the whole soil profile)
c ... avh2o (3)   water available to plants in the top 2 layers (top 30 cm)
c ... avw         available water in current soil layer
c ... awilt       the wilting point of the  ith soil layer(fraction)
c ... awtl        the weight factor for transpiration water loss from the ith
c ...             soil layer(nod)
c ... evap        the water evaporated from the  soil and vegetation(cm/mon)
c ... inputs      rain + irrigation
c ... winputs     inputs which are water (not converted to snow), includes
c ...             melted snow
c ... irract      ammount of irrigation (cm)
c ... nlayer      number of soil layers with water available for plant survival
c ... nlaypg      number of soil layers with water available for plant growth
c ... petrem      remaining pet, updated after each incremental h2o loss
c ... pevp        the potential evaporation rate from the top  soil layer (cm/day)
c ... rain        the total monthly rainfall (cm/month)
c ... runoff      the monthly runoff (cm/month)
c ... rwcf        the relative water content of the ith soil layer(0-1)
c ... snlq        the liquid water in the snow pack
c ... tav         average monthly air temperature (2m-c)
c ... tran        transpriation water loss(cm/mon)
c ... trl         transpiration water loss

c ... Initialize Variables
      add = 0.0
      amelt = 0.0
      asimx = 0.0
      avh2o(1) = 0.0
      avh2o(2) = 0.0
      avh2o(3) = 0.0
      evap = 0.0
      pevp = 0.0
      pttr = 0.0
      runoff = 0.0
      tran = 0.0
      trap = 0.01
      abs = 0.0

c ... Calculate total water inputs 
      inputs = rain + irract

c ... Throughout, uses petrem as remaining energy for pet after
c ... each melting and evaporation step.  Initially calculated
c ... pet is not modified.  Pulliam 9/94
      petrem = pet

c ... Determine the snow pack, melt snow, and evaporate from the snow pack
      call snowcent(tmelt, tave, inputs, winputs, snow, snlq, petrem,
     &              amelt, evap, month)

c ... Compute runoff -rm 12/96
c ... Probert, M.E., B.A. Keating, J.P. Thompson, and W.J. Parton. 1995.
c ... Modelling water, nitrogen, and crop yield for a long-term
c ... fallow management experiment. Australian Journal of Experimental
c ... Agriculture 35:941-950.
c ... Using equation for plots with surface residue.
c      runoff = MAX(0.0, 0.15 * (winputs - 8.0))
c ... Replace constant values in runoff equation with user specified values,
c ... cak - 05/27/03
      runoff = MAX(0.0, fracro * (winputs - precro))
c ... subtract runoff from net water inputs.
      winputs = winputs - runoff

c ... Calculate bare soil water loss and interception
c ... when air temperature is above freezing and no snow cover.
c ... Mofified 9/94 to allow interception when t < 0 but no snow
c ... cover, Pulliam
      if (snow .eq. 0.0) then

c ..... Calculate total canopy cover and litter, put cap on effects:
        sd = aliv + adead
        if (sd .gt. 800.0) sd = 800.0
        if (alit .gt. 400.0) alit = 400.0

c ..... canopy interception, fraction of  precip (aint):
        aint = (0.0003 * alit + 0.0006 * sd) * fwloss(1)

c ..... Bare soil evaporation, fraction of precip (abs):
        abs = 0.5 * exp((-0.002 * alit) - (0.004 * sd)) * fwloss(2)

c ..... Calculate total surface evaporation losses, maximum 
c ..... allowable is 0.4 * pet. -rm 6/94
        evl = MIN(((abs + aint) * winputs), (0.4 * petrem))
        evap = evap + evl

c ..... Calculate remaining water to add to soil and potential
c ..... transpiration as remaining pet:
c        add = add + inputs - evl
        add = winputs - evl
        trap = petrem - evl
      endif

c ... Determine potential transpiration water loss (trap, cm/mon) as a
c ... function of precipitation and live biomass.
c ... If temperature is less than 2C turn off transpiration. -rm 6/94
      if (tave .lt. 2.0) then
        pttr = 0.0
      else
        pttr = petrem * 0.65 * (1.0 - exp(-0.020 * aliv)) * co2val
      endif
      if (pttr .le. trap) trap = pttr
      if (trap .le. 0.0) trap = 0.01

c ... Maintain pttr on a monthly basis for harvest
      hpttr(month) = pttr

c ... Calculate the potential evaporation rate from the top soil layer
c ... (pevp-cm/day).  This is not actually taken out until after
c ... transpiration losses
      pevp = petrem - trap - evl
      if (pevp .lt. 0.0) pevp = 0.0

c ... Transpire water from added water first, before passing water
c ... on to soil.  This is necessary for a monthly time step to
c ... give plants in wet climates adequate access to water for
c ... transpiration. -rm 6/94, Pulliam 9/94
      tran = MIN((trap - .01), add)
      trap = trap - tran
      add = add - tran

c ... Add water to the soil
c ... Changed to add base flow and storm flow.  -rm 2/92

      strm = 0.0
      base = 0.0
      stream(1) = 0.0

      do 10 jj=1,nlayer
c ..... Add water to layer jj:
        asmos(jj) = asmos(jj) + add

c ..... Calculate field capacity of soil, drain soil, pass excess
c ..... on to amov:
        afl = adep(jj) * afiel(jj)
        if (asmos(jj) .gt. afl) then
          amov(jj) = asmos(jj) - afl
          asmos(jj) = afl

c ....... If you are at the bottom layer, compute storm flow.
          if (jj .eq. nlayer) strm = amov(jj) * stormf
        else
          amov(jj) = 0.0
        endif

c ..... Copy amov to add, continue with next layer:
        add = amov(jj)
10    continue

c ... Compute base flow and stream flow for H2O.
c ... Put water draining out bottom that doesn't go to stormflow
c ... into nlayer+1 holding tank:
      asmos(nlayer+1) = asmos(nlayer+1) + add - strm

c ... Drain baseflow fraction from holding tank:
      base = asmos(nlayer+1) * basef
      asmos(nlayer+1) = asmos(nlayer+1) - base

c ... Streamflow = stormflow + baseflow:
c      stream(1) = strm + base
c ... Streamflow = stormflow + baseflow + runoff:
c ... Added runoff into stream(1) -rm 12/96
      stream(1) = strm + base + runoff

c ... Save asmos(1) before transpiration for future use:
      asimx=asmos(1)

c ... Calculate transpiration water loss from each layer
c ... This section was completely rewritten by Pulliam, though it
c ... should still do the same thing.  9/94
      rwc1 = 0.0
      tot = 0.0
      tot2 = 0.0
      do 20 jj = 1, nlayer

c ..... Calculate available water in layer, asmos minus wilting point:
        avw = asmos(jj) - awilt(jj) * adep(jj)
        if (avw. lt. 0.0) avw = 0.0
c ..... Calculate available water weighted by transpiration depth
c ..... distribution factors:
        awwt(jj) = avw * awtl(jj)
c ..... Sum up available water:
        tot = tot + avw
c ..... Sum up weighted available water:
        tot2 = tot2 + awwt(jj)
20    continue

c ... Calculate the actual transpiration water loss(tran-cm/mon)
c ... Also rewritten by Pulliam 9/94, should do the same thing
c ... Update potential transpiration to be no greater than available water:
      trap = MIN(tot,trap)

c ..... Calculate a dynamic value for nlaypg based on the crop and/or tree
c ..... option used, cak - 01/29/03
        if (cursys .eq. SAVSYS) then
c ....... For crops and grasses a leaf area of 1 = 100 grams of biomass
          croplai = aglivc * 2.5 * 0.01
          treelai = rleavc * 2.5 * btolai
          totlai = croplai + treelai
          if (totlai .gt. 0.0) then
            nlaypg = nint(line(treelai/totlai, 0.0, croplai, 1.0,
     &                         treelai))
          else
            nlaypg = min(claypg, tlaypg)
          endif
          if (nlaypg .lt. min(claypg, tlaypg)) then
            nlaypg = min(claypg, tlaypg)
          endif
          if (nlaypg .gt. max(claypg, tlaypg)) then
            nlaypg = max(claypg, tlaypg)
          endif
        endif

c ... Transpire water from each layer:
      if (tot2 .gt. 0.) then
c ..... Calculate available water in layer jj:
c ..... Transpiration occurs in the top nlaypg layers, cak 01/29/03
c        do 30  jj = 1, nlayer
        do 30  jj = 1, nlaypg
          avinj = asmos(jj) - awilt(jj) * adep(jj)
          if (avinj .lt. 0.0) avinj = 0.0

c ....... Calculate transpiration loss from layer jj, using weighted
c ....... water availabilities:
          trl = (trap * awwt(jj))/tot2
          if (trl .gt. avinj) trl = avinj
          asmos(jj) = asmos(jj) -trl
          avinj = avinj - trl
          tran = tran + trl
          rwcf(jj) = (asmos(jj)/adep(jj)-awilt(jj)) /
     &               (afiel(jj)-awilt(jj))

c ....... Sum up water available to plants for growth:
          avh2o(1) = avh2o(1) + avinj

c ....... Calculate parameter of H2O accumulation in top 2 soil layers:
          if (jj .le. 2) avh2o(3) = avh2o(3) + avinj
30      continue

        do 35 jj = 1, nlayer
c ....... Sum up water available to plants for survival:
          avh2o(2) = avh2o(2) + avinj
35      continue
      endif

c ... Set htran for use in harvst.f
      htran(month) = tran

c ... Evaporate water from the top layer
c ... Rewritten by Pulliam, should still do the same thing 9/94

c ... Minimum relative water content for top layer to evaporate:
      fwlos = 0.25

c ... Fraction of water content between fwlos and field capacity:
      evmt = (rwcf(1)-fwlos)/(1.-fwlos)
      if (evmt .le. 0.01) evmt = 0.01

c ... Evaporation loss from layer 1:
      evlos = evmt * pevp * abs * 0.10
      avinj = asmos(1) - awilt(1) * adep(1)
      if (avinj .lt. 0.0) avinj = 0.0
      if (evlos .gt. avinj) evlos = avinj
      asmos(1) = asmos(1) - evlos
      evap = evap + evlos

c ... Recalculate rwcf(1) to estimate mid-month water content
      avhsm = (asmos(1) + rwc1 * asimx)/(1. + rwc1)
      rwcf(1)=(avhsm/adep(1)-awilt(1))/(afiel(1)-awilt(1))

c ... Update available water pools minus evaporation from top layer
      avh2o(1) = avh2o(1) - evlos
      avh2o(2) = avh2o(2) - evlos
      avh2o(3) = avh2o(3) - evlos

c ... Compute annual actual evapotranspiration
      annet = annet + evap + tran

      return
      end
