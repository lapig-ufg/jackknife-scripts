
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


c                           DISCLAIMER
c
c        Neither the Great Plains System Research Unit - USDA (GPSR) nor
c     Colorado State University (CSU) nor any of their employees make
c     any warranty or assumes any legal liability or responsibility for
c     the accuracy, completeness, or usefulness of any information,
c     apparatus, product, or process disclosed, or represents that its
c     use would not infringe privately owned rights.  Reference to any
c     special commercial products, process, or service by tradename,
c     trademark, manufacturer, or otherwise, does not necessarily
c     constitute or imply endorsement, recommendation, or favoring by
c     the GPSR or CSU.  The views and opinions of the authors do not
c     necessarily state or reflect those of GPSR or CSU and shall not
c     be used for advertising or product endorsement.

      program main

c ... Century Soil Organic Matter Model
c ... Simulation of carbon, nitrogen, phosphorous, and sulfur cycling
c ... As of Dec. 1991, uses a 1 month time step
c ... Project - Soil Fertility in the Great Plains
c ... Modeler - Bill Parton
c ... Programmers - Vicki Kirchner, Becky McKeown, Laura Harding,
c ...               Melannie Hartman

c ... State variables and flows are grams/m2.

      implicit none
      include 'const.inc'
      include 'dovars.inc'
      include 'param.inc'
      include 'plot1.inc'
      include 'plot3.inc'
      include 'site.inc'
      include 't0par.inc'
      include 'timvar.inc'
      include 'wth.inc'
      include 'zztim.inc'

c ...               (unit 1) = plot/print file used by modaid (unformatted)
c ... <site>.100    (unit 7) = parameter values and initial values for
c ...                          state variables; see subroutine sitein.
c ... fix.100       (unit 8) = fixed parameter values values for
c ...                          state variables; see subroutine fixin.
c ...               (unit 9) = a file of weather data read in subroutines
c ...                          wthini, weathr
c ... c14data      (unit 10) = a data file specifying years in which labeled
c ...                          carbon is added via plant growth and what
c ...                          fraction of the growth is labeled.
c ... nscale.dat   (unit 20) = a data file specifying years in which N input
c ...                          scalars are used and the scalar values
c ... omadscale.dat(unit 30) = a data file specifying years in which organic
c ...                          matter input scalars are used and the scalar
c ...                          values
c ... phscale.dat  (unit 40) = a data file specifying years in which pH
c ...                          scalars are used and the scalar values
c ... precscale.dat(unit 50) = a data file specifying years in which
c ...                          precipitation scalars are used and the scalar
c ...                          values, precipitation scalar are multipliers
c ... tmaxscale.dat(unit 55) = a data file specifying years in which
c ...                          maximum temperature scalars are used and the
c ...                          scalar values, maximum temperature scalar are
c ...                          addends
c ... tminscale.dat(unit 60) = a data file specifying years in which
c ...                          minimum temperature scalars are used and the
c ...                          scalar values, minimum temperature scalar are
c ...                          addends

