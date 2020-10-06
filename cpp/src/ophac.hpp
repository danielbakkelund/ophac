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

#ifndef OPHAC_HPP
#define OPHAC_HPP

#include <vector>
#include <set>
#include <ostream>

namespace ophac {

  typedef double       ftype;
  typedef unsigned int uint;

  enum Linkage {single, average, complete};

  std::ostream& operator << (std::ostream&,const Linkage);
  
  
  typedef std::vector<uint>    Sizes;
  typedef std::vector<ftype>   Dists;
  typedef std::pair<uint,uint> Pair;
  typedef std::vector<Pair>    Relation;
  typedef std::vector<uint>    Quiver;
  typedef std::vector<Quiver>  Quivers;

  typedef std::pair<ftype,Pair> Merge;
  typedef std::vector<Merge>    Merges;

  const Pair  no_pair  {-1,-1};
  const Merge no_merge {-1,no_pair};

  Merges linkage_untied(const Dists&,const Quivers&,const Linkage);
  
  Sizes newSizes(const uint);
  Sizes mergeSizes(const Sizes&,const uint,const uint);
  
  Quivers fromRelation(const Relation&, const uint);
  bool    hasPath     (const Quivers&,  const uint, const uint);
  bool    canMerge    (const Quivers&,  const uint, const uint);
  Quivers mergeQuivers(const Quivers&,  const uint, const uint);

  Dists mergeDists(const Dists&,const Sizes&,const uint,const uint,const Linkage);

  Merge findMerge(const Dists&,const Quivers&);

  Pair toMatrixIdx(const uint,const uint);
  uint toLinearIdx(const Pair&,const uint);
  
  template<class T>
  std::ostream& operator << (std::ostream&,const std::vector<T>&);
  template<class S,class T>
  std::ostream& operator << (std::ostream&,const std::pair<S,T>&);

  /// LINKAGE
  
  template<class Lnk>
  class BaseLinkage {
    const Lnk& lnk;
  public:
    BaseLinkage(const Lnk&);
    BaseLinkage(const BaseLinkage&);
    ~BaseLinkage();
    
    Dists operator () (const Dists&,
		       const uint,const uint,const uint) const;
    
  };
  
  struct SL {
    const uint n;
    SL(const uint);
    SL(const SL&);
    ~SL();
    ftype operator () (const Dists&,const uint,const uint,const uint) const;
  };

  struct CL {
    const uint n;
    CL(const uint);
    CL(const CL&);
    ~CL();
    ftype operator () (const Dists&,const uint,const uint,const uint) const;
  };

  struct AL {
    const Sizes s0;
    AL(const Sizes&);
    AL(const AL&);
    ~AL();
    ftype operator () (const Dists&,const uint,const uint,const uint) const;
  };

  
} // end namespace ophac


template<class Lnk>
ophac::BaseLinkage<Lnk>::BaseLinkage(const Lnk& l):
  lnk(l)
{}

template<class Lnk>
ophac::BaseLinkage<Lnk>::BaseLinkage(const BaseLinkage& l):
  lnk(l.lnk)
{}

template<class Lnk>
ophac::BaseLinkage<Lnk>::~BaseLinkage()
{}
  
template<class Lnk>
ophac::Dists
ophac::BaseLinkage<Lnk>::operator () (const Dists& d0,
				      const uint i, const uint j, const uint n) const {
  const uint N = ((n-1)*(n-2))/2; 
  Dists dists(N);
  uint  lindex = 0;
  for(uint s=0; s<n; ++s) {
    if(s == j) {
      continue;
    }
    for(uint t=s+1; t<n; ++t) {
      if(t == j) {
	continue;
      } else if(s == i) {
	dists[lindex] = lnk(d0,i,j,t);
	++lindex;
      } else if(t == i) {
	dists[lindex] = lnk(d0,i,j,s);
	++lindex;
      } else {
	const uint k  = toLinearIdx(Pair{s,t},n);
	dists[lindex] = d0[k];
	++lindex;
      }
    }
  }
  return dists;
}

template<class T>
std::ostream&
ophac::operator << (std::ostream& out,const std::vector<T>& vec) {
  out<<'[';
  for(uint i=0; i<vec.size(); ++i) {
    out<<vec[i];
    if(i < vec.size()-1) {
      out<<',';
    }
  }
  return out<<']';
}

template<class S,class T>
std::ostream&
ophac::operator << (std::ostream& out,const std::pair<S,T>& q) {
  return out<<'{'<<q.first<<','<<q.second<<'}';
}

#endif // OPHAC_HPP
