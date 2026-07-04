import os

# Compatibility shim: when launched from ./backend, make `backend.*` resolve
# against the parent package directory.
__path__ = [os.path.dirname(os.path.dirname(__file__))]
