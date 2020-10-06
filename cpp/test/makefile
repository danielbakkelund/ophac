
STD=c++17

LOCALFLAGS=

STDFLAG =
ifneq ($(STD),)
STDFLAG += -std=$(STD)
endif

DEPFILE = .dependencies

RM = rm -f

SRCFILES := $(wildcard *.cpp)
OBJFILES := $(patsubst %.cpp,%.o,$(SRCFILES))

JSONDIR      = ../json
CPUNITDIR    = cpunit
CPUNITLIBDIR = $(CPUNITDIR)/lib
TESTCINC     = $(CINC) -I$(CPUNITDIR)/src -I$(JSONDIR)/include
TESTCFLAGS   = $(CFLAGS) 
TESTLNFLAGS  = $(CLNLIBS) -L$(CPUNITDIR)/lib -lCPUnit

PRODSRC := $(wildcard ../src/*)

CC = g++
CFLAGS = $(STDFLAG) -g -c -I../src -Icpunit/src -I$(JSONDIR)/include -Wall -O0  -D_POSIX_TIMERS $(LOCALFLAGS)
COMPILE = $(CC) $(CFLAGS) # -DSHOW_ERRORS

LNK = g++
LFLAGS = -L../release/lib $(TESTLNFLAGS) -lophacuntied

default: all
	./tester -a

# Dependency: CPUnit
$(CPUNITDIR):
	mkdir $@
	@echo "Downloading head of qpr branch of CPUnit..."
	svn checkout svn://svn.code.sf.net/p/cpunit/code/branches/qpr $(CPUNITDIR)
	@echo "Building CPUnit..."
	cd $(CPUNITDIR) && make STD=$(STD) all # ./build_cpunit
	@echo "Done building CPUnit!"
	@echo "Make sure to add $(CPUNITDIR)/src to the include path and $(CPUNITDIR)/lib/libCPUnit.a to the libraries"


$(JSONDIR):
	mkdir $@
	@echo Downloading head of 
	git clone https://github.com/nlohmann/json.git $(JSONDIR)

all : tester

tester:  $(CPUNITDIR) $(JSONDIR) $(OBJFILES) 
	$(LNK) -o tester $(LFLAGS) $(OBJFILES)

%.o: %.cpp
	$(COMPILE) -o $@ $<

clean:
	@$(RM) $(OBJFILES) tester

depend:
	@echo "" > $(DEPFILE)
	@makedepend -f$(DEPFILE) -I../src $(SRCFILES)

-include $(DEPFILE)
