setup_fastjet() {
    export FASTJETLOCATION=/Users/francesco/fastjet-install/
    export LD_LIBRARY_PATH=${FASTJETPATH}lib/:$LD_LIBRARY_PATH
}

setup_fastjet