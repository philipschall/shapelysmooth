"""Smooth a polyline using Taubin, Chaikin, or Catmull-Rom algorithms."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, TypeVar

from _shapelysmooth import catmullrom, chaikin, taubin
from shapely.geometry import LineString, MultiPoint, Polygon

if TYPE_CHECKING:
    GTypeVar = TypeVar("GTypeVar", LineString, Polygon, list[tuple[float, float]])


__all__ = ["taubin_smooth", "chaikin_smooth", "catmull_rom_smooth"]
__version__ = "0.2.1"


class InputeTypeError(TypeError):
    def __init__(self):
        self.message = (
            "`geometry` must be LineString, Polygon, or a list of (x, y) coordinates."
        )
        super().__init__(self.message)


def _get_coords(
    geometry: LineString | Polygon | list[tuple[float, float]],
) -> tuple[list[tuple[float, float]], list[list[tuple[float, float]]] | None]:
    """Get the coordinates of the geometry."""
    if isinstance(geometry, LineString):
        return geometry.coords, None  # pyright: ignore[reportReturnType]
    if isinstance(geometry, Polygon):
        return geometry.exterior.coords, [hole.coords for hole in geometry.interiors]
    try:
        mp = MultiPoint(geometry)
    except (TypeError, AttributeError, ValueError) as ex:
        raise InputeTypeError from ex
    return [(p.x, p.y) for p in mp.geoms], None


def _smooth_geometry(
    geometry: GTypeVar, smooth_func: Callable[..., GTypeVar], *args: Any
) -> GTypeVar:
    """Smooth the geometry using the specified smoothing function."""
    coords, interior_coords = _get_coords(geometry)
    coords_smoothed = smooth_func(coords, *args)
    if isinstance(geometry, LineString):
        return LineString(coords_smoothed)
    if isinstance(geometry, Polygon) and interior_coords is not None:
        interior_coords_smoothed = [smooth_func(c, *args) for c in interior_coords]
        return Polygon(coords_smoothed, interior_coords_smoothed)
    return coords_smoothed


def taubin_smooth(
    geometry: GTypeVar, factor: float = 0.5, mu: float = -0.5, steps: int = 5
) -> GTypeVar:
    """
    Taubin polyline smoothing.

    Parameters
    ----------
    geometry : shapely.LineString, shapely.Polygon, or list
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

    Returns
    -------
    output : shapely.LineString, shapely.Polygon, or list
        The smoothed geometry.
    """
    return _smooth_geometry(geometry, taubin, factor, mu, steps)


def chaikin_smooth(geometry: GTypeVar, iters: int = 5, keep_ends: bool = True) -> GTypeVar:
    """
    Polyline smoothing using Chaikin's corner cutting algorithm.

    Parameters
    ----------
    geometry : shapely.LineString, shapely.Polygon, or list
        Geometric object consisting of polylines to smooth. A shapely
        Linestring or Polygon, or a list containing tuples of (x, y)
        coordinates.
    iters : int
        Number of iterations. Default value: 3.
    keep_ends : bool
        Preserve the original start and end nodes of the polyline. Not
        applicable to closed polylines. Default value: True.

    Returns
    -------
    output : shapely.LineString, shapely.Polygon, or list
        The smoothed geometry.
    """
    return _smooth_geometry(geometry, chaikin, iters, keep_ends)


def catmull_rom_smooth(geometry: GTypeVar, alpha: float = 0.5, subdivs: int = 10) -> GTypeVar:
    """
    Polyline smoothing using Catmull-Rom splines.

    Parameters
    ----------
    geometry : shapely.LineString, shapely.Polygon, or list
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

    Returns
    -------
    output : shapely.LineString, shapely.Polygon, or list
        The smoothed geometry.
    """
    return _smooth_geometry(geometry, catmullrom, alpha, subdivs)
