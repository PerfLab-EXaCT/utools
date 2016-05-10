# -*-Mode: makefile;-*-

#*BeginPNNLCopyright*********************************************************
#
# $HeadURL$
# $Id$
#
#***********************************************************EndPNNLCopyright*

#****************************************************************************
# $HeadURL$
#
# Nathan Tallent
#****************************************************************************

CC = mpicc

#DO_PAPI = 1
PAPI = $(HOME)/pkg/papi
PAPI_LIB = $(PAPI)/lib
PAPI_INC = $(PAPI)/include

#****************************************************************************

mpitime = libmpitime.so

$(mpitime)_SRCS = main.c

$(mpitime)_CFLAGS = -O3 -g -fPIC
ifdef DO_PAPI
  $(mpitime)_CFLAGS += -I$(PAPI_INC)
endif

$(mpitime)_LDFLAGS = -shared

$(mpitime)_LIBS =

$(mpitime)_LDADD =
ifdef DO_PAPI
  $(mpitime)_LDADD += -L$(PAPI_LIB) -Wl,-rpath $(PAPI_LIB) -lpapi
endif
#$(mpitime)_LDADD += -lrt # clock_gettime

#****************************************************************************

MK_SUBDIRS =

MK_PROGRAMS_C = $(mpitime)

include Makefile-template.mk

#****************************************************************************
