import os
import sys

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(DIR, "external", "pybind11"))

from glob import glob

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

del sys.path[-1]

ext_modules = [
    Pybind11Extension(
        "_shapelysmooth",
        include_dirs=["./src"],
        sources=sorted(glob("src/*.c*")),
        define_macros=[("_shapelysmooth", "_shapelysmooth")],
        extra_compile_args=["-O3", "-Wall"],
    ),
]

setup(
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
)
