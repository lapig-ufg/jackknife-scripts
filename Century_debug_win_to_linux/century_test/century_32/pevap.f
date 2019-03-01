
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


C ... PEVAP.F

      real function pevap(mnum)
 
      implicit none
      include 'const.inc'
      include 'param.inc'
      include 'parfx.inc'
      include 'site.inc'

c ... Argument declarations
      integer   mnum

c ... Calculate PET using the FAO Penman-Monteith equation,
c ... cak - 04/07/03
c ... Reference:  http://www.fao.org/docrep/X0490E/x0490e08.htm

c ... Function declarations
      real      shwave
      external  shwave

c ... Local variables
      real daypet, monpet, trange, tmean
      real const1
      real const2
      real langleys2watts

      const1 = 0.0023
      const2 = 17.8
      langleys2watts = 54.0

c ... Compute PET for Julian day that falls in the middle of the
c ... current month
      trange = maxtmp(mnum) - mintmp(mnum)
      tmean = (maxtmp(mnum) + mintmp(mnum))/2.0
      daypet = const1 * (tmean + const2) * sqrt(trange) *
     &         (shwave(mnum, sitlat) / langleys2watts)

c ... Calculate monthly PET amount and convert mm to cm */
      monpet = (daypet * 30.) / 10.
      if (monpet .lt. 0.5) then
        monpet = 0.5
      endif

c ... fwloss(4) is a modifier for PET loss.   vek may90
      pevap = monpet*fwloss(4)

      return
      end
