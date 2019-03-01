#
#  Creates "list100" executable
#
#
#Source code:	list100.f
#Include files:	outval.inc
#		table.inc
f77 -u -g -c list100.f
f77 -u -g -c table.f
f77 -g -o list100 list100.o table.o

