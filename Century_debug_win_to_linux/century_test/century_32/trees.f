
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      subroutine trees (bgwfunc)

      implicit none
      include 'dovars.inc'
      include 'fertil.inc'
      include 'parcp.inc'
      include 'plot1.inc'
      include 'plot2.inc'
      include 'timvar.inc'
      include 'zztim.inc'

c ... Argument declarations
      real      bgwfunc

c ... Simulate forest production for the month.

c ... Fortran to C prototype
      INTERFACE

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

c ... Local variables
      integer ii

c ... Option to add organic matter; added here so that it won't be
c ... done twice in savanna
      if (doomad) then
        call partit(astgc*OMADscalar(month),astrec,1,csrsnk,esrsnk,
     &              astlig,astlbl)
c ..... Update OMAD accumulator output variables, cak - 07/13/2006
        omadac = omadac + (astgc*OMADscalar(month))
        do 20 ii = 1, 3
          omadae(ii) = omadae(ii) +
     &                 (astgc*OMADscalar(month) * astrec(ii))
20      continue
c ..... don't let organic matter be added twice in savana
        doomad = .FALSE.
      endif

c ... Update flows so direct absorption will be accounted for
c ... before plant uptake
      call flowup(time)
      call flowup_double(time)
      call flowup_double_in(time)
      call flowup_double_out(time)
      call sumcar

      call treegrow()

c ... Death of tree parts
      call wdeath(tave, bgwfunc)

c ... Update state variables and accumulators and sum carbon isotopes.
      call flowup(time)
      call flowup_double(time)
      call flowup_double_in(time)
      call flowup_double_out(time)
      call sumcar

      return
      end
