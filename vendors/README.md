## Third-Party Dependencies

This project makes use of the following third-party dependencies:

* Google Test

Dependency details can be found below.

## Google Test

**Source:** [https://github.com/google/googletest](https://github.com/google/googletest)

**License:** BSD 3-clause (see `googletest/LICENSE`)

**Version:** 1.8.###

**Build Instructions (Windows):**

via [Git Bash](http://gitforwindows.org)

```
git clone https://github.com/google/googletest.git
cd googletest/
cmake CMakeLists.txt
```
Open `googletest-distribution.sln` and build for all configurations.

**Build Instructions (Ubuntu):**

via Terminal

```
git clone https://github.com/google/googletest.git
cd googletest/
cmake CMakeLists.txt
make
```

Generated libraries are in `googlemock/gtest/`.
