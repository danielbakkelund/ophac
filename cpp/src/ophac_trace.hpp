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

#ifndef OPHAC_TRACE_HPP
#define OPHAC_TRACE_HPP

#ifdef DEBUG

#include <iostream>
#include <sstream>

#define OPHAC_DTRACE(x) {std::cout<<x<<std::endl;}

#define OPHAC_ASSERT(x) {if(!(x)){std::ostringstream msg; msg<<"OPHAC ASSERT file:"<<__FILE__<<" line:"<<__LINE__<<" -- "<<(#x); throw std::logic_error(msg.str());}}

#else // not DEBUG

#define OPHAC_DTRACE(x)
#define OPHAC_ASSERT(x)

#endif // DEBUG

#endif // OPHAC_TRACE_HPP
