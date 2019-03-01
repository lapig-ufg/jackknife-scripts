
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      subroutine prcgrw(imnth)

      implicit none
      include 'const.inc'
      include 'parcp.inc'
      include 'wth.inc'

c ... Argument declarations
      integer imnth

c ... Compute growing season precipiation

c ... Local variables
      integer mm

      grwprc = 0.

      do 10 mm = imnth, MONTHS
        grwprc = grwprc + prcurr(mm)
10    continue

      do 20 mm = 1, imnth - 1
        grwprc = grwprc + prcnxt(mm)
20    continue

      return
      end
