from glob import glob

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

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
