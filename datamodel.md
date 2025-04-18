### Copyright 2020 Daniel Bakkelund

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.<br>
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.<br>
 You should have received a copy of the GNU Lesser General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.

# The data model used is as follows:

The elements to be clustered are always `N` integers in the
  range `{0,...,N-1}`. The dissimilarity measure is a matrix-like
  object, say `D`, and the dissimilarity between elements `a` and `b`
  is, thus, `D[a,b]`.

The file `ophac.dtypes.py` contains the data types used, and
they are as follows:

### Partition
  A class representing the partition of a set.
  Contains functionality to e.g. merge to blocks into one.

### Quivers
  The class used to represent a strict partial order.
  Let `(X,<)` be the ordered set.
  A `Quivers` object can be instantiated in two ways:
  1. Passing an array of arrays, where the `i`-th array
      contains the value `j` if `i<j`.
  1.  An array representing the actual relation, i.e.
      a set of pairs `(i,j)`, meaning that `i<j`.
      If this method if instantiation is used, the number of
      elements in the set must also be passed as a parameter.


  Notice that, if `i<j` and `j<k`, it is sufficient to supply this
  information; the transitive closure is calculated by the `Quivers`
  object.

  The `Quivers` objects contain methods for checking whether there is
  a path from `a` to `b`, for merging two elements, for checking for cycles,
  and also for checking whether two elements can be merged without
  introducing a cycle.

### DistMatrix
  The data type used to represent dissimilarity measures, metrics and ultrametrics.
  If the data set has `N` points, the `DistMatrix` object is instantiated by passing an
  array of length `N(N-1)/2`, containing the upper half of the distances in row-wise
  order.

  The `DistMatrix` objects are not merged directly, but through the use of _linkage
  objects_.

### AgglomerativeClustering
  This object represents a hierarchical clustering. The data type contains two
  internal pieces of information:
  1. The indices of the merged blocks in the Partition as a sequence of pairs (i,j)
  2. The distances at which the different merges took place


  The AC-objects can be accessed in array fashion, meaning that it is possible
  to extract slices and subsets using the bracket operator. By using the merge(...)
  method in the `ophac.dtypes` module, we can produce a sequence of `Partition` objects,
  one for each step in the clustering process as follows:

  Assume we have clustered a `12`-point space

```python
   from ophac.dtypes import merge, Partition
   ac = ... # AC objcect from clustering the 12-point space
   partitions = []
   for i in range(len(ac)):
      aci = ac[:i+1]
      Pi  = merge(Partition(n=12), aci.joins)
      partitions.append(Pi)
```

  This will produce an array with every partition generated during the
  clustering process, and in the correct order.