c ... If you're getting floating point errors mentioned after you exit
c ... Century, uncomment the following lines, recompile, run Century
c ... in dbx with the 'catch FPE' option to find the offending code.
c ... You can also run Century outside of dbx, in which case you will
c ... get messages on your screen giving you an fpe error code (see
c ... the Floating Point Programmer's Guide, p20) and a not-very-
c ... useful-to-3rd-or-4th-generation-language-programmers location.
c ... The error handler 'mysigal' is a Fortran callable C routine
c ... written by Martin Fowler; it can be replaced by any user written
c ... handler or any of several library handlers, the most useful
c ... probably being SIGFPE_ABORT.  The calls to ieee_handler won't
c ... compile using poa's binaries.

c      external mysigal
c      ieeer=ieee_handler('set','invalid',SIGFPE_ABORT)
c      ieeer=ieee_handler('set','division',mysigal)
c      ieeer=ieee_handler('set','overflow',mysigal)
c      ieeer=ieee_handler('set','underflow',SIGFPE_ABORT)

c ... You probably won't want to uncomment the following line; inexact
c ... floating point signals occur all over the place.

c      ieeer=ieee_handler('set','inexact',mysigal)

c ... Function declarations
      real     line
      external line

c ... Local variables
      integer outmo, mon, frstmth, tfstmth
      logical grassprod, treeprod
      real month_vals(12), neg_month_vals(12)

      data month_vals /0.08, 0.17, 0.25, 0.33, 0.42, 0.50, 0.58, 0.67,
     &                 0.75, 0.83, 0.92, 1.0/
      data neg_month_vals /-0.92, -0.83, -0.75, -0.67, -0.58, -0.50,
     &                     -0.42, -0.34, -0.25, -0.17, -0.08, 0.0/
      data frstmth /1/
      data tfstmth /1/

c ... Saved variables
      save frstmth, tfstmth

c!! Code for Victor
c      open(unit=99, file="forest.out", status='NEW', err=999)
c      write(99,*)"  Time    Leaf                              ",
c     &           "Fine Root"
c      write(99,*)"          Carbon   N       P       S        ",
c     &           "Carbon   N       P       S"
c!! End of code change for Victor

c ... Obtain startup information from user, do initializations based on
c ... answers to Modaid questions
      call detiv

c ... Write out starting values
      call wrtbin(simyear + month/12.)

c ... Update month
20    continue
      if (month .eq. 12) then
        simyear = simyear + 1
      endif
      month = mod(month,12) + 1

c ... If time is greater than the ending time for the current block,
c ... read the next block
      if ((abs(time - blktnd) .lt. (0.5 * dt)) .and.
     &    (abs(time - tend)   .gt. (0.5 * dt))) then
        call readblk()
      endif

c ... Perform annual tasks
      if (month .eq. 1) then
        call eachyr
      endif

c ... Compute SITPOT as a function of the annual precipitation, cak - 05/02/03
c ... sitpot_m is the SITPOT parameter value as read from the tree.100 file
c ... for the current tree, cak - 11/21/01
c      if (prcann .lt. 30.0) then
c        sitpot = 1000.0
      if (prcurr(month) .lt. 20.0/6.0) then
        sitpot = 1500.0
c      else if (prcann .gt. 70.0) then
c        sitpot = 3000.0
c      else if (prcann .gt. 90.0) then
c        sitpot = 4000.0
c      else if (prcann .gt. 80.0) then
c        sitpot = 3500.0
      else if (prcurr(month) .gt. 90.0/6.0) then
        sitpot = 3250.0
      else
c        sitpot = line(prcann, 30.0, 1000.0, 70.0, 3000.0)
c        sitpot = line(prcann, 30.0, 1000.0, 90.0, 4000.0)
c        sitpot = line(prcann, 30.0, 1000.0, 80.0, 3500.0)
        sitpot = line(prcurr(month),20.0/6.0,1500.0,90.0/6.0,3250.0)
      endif
      sitpot = sitpot * sitpot_m

c ... The main driver for the model; call decomposition, growth, etc.
      call simsom()

c ... Update production output variables for grass/crop system
      if (dofrst) then
c ..... If no production has occurred over the past year the growing
c ..... season production output variables get reset to zero,
c ..... initialize the monthly production values for the year,
c ..... cak - 10/02/03
        grassprod = .false.
        do 30 mon = 1, MONTHS
          if ((agcmth(mon).gt.0.001) .or. (bgcmth(mon).gt.0.001)) then
            grassprod = .true.
          endif
30      continue
        if (.not. grassprod) then
          agcprd = 0.0
          bgcprd = 0.0
        endif
c ..... Initialize monthly production values
        do 40 mon = 1, 12
          agcmth(mon) = 0
          bgcmth(mon) = 0
40      continue
        agcmth(month) = agcacc
        bgcmth(month) = bgcacc
        frstmth = month
      else
c ..... Save monthly production values, cak - 10/01/03
        agcmth(month) = agcacc
        bgcmth(month) = bgcacc
        do 50 mon = month-1, frstmth, -1
          agcmth(month) = agcmth(month) - agcmth(mon)
          bgcmth(month) = bgcmth(month) - bgcmth(mon)
50      continue
        if (month .lt. frstmth) then
          do 60 mon = 12, frstmth, -1
            agcmth(month) = agcmth(month) - agcmth(mon)
            bgcmth(month) = bgcmth(month) - bgcmth(mon)
60        continue
          do 70 mon = month-1, 1, -1
            agcmth(month) = agcmth(month) - agcmth(mon)
            bgcmth(month) = bgcmth(month) - bgcmth(mon)
70        continue
        endif
        agcmth(month) = max(0.0, agcmth(month))
        bgcmth(month) = max(0.0, bgcmth(month))
      endif

c ... Update production output variables for forest system
      if (dofone) then
c ..... If no production has occurred over the past year the growing
c ..... season production output variables get reset to zero,
c ..... initialize the monthly production values for the year,
c ..... cak - 10/02/03
        treeprod = .false.
        do 80 mon = 1, MONTHS
          if (fcmth(mon) .gt. 0.001) then
            treeprod = .true.
          endif
80      continue
        if (.not. treeprod) then
          rlvprd = 0.0
          frtprd = 0.0
          fbrprd = 0.0
          rlwprd = 0.0
          crtprd = 0.0
          fcprd = 0.0
        endif
c ..... Initialize monthly production values
        do 90 mon = 1, 12
          fcmth(mon) = 0
90      continue
        fcmth(month)  = fcacc
        tfstmth = month
      else
c ..... Save monthly production values, cak - 10/01/03
        fcmth(month)  = fcacc
        do 100 mon = month-1, tfstmth, -1
          fcmth(month)  = fcmth(month)  - fcmth(mon)
100     continue
        if (month .lt. tfstmth) then
          do 110 mon = 12, frstmth, -1
            fcmth(month)  = fcmth(month)  - fcmth(mon)
110       continue
          do 120 mon = month-1, 1, -1
            fcmth(month)  = fcmth(month)  - fcmth(mon)
120       continue
        endif
        fcmth(month)  = max(0.0, fcmth(month))
      endif

c ... Update time
c ... Add calculation to handle time drift caused by inexact floating
c ... point addition, cak - 08/23/01
c      time = time + dt
c ... Add calculation to handle incrementing the month for negative years,
c ... cak - 03/29/02
      if (time .ge. 0.0) then
        time = int(time) + month_vals(month)
      else
        time = int(time) + neg_month_vals(month)
        if (month .eq. 1) then
          time = time + 1.0
        endif
      endif
      if (time .ge. -1.0e-07 .and. time .le. 1.0e-07) then
        time = 0.0
      endif

c ... Write out values
      if ((simyear .ge. strplt) .and. (month .ge. pltmo) .and.
     &    (month .ge. outmo)) then
c      if ((tplt - time) .lt. (dt * 0.5)) then
        call wrtbin(simyear + month/12.)
c        tplt = time + dtpl
        tplt = simyear * 12 + dtpl
        strplt = tplt / 12
        outmo = mod(tplt,12)
        if (outmo .eq. 0) then
          outmo = pltmo
        endif
      endif

c ... Run for tend years
      if ((tend-time) .gt. (dt*.5)) then
        goto 20
      endif

c ... Write out final values
      call wrtbin(simyear + month/12.)

c ... Close data files

c ... Close the weather file
      close(unit=9)
c ... Close the c14data file if necessary
      if (labtyp .gt. 0) then
        close(unit=10)
      endif
c ... Close the nscale.dat file if necessary
      if (Ninput .gt. 0) then
        close(unit=20)
      endif
c ... Close the omadscale.dat file if necessary
      if (OMADinput .gt. 0) then
        close(unit=30)
      endif
c ... Close the phscale.dat file if necessary
      if (phsys .gt. 0) then
        close(unit=40)
      endif
c ... Close the precscale.dat file if necessary
      if (wthinput .eq. 4 .or. wthinput .eq. 5) then
        close(unit=50)
      endif
c ... Close the tmaxscale.dat file if necessary
      if (wthinput .eq. 2 .or. wthinput .eq. 3 .or.
     &    wthinput .eq. 5) then
        close(unit=55)
      endif
c ... Close the tminscale.dat file if necessary
      if (wthinput .eq. 1 .or. wthinput .eq. 3 .or.
     &    wthinput .eq. 5) then
        close(unit=60)
      endif
c ... Close the schedule file
      close(unit=15)

c!! Close the file created for Victor
c      close(unit=99)
c!! End of change for Victor

c ... Mark end of file
      endfile(unit=1)

c ... Close binary file
      close(unit=1)

      write(*,*) 'Execution success.'
      STOP 'Execution success.'

c!! Error message for code added for Victor
c999   write(*,*)"Unable to create forest output file!"
c      STOP "Remove or rename forest.out file before running Century."
!! End of error message for code added for Victor

      end
