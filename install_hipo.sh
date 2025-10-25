#!/bin/bash

cd hipo

# Copy from the hipo README
echo "meson setup build --prefix=`dirname $PWD` --reconfigure"
meson setup build --prefix=`dirname $PWD` --reconfigure
cd build
ninja           # compiles
ninja install   # installs to your specified prefix (../install/, in the example)
ninja test      # runs the tests
ninja clean     # clean the build directory, if you need to start over

cd -
