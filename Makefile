CXXFLAGS =   -O2 -Wall 

.PHONY: clean debug all

all: setup run

setup:
	mkdir -p lib

 run:  lib/run.so lib/Reclustering.so
	$(CXX) lib/run.so lib/Reclustering.so -o $@ \
 	$(CXXFLAGS) -Wno-shadow  \
	`root-config --glibs` \
	-I./include -L./lib \
	-L$(FASTJETLOCATION)/lib `$(FASTJETLOCATION)/bin/fastjet-config --libs --plugins ` -lfastjetcontribfragile \

lib/run.so: src/run.C lib/Reclustering.so   
	$(CXX) -o $@ -c $<  \
	$(CXXFLAGS) -Wno-shadow -fPIC -shared \
	`$(FASTJETLOCATION)/bin/fastjet-config --cxxflags --plugins` \
	-I./include -L./lib \
	`root-config --cflags` 

lib/Reclustering.so : src/Reclustering.cc include/Reclustering.h 
	$(CXX) -o $@ -c $<  \
	$(CXXFLAGS) -Wno-shadow -fPIC -shared \
	`$(FASTJETLOCATION)/bin/fastjet-config --cxxflags --plugins` \
	-I./include \
	`root-config --cflags --libs` 

clean:
	rm -rf run
	rm -rf lib
	rm -f *~

install:
	install run -t ${HOME}/local/bin
