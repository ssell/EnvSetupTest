# Creates all project and solution files using CMake.
# The generator used is determined by the active operating system.

import os
import logging
import subprocess
import argparse
import shutil 

from sys import platform

COMPILER_WIN       = "msvc140"                        # Compiler identifier added to library output (example: API_msvc140.dll)
COMPILER_LINUX     = ""                               # Compiler identifier added to library output
COMPILER_OSX       = ""                               # Compiler identifier added to library output
GENERATOR_WIN32    = "Visual Studio 15 2017"          # CMake generator to use for Windows x86
GENERATOR_WIN64    = "Visual Studio 15 2017 Win64"    # CMake generator to use for Windows x64
GENERATOR_LINUX32  = ""                               # CMake generator to use for Linux
GENERATOR_LINUX64  = ""                               # CMake generator to use for Linux
GENERATOR_OSX32    = ""                               # CMake generator to use for OS X
GENERATOR_OSX64    = ""                               # CMake generator to use for OS X 
API_DIR            = "API/"                           # Main directory for the API project  
BUILD_DIR          = "build/"                         # Build subdirectory within project directories
BUILD_SUBDIR_WIN32 = "VS2017_x86/"                    # Subdirectory within build for Windows x86 projects
BUILD_SUBDIR_WIN64 = "VS2017_x64/"                    # Subdirectory within build for Windows x64 projects
BUILD_SUBDIR_LINUX = ""                               # Subdirectory within build for Linux projects
BUILD_SUBDIR_OSX   = ""                               # Subdirectory within build for OS X projects

# "cmake -DPARAM_COMPILER=... -DPARAM_ARCH=... -G generator outputpath"
CMAKE_COMMANDS32  = ["cmake", "-DPARAM_COMPILER=", "-DPARAM_ARCH=x86", "-G", "", "../../"]
CMAKE_COMMANDS64  = ["cmake", "-DPARAM_COMPILER=", "-DPARAM_ARCH=x64", "-G", "", "../../"]

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
# - OS CMake Commands                                                  - #
# ---------------------------------------------------------------------- #

def GetWindowsCommand():
    logger.info("Detected Windows operating system.")
    CMAKE_COMMANDS32[1] += COMPILER_WIN
    CMAKE_COMMANDS64[1] += COMPILER_WIN
    CMAKE_COMMANDS32[4]  = GENERATOR_WIN32
    CMAKE_COMMANDS64[4]  = GENERATOR_WIN64

def GetLinuxCommand():
    logger.info("Detected Linux operating system.")

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
        logger.info("\tcmake " + command[1] + " " + command[2] + " " + command[3] + " \"" + command[4] + "\" " + command[5] + "")
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
# ---------------------------------------------------------------------- #\

if args.clean is True:

    if os.path.exists(API_DIR + BUILD_DIR):
        logger.info("Cleaning '" + API_DIR + BUILD_DIR + "' ...")
        shutil.rmtree(API_DIR + BUILD_DIR)

    logger.info("... Cleaning complete.")
    exit(0)

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
    buildDir32  += BUILD_SUBDIR_LINUX32
elif platform == "darwin":
    GetOSXCommand()
    buildDir32  += BUILD_SUBDIR_OSX32
elif platform == "win32" or platform == "win64":
    GetWindowsCommand()
    useShell     = True
    buildDir32  += BUILD_SUBDIR_WIN32
    buildDir64  += BUILD_SUBDIR_WIN64
else:
    logger.error("Unsupported operating system. Cancelling build configuration.")
    exit(1)

# ---------------------------------------------------------------------- #
# - Configure projects                                                 - #
# ---------------------------------------------------------------------- #

SetupAPI(cmakeCommand, useShell, buildDir32, CMAKE_COMMANDS32)
SetupAPI(cmakeCommand, useShell, buildDir64, CMAKE_COMMANDS64)

