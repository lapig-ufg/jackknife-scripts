
c              Copyright 1993 Colorado State University
c                       All Rights Reserved


      subroutine weathr(precip,prcstd,prcskw,mintmp,maxtmp)

      implicit none
      include 'chrvar.inc'
      include 'const.inc'
      include 'wth.inc'
      include 'zztim.inc'
      
c ... Argument declarations
      real      precip(12), prcstd(12), prcskw(12),
     &          mintmp(12), maxtmp(12)

c ... Determines the current year values for precipitation and
c ... temperature and next year values for precipitation for predicting
c ... production potential.

c ... Function declarations
      real      anorm, sknorm
      external  anorm, sknorm

c ... Local variables
      integer   mm
      character label*4

c ... Current year precipitation, regardless of wthr type
      do 10 mm = 1, MONTHS
        prcurr(mm) = prcnxt(mm)
10    continue

c ... Weather option M uses the same weather data for each year
      if (wthr .eq. 'M') then
        do 20 mm = 1, MONTHS
          prcurr(mm) = precip(mm)
          prcnxt(mm) = precip(mm)
20      continue
        goto 999
      endif

c ... Weather option S
      if (wthr .eq. 'S') then
c ..... If skewness value is 0.0, select precipitation values from
c ..... normal distribution
c ..... Else, use skewness value to generate precip values
        do 30 mm = 1, MONTHS
          if (prcskw(mm) .eq. 0.0) then
            prcnxt(mm) = max(0.0, anorm(precip(mm),prcstd(mm)))
          else
            prcnxt(mm) = max(0.0, 
     &                  sknorm(precip(mm), prcstd(mm), prcskw(mm)))
          endif
30      continue
        goto 999
      endif

c ... Weather options F and C, read from weather data file
40    format(a4,6x,12f7.0)

c ... Current year temperatures

c ... Minimum monthly temperatures at 2 meters (deg c)
      read(9,40) label, mintmp
      if (label .ne. wlabel(2)) then
        call faterr(label,wlabel(2))
      endif

c ... Check for -99.99 missing values flag
      do 50 mm = 1, MONTHS
        if (mintmp(mm) .eq. -99.99) then
          mintmp(mm) =  tmn2m(mm)
        endif
50    continue

c ... Maximum monthly temperatures at 2 meters (deg c)
      read(9,40) label, maxtmp
      if (label .ne. wlabel(3)) then
        call faterr(label,wlabel(3))
      endif

c ... Check for -99.99 missing values flag
      do 60 mm = 1, MONTHS
        if (maxtmp(mm) .eq. -99.99) then
          maxtmp(mm) =  tmx2m(mm)
        endif
60    continue

c ... Next year precipitation (cm/month)
70    read(9,40,end=90) label,prcnxt
      if (label .ne. wlabel(1)) then
        call faterr(label,wlabel(1))
      endif

c ... Check for -99.99 and generate skewed values for ones found
      do 80 mm = 1, MONTHS
        if (prcnxt(mm) .eq. -99.99) then
          if (prcskw(mm) .eq. 0.0) then
            prcnxt(mm) = max(0.0, anorm(precip(mm),prcstd(mm)))
          else
            prcnxt(mm) = max(0.0, 
     &                  sknorm(precip(mm), prcstd(mm), prcskw(mm)))
          endif
        endif
80    continue

999   continue

c ... Apply weather scalars to the climate values as indicated,
c ... cak - 10/18/05
      if (wthinput .eq. 4 .or. wthinput .eq. 5) then
        do 100 mm = 1, MONTHS
          prcnxt(mm) = prcnxt(mm) * precscalar(mm)
100     continue
      endif
      if (wthinput .eq. 2 .or. wthinput .eq. 3 .or.
     &    wthinput .eq. 5) then
        do 110 mm = 1, MONTHS
          maxtmp(mm) = maxtmp(mm) + tmaxscalar(mm)
110     continue
      endif
      if (wthinput .eq. 1 .or. wthinput .eq. 3 .or.
     &    wthinput .eq. 5) then
        do 120 mm = 1, MONTHS
          mintmp(mm) = mintmp(mm) + tminscalar(mm)
120     continue
      endif
c ... Check that application of scalars to temperature values does
c ... not result in invalid weather values
      do 130 mm = 1, MONTHS
        if (mintmp(mm) .gt. maxtmp(mm)) then
          write(*,*)
          write(*,*) 'Error: minimum temperature: ', mintmp(mm)
          write(*,*) '       greater than maximum temperature: ',
     &               maxtmp(mm)
          write(*,*) '       in month: ', mm, ' year: ', int(time)
          write(*,*) 'Ending simulation!'
          write(*,*)
          STOP
        endif
130   continue

      return

c ... End of file encountered; rewind and reuse.
90    rewind 9
      goto 70

      end
