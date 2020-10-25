
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <mutex>
#include <cstdlib>
#include <ophac.hpp>

namespace py = pybind11;

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

static int theSeed = -1;
static std::mutex mx;
uint32_t ophac_pybind_seed(const uint32_t s) {
  std::lock_guard<std::mutex> lock(mx);
  if(theSeed == -1) {
    std::srand(s);
    theSeed = s;
  }
  return theSeed;
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

  m.def("seed",
	&ophac_pybind_seed,
	"Seed function.");
}
