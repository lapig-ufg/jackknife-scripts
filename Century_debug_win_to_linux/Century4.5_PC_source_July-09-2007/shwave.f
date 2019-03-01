
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      real function shwave(month, sitlat)

      implicit none
      include 'pi.inc'

c ... Argument declarations
      integer month
      real    sitlat

c ... This code was extracted from the petfunc function from the
c ... subwatr.f Soilwater Model source code file.
c ...
c ... Calculate the short wave radiation outside the atmosphere using
c ... Pennmans equation (1948)
c ...
c ... Inputs:
c ...   month  - current month (1-12)
c ...   sitlat - latitude of current site (degrees)
c ...
c ... Output:
c ...   shwave - short wave solar radiation outside the atmosphere
c ...
c ... Local variables:
c ...   ahou            - ?
c ...   declin          - declination (radians)
c ...   jday()          - Julian day for middle of current month
c ...   par1, par2      - parameters in computation of ahou
c ...   rlatitude       - latitude of the site (in radians)
c ...   solrad          - solar radiation (ly/day)
c ...   transcof(month) - transmission coefficient for the month

c ... Local variables
      real    ahou
      real    declin
      real    par1
      real    par2
      real    rlatitude
      real    solrad
      real    temp
      real    transcof(12)
      integer jday(12)

c ... Julian date in the middle of each month of the year
      data jday /16,46,75,106,136,167,197,228,259,289,320,350/
      data transcof /0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8/

c ... Convert latitude from degrees to radians
      rlatitude = sitlat * (PI / 180.0)

c ... Calculate the short wave solar radiation on a clear day using a
c ... equation presented by Sellers(1965)

      declin=0.401426*sin(6.283185*(real(jday(month))-77.0)/365.0)
      temp = 1.0-(-tan(rlatitude)*tan(declin))**2
      if (temp .lt. 0.0) then
        temp = 0.0
      endif
      par1=sqrt(temp)
      par2=(-tan(rlatitude)*tan(declin))

      ahou=atan2(par1,par2)
      if(ahou.lt.0.0) then
        ahou=0.0
      endif

      solrad=917.0*transcof(month)*(ahou*sin(rlatitude)*sin(declin)+
     &       cos(rlatitude)*cos(declin)*sin(ahou))

c ... Determine the short wave radiation outside the atmosphere
      shwave=solrad/transcof(month)

      return
      end
