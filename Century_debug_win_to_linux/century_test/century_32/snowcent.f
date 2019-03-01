
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      subroutine snowcent(tmelt, tave, pptactual, pptsoil, snow, snlq,
     &                    petrem, melt, evap, month)

      implicit none
      include 'site.inc'

c ... Argument declarations
      integer month
      real    evap, melt, petrem, pptactual, pptsoil, snow, snlq,
     &        tave, tmelt(2)

c ... Determine the snow pack, melt snow, and evaporate from the snow pack

c ... Inputs:
c ...   evap      - the water evaporated from the  soil and vegetation
c ...               (cm/mon)
c ...   month     - the current month (1 - 12)
c ...   petleft   - the potential evaporation rate (cm H2O/day)
c ...   pptactual - the current month's precipitation (cm H2O)
c ...   snlq      - the liquid water in the snowpack (cm H2O)
c ...   snow      - current snowpack (equiv. cm H2O)
c ...   tave      - the average monthly air temperature (deg C - 2m)
c ...   tmelt[]   - tmelt[0] = melting temperature (C), if temperature is >= 
c ...               this value, snow is allowed to melt and is added 
c ...               to the precipitation
c ...               tmelt[1] = the slope of the melting equation
c ...               (cm snow / degree C)
c ...
c ... Outputs:
c ...   evap    - the water evaporated from the  soil and vegetation
c ...             (cm/mon)
c ...   melt    - the amount of snow drained from the snowpack if 
c ...             monthly air temperature is warm enough (cm H2O)
c ...   petleft - the potential evaporation rate, adjusted for sublimation
c ...             of snow (cm/day).  
c ...   pptsoil - precipitation adjusted for snow accumulation and melt
c ...             (water available to infiltrate the soil) (cm) 
c ...   snlq    - the liquid water in the snowpack (cm H2O)
c ...   snow    - current snowpack (equiv. cm H2O)
c ...
c ... Local variables:
c ...   accum   - the amount of snow added to the snowpack (cm H2O)
c ...   add     - amount of water from melted snow to add to soil (cm H2O)
c ...   evsnow  - amount of water sublimated from the snowpack and liquid snow
c ...             (cm H2O)
c ...   snowtot - the sum of snow and liquid water in the snow (cm H2O)

c ... Function declarations
      real     shwave
      external shwave

c ... Local variables
      real      accum, add, evsnow, snowtot

      accum = 0.0
      add = 0.0
      evsnow = 0.0
      snowtot = 0.0
      pptsoil = pptactual

c ... When mean monthly air temperature is below freezing, 
c ... precipitation is in the form of snow.
      if (tave .le. 0.0) then
        snow = snow + pptactual
        accum = pptactual
        pptsoil = 0.0
      endif
c ... Add rain-on-snow to snowpack liquid (snlq)
      if (snow .gt. 0.0) then
        snlq = snlq + pptsoil
        pptsoil = 0.0
      endif

c ... Evaporate water from the snow pack (rewritten Pulliam 9/94 to
c ... evaporate from both snow aqnd snlq in proportion)  
c ... Coefficient 0.87 relates to heat of fusion for ice vs. liquid water
c ... wasn't modified as snow pack is at least 95% ice.
      if (snow .gt. 0) then
c ..... Calculate cm of snow that remaining pet energy can evaporate:
        evsnow = petrem * 0.87
c ..... Calculate total snowpack water, ice + liquid:
        snowtot = snow + snlq
c ..... Don't evaporate more snow than actually exists:
        if (evsnow .gt. snowtot) then
          evsnow = snowtot
        endif
c ..... Take evsnow from snow and snlq in proportion:
        snow = snow - evsnow * (snow/snowtot)
        snlq = snlq - evsnow * (snlq/snowtot)
c ..... Add evaporated snow to evaporation accumulator (evap):
        evap = evap + evsnow
c ..... Decrement remaining pet by energy used to evaporate snow and
c ..... phase transform the snow:
        petrem = petrem - evsnow / 0.87
        if (petrem .lt. 0.0) then
          petrem = 0.0
        endif
      endif

c ... Melt snow if air temperature is above minimum (tmelt(1))
      if (snow .gt. 0.0 .and. tave .ge. tmelt(1)) then
c ..... Calculate the amount of snow to melt:
c ..... Added effect of solar radiation outside the atmosphere on
c ..... snowmelt, cak - 12/11/02
        melt = tmelt(2) * (tave - tmelt(1)) * shwave(month,sitlat)
        if (melt .lt. 0.0) then
          melt = 0.0
        endif
        if ((snow - melt) .gt. 0.0) then
          snow = snow - melt
        else
          melt = snow
          snow = 0.0
        endif
c ..... Melted snow goes to liquid snow and drains excess:
        snlq = snlq + melt
c ..... Drain snowpack to 50% liquid content (weight/weight), excess to soil:
        if (snlq .gt. (0.5 * snow)) then
          add = snlq - 0.5 * snow
          snlq = snlq - add
          pptsoil = pptsoil + add
c ....... Return the amount of water draining into the soil
          melt = pptsoil
        endif
      endif 

      return
      end
