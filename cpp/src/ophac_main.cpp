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

#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp>
#include <cstdlib>
#include <ctime>
#include "ophac.hpp"
#include "ophac_json.hpp"

void seed(const unsigned int s) {
  std::srand(s);
}

int main(const int nargs, const char** args) {
  if(nargs < 3) {
    std::cout<<"Usage: ophac_main <input>.json <output>.json"<<std::endl;
    return 666;
  }
  
  const std::string infname  = args[1];
  const std::string outfname = args[2];

  std::ifstream inf(infname);
  nlohmann::json input;
  inf >> input;
  inf.close();

  if(input.contains("seed")) {
    const unsigned int s = input["seed"].get<unsigned int>();
    seed(s);
  } else {
    seed(std::time(nullptr));
  }

  const nlohmann::json result = ophac::json::linkage(input);
  std::ofstream out(outfname);
  out<<result;
  out.flush();
  out.close();
  
  return 0;
}
