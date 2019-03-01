
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      real function randu(k)

      implicit none

c ... Argument declarations
      integer k

c ... ******************** flowlib ********************* 
c ...
c ...     (run-time sub-set of modaid, exclusive of modctl) 
c ...
c ...     release 1.0  (first formal release of modaid) 
c ...
c ...     james m. vevea
c ...     natural resource ecology lab
c ...     colorado state university 
c ...     fort collins, colorado	80523 
c ...
c ... randu is based on knuth's seminumerical algorithms 
c ... i changed the values that he suggested to allow
c ... running on a 16 bit integer machine, such as many
c ... dec systems

c ... Local variables
      integer itab(64), ii, ia, ic, ictr, 
     &        ixold, ixoldi, iyold, iyoldi, m
      real    am
      logical init 

c ... the table, and the value for init need to be saved.
      save itab, init, ictr, am, ixold, iyold

      data init/.false./ 
      data ixoldi,iyoldi/57721,17810/
      data m,ia,ic/566927,3612,5701/ 

      if ((.not. init) .or. k.lt.0) then
        am = m 
        init = .true.
        ixold = ixoldi
        iyold = iyoldi
        do 99 ii=1,64 
          ixold = mod((ia*ixold + ic),m) 
          itab(ii) = ixold
99      continue 
      endif
      if (k.le.0) ictr = 0
      ictr = ictr + 1
      k = ictr
      iyold = mod((ia*iyold + ic),m) 
      ixold = mod((ia*ixold + ic),m) 
      ii = 1 + mod(iyold,64)
      randu = float(itab(ii)) / am
      itab(ii) = ixold

      return 
      end
