CXX=g++
AR=ar
RANLIB=ranlib

ROOTPATH=$(CURDIR)

CXXFLAGS= -g -Wall -O3 -std=c++11 -Wpedantic -DHAVE_CONFIG_H -fPIC
CFLAGS=

#first install opencore-amr
#then install libfvad and libsndfile
#modify these path

AMRROOT=/home/gzdinghanyu/opencore-amr

INCLUDEDIR= . $(AMRROOT)/include/opencore-amrnb $(AMRROOT)/include/opencore-amrwb
INCLUDEDIRFLAGS = $(addprefix -I,$(INCLUDEDIR))
LIBDIR = $(AMRROOT)/lib -L$(AMRROOT)/lib
LDLIBS= m opencore-amrwb opencore-amrnb
LDLIBSFLAGS = $(addprefix -l,$(LDLIBS))
STATICLIBS = $(AMRROOT)/lib/libopencore-amrwb.a $(AMRROOT)/lib/libopencore-amrnb.a

BINFILES =
OBJFILES = wavwriter.o amr-dec.o amrnb-dec.o amrwb-dec.o $(addsuffix .o,$(BINFILES))

EXTERNALOBJ=

all: objbuild binbuild

makesubdir:
	make -C $(ROOTPATH)/src

objbuild: $(EXTERNALOBJ) $(OBJFILES) generateLib

binbuild: objbuild $(EXTERNALOBJ) $(BINFILES)

$(EXTERNALOBJ): %.o: %.c
	$(CXX) $(CXXFLAGS) $(INCLUDEDIRFLAGS) -c $< -o $@

$(OBJFILES): %.o: %.cc
	$(CXX) $(CXXFLAGS) $(INCLUDEDIRFLAGS) -c $< -o $@

generateLib: $(OBJFILES)
	test -d $(ROOTPATH)/mylib || mkdir -p $(ROOTPATH)/mylib || exit 1
	$(AR) -cr libamr.a $(OBJFILES) $(EXTERNALOBJ)
	$(CXX) $(CXXFLAGS) -shared $(OBJFILES) $(EXTERNALOBJ) -o libamr.so -Wl,-rpath,$(LIBDIR) $(LDLIBSFLAGS) $(STATICLIBS)
	$(RANLIB) libamr.a
	mv libamr.a $(ROOTPATH)/mylib
	mv libamr.so $(ROOTPATH)/mylib

$(BINFILES): 
	$(CXX) $(CXXFLAGS) $(INCLUDEDIRFLAGS) -o $@ -Wl,-rpath,$(LIBDIR) $(LDLIBSFLAGS) -Wl,-rpath,$(ROOTPATH)/mylib -L$(ROOTPATH)/mylib -lamr

clean:
	@rm -f $(BINFILES) *.o *.a
	@rm -rf $(ROOTPATH)/mylib


.PHONY: clean all objbuild binbuild
