#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "smoothing.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_shapelysmooth, m) {
	m.def("catmullrom", &CatmullRom);
	m.def("chaikin", &Chaikin);
	m.def("taubin", &Taubin);
}
