from _shapelysmooth import taubin, chaikin, catmullrom
from shapely.geometry import LineString
from shapely.geometry import Polygon
from typing import List, Tuple, Union

def taubin_smooth(
    geometry: Union[LineString, Polygon, List[Tuple[float, float]]],
    factor: float = 0.5,
    mu: float = -0.5,
    steps: int = 5
):
    """
    Taubin polyline smoothing.

    Parameters:
    ----------
    geometry : shapely.geometry.LineString | shapely.geometry.Polygon | list
        Geometric object consisting of polylines to smooth. A shapely
        Linestring or Polygon, or a list containing tuples of (x, y)
        coordinates.
    factor : float
        How far each node is moved toward the average position of its
        neighbours during every second iteration. 0 < factor < 1.
        Default value: 0.5.
    mu : float
        How far each node is moved opposite the direction of the average
        position of its neighbours during every second iteration. 0 < -mu < 1.
        Default value: -0.5.
    steps : int
        Number of smoothing steps. Default value: 5.
    
    Returns:
    -------
    output : shapely.geometry.LineString | shapely.geometry.Polygon | list
        The smoothed geometry.
    """
    if isinstance(geometry, LineString):
        return LineString(taubin(geometry.coords, factor, mu, steps))
    elif isinstance (geometry, Polygon):
        return Polygon(taubin(geometry.exterior.coords, factor, mu, steps),
                       [taubin(hole.coords, factor, mu, steps) for hole in
                        geometry.interiors])
    elif isinstance (geometry, list):
        return taubin(geometry, factor, mu, steps)

def chaikin_smooth(
    geometry: Union[LineString, Polygon, List[Tuple[float, float]]],
    iters: int = 5,
    keep_ends: bool = True
):
    """
    Polyline smoothing using Chaikin's corner cutting algorithm.

    Parameters:
    ----------
    geometry : shapely.geometry.LineString | shapely.geometry.Polygon | list
        Geometric object consisting of polylines to smooth. A shapely
        Linestring or Polygon, or a list containing tuples of (x, y)
        coordinates.
    iters : int
        Number of iterations. Default value: 3.
    keep_ends : bool
        Preserve the original start and end nodes of the polyline. Not
        applicable to closed polylines. Default value: True.

    Returns:
    -------
    output : shapely.geometry.LineString | shapely.geometry.Polygon | list
        The smoothed geometry.
    """
    if isinstance(geometry, LineString):
        return LineString(chaikin(geometry.coords, iters, keep_ends))
    elif isinstance (geometry, Polygon):
        return Polygon(chaikin(geometry.exterior.coords, iters, keep_ends),
                       [chaikin(hole.coords, iters, keep_ends) for hole in
                        geometry.interiors])
    elif isinstance (geometry, list):
        return chaikin(geometry, iters, keep_ends)

def catmull_rom_smooth(
    geometry: Union[LineString, Polygon, List[Tuple[float, float]]],
    alpha: float = 0.5,
    subdivs: int = 10
):
    """
    Polyline smoothing using Catmull-Rom splines.

    Parameters:
    ----------
    geometry : shapely.geometry.LineString | shapely.geometry.Polygon | list
        Geometric object consisting of polylines to smooth. A shapely
        Linestring or Polygon, or a list containing tuples of (x, y)
        coordinates.
    alpha : float
        Tension parameter. 0 <= alpha <= 1.
        For uniform Catmull-Rom splines, alpha = 0.
        For centripetal Catmull-Rom splines, alpha = 0.5.
        For chordal Catmull-Rom splines, alpha = 1.0.
        Default value: 0.5
    subdivs : int
        Number of subdivisions of each polyline segment. Default value: 10.
    
    Returns:
    -------
    output : shapely.geometry.LineString | shapely.geometry.Polygon | list
        The smoothed geometry.
    """
    if isinstance(geometry, LineString):
        return LineString(catmullrom(geometry.coords, alpha, subdivs))
    elif isinstance (geometry, Polygon):
        return Polygon(catmullrom(geometry.exterior.coords, alpha, subdivs),
                       [catmullrom(hole.coords, alpha, subdivs) for hole in
                        geometry.interiors])
    elif isinstance (geometry, list):
        return catmullrom(geometry, alpha, subdivs)
