
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      real function sknorm(mean, sd, skew)

      implicit none
      include 'parfx.inc'

c ... Argument declarations
      real      mean, sd, skew

c ... by Alister Metherell, from EPIC Model

c ... Function declarations
      real      gasdev
      external  gasdev

c ... Determine skewed value
      if (skew .eq. 0.0) then
        sknorm = mean + sd*gasdev(seed)
      else
        sknorm = mean + 2*sd/skew*
     &           ((skew/6*(gasdev(seed)-skew/6)+1)**3 - 1)
      endif

      return
      end
