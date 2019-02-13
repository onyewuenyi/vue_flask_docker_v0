"""All controllers for var collections """
import os
import glob

# NOTE
# get path of script run
print(__file__)

# get dir of the script run
os.path.dirname(__file__)

__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]
