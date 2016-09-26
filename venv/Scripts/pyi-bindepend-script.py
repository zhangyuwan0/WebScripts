#!e:\web scrapings\venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'PyInstaller==3.2','console_scripts','pyi-bindepend'
__requires__ = 'PyInstaller==3.2'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('PyInstaller==3.2', 'console_scripts', 'pyi-bindepend')()
    )
