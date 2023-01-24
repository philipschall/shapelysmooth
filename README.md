[![PyPI version shields.io](https://img.shields.io/pypi/v/shapelysmooth.svg)](https://pypi.python.org/pypi/shapelysmooth/)

<p align="center">
  <img src="https://github.com/philipschall/shapelysmooth/blob/main/images/main.png?raw=true" width="519" height="294" />
</p>

`shapelysmooth` is a polyline smoothing package for Python - mainly intended for use on shapely LineStrings and Polygons.
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Methods](#methods)
    + [Taubin Smoothing - `taubin_smooth`](#taubin)
    + [Chaikin Interpolation - `chaikin_smooth`](#chaikin)
    + [Catmull-Rom Spline Interpolation - `catmull_rom_smooth`](#catmullrom)
  * [Smoothing Collections of Geometries](#smoothing-collections-of-geometries)
  * [Smoothing Geometries stored in Numpy Arrays](#smoothing-geometries-stored-in-numpy-arrays)

## Requirements

This package requires
- Python >=3.6
- shapely

## Installation
Build from source, or

    pip install shapelysmooth

## Methods
Currently, three smoothing methods are provided, suited to different use cases.

<a id="taubin"></a>
### Taubin Smoothing - `taubin_smooth`
---
    >>> from shapelysmooth import taubin_smooth
    >>> smoothed_geometry = taubin_smooth(geometry, factor, mu, steps)
Taubin polyline smoothing.

**Parameters**

<code><b>geometry</b> : LineString | Polygon | list</code>
>Geometric object consisting of polylines to smooth. A `shapely.geometry.Linestring` or `shapely.geometry.Polygon` or a `list` containing tuples of $(x, y)$ coordinates.

<code><b>factor</b> : float</code>
>How far each node is moved toward the average position of its neighbours during every second iteration. $0 <$ `factor` $< 1$. Default value: $\mathbf{0.5}$.

<code><b>mu</b> : float</code>
>How far each node is moved opposite the direction of the average position of its neighbours during every second iteration. $0 <$ `-mu` $< 1$. Default value: $\mathbf{-0.5}$.

<code><b>steps</b> : int</code>
>Number of smoothing steps. Default value: $\mathbf{5}$.

**Returns**

<code><b>output</b> : LineString | Polygon | List</code>
> The smoothed geometry.
---
The Laplacian smoothing algorithm defines for each interior node in a polyline consisting of nodes $(p_0, p_1,..., p_n)$ the Laplacian, $L$, of node $p_i$ as
$$L(p_i)=\frac{1}{2}p_{i+1}+\frac{1}{2}p_{i-1}-p_i.$$
For a given factor $\lambda$, node $p_i$ is at each iteration redefined as:
$$p_i\leftarrow p_i+\lambda L(p_i).$$
Geometrically this corresponds to moving $p_i$ a fraction $\lambda$ of the distance toward the average of its neighbouring nodes, in the direction of that average. However, this will cause cause shrinkage, i.e. closed polylines will eventually collapse to a point. Taubin smoothing prevents this by, at every second iteration, instead redefining each node $p_i$ as
$$p_i\leftarrow p_i+\mu L(p_i),$$
where $0<-\mu<1$. This corresponds to moving $p_i$ a fraction $-\mu$ of the distance toward the average of it's neighbouring nodes, but in the opposite direction to that of the average. One step of Taubin smoothing therefore consists of two iterations of Laplacian smoothing, with different factors - one positive one negative.

See
>[Gabriel Taubin. 1995. Curve and Surface Smoothing Without Shrinkage. IEEE International Conference on Computer Vision. 852-857.  ](https://graphics.stanford.edu/courses/cs468-01-fall/Papers/taubin-smoothing.pdf)

The implementation also supports closed polylines and polygons (with or without holes).
<p align="center">
  <img src="https://github.com/philipschall/shapelysmooth/blob/main/images/laplace1.png?raw=true" width="500" height="239" />
</p>

<a id="chaikin"></a>
### Chaikin Interpolation - `chaikin_smooth`
---
    >>> from shapelysmooth import chaikin_smooth
    >>> smoothed_geometry = chaikin_smooth(geometry, iters, keep_ends)
Polyline smoothing based on Chaikin's Corner Cutting algorithm.

**Parameters**

<code><b>geometry</b> : LineString | Polygon | list</code>
>Geometric object consisting of polylines to smooth. A `shapely.geometry.Linestring` or `shapely.geometry.Polygon` or a `list` containing tuples of $(x, y)$ coordinates.

<code><b>iters</b> : int</code>
>Number of iterations. Default value: $\mathbf{5}$.

<code><b>keep_ends</b> : bool</code>
>Preserve the original start and end nodes of the polyline. Not applicable to closed polylines and polygons. (The original algorithm results in a contraction of the start and end nodes). Default value: **`True`**.

**Returns**

<code><b>output</b> : LineString | Polygon | List</code>
> The smoothed geometry.
---
Chaikin's Corner Cutting algorithm smooths a polyline by iterative refinement of the nodes of the polyline. At each iteration, every node is replaced by two new nodes: one a quarter of the way to the next node, and one quarter of the way to the previous node.

Note that the algorithm (roughly) doubles the amount of nodes at each iteration, therefore care should be taken when selecting the number of iterations.

Instead of the original iterative algorithm by Chaikin, this implementation makes use of the equivalent multi-step algorithm introduced by Wu et al. See
>[Ling Wu, Jun-Hai Yong, You-Wei Zhang, and Li Zhang. 2004. Multi-step Subdivision Algorithm for Chaikin Curves. In Proceedings of the First international conference on Computational and Information Science (CIS'04). Springer-Verlag, Berlin, Heidelberg. 1232–1238.](https://sci-hub.st/10.1007/978-3-540-30497-5_188)

By default, the algorithm will not contract the endpoints of an open polyline. Set the `keep_ends` parameter if this behaviour is unwanted.

<p align="center">
  <img src="https://github.com/philipschall/shapelysmooth/blob/main/images/chaikin1.png?raw=true" width="500" height="239" />
</p>

The implementation also supports closed polylines and polygons (with or without holes).

<p align="center">
  <img src="https://github.com/philipschall/shapelysmooth/blob/main/images/chaikin2.png?raw=true" width="240" height="239" />
</p>

<a id="catmullrom"></a>
### Catmull-Rom Spline Interpolation - `catmull_rom_smooth`
---
    >>> from shapelysmooth import catmull_rom_smooth
    >>> smoothed_geometry = catmull_rom_smooth(geometry, alpha, subdivs)
Polyline smoothing using Catmull-Rom splines.

**Parameters**

<code><b>geometry</b> : LineString | Polygon | list</code>
>Geometric object consisting of polylines to smooth. A `shapely.geometry.Linestring` or `shapely.geometry.Polygon` or a `list` containing tuples of $(x, y)$ coordinates.

<code><b>alpha</b> : float</code>
> Tension parameter. $0 \leq$ `alpha` $\leq 1$. For uniform Catmull-Rom splines, `alpha`  $= 0$. For centripetal Catmull-Rom splines, `alpha`  $= 0.5$. For chordal Catmull-Rom splines, `alpha`  $= 1.0$. Default value: $\mathbf{0.5}$.

<code><b>subdivs</b> : int</code>
> Number of subdivisions of each polyline segment. Default value: $\mathbf{10}$.

**Returns**

<code><b>output</b> : LineString | Polygon | List</code>
> The smoothed geometry.
---
Catmull-Rom splines are a class of cubic splines which can be efficiently calculated, and have the property that they pass through each interpolation node. The splines are piecewise-defined, but have $C^1$ continuity throughout.

For more detail see
>[Edwin Catmull, Raphael Rom. 1974. A Class of Local Interpolating Splines. Computer Aided Geometric Design. Academic Press. 317-326.](https://sci-hub.hkvisa.net/10.1016/b978-0-12-079050-0.50020-5)

This implementation makes use of the algorithm proposed by Barry and Goldman, see
>[Philip Barry and Ronald Goldman. 1988. Recursive evaluation algorithm for a class of Catmull-Rom splines. ACM Siggraph Computer Graphics. 22. 199-204.](https://www.researchgate.net/profile/Ronald-Goldman/publication/220720141_Recursive_evaluation_algorithm_for_a_class_of_Catmull-Rom_splines/links/559d5d3d08ae76bed0bb3523/Recursive-evaluation-algorithm-for-a-class-of-Catmull-Rom-splines.pdf)

There are three types of Catmull-Rom splines: uniform, centripetal and chordal, which are determined by tension parameter, $\alpha$, values of $0$, $0.5$ and $1$, respectively. Note that uniform Catmull-Rom splines may contain spurious self-intersections.
<p align="center">
  <img src="https://github.com/philipschall/shapelysmooth/blob/main/images/catmullrom1.png?raw=true" width="500" height="239" />
</p>
The implementation also supports closed polylines and polygons (with or without holes).
<p align="center">
  <img src="https://github.com/philipschall/shapelysmooth/blob/main/images/catmullrom2.png?raw=true" width="240" height="239" />
</p>

## Smoothing Collections of Geometries
Objects of type `shapely.geometry.MultiLineString` and `shapely.geometry.MultiPolygon` can be smoothed by making use of the `geoms` property provided by these classes.

    >>> from shapely.geometry import MultiPolygon
    >>> from shapelysmooth import chaikin_smooth
    >>> polys = MultiPolygon(...)
    >>> smoothed_polys = MultiPolygon([chaikin_smooth(poly) for poly in polys.geoms])

## Smoothing Geometries stored in Numpy Arrays
Given a `numpy.array` of shape $(n, 2)$ (thus containing $n$ 2-dimensional coordinates or nodes), it can be smoothed as follows.
    
    >>> import numpy as np
    >>> from shapelysmooth import chaikin_smooth
    >>> array = np.array(...)
    >>> array_smoothed = np.array(chaikin_smooth(list(map(tuple, array))))

Direct support for Numpy arrays is being worked on for a future version.
