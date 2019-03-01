
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      common/pheno/basetemp, dayhrs, decidgrow, ddbase, hrsinc,
     &             leafout, mnddhrv, mxddhrv, tmpgerm, tmpkill, tmplff,
     &             tmplfs

c ... basetemp   - base temperature for crop growth, growing degree
c ...              days will accumulate only on days when the average
c ...              temperature is greater than the base temperature for
c ...              the crop (degrees C)
c ... dayhrs     - number of hours in a day based on julian date
c ... ddbase     - thermal units (growing degree days) required to
c ...              trigger a senescence event for a perennial plant
c ...              (FRTCINDX 3) or a non-grain filling annual
c ...              (FRTCINDX = 4) or anthesis for a grain filling
c ...              annual (FRTCINDX 5 or 6)
c ... decidgrow  - true if in period between leaf out and leaf
c ...              drop in a deciduous forest
c ... hrsinc     - indicates if the length of days in increasing
c ...              or decreasing
c ... leafout    - indicates if leafout has occured for a decidious
c ...              tree
c ... mnddhrv    - minimum number of degree days from anthesis to
c ...              harvest for grain filling annuals (FRTCINDX 5 or 6)
c ... mxddhrv    - maximum number of degree days from anthesis to
c ...              harvest for grain filling annuals (FRTCINDX 5 or 6)
c ... tmpgerm    - soil temperature required to achieve seed
c ...              germination, degrees C
c ... tmpkill    - air temperature at which plant growth stops,
c ...              degrees C
c ... tmplff     - temperature at which leaf drop will occur in a
c ...              deciduous tree type, degrees C
c ... tmplfs     - temperature at which leaf out will occur in a
c ...              deciduous tree type, degrees C

      real basetemp, dayhrs, ddbase, mnddhrv, mxddhrv, tmpgerm,
     &     tmpkill, tmplff, tmplfs
      logical decidgrow, hrsinc, leafout

      save /pheno/
