#################
# 'make' build parameters
#################
MAKEFILE      = Makefile

SHELL	      = /bin/sh

#################
# Compiler parameters
#################
# COMPFLAGS - Used to set Compiler parameters on the command line. For options
#             commonly used during development (debug, static, optimize, etc).
# BLINCLINK - Used to set the compiler options needed to support BLIncLink
#             builds (via the softbench "make" script).

# For Bounds Checking and Debugging on HP turn on:
#COMPFLAGS     = -g +FPV +FPZ +FPO +FPI +FPD
#COMPFLAGS     = -g -Aa +FPV +FPZ +FPO +FPI +FPD

# For optimized runs on HP:
#COMPFLAGS     = +O3 +FPD

BLINCLINK     =

# For Bounds Checking and Debugging on HP turn on:
#FFLAGS	      = -u -N -C +T +ppu +U77 $(BLINCLINK) $(COMPFLAGS)
#CFLAGS	      = -Aa $(BLINCLINK) $(COMPFLAGS)

# For optimized runs on HP:
#FFLAGS	      = +ppu +U77 $(BLINCLINK) $(COMPFLAGS)
#CFLAGS	      = -Aa $(BLINCLINK) $(COMPFLAGS)

# For work with the Modaid crapola:
#FFLAGS	      = -g -c -N +U77 $(BLINCLINK) $(COMPFLAGS)

# For work with the IBM xlf compiler:
#FFLAGS	      = -g -c -C -qextname $(BLINCLINK) $(COMPFLAGS)

# For work with the SUN compiler:
#FFLAGS	      = -g -c -C $(BLINCLINK) $(COMPFLAGS)
FFLAGS	      =  -fno-underscoring -fno-second-underscore -c -O2 $(BLINCLINK) $(COMPFLAGS)

CCFLAGS       = $(BLINCLINK) $(COMPFLAGS)
CXXFLAGS      = $(BLINCLINK) $(COMPFLAGS)
C++FLAGS      = $(BLINCLINK) $(COMPFLAGS)

# For HP ansi C
# ANSI_CC	= cc
# ANSI_CFLAGS	= $(CFLAGS)

# For GNU ansi C
ANSI_CC	= gfortran
ANSI_CFLAGS	= -ansi


#################
# Special 'mkmf' macros
#################
# SUFFIX   - List of additional file name suffixes for 'mkmf' to know about

SUFFIX         =    





#################
# User-added macros
#################
# (Add any other macros which are to be set through 'mkmf')

#################
# Header file parameters 
#################

#    Uncomment this if you want system header files to be expanded
#
# SYSHDRS       =

EXTHDRS	      =

HDRS	      = flow.h,flow_double.h

#################
# Loader and options to be used for the final program link step.
#################

# For HP, SUN
LD	      = gfortran
#LD	      = ld

# For IBM
#LD            = xlf

# For HP debugging
#LDFLAGS	      = +U77 +FPV +FPZ +FPO $(COMPFLAGS)
#LDFLAGS	      = -m -t -v -z +FPV +FPZ +FPO $(COMPFLAGS) -lU77

# For all machines with general debugging.
LDFLAGS       = $(COMPFLAGS)

#################
# Library parameters
#################
# LIBS       - Archive or shared libraries in development (the archive
#              libraries are not compiled BLIncLink).
# SYSLIBS    - Libraries not in development (may specify with "-l" options)
# ARCHIVES   - Archive libraries in development which are compiled BLIncLink.
# NONPRELINK - Object files not guaranteed to be compiled BLIncLink.
#
#              (Refer to the blinclink(5) reference pages for more details)

LIBS          =

# For HP only
#SYSLIBS      = -lm -lU77

# For SUN
SYSLIBS	      = -lm

ARCHIVES      = 

NONPRELINK    = 

#################
# Program parameters
#################

PROGRAM       = century
#PROGRAM       = century.dbg

