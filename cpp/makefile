
STD=c++11

LOCALFLAGS=

DEBUGFLAGS= # -D DEBUG

OPTFLAGS = -O3 #-g -O1

STDFLAG =
ifneq ($(STD),)
STDFLAG += -std=$(STD)
endif

DEPFILE = .dependencies

JSONDIR = json
DISTDIR = release
LIBDIR  = $(DISTDIR)/lib
LIBBIN  = libophacuntied.a
INCDIR  = $(DISTDIR)/include
LIBFILE = $(LIBDIR)/$(LIBBIN)
EXEFILE = $(LIBDIR)/ophac_untied

CC = g++
CFLAGS = $(STDFLAG) -W -Wall -pedantic $(OPTFLAGS) -I./src -I$(JSONDIR)/include $(LOCALFLAGS) $(DEBUGFLAGS)
COMPILE = $(CC) -c $(CFLAGS) 

LIB_LNK    = ar
LIB_LFLAGS = -rcs
LIB_LINK   = $(LIB_LNK) $(LIB_LFLAGS)

EXE_LNK    = g++
EXE_LFLAGS = -L$(LIBDIR) -lophacuntied -o
EXE_LINK   = $(EXE_LNK) $(EXE_LFLAGS)

PYBIND_SRC = $(wildcard pybind_src/*.cpp)
PYBIND_MOD = ophac_cpp
PYBIND_INC = `python3 -m pybind11 --includes`
PYBIND_BIN = $(LIBDIR)/$(PYBIND_MOD)`python3-config --extension-suffix`
PYBIND_LNK = -L$(LIBDIR) -lophacuntied -o $(PYBIND_BIN)

RM = rm -f

SRCFILES := $(wildcard src/*.cpp)
OBJFILES := $(patsubst %.cpp,%.o,$(SRCFILES))

default: 
	@$(MAKE) install
	@$(MAKE) pybind

all: 
	@$(MAKE) install
	@$(MAKE) run_tests

nolink: $(OBJFILES)

#libfile: $(OBJFILES) $(LIBFILE) 

$(JSONDIR):
	@mkdir $@
	@echo Downloading head of 
	git clone https://github.com/nlohmann/json.git $(JSONDIR)

$(DISTDIR):
	@mkdir $@

$(LIBDIR): $(DISTDIR)
	@mkdir $@

$(INCDIR): $(DISTDIR)
	@mkdir $@

$(LIBFILE): $(LIBDIR) $(OBJFILES) $(SRCFILES)
	$(RM) $(LIBFILE)
	$(LIB_LINK) $(LIBFILE) $(filter-out src/*_main.o, $(OBJFILES))

$(EXEFILE): $(LIBDIR) $(OBJFILES) $(SRCFILES)
	$(RM) $(EXEFILE)
	$(EXE_LINK) $(EXEFILE) $(wildcard src/*_main.o)

pybind:
	$(CC) $(CFLAGS) -undefined dynamic_lookup $(PYBIND_SRC) $(PYBIND_INC) $(PYBIND_LNK)

tests: install
	@cd test && $(MAKE) STD=$(STD) LOCALFLAGS=$(LOCALFLAGS) all

run_tests:
	@cd test && $(MAKE) STD=$(STD) LOCALFLAGS=$(LOCALFLAGS)

install: $(LIBFILE) $(INCDIR) $(EXEFILE)
	@cd $(LIBDIR) && echo $(LIBFILE) " installed"
	@cp src/*.hpp $(INCDIR) 	#@cp src/*.tpp $(INCDIR)

%.o: %.cpp | $(JSONDIR)
	$(COMPILE) -o $@  $<

include $(wildcard src/*.P)

clean_tests:
	@cd test && $(MAKE) clean

clean:
	@$(RM) $(OBJFILES) $(LIBFILE)
	@make clean_tests

depend:
	@echo "" > $(DEPFILE)
	@makedepend -f$(DEPFILE) $(SRCFILES)
	@cd test && $(MAKE) depend

-include $(DEPFILE)
