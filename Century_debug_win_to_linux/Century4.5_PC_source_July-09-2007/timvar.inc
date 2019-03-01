
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


c ... Time variables not declared by Time-0
c ... blktnd = ending time of the block
c ... decodt = time step used for the decomposition model
c ... month  = current month
c ... strtyr = starting year of the block
c ... tplt   = next time (years) when variables should be written to the
c ...          plot file
c ... simyear = current simulation year
c ... strplt  = year to start outputting information to the *.bin file
c ... pltmo   = month to start outputting information to the *.bin file

      common/timvar/blktnd, decodt, month, strtyr, tplt, simyear,
     &              strplt, pltmo
      integer month, strtyr, simyear, strplt, pltmo, tplt
      real blktnd, decodt

      save /timvar/