SRCS	      = adjlig.f \
		agdrat.f \
		anerob.f \
		annacc.f \
		anorm.f \
		bgdrat.f \
		calciv.f \
		candec.f \
		ckdata.f \
		cmplig.f \
		co2eff.f \
		crop.f \
		cropin.f \
		sitein_grid.f \
		default.f \
		initialize.f \
		csa_detiv.f \
		csa_main.f \
		csched.f \
		cultin.f \
		cultiv.f \
		cutrtn.f \
		potprod.f \
		surftemp.f \
		cycle.f \
		fltce.f \
		cropdync.f \
		climscale.f \
		omadscale.f \
		nscale.f \
		phshift.f \
		daylen.c \
		declig.f \
		decomp.f \
		dedrem.f \
		droot.f \
		dshoot.f \
		eachyr.f \
		erosn.f \
		esched.f \
		extend.f \
		falstd.f \
		faterr.f \
		ferr.c \
		fertin.f \
		firein.f \
		firrtn.f \
		fixin.f \
		floclr.c \
		flow.c \
		flowd.c \
		flow_double.c \
		flow_double_in.c \
		flow_double_out.c \
		flowd_double.c \
		flowup_double.c \
		flowup_double_in.c \
		flowup_double_out.c \
		flowd_double_in.c \
		flowd_double_out.c \
		floclr_double.c\
		floclr_double_in.c\
		floclr_double_out.c\
		flowup.c \
		fracis.f \
		frem.f \
		fsfunc.f \
		gpdf.f \
		grazin.f \
		grazrst.f \
		grem.f \
		grochk.f \
		growth.f \
		snowcent.f \
		h2olos.f \
		harvin.f \
		harvst.f \
		inprac.f \
		irrgin.f \
		irrigt.f \
		killrt.f \
		lacalc.f \
		laprod.f \
		leach.f \
		leafa.f \
		line.f \
		litburn.f \
		litdec.f \
		livrem.f \
		message.f \
		mnracc.f \
		nutrlm.f \
		omadin.f \
		parse.f \
		partit.f \
		pevap.f \
		potcrp.f \
		shwave.f \
		treedync.f \
		potfor.f \
		pprdwc.f \
		prcgrw.f \
		predec.f \
		prelim.f \
		pschem.f \
		froota.f \
		ramp.f \
		randu.f \
		ranfun.f \
		readblk.f \
		respir.f \
		restrp.f \
		rtimp.f \
		savarp.f \
		schedl.f \
		simsom.f \
		sitein.f \
		sknorm.f \
		soilos.f \
		somdec.f \
		sumcar.f \
		tcalc.f \
		treein.f \
		trees.f \
		treegrow.f \
		tremin.f \
		wdeath.f \
		weathr.f \
		woodec.f \
		wrtbin.f \
		wthini.f

OBJS	      = adjlig.o \
		agdrat.o \
		anerob.o \
		annacc.o \
		anorm.o \
		bgdrat.o \
		calciv.o \
		candec.o \
		ckdata.o \
		cmplig.o \
		co2eff.o \
		crop.o \
		cropin.o \
		sitein_grid.o \
		default.o \
		initialize.o \
		csa_detiv.o \
		csa_main.o \
		csched.o \
		cultin.o \
		cultiv.o \
		cutrtn.o \
		potprod.o \
		surftemp.o \
		cycle.o \
		fltce.o \
		cropdync.o \
		climscale.o \
		omadscale.o \
		nscale.o \
		phshift.o \
		daylen.o \
		declig.o \
		decomp.o \
		dedrem.o \
		droot.o \
		dshoot.o \
		eachyr.o \
		erosn.o \
		esched.o \
		extend.o \
		falstd.o \
		faterr.o \
		ferr.o \
		fertin.o \
		firein.o \
		firrtn.o \
		fixin.o \
		floclr.o \
		flow.o \
		flowd.o \
		flow_double.o \
		flow_double_in.o \
		flow_double_out.o \
		flowd_double.o \
		flowup_double.o \
		flowup_double_in.o \
		flowup_double_out.o \
		flowd_double_in.o \
		flowd_double_out.o \
		floclr_double.o\
		floclr_double_in.o\
		floclr_double_out.o\
		froota.o \
		flowup.o \
		fracis.o \
		frem.o \
		fsfunc.o \
		gpdf.o \
		grazin.o \
		grazrst.o \
		grem.o \
		grochk.o \
		growth.o \
		snowcent.o \
		h2olos.o \
		harvin.o \
		harvst.o \
		inprac.o \
		irrgin.o \
		irrigt.o \
		killrt.o \
		lacalc.o \
		laprod.o \
		leach.o \
		leafa.o \
		line.o \
		litburn.o \
		litdec.o \
		livrem.o \
		message.o \
		mnracc.o \
		nutrlm.o \
		omadin.o \
		shwave.o \
		treedync.o \
		parse.o \
		partit.o \
		pevap.o \
		potcrp.o \
		potfor.o \
		pprdwc.o \
		prcgrw.o \
		predec.o \
		prelim.o \
		pschem.o \
		ramp.o \
		randu.o \
		ranfun.o \
		readblk.o \
		respir.o \
		restrp.o \
		rtimp.o \
		savarp.o \
		schedl.o \
		simsom.o \
		sitein.o \
		sknorm.o \
		soilos.o \
		somdec.o \
		sumcar.o \
		tcalc.o \
		treein.o \
		treegrow.o \
		trees.o \
		tremin.o \
		wdeath.o \
		weathr.o \
		woodec.o \
		wrtbin.o \
		wthini.o

