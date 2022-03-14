#! /usr/bin/env sh

git clone https://openmodelica.org/git-readonly/OpenModelica.git openmodelica
cd openmodelica
git checkout tags/v1.18.1
git submodule update --init --recursive common libraries doc OMCompiler OMShell
autoconf
./configure --prefix=/usr --disable-modelica3d --with-omniORB=/usr
make -j4
make install
