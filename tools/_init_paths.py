# -- python imports --
import sys
import os.path as osp
from pathlib import Path

this_dir = Path(osp.dirname(osp.realpath(__file__)))
lib_path = this_dir / Path("/lib/")
sys.path.append(lib_path)
