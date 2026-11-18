"""Allow `python -m aibi_toolkit` to behave like the `aibi` console script.

The console script is the documented entry point (`aibi ...`); this module
exists so that people who reach for `python -m` get the same CLI.
"""

import sys

from aibi_toolkit.cli import main

if __name__ == "__main__":
    sys.exit(main())
