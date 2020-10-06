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

#include "ophac_trace.hpp"
#include "ophac.hpp"
#include <set>
#include <cmath>
#include <stdexcept>

ophac::Merges
ophac::linkage_untied(const Dists& D0,const Quivers& Q0,const Linkage L) {
  Merges result;
  Dists   D = D0;
  Quivers Q = Q0;
  Sizes   S = newSizes(Q.size());
  Merge merge = findMerge(D,Q);
  while(merge != no_merge) {
    result.push_back(merge);
    const uint a = merge.second.first;
    const uint b = merge.second.second;
    D = mergeDists(D,S,a,b,L);
    S = mergeSizes(S,a,b);
    Q = mergeQuivers(Q,a,b);
    merge = findMerge(D,Q);
  }
  return result;
}

std::ostream&
ophac::operator << (std::ostream& out,const Linkage l) {
  switch(l) {
  case single:
    return out<<"single linkage";
  case average:
    return out<<"average linkage";
  case complete:
    return out<<"complete linkage";
  default:
    throw std::invalid_argument("Unknown linkage.");
  }
}

ophac::Sizes ophac::newSizes(const uint n) {
  return Sizes(n,1);
}

ophac::Sizes
ophac::mergeSizes(const Sizes& s0,const uint a,const uint b) {
  Sizes result(s0.size()-1);
  for(uint i=0; i<b; ++i) {
    result[i] = s0[i];
  }
  result[a] += s0[b];
  for(uint i=b+1; i<s0.size(); ++i) {
    result[i-1] = s0[i];
  }
  return result;
}

ophac::Quivers
ophac::fromRelation(const Relation &rel, const uint n) {
  Quivers result(n);
  for(const Pair &p : rel) {
    result[p.first].push_back(p.second);
  }
  return result;
}

namespace {
  bool
  ophac_hasPath(const ophac::Quivers& Q, const ophac::uint a, const ophac::uint b,
		std::set<ophac::uint> &visited) {
    if(visited.find(a) != visited.end()) {
      return false;
    }
    visited.insert(a);
    
    for(const ophac::uint c : Q[a]) {
      if(b == c) {
	return true;
      }
      if(ophac_hasPath(Q,c,b,visited)) {
	return true;
      }
    }
    //visited.erase(a);
    return false;
  }
}

bool
ophac::hasPath(const Quivers& rel, const uint a, const uint b) {
  std::set<uint> visited;
  return ::ophac_hasPath(rel,a,b,visited);
}

bool
ophac::canMerge(const Quivers& rel, const uint a, const uint b) {
  return !hasPath(rel,a,b) && !hasPath(rel,b,a);
}

namespace {
  
  void
  ophac_transferQuiver(const ophac::Quiver &q, const uint a, const uint b,
		       ophac::Quiver &out) {
    ophac::Quiver tmp;
    for(const uint j : q) {
      if(j < b) {
	tmp.push_back(j);
      } else if(j > b) {
	tmp.push_back(j-1);
      } else /* j == b */ {
	tmp.push_back(a);
      }
    }
    // Unique and sorted...
    const std::set<uint> x(tmp.begin(),tmp.end());
    out = ophac::Quiver(x.begin(),x.end());
  } 
}

ophac::Quivers
ophac::mergeQuivers(const Quivers& Q, const uint a, const uint b) {
  Quivers result(Q.size()-1);
  for(uint i=0; i<a; ++i) {
    ::ophac_transferQuiver(Q[i],a,b,result[i]);
  }
  
  Quiver A(Q[a].begin(),Q[a].end());
  A.insert(A.end(),Q[b].begin(),Q[b].end());
  ::ophac_transferQuiver(A,a,b,result[a]);
  
  for(uint i=a+1; i<b; ++i) {
    ::ophac_transferQuiver(Q[i],a,b,result[i]);
  }
  
  for(uint i=b+1; i<Q.size(); ++i) {
    ::ophac_transferQuiver(Q[i],a,b,result[i-1]);
  }
  return result;
}

namespace {
  struct dpair_cmp {
    typedef std::pair<uint,ophac::ftype> T;
    bool operator () (const T &a, const T &b) const {
      return a.second < b.second;
    }
  };
}

