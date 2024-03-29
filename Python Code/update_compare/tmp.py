import os

# Change current working directory to where the script is located
os.chdir(os.path.dirname(os.path.realpath(__file__)))

from glob import glob
paths = glob('*/')
print(paths)