# Creates all project and solution files using CMake.
# The generator used is determined by the active operating system.

import os
import logging
import subprocess

from sys import platform

GENERATOR_WINDOWS    = "Visual Studio 15 2017"          # CMake generator to use for Windows
GENERATOR_LINUX      = ""                               # CMake generator to use for Linux
GENERATOR_OSX        = ""                               # CMake generator to use for OS X
API_DIR              = "API/"                           # Main directory for the API project  
BUILD_DIR            = "build/"                         # Build subdirectory within project directories
BUILD_SUBDIR_WINDOWS = "VS2017/"                        # Subdirectory within build for Windows projects
BUILD_SUBDIR_LINUX   = ""                               # Subdirectory within build for Linux projects
BUILD_SUBDIR_OSX     = ""                               # Subdirectory within build for OS X projects

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
    win32CMakeCommand = ["cmake", "-G", GENERATOR_WINDOWS, "../../"]
    return win32CMakeCommand

def GetLinuxCommand():
    logger.info("Detected Linux operating system.")

def GetOSXCommand():
    logger.info("Detected OS X operating system.")

# ---------------------------------------------------------------------- #
# - API Project Setup                                                  - #
# ---------------------------------------------------------------------- #

def SetupAPI(cmakeCommand, useShell, buildDir):
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

        # Build x86 projects/solutions
        logger.info("\tcmake -G \"" + cmakeCommand[2] + "\" " + cmakeCommand[3] + "")
        retVal = subprocess.check_call(cmakeCommand, stderr=subprocess.STDOUT, shell=useShell)

        if retVal == 0:
            logger.info("... returned " + str(retVal))
        else:
            logger.error("... returned " + str(retVal))

        # Build x64 projects/solutions
        cmakeCommand[2] += " Win64"

        logger.info("\tcmake -G \"" + cmakeCommand[2] + "\" " + cmakeCommand[3] + "")
        retVal = subprocess.check_call(cmakeCommand, stderr=subprocess.STDOUT, shell=useShell)

        if retVal == 0:
            logger.info("... returned " + str(retVal))
        else:
            logger.error("... returned " + str(retVal))

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
# - Operating system entry                                             - #
# ---------------------------------------------------------------------- #

logger.info("Beginning project configuration ...")

cmakeCommand = [""]
useShell     = False
buildDir     = BUILD_DIR 

if platform == "linux" or platform == "linux2":
    cmakeCommand = GetLinuxCommand()
    buildDir    += BUILD_SUBDIR_LINUX
elif platform == "darwin":
    cmakeCommand = GetOSXCommand()
    buildDir    += BUILD_SUBDIR_OSX
elif platform == "win32" or platform == "win64":
    cmakeCommand = GetWindowsCommand()
    useShell     = True
    buildDir    += BUILD_SUBDIR_WINDOWS
else:
    logger.error("Unsupported operating system. Cancelling build configuration.")
    exit(1)

# ---------------------------------------------------------------------- #
# - Configure projects                                                 - #
# ---------------------------------------------------------------------- #

SetupAPI(cmakeCommand, useShell, buildDir)

