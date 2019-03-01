
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


C ... DECOMP.F

      subroutine decomp(dtm,decsys)

      implicit none
      include 'const.inc'

c ... Argument declarations
      real      dtm
      integer   decsys

c ... Decomposition Submodel (rewritten by vek 04/91)

c                   ********** LITTER **********

c ... Decompose structural and metabolic components for surface and soil.

      call litdec(dtm)

c                   *********** WOOD ***********

c ... If the system is a forest or savanna...
c ... Decompose dead fine branches, large wood, and coarse roots.
c ... Dead fine roots are in the soil structural compartment.

      if (decsys .eq. FORSYS) then
        call woodec(dtm)
      endif

c                 ***** SOIL ORGANIC MATTER *****

c ... Decompose som1 (surface and soil), som2, and som3.

      call somdec(dtm)

      return
      end
