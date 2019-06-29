import importlib
import sys



def _import(module):
    sys_modules = dict(sys.modules)
    importlib.invalidate_caches()
    importlib.import_module(module, package=None)
    sys.modules.clear()
    sys.modules.update(sys_modules)


FAILURE = True
if FAILURE:
    _import('extract')

_import('extract.one')
_import('extract.two')

"""
If FAILURE if False, the program completes.
If FAILURE is True, it throws this exception.

Traceback (most recent call last):
  File "main.py", line 16, in <module>
    _import('extract.two')
  File "main.py", line 7, in _import
    importlib.import_module(module)
  File "/code/env/nc/lib/python3.6/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 994, in _gcd_import
  File "<frozen importlib._bootstrap>", line 971, in _find_and_load
  File "<frozen importlib._bootstrap>", line 955, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 665, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 678, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "/code/test/strange_import/extract/two.py", line 1, in <module>
    from . import one
ImportError: cannot import name 'one'
"""
