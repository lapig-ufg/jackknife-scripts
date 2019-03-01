
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      subroutine wthini(precip,prcstd,prcskw,mintmp,maxtmp)

      implicit none
      include 'chrvar.inc'
      include 'const.inc'
      include 'wth.inc'
      include 'zztim.inc'

c ... Argument declarations
      real      precip(12), prcstd(12), prcskw(12), mintmp(12), 
     &          maxtmp(12)

c ... Determine what weather data will be used.

c ... Function declarations
      real      anorm, sknorm
      external  anorm, sknorm

c ... Local variables
      integer   mm
      character label*4, string*80

c ... Weather options
c ... 'M' use the precipitation and temperature values which were
c ...     read from the site.100 file
c ... 'S' use the temperature values which were read from the site.100
c ...     file; select precipitation values from a skewed or 
c ...     from a normal distribution using values in precip as means
c ...     and values in prcstd as standard deviations and values in 
c ...     prcskw as skewed.
c ... 'F' Open an actual weather data file and read precipitation and
c ...     temperature data.
c ... 'C' Continue reading precipitation and temperature data
c ...     from the current weather file.

c ... Initialize mintmp and maxtmp
      do 10 mm = 1, MONTHS
        mintmp(mm) = tmn2m(mm)
        maxtmp(mm) = tmx2m(mm)
10    continue

      if (wthr .eq. 'M') then
c ..... Use values in precip
        do 20 mm = 1, MONTHS
          prcnxt(mm) = precip(mm)
20      continue

      elseif (wthr .eq. 'S') then

c ..... If skewness value is 0.0, select precipitation values from
c ..... normal distribution
c ..... Else, use skewness value to generate precip values
        do 30 mm = 1, MONTHS
          if (prcskw(mm) .eq. 0.0) then
            prcnxt(mm) = max(0.0, anorm(precip(mm),prcstd(mm)))
          else
            prcnxt(mm) = max(0.0, 
     &                      sknorm(precip(mm), prcstd(mm), prcskw(mm)))
          endif
30      continue

      elseif (wthr .eq. 'F') then
c ..... Read from weather data file
        open(unit=9,file=wthnam,status='OLD',err=1000)
        rewind 9

        read(9,40,end=50) label,prcnxt
40      format(a4,6x,12f7.0)
        goto 60

c ..... Error reading from weather file
50      string = '   The weather data file could not be read: ' //
     &            wthnam
        call message(string)
        STOP

60      if (label .ne. wlabel(1)) then
          call faterr(label,wlabel(1))
        endif

c ..... Check for -99.99 values and generate skewed values for ones found
        do 70 mm = 1, MONTHS
          if (prcnxt(mm) .eq. -99.99) then
            if (prcskw(mm) .eq. 0.0) then
              prcnxt(mm) = max(0.0, anorm(precip(mm),prcstd(mm)))
            else
              prcnxt(mm) = max(0.0, 
     &                        sknorm(precip(mm),prcstd(mm),prcskw(mm)))
            endif
          endif
70      continue

      elseif (wthr .eq. 'C') then
c ..... Continue with current weather file
      endif

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

1000  call message(' Fatal error: unknown weather file :'//wthnam)
      stop ' Abnormal Termination'

      end
