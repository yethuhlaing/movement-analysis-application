# setup.py
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine-tuning.
build_exe_options = {"packages": ["os"], 
                     "excludes": [],
                    }

# Base must be "Win32GUI" for GUI applications on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"
# Define the executables
executables = [
    Executable(
        "app.py",
        icon="./assets/lab-logo.ico",  # Path to your icon file
        base=base
    ),

]
setup(
    name = "Movement Analysis",
    version = "1.0",
    description = "My application!",
    options = {"build_exe": build_exe_options},
    executables = executables
)