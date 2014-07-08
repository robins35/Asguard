#!/bin/bash

MYPATH=$(pwd)
TAHOEPATH=~/.tahoeinstall

#install
mkdir $TAHOEPATH
echo N | wget -O tahoestuff.zip tahoe-lafs.org/source/tahoe-lafs/releases/allmydata-tahoe-1.10.0.zip
mv tahoestuff.zip $TAHOEPATH
cd $TAHOEPATH
unzip tahoestuff.zip
cd allmydata-tahoe-1.10.0
python setup.py build

#run
PATH=$PATH:$TAHOEPATH/allmydata-tahoe-1.10.0/bin/
tahoe create-client
if [ -a $MYPATH/danes-tahoe.cfg ]
	then
	mv $MYPATH/danes-tahoe.cfg ~/.tahoe/tahoe.cfg
else
	echo Y | wget -O ~/.tahoe/tahoe.cfg http://sw.cs.wwu.edu/~croftp2/config/danes-tahoe.cfg
fi

tahoe start
