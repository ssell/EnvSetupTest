# Creates all project and solution files using CMake.
# The generator used is determined by the active operating system.

import os
import logging
import subprocess
import argparse
import shutil 

from sys import platform

COMPILER_WIN         = "msvc141"                        # Compiler identifier added to library output (example: API_msvc141.dll)
COMPILER_LINUX       = ""                               # Compiler identifier added to library output
COMPILER_OSX         = ""                               # Compiler identifier added to library output
GENERATOR_WIN32      = "Visual Studio 15 2017"          # CMake generator to use for Windows x86
GENERATOR_WIN64      = "Visual Studio 15 2017 Win64"    # CMake generator to use for Windows x64
GENERATOR_LINUX      = "Unix Makefiles"                 # CMake generator to use for Linux
GENERATOR_OSX        = "Xcode"                          # CMake generator to use for OS X
API_DIR              = "API/"                           # Main directory for the API project  
BUILD_DIR            = "build/"                         # Build subdirectory within project directories
BUILD_SUBDIR_WIN32   = "VS2017_x86/"                    # Subdirectory within build for Windows x86 projects
BUILD_SUBDIR_WIN64   = "VS2017_x64/"                    # Subdirectory within build for Windows x64 projects
BUILD_SUBDIR_LINUX32 = "linux_x86/"                     # Subdirectory within build for Linux x86 projects
BUILD_SUBDIR_LINUX64 = "linux_x64/"                     # Subdirectory within build for Linux x64 projects
BUILD_SUBDIR_OSX32   = "osx_x86/"                       # Subdirectory within build for OS X x86 projects
BUILD_SUBDIR_OSX64   = "osx_x64/"                       # Subdirectory within build for OS X x64 projects

# "cmake -DPARAM_COMPILER=... -DPARAM_ARCH=... ...additionalarguments... -G generator outputpath"
CMAKE_COMMANDS32  = ["cmake", "-DPARAM_COMPILER=", "-DPARAM_ARCH=x86", "", "-G", "", "../../"]
CMAKE_COMMANDS64  = ["cmake", "-DPARAM_COMPILER=", "-DPARAM_ARCH=x64", "", "-G", "", "../../"]

# ---------------------------------------------------------------------- #
# - Context manager for changing the current working directory         - #
# ---------------------------------------------------------------------- #

class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)
        logger.info("cd '" + self.newPath + "'")

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
        logger.info("cd '" + self.savedPath + "'")
    
# ---------------------------------------------------------------------- #
# - Clean Command                                                      - #
# ---------------------------------------------------------------------- #

def Clean():
    if os.path.exists(API_DIR + BUILD_DIR):
        logger.info("Cleaning '" + API_DIR + BUILD_DIR + "' ...")
        shutil.rmtree(API_DIR + BUILD_DIR)

    logger.info("... Cleaning complete.")

# ---------------------------------------------------------------------- #
# - OS CMake Commands                                                  - #
# ---------------------------------------------------------------------- #

def GetWindowsCommand():
    logger.info("Detected Windows operating system.")
    CMAKE_COMMANDS32[1] += COMPILER_WIN
    CMAKE_COMMANDS64[1] += COMPILER_WIN
    CMAKE_COMMANDS32[5]  = GENERATOR_WIN32
    CMAKE_COMMANDS64[5]  = GENERATOR_WIN64

def GetLinuxCommand():
    logger.info("Detected Linux operating system.")
    CMAKE_COMMANDS32[1] += COMPILER_LINUX
    CMAKE_COMMANDS64[1] += COMPILER_LINUX
    CMAKE_COMMANDS32[3]  = "-DCMAKE_CXX_COMPILER=/usr/bin/g++"
    CMAKE_COMMANDS64[3]  = "-DCMAKE_CXX_COMPILER=/usr/bin/g++"
    CMAKE_COMMANDS32[5]  = GENERATOR_LINUX
    CMAKE_COMMANDS64[5]  = GENERATOR_LINUX

def GetOSXCommand():
    logger.info("Detected OS X operating system.")

# ---------------------------------------------------------------------- #
# - API Project Setup                                                  - #
# ---------------------------------------------------------------------- #

def SetupAPI(cmakeCommand, useShell, buildDir, command):
    logger.info("Configuring API projects ...")
    logger.info("Verifying API directory '" + API_DIR + "'")

    if not os.path.exists(API_DIR):
        logger.error("API directory not found. Exiting API setup.")
        return

    buildPath = API_DIR + buildDir 

    logger.info("Verifying Build directory '" + buildPath + "'")

    if not os.path.exists(buildPath):
            logger.info("Build directory not found. Creating directory ...")
            try:
                os.makedirs(buildPath)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    logger.error("Failed to create build directory.")
                    return

    with cd(buildPath):
        logger.info(" ".join(command))
        retVal = subprocess.check_call(command, stderr=subprocess.STDOUT, shell=useShell)

        if retVal == 0:
            logger.info("... returned " + str(retVal))
        else:
            logger.error("... returned " + str(retVal))

# ---------------------------------------------------------------------- #
# - Arguments                                                            #
# ---------------------------------------------------------------------- #

parser = argparse.ArgumentParser("ConfigureProjects")
parser.add_argument("--clean", nargs="?", const=True, default=False, help="cleans all generated directories and files")
parser.add_argument("--rebuild", nargs="?", const=True, default=False, help="cleans all generated directories and files prior to running cmake")
args = parser.parse_args()

# ---------------------------------------------------------------------- #
# - Logger Setup                                                       - #
# ---------------------------------------------------------------------- #

logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename="ConfigureProjects.log",
                    filemode="w",
                    level=logging.INFO)

logger             = logging.getLogger("ConfigureProjects")
formatter          = logging.Formatter()
file_log_handler   = logging.FileHandler("ConfigureProjects.log")
stderr_log_handler = logging.StreamHandler()

logger.addHandler(file_log_handler)
logger.addHandler(stderr_log_handler)
file_log_handler.setFormatter(formatter)
stderr_log_handler.setFormatter(formatter)

# ---------------------------------------------------------------------- #
# - Check for clean                                                    - #
# ---------------------------------------------------------------------- #

if args.clean is True:
    Clean()
    exit(0)

if args.rebuild is True:
    Clean()

# ---------------------------------------------------------------------- #
# - Operating system entry                                             - #
# ---------------------------------------------------------------------- #

logger.info("Beginning project configuration ...")

cmakeCommand = [""]
useShell     = False
buildDir32   = BUILD_DIR 
buildDir64   = BUILD_DIR 

if platform == "linux" or platform == "linux2":
    GetLinuxCommand()
    buildDir32 += BUILD_SUBDIR_LINUX32
    buildDir64 += BUILD_SUBDIR_LINUX64
elif platform == "darwin":
    GetOSXCommand()
    buildDir32 += BUILD_SUBDIR_OSX32
    buildDir64 += BUILD_SUBDIR_OSX64
elif platform == "win32" or platform == "win64":
    GetWindowsCommand()
    useShell     = True
    buildDir32 += BUILD_SUBDIR_WIN32
    buildDir64 += BUILD_SUBDIR_WIN64
else:
    logger.error("Unsupported operating system. Cancelling build configuration.")
    exit(1)

# ---------------------------------------------------------------------- #
# - Configure projects                                                 - #
# ---------------------------------------------------------------------- #

SetupAPI(cmakeCommand, useShell, buildDir32, CMAKE_COMMANDS32)
SetupAPI(cmakeCommand, useShell, buildDir64, CMAKE_COMMANDS64)

