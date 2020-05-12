# RandomXStressGUI

This program provides an easy to use GUI interface for the RandomX benchmarking tool developed by 00-matt here https://github.com/00-matt/randomx-stress.

Give it a couple seconds to start up and a couple seconds after pressing Start.

Checking Hugepages causes it to crash on my computer, but I think it's just cause I don't have hugepages enabled (it crashes if I try to run the underlying program from command line with -H also).

![Not running](https://i.imgur.com/oeRk2vA.png?1)

![Running](https://i.imgur.com/KVHnpTM.png?1)


### If you want to build [randomx-stress](https://github.com/00-matt/randomx-stress) yourself, here are instructions:  

#### Install gcc, g++, cmake, and git through your package manager

```git clone https://github.com/tevador/randomx.git
mkdir randomx/build
pushd $_
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
cp librandomx.a /usr/local/lib/
cp ../src/randomx.h /usr/local/include/
popd

git clone https://github.com/00-matt/randomx-stress.git
mkdir randomx-stress/build
cd $_
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
./randomx-stress --args --here
```  

#### If you want to build an exe you can use Visual Studio on Windows (somehow...) or use mingw on Windows or as a cross compiler.
