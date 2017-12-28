# Builds all projects/solutions.abs

import os
import logging
import subprocess
import argparse
import sys

from sys import platform

BUILDALL_DIR = "build/"

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
# - Build All Linux                                                    - #
# ---------------------------------------------------------------------- #

def BuildAllLinux():
    logger.info("Building all Linux projects ...")

# ---------------------------------------------------------------------- #
# - Build All Windows                                                  - #
# ---------------------------------------------------------------------- #

def BuildAllWindows():
    logger.info("Building all Window projects ...")
    logger.info("Looking for build all directory '" + BUILDALL_DIR + "' ...")

    if not os.path.exists(BUILDALL_DIR):
        logger.error("Failed to find build all directory. Make sure ConfigureProjects.py was run.")
        return False
    
    logger.info("... Found build all directory.")
    buildResult = True

    with cd(BUILDALL_DIR):
        slnFiles = [os.path.join(root, name)                      # https://stackoverflow.com/a/5817256/735425
                    for root, dirs, files in os.walk(".")
                    for name in files 
                    if name.endswith(".sln")]

        commandList = ["msbuild", "", "/t:build", "/p:Configuration=Release"]

        if args.clean is True:
            commandList[2] = "/t:clean"
        elif args.rebuild is True:
            commandList[2] = "/t:rebuild"

        if args.debug is True:
            commandList[3] = "/p:Configuration=Debug"

        for slnFile in slnFiles:
            logger.info("Found sln file '" + slnFile + "' ...")

            commandList[1] = os.path.abspath(slnFile)
            logger.info(" ".join(commandList))

            retVal = subprocess.run(commandList, shell=True)

            if retVal.returncode == 0:
                logger.info("... '" + slnFile + "' build returned " + str(retVal))
            else:
                logger.error("... '" + slnFile + "' build returned " + str(retVal))
                buildResult = False

    return buildResult

# ---------------------------------------------------------------------- #
# - Arguments                                                            #
# ---------------------------------------------------------------------- #

parser = argparse.ArgumentParser("ConfigureProjects")
parser.add_argument("--clean", nargs="?", const=True, default=False, help="cleans all generated directories and files")
parser.add_argument("--rebuild", nargs="?", const=True, default=False, help="cleans all generated directories and files prior to running cmake")
parser.add_argument("--debug", nargs="?", const=True, default=False, help="builds debug configuration of all projects")
args = parser.parse_args()

# ---------------------------------------------------------------------- #
# - Logger Setup                                                       - #
# ---------------------------------------------------------------------- #

logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename="BuildAll.log",
                    filemode="w",
                    level=logging.INFO)

logger             = logging.getLogger("BuildAll")
formatter          = logging.Formatter()
file_log_handler   = logging.FileHandler("BuildAll.log")
stdout_log_handler = logging.StreamHandler(sys.stdout)

logger.addHandler(file_log_handler)
logger.addHandler(stdout_log_handler)
file_log_handler.setFormatter(formatter)
stdout_log_handler.setFormatter(formatter)

# ---------------------------------------------------------------------- #
# - Operating system entry                                             - #
# ---------------------------------------------------------------------- #

logger.info("Beginning project build ...")

if platform == "linux" or platform == "linux2":
    BuildAllLinux()
elif platform == "win32" or platform == "win64":
    BuildAllWindows()
else:
    logger.error("Unsupported operating system. Cancelling build.")
    exit(1)