ophac::Merge
ophac::findMerge(const Dists &D,const Quivers &Q) {
  typedef std::pair<uint,ftype>       DPair;
  typedef std::set<DPair,::dpair_cmp> DPairVec;
  DPairVec dpairs;
  for(uint i=0; i<D.size(); ++i) {
    dpairs.insert({i,D[i]});
  }
  for(const DPair &p: dpairs) {
    const Pair xy = toMatrixIdx(p.first, Q.size());
    if(canMerge(Q,xy.first,xy.second)) {
      OPHAC_DTRACE("findMerge -- can merge "<<xy<<" with distance "<<p.second<<'.');
      return {p.second,xy};
    }
  }
  return {-1,no_pair};
}

ophac::Pair
ophac::toMatrixIdx(const uint k, const uint n) {
  const uint i = n - 2 - static_cast<int>((std::sqrt(-8.0*k + 4*n*(n-1)-7)/2.0 - 0.5));
  const uint j = k + i + 1 - (n*(n-1))/2 + ((n-i)*(n-i-1))/2;
  return {i,j};
}

ophac::uint
ophac::toLinearIdx(const Pair &p, const uint n) {
  const uint i = p.first;
  const uint j = p.second;
	       
  const uint N = n*(n-1)/2;          // Half matrix size
  const uint r = ((n-i)*(n-i-1))/2;  // Half matrix size including and below point
  const uint h = j-i-1;              // Number of cells to the right of the diagonal
  return N - r + h;
}

////////////////////////////////////////////////////////////////////////////////
//                               MERGE CODE
////////////////////////////////////////////////////////////////////////////////

ophac::Dists
ophac::mergeDists(const Dists& D,const Sizes& s,
		  const uint a, const uint b,
		  const Linkage L) {
  const uint n = s.size();
  switch(L) {
  case single:
    {
      const SL sl(n);
      const BaseLinkage linker(sl);
      return linker(D,a,b,n);
    }
  case average:
    {
      const AL al(s);
      const BaseLinkage linker(al);
      return linker(D,a,b,n);
    }
  case complete:
    {
      const CL cl(n);
      const BaseLinkage linker(cl);
      return linker(D,a,b,n);
    }
  default:
    throw std::invalid_argument("Unknown linkage.");
  }
}


ophac::SL::SL(const uint u) :
  n(u)
{}

ophac::SL::SL(const SL& sl) :
  n(sl.n)
{}

ophac::SL::~SL()
{}

ophac::ftype
ophac::SL::operator () (const Dists& d,const uint a,const uint b,const uint x) const {
  const uint i1 = toLinearIdx({std::min(a,x),std::max(a,x)},n);
  const uint i2 = toLinearIdx({std::min(b,x),std::max(b,x)},n);
  return std::min(d[i1],d[i2]);
}

ophac::CL::CL(const uint u) :
  n(u)
{}

ophac::CL::CL(const CL& cl) :
  n(cl.n)
{}

ophac::CL::~CL()
{}

ophac::ftype
ophac::CL::operator () (const Dists& d, const uint a, const uint b, const uint x) const{
  const uint i1 = toLinearIdx({std::min(a,x),std::max(a,x)},n);
  const uint i2 = toLinearIdx({std::min(b,x),std::max(b,x)},n);
  return std::max(d[i1],d[i2]);
}

ophac::AL::AL(const Sizes& _s)  :
  s0(_s)
{}

ophac::AL::AL(const AL& al) :
  s0(al.s0)
{}

ophac::AL::~AL()
{}

#include <iostream>

ophac::ftype
ophac::AL::operator () (const Dists& d, const uint a, const uint b, const uint x)const {
  const ftype s1 = static_cast<ftype>(s0[a]);
  const ftype s2 = static_cast<ftype>(s0[b]);
  const uint i1 = toLinearIdx({std::min(a,x),std::max(a,x)},s0.size());
  const uint i2 = toLinearIdx({std::min(b,x),std::max(b,x)},s0.size());
  const ftype d1 = d[i1];
  const ftype d2 = d[i2];
  OPHAC_DTRACE("AL-link; d1:"<<d1<<" d2:"<<d2<<" s1:"<<s1<<" s2:"<<s2);
  return ((s1*d1)+(s2*d2))/(s1+s2);
}
  
