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
#include "ophac.hpp"

using namespace ophac;

namespace TestLinkages {
  
  /**
   * Figure 3.5 in Jain and Dubes (1988)
   **/
  CPUNIT_TEST(TestLinkages,test_fig_3_5) {

    const uint  N     = 5;
    const Dists D     = {5.8, 4.2, 6.9, 2.6,
			 6.7, 1.7, 7.2,
			 1.9, 5.6,
			 7.6};
    const Linkage L   = single;
    const Quivers Q   = Quivers(N);
    const Merges  lnk = linkage_untied(D,Q,L);

    const Relation expJoins = {{1,3},{1,2},{0,2},{0,1}};
    const Dists    expDists = {1.7, 1.9, 2.6, 4.2};
    const Merges expMerges  = {{1.7,{1,3}},{1.9,{1,2}},{2.6,{0,2}},{4.2,{0,1}}};

    cpunit::assert_equals(expMerges, lnk);
  }

  CPUNIT_TEST(TestLinkages,test_merge_SL) {
    const Dists D0 = {1.1, 2.1,
		      3.1};

    const Dists D1       = mergeDists(D0,newSizes(3),0,2,single);
    const Dists expected = {1.1};
    cpunit::assert_equals(expected,D1);
  }

  CPUNIT_TEST(TestLinkages,test_merge_CL) {
    const Dists D0 = {1.1, 2.1,
		      3.1};

    const Dists D1       = mergeDists(D0,newSizes(3),0,2,complete);
    const Dists expected = {3.1};
    cpunit::assert_equals(expected,D1);
  }
  
  CPUNIT_TEST(TestLinkages,test_merge_AL) {
    const Dists D0 = {1.1, 2.1,
		      3.1};
    const Sizes S0 = {1,2,3};
    
    const Dists D1       = mergeDists(D0,S0,0,2,average);
    const Dists expected = {10.4/4.0};
    cpunit::assert_equals(expected,D1);
  }
}
