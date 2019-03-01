
c               Copyright 1993 Colorado State University
c                       All Rights Reserved


      subroutine potprod(cancvr)

      implicit none
      include 'const.inc'
      include 'param.inc'
      include 'parcp.inc'
      include 'parfs.inc'
      include 'parfx.inc'
      include 'plot1.inc'
      include 'plot3.inc'
      include 'potent.inc'
      include 'seq.inc'
      include 'timvar.inc'

c ... Argument declarations
      real cancvr

c ... Local Variables
      real pp
      real tmns, tmxs

c ... Calculate temperature...
      if (cursys .eq. FORSYS) then
c ..... Live biomass
        aglivb = rleavc * 2.5
c ..... Surface litter biomass
c ..... Second mod to remove effect of woodc -rm 1/91
        sfclit = (strucc(SRFC) + metabc(SRFC)) * 2.0
c ..... Standing dead biomass
        stdead = 0.0
c ..... Wood biomass
        woodb = (rlwodc + fbrchc) * 2.0

      elseif (cursys .eq. SAVSYS) then
c ..... Live biomass
        aglivb = (rleavc + aglivc) * 2.5
c ..... Surface litter biomass
        sfclit = (strucc(SRFC) + metabc(SRFC)) * 2.0
c ..... Standing dead biomass
        stdead = stdedc * 2.5
c ..... Wood biomass
        woodb = (rlwodc + fbrchc) * 2.0

      else
c ..... Live biomass
        aglivb = aglivc * 2.5
c ..... Surface litter biomass
        sfclit = (strucc(SRFC) + metabc(SRFC)) * 2.5
c ..... Standing dead biomass
        stdead = stdedc * 2.5
c ..... Wood biomass
        woodb = 0.0
      endif

      call surftemp(elitst, pmxtmp, pmntmp, pmxbio, maxtmp(month),
     &              mintmp(month), tmxs, tmns, stemp)

c ... Determine potential production if it's during the growth season.
c ... The variable, pp, is used below to recompute aglivb for use in h2olos.
      pp = 0.0

c ... For a Crop System...
      if (crpgrw .eq. 1) then
        call potcrp(month,cancvr)
        pp = pcropc
      endif

c ... For a Forest System...
      if (forgrw .eq. 1) then
        call potfor(month)
        pp = pforc
      endif

      if (cursys .eq. CRPSYS) then
        aglivb = aglivb + 0.25 * pp * 2.5
      endif

      return
      end
