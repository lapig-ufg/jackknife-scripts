
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


C ... RANFUN.F

      real function gasdev(idum)

      implicit none

c ... Argument declarations
      integer  idum

c ... THESE FUNCTIONS ARE NOT FOR SOURCE CODE DISTRIBUTION
c ... --Laura Harding (1993)

c ... GASDEV
c ... (C) 1986 Numerical Recipes Software

c ... Function declarations
      real      ran1
      external  ran1

c ... Local variables
      integer   iset
      real      fac, gset, r, v1, v2
      save      gset

      data      iset/0/

      if (iset .eq. 0) then
1       v1 = 2. * ran1(idum) - 1.
        v2 = 2. * ran1(idum) - 1.
        r = v1**2 + v2**2
        if (r .ge. 1. .or. r .eq. 0.) then
          goto 1
        endif
        fac = sqrt(-2. * log(r)/r)
        gset = v1 * fac
        gasdev = v2 * fac
        iset = 1
      else
        gasdev = gset
        iset = 0
      endif

      return
      end


c ... RAN1
c ... (C) 1986 Numerical Recipes Software

      real function ran1(idum)

      implicit none

c ... Argument declarations
      integer   idum

c ... Local variables
      integer   ia1, ia2, ia3, ic1, ic2, ic3, iff, ix1, ix2, ix3, jj,
     &          m1, m2, m3
      real      r(97), rm1, rm2
      save      r, ix1, ix2, ix3

      parameter (m1=259200,ia1=7141,ic1=54773,rm1=3.8580247e-6)
      parameter (m2=134456,ia2=8121,ic2=28411,rm2=7.4373773e-6)
      parameter (m3=243000,ia3=4561,ic3=51349)
      data      iff /0/

      if (idum .lt. 0 .or. iff .eq. 0) then
        iff = 1  
        ix1 = mod(ic1 - idum, m1)
        ix1 = mod(ia1 * ix1 + ic1, m1)
        ix2 = mod(ix1, m2)
        ix1 = mod(ia1 * ix1 + ic1, m1)
        ix3 = mod(ix1, m3)
        do 10 jj = 1, 97
          ix1 = mod(ia1 * ix1 + ic1, m1)
          ix2 = mod(ia2 * ix2 + ic2, m2)
          r(jj) = (float(ix1) + float(ix2) * rm2) * rm1
10      continue
        idum = 1
      endif
      ix1 = mod(ia1 * ix1 + ic1, m1)
      ix2 = mod(ia2 * ix2 + ic2, m2)
      ix3 = mod(ia3 * ix3 + ic3, m3)
      jj = 1 + (97 * ix3)/m3
      if (jj .gt. 97 .or. jj .lt. 1) then
        pause
      endif
      ran1 = r(jj)
      r(jj) = (float(ix1) + float(ix2) * rm2) *rm1

      return
      end
