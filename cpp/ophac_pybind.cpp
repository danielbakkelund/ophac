//////////////////////////////////////////////////////////////////////////////// 
// Copyright 2020 Daniel Bakkelund
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.
//////////////////////////////////////////////////////////////////////////////// 

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <mutex>
#include <cstdlib>
#include "ophac.hpp"
#include "ophac_facade.hpp"

namespace py = pybind11;

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
