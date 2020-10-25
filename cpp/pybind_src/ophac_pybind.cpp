
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <ophac.hpp>

namespace py = pybind11;

/*
  Support conversion string -> Linkage (enum)
*/

ophac::Merges
linkage_approx(const ophac::Dists& D0,
	       const ophac::Quivers& Q0,
	       const std::string& lnk) {
  return ophac::linkage_approx(D0,Q0,ophac::linkageFromString(lnk));
}


ophac::Merges
linkage_untied(const ophac::Dists& D0,
	       const ophac::Quivers& Q0,
	       const std::string &lnk) {
  return ophac::linkage_untied(D0,Q0,ophac::linkageFromString(lnk));
}

PYBIND11_MODULE(ophac_cpp, m) {
  m.doc() = "C++ implementation of some OPHAC routines.";
  
  m.def("linkage_untied",
	&linkage_untied,
	"Only to be used for an un-tied dissimilarity measure.",
	py::arg("dists"),
	py::arg("quivers"),
	py::arg("lnk"));
  
  m.def("linkage_approx",
	&linkage_approx,
	"Produces an 1-fold approximation through resolving ties by random.",
	py::arg("dists"),
	py::arg("quivers"),
	py::arg("lnk"));
}
