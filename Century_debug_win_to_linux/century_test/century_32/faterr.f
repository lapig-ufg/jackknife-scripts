
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      subroutine faterr(itell1,itell2)

      implicit none

c ... Argument declarations
      character*4 itell1, itell2

c ... An error on the weather data file has been detected;
c ... terminate execution.

c ... Local variables
      character*80 string

      call message('    ')
      call message('   The weather file is out of sequence.')
      string = '   A record for ' // itell2 // ' was expected.'
      call message(string)
      string = '   The record read was labeled ' // itell1 // '.'
      call message(string)

      STOP
      end