#################
#  'lint' parameters
#################

LINTLIBS      =

LINTFLAGS     = -u $(CFLAGS)

#################
#  'print' parameters
#################

PRINT	      = pr

PRINTFLAGS    =

LP	      = lp

LPFLAGS       = 

#################
# 'install'/'update' parameters
#################

DEST	      = .

INSTALL	      = install

#################
# Target Rules
#################

all:		$(PROGRAM)

all.blinc:	$(PROGRAM).blinc

all.prelink:	$(PROGRAM).prelink

$(PROGRAM):           $(NONPRELINK) $(OBJS) $(ARCHIVES) $(LIBS) $(MAKEFILE)
		@echo "Linking $(PROGRAM) ..."
		$(LD) -o $(PROGRAM) $(LDFLAGS) $(NONPRELINK) \
			$(OBJS) $(ARCHIVES) $(LIBS) $(SQLLIBS) $(SYSLIBS)
		@echo "done"

$(PROGRAM).prelink:   $(OBJS) $(ARCHIVES) $(PROGRAM).alt.blinc
		@echo "Prelinking $(PROGRAM) ..."
		$(LD) -o $(PROGRAM) $(LDFLAGS) \
			-prelink $(OBJS) $(ARCHIVES)
		$(LD) -o $(PROGRAM) $(LDFLAGS) $(NONPRELINK) \
			-blinc $(LIBS) $(SQLLIBS) $(SYSLIBS)
		@echo "" > $(PROGRAM).blinc
		@echo "done"

$(PROGRAM).blinc:     $(OBJS) $(ARCHIVES) $(PROGRAM).alt.blinc
		@echo "BLIncLinking $(PROGRAM) ..."
		$(LD) -o $(PROGRAM) $(LDFLAGS) $(NONPRELINK) \
			-blinc  $?  $(LIBS) $(SQLLIBS) $(SYSLIBS)
		@echo "" > $(PROGRAM).blinc
		@echo "done"

$(PROGRAM).alt.blinc: $(NONPRELINK) $(LIBS) $(MAKEFILE)
		@echo "" > $(PROGRAM).alt.blinc


clean:;		@rm -f $(OBJS) core

clobber:;	@rm -f $(OBJS) core tags \
		$(PROGRAM) $(PROGRAM).blinc $(PROGRAM).bld_history \
		$(PROGRAM)_bld.sl $(PROGRAM).alt.blinc
		@if [ -n "$(ARCHIVES)" ] ; \
		then \
		  liblist=$(ARCHIVES); \
		  for file in $$liblist; \
		  do \
		    lfile=`basename $$file`; \
		    rm -f $${lfile}.bld_history $${lfile}.bld_stamp; \
		  done; \
		fi

depend:;	@mkmf -f $(MAKEFILE) ROOT=$(ROOT)

echo:;		@echo $(HDRS) $(SRCS)

index:;		@ctags -wx $(HDRS) $(SRCS)

install:	$(PROGRAM)
		@echo Installing $(PROGRAM) in $(DEST)
		@-strip $(PROGRAM)
		@if [ $(DEST) != . ]; then \
                (rm -f $(DEST)/$(PROGRAM); $(INSTALL) -f $(DEST) $(PROGRAM)); fi

lint:		$(LINTLIBS) $(SRCS) $(HDRS) $(EXTHDRS)
		lint $(LINTFLAGS) $(LINTLIBS) $(SRCS)

print:;		@$(PRINT) $(PRINTFLAGS) $(HDRS) $(SRCS) | $(LP) $(LPFLAGS)

tags:           $(HDRS) $(SRCS); @ctags $(HDRS) $(SRCS)

update:		$(DEST)/$(PROGRAM)

touch:;		@touch $(SRCS) $(HDRS)

#$(DEST)/$(PROGRAM): $(SRCS) $(LIBS) $(HDRS) $(EXTHDRS)
#		@$(MAKE) -f $(MAKEFILE) ROOT=$(ROOT) DEST=$(DEST) install

.c.o:
	@echo Compiling $< [$(LANGUAGE)] [UX-CODE]
	$(ANSI_CC) -c $(ANSI_CFLAGS) $< -o $@

###
annacc.o: const.inc plot1.inc plot2.inc param.inc
anorm.o: pi.inc
calciv.o: chrvar.inc const.inc ligvar.inc param.inc parcp.inc parfs.inc \
	plot1.inc plot3.inc site.inc zztim.inc
