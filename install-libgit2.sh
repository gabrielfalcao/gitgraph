#!/bin/bash
LIBGIT2_VERSION="$(grep pygit2 requirements.txt | sed 's/^.*=//g')"
export LIBGIT2_VERSION
export LIBGIT2=/usr
tarball="v${LIBGIT2_VERSION}.tar.gz"
folder="libgit2-${LIBGIT2_VERSION}"
if [ ! -e "${tarball}" ]; then
    wget -q "https://github.com/libgit2/libgit2/archive/${tarball}"
fi
if [ ! -e "${folder}" ]; then
    tar xzf "v${LIBGIT2_VERSION}.tar.gz"
fi

cd "${folder}" || echo
cmake .
make
sudo make install
sudo ldconfig
pip install "pygit2==${LIBGIT2_VERSION}"
