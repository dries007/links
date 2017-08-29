import sys
import os

path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)

# That was all required to make this line work.
# Since we are inside the actual links folder, we can't refer to it by links, unless we add it to the path.
# ...Something about python being elegant until its not...

from links import manager

# This is run when the module is ran with "python -m links"

manager.run()
