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

#include <cpunit>
#include "ophac_json.hpp"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

namespace TestJson {
  
  /**
   * Figure 3.5 in Jain and Dubes (1988)
   **/
  CPUNIT_TEST(TestJson,test_fig_3_5) {

    json input;
    input["D"] = {5.8, 4.2, 6.9, 2.6,
		  6.7, 1.7, 7.2,
		  1.9, 5.6,
		  7.6};
    input["Q"] = ophac::Quivers(5);
    input["L"] = "single";
    input["mode"] = "untied";
    
    json expected;
    expected["dists"] = {1.7, 1.9, 2.6, 4.2};
    expected["joins"] = {{1,3},{1,2},{0,2},{0,1}};

    const json result = ophac::json::linkage(input);

    cpunit::assert_equals(expected,result);
  }
}