candec.o: const.inc
cmplig.o: const.inc param.inc wth.inc zztim.inc
co2eff.o: const.inc param.inc parfx.inc plot1.inc
sitein_grid.o: const.inc doubles.inc param.inc plot1.inc plot3.inc site.inc wth.inc
default.o: chrvar.inc comput.inc doubles.inc dovars.inc dynam.inc fertil.inc forrem.inc isovar.inc \
	ligvar.inc param.inc parcp.inc parfs.inc parfx.inc pheno.inc plot1.inc plot2.inc plot3.inc \
	potent.inc schvar.inc  seq.inc site.inc t0par.inc timvar.inc wth.inc zztim.inc
initialize.o: chrvar.inc const.inc dovars.inc fertil.inc param.inc plot1.inc plot2.inc seq.inc \
	timvar.inc wth.inc zztim.inc
crop.o: dovars.inc isovar.inc ligvar.inc parcp.inc plot2.inc const.inc \
	param.inc seq.inc plot1.inc
cropin.o: chrvar.inc comput.inc const.inc isovar.inc ligvar.inc param.inc \
	parcp.inc parfs.inc parfx.inc plot1.inc seq.inc
csa_detiv.o: chrvar.inc const.inc doubles.inc dovars.inc fertil.inc param.inc \
	parfs.inc plot1.inc potent.inc seq.inc t0par.inc timvar.inc wth.inc zztim.inc
csa_main.o: t0par.inc timvar.inc zztim.inc
csched.o: const.inc zztim.inc
cultin.o: parcp.inc
cultiv.o: const.inc param.inc parcp.inc plot1.inc zztim.inc
cutrtn.o: const.inc forrem.inc param.inc parfs.inc plot1.inc plot2.inc \
	plot3.inc zztim.inc
surftemp.o: param.inc parcp.inc parfs.inc site.inc timvar.inc zztim.inc
potprod.o: const.inc param.inc parcp.inc parfs.inc parfx.inc plot1.inc plot3.inc \
	potent.inc seq.inc timvar.inc
cycle.o: comput.inc const.inc dovars.inc param.inc parcp.inc parfs.inc \
	parfx.inc plot1.inc plot2.inc plot3.inc potent.inc seq.inc wth.inc
fltce.o: comput.inc const.inc dovars.inc parcp.inc
cropdync.o: comput.inc const.inc param.inc parcp.inc parfx.inc plot1.inc potent.inc
climscale.o: wth.inc
omadscale.o: fertil.inc
nscale.o: fertil.inc
phshift.o: param.inc
declig.o: const.inc zztim.inc
decomp.o: const.inc
dedrem.o: const.inc forrem.inc param.inc plot2.inc plot3.inc zztim.inc
droot.o: const.inc param.inc parcp.inc parfx.inc plot1.inc
dshoot.o: const.inc dovars.inc param.inc parcp.inc parfx.inc plot1.inc \
	plot2.inc zztim.inc
eachyr.o: comput.inc const.inc isovar.inc ligvar.inc param.inc parcp.inc parfs.inc \
	plot1.inc plot2.inc plot3.inc potent.inc seq.inc site.inc wth.inc zztim.inc
erosn.o: const.inc plot1.inc plot2.inc zztim.inc
esched.o: zztim.inc
extend.o: outval.inc
falstd.o: const.inc param.inc parcp.inc plot1.inc
ferr.o: flow.h
fertin.o: fertil.inc const.inc
firein.o: parcp.inc const.inc
firrtn.o: const.inc dovars.inc forrem.inc param.inc plot1.inc plot2.inc \
	plot3.inc zztim.inc
fixin.o: const.inc parfx.inc
floclr.o: flow.h
flow.o: flow.h
flow_double.o: flow_double.h
flow_double_in.o: flow_double_in.h
flow_double_out.o: flow_double_out.h		
flowup_double.o: flow_double.h
flowup_double_in.o: flow_double_in.h
flowup_double_out.o: flow_double_out.h
floclr_double.o: flow_double.h
floclr_double_in.o: flow_double_in.h
floclr_double_out.o: flow_double_out.h
frem.o: const.inc forrem.inc
grazin.o: parcp.inc const.inc
grem.o: const.inc dovars.inc param.inc parcp.inc plot1.inc plot2.inc \
	zztim.inc seq.inc
grochk.o: pheno.inc timvar.inc zztim.inc
growth.o: comput.inc const.inc dovars.inc fertil.inc param.inc \
	parcp.inc parfx.inc plot1.inc plot2.inc plot3.inc potent.inc seq.inc \
	site.inc zztim.inc
