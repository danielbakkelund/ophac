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

#include <stdexcept>
#include <sstream>
#include <nlohmann/json.hpp>

#include "ophac_json.hpp"
#include "ophac.hpp"
#include "ophac_trace.hpp"

ophac::Linkage
ophac::json::strToLinkage(const std::string L) {
  if(L == "single") {
    return single;
  }
  if(L == "complete") {
    return complete;
  }
  if(L == "average") {
    return average;
  }
  throw std::invalid_argument(L);
}

nlohmann::json
ophac::json::linkage(const nlohmann::json& input) {
  using json = nlohmann::json;
  OPHAC_DTRACE("ophac::json::linkage(...)");

  
  const Dists   D = input["D"].get<Dists>();
  const Quivers Q = input["Q"].get<Quivers>();
  const Linkage L = strToLinkage(input["L"]);
  OPHAC_DTRACE("ophac::json::linkage - deserialised; n:"<<Q.size()<<" L:"<<L<<".");

  Merges merges;

  if(input["mode"] == "untied") {
    OPHAC_DTRACE("Running untied linkage mode.");
    merges = linkage_untied(D,Q,L);
    OPHAC_DTRACE("ophac::json::linkage - Untied linkage completed; #merges:"<<
		 merges.size());
  } else
    if(input["mode"] == "approx") {
      OPHAC_DTRACE("Running approx linkage mode.");
      merges = linkage_approx(D,Q,L);
      OPHAC_DTRACE("ophac::json::linkage - Approximate linkage completed; #merges:"<<
		   merges.size());
  } else {
    std::ostringstream msg;
    msg<<"Unsupported mode: '"<<input["mode"]<<',';
    throw std::invalid_argument(msg.str());
  }

  Dists    dists;
  Relation pairs;
  for(const Merge &m : merges) {
    dists.push_back(m.first);
    pairs.push_back(m.second);
  }

  json result;
  result["dists"] = json(dists);
  result["joins"] = json(pairs);
  return result;
}
