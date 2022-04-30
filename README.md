# Tracking antenna control

This repository implements control software for the tracking antenna,
which can automatically point the antenna towards the rover to ensure
the best signal quality.

## Building the project

Start from the top-level directory of the project.
1. Make a `build` directory (if one doesn't already exist), and enter it:
```bash
mkdir -p build && cd build
```
2. Run CMake to locate libraries and generate Makefiles:
```bash
cmake ..
```
3. Compile the code:
```bash
cmake --build . -j$(nproc) # nproc will return the number of cores on your machine
```

Finally, you can run the project with `./antenna`. You can run the tests with `./tests`.