snowcent.o: site.inc
h2olos.o: const.inc param.inc parfs.inc parfx.inc plot1.inc plot3.inc seq.inc
harvin.o: parcp.inc param.inc
harvst.o: const.inc param.inc parcp.inc plot1.inc plot2.inc zztim.inc
inprac.o: const.inc dovars.inc timvar.inc plot1.inc plot2.inc plot3.inc
irrgin.o: parcp.inc
irrigt.o: param.inc parcp.inc plot1.inc wth.inc
killrt.o: const.inc forrem.inc param.inc parfs.inc plot2.inc plot3.inc \
	zztim.inc
leafa.o: parfs.inc
litburn.o: const.inc param.inc parcp.inc plot1.inc plot2.inc zztim.inc
litdec.o: comput.inc const.inc param.inc parcp.inc parfx.inc plot1.inc \
	plot2.inc
livrem.o: const.inc forrem.inc param.inc plot2.inc plot3.inc zztim.inc
nutrlm.o: const.inc
omadin.o: parcp.inc const.inc
shwave.o: pi.inc
treedync.o: comput.inc const.inc param.inc parfs.inc parfx.inc pheno.inc \
	plot1.inc plot3.inc potent.inc
partit.o: const.inc param.inc parfx.inc plot1.inc zztim.inc
pevap.o: const.inc param.inc parfx.inc site.inc
potcrp.o: comput.inc const.inc dovars.inc param.inc parcp.inc parfx.inc \
	plot1.inc plot3.inc potent.inc seq.inc site.inc wth.inc
potfor.o: comput.inc const.inc dynam.inc param.inc parfs.inc parfx.inc pheno.inc \
	plot1.inc plot3.inc potent.inc site.inc wth.inc
prcgrw.o: const.inc parcp.inc wth.inc
predec.o: comput.inc const.inc param.inc parfx.inc plot1.inc plot3.inc \
	seq.inc
prelim.o: comput.inc const.inc param.inc parcp.inc parfs.inc parfx.inc \
	pheno.inc plot1.inc plot2.inc seq.inc site.inc t0par.inc timvar.inc \
	wth.inc zztim.inc
pschem.o: const.inc param.inc parfx.inc plot1.inc site.inc zztim.inc
readblk.o: chrvar.inc const.inc param.inc schvar.inc seq.inc t0par.inc \
	timvar.inc zztim.inc site.inc
respir.o: const.inc param.inc parfx.inc zztim.inc
restrp.o: const.inc fertil.inc parfx.inc seq.inc zztim.inc
savarp.o: comput.inc const.inc param.inc plot1.inc plot2.inc plot3.inc
schedl.o: chrvar.inc const.inc dovars.inc fertil.inc forrem.inc param.inc \
	parcp.inc parfs.inc plot1.inc plot2.inc schvar.inc seq.inc timvar.inc \
	zztim.inc
simsom.o: comput.inc const.inc dovars.inc fertil.inc isovar.inc ligvar.inc \
	param.inc parfs.inc parfx.inc pheno.inc plot1.inc plot2.inc plot3.inc \
	potent.inc seq.inc site.inc t0par.inc timvar.inc wth.inc zztim.inc
sitein.o: const.inc param.inc plot1.inc plot3.inc site.inc wth.inc
sknorm.o: parfx.inc
soilos.o: const.inc
somdec.o: comput.inc const.inc param.inc parcp.inc parfx.inc plot1.inc \
	plot2.inc zztim.inc
sumcar.o: plot1.inc plot2.inc plot3.inc
treein.o: chrvar.inc const.inc isovar.inc param.inc parcp.inc parfs.inc \
	site.inc
treegrow.o: const.inc dynam.inc fertil.inc isovar.inc param.inc parfs.inc parfx.inc \
	plot1.inc plot2.inc plot3.inc potent.inc zztim.inc
trees.o: const.inc dovars.inc fertil.inc param.inc parcp.inc \
	parfs.inc parfx.inc plot1.inc plot2.inc plot3.inc potent.inc seq.inc \
	zztim.inc
tremin.o: forrem.inc const.inc
wdeath.o: const.inc dovars.inc isovar.inc param.inc parfs.inc pheno.inc \
	plot3.inc timvar.inc zztim.inc
weathr.o: chrvar.inc const.inc wth.inc
woodec.o: comput.inc const.inc param.inc parfs.inc parfx.inc plot1.inc \
	plot2.inc plot3.inc
wrtbin.o: outval.inc
wthini.o: chrvar.inc const.inc wth.inc

