
#include "ophac.hpp"
#include "ophac_facade.hpp"

ophac::Merges
linkage_approx(const ophac::Dists& D0,
	       const ophac::Quivers& Q0,
	       const std::string& lnk) {
  ophac::Merges result = ophac::linkage_approx(D0,Q0,ophac::linkageFromString(lnk));
  ensure_monotone(result);
  return result;
}

ophac::Merges
linkage_untied(const ophac::Dists& D0,
	       const ophac::Quivers& Q0,
	       const std::string &lnk) {
  ophac::Merges result = ophac::linkage_untied(D0,Q0,ophac::linkageFromString(lnk));
  ensure_monotone(result);
  return result;
}

void
ensure_monotone(ophac::Merges& merges) {
  for(uint i=1; i<merges.size(); ++i) {
    if(merges[i].first < merges[i-1].first) {
      OPHAC_ASSERT(merges[i-1].first - merges[i].first < 1.0e-12);
      merges[i].first = merges[i-1].first;
    }
  }
}
