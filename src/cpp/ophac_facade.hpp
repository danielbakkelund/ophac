#ifndef OPHAC_FACADE_HPP
#define OPHAC_FACADE_HPP

#include "ophac.hpp"

ophac::Merges linkage_approx(const ophac::Dists&,
			     const ophac::Quivers&,
			     const std::string&);
ophac::Merges linkage_untied(const ophac::Dists&,
			     const ophac::Quivers&,
			     const std::string&);


void ensure_monotone(ophac::Merges&);

#endif // OPHAC_FACADE_HPP
