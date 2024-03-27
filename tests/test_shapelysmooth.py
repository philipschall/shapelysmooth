from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, TypeVar

import pytest
from shapely.geometry import LineString, Polygon

import shapelysmooth as ss

if TYPE_CHECKING:
    GTypeVar = TypeVar("GTypeVar", LineString, Polygon, list[tuple[float, float]])


def _is_close(a: float, b: float, tol: float = 1e-3) -> bool:
    return abs(a - b) < tol


def assert_allclose(
    a: list[tuple[float, float]], b: list[tuple[float, float]], tol: float = 1e-3
) -> None:
    assert all(_is_close(x, xe, tol) and _is_close(y, ye, tol) for (x, y), (xe, ye) in zip(a, b))


class TestSmoothingCoords:
    @pytest.fixture()
    def coords(self):
        return [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)]

    @pytest.mark.parametrize(
        ("method", "expected", "kwargs"),
        [
            (
                ss.taubin_smooth,
                [(0.0, 0.0), (1.0, 0.4494), (2.0, 0.6334), (3.0, 0.4494), (4.0, 0.0)],
                {},
            ),
            (
                ss.chaikin_smooth,
                [
                    (0.0, 0.0),
                    (0.75, 0.75),
                    (1.25, 0.75),
                    (1.75, 0.25),
                    (2.25, 0.25),
                    (2.75, 0.75),
                    (3.25, 0.75),
                    (4.0, 0.0),
                ],
                {"iters": 1},
            ),
            (
                ss.catmull_rom_smooth,
                [
                    (0.0, 0.0),
                    (0.375, 0.5),
                    (1.0, 1.0),
                    (1.5, 0.5),
                    (2.0, 0.0),
                    (2.5, 0.5),
                    (3.0, 1.0),
                    (3.4358, 0.5784),
                    (4.0, 0.0),
                ],
                {"subdivs": 2},
            ),
        ],
    )
    def test_smoothing_coords(
        self,
        coords: list[tuple[float, float]],
        method: Callable[..., GTypeVar],
        expected: list[tuple[float, float]],
        kwargs: dict[str, Any],
    ):
        smoothed = method(coords, **kwargs)
        assert_allclose(smoothed, expected)


class TestSmoothingLine:
    @pytest.fixture()
    def line(self):
        return LineString([(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)])

    @pytest.mark.parametrize(
        ("method", "expected", "kwargs"),
        [
            (
                ss.taubin_smooth,
                [(0.0, 0.0), (1.0, 0.4494), (2.0, 0.6334), (3.0, 0.4494), (4.0, 0.0)],
                {},
            ),
            (
                ss.chaikin_smooth,
                [
                    (0.0, 0.0),
                    (0.75, 0.75),
                    (1.25, 0.75),
                    (1.75, 0.25),
                    (2.25, 0.25),
                    (2.75, 0.75),
                    (3.25, 0.75),
                    (4.0, 0.0),
                ],
                {"iters": 1},
            ),
            (
                ss.catmull_rom_smooth,
                [
                    (0.0, 0.0),
                    (0.375, 0.5),
                    (1.0, 1.0),
                    (1.5, 0.5),
                    (2.0, 0.0),
                    (2.5, 0.5),
                    (3.0, 1.0),
                    (3.4358, 0.5784),
                    (4.0, 0.0),
                ],
                {"subdivs": 2},
            ),
        ],
    )
    def test_smoothing_line(
        self,
        line: LineString,
        method: Callable[..., GTypeVar],
        expected: list[tuple[float, float]],
        kwargs: dict[str, Any],
    ):
        smoothed = method(line, **kwargs)
        assert_allclose(smoothed.coords, expected)


class TestSmoothingPoly:
    @pytest.fixture()
    def poly(self):
        return Polygon(
            [(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)], [[(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)]]
        )

    @pytest.mark.parametrize(
        ("method", "expected", "kwargs"),
        [
            (
                ss.taubin_smooth,
                [
                    (1.144, 1.144),
                    (1.856, 1.144),
                    (1.856, 1.856),
                    (1.144, 1.856),
                    (1.144, 1.144),
                    (1.3813, 1.3813),
                    (1.6187, 1.3813),
                    (1.6187, 1.6187),
                    (1.3813, 1.6187),
                    (1.3813, 1.3813),
                ],
                {},
            ),
            (
                ss.chaikin_smooth,
                [
                    (0.75, 0.0),
                    (2.25, 0.0),
                    (3.0, 0.75),
                    (3.0, 2.25),
                    (2.25, 3.0),
                    (0.75, 3.0),
                    (0.0, 2.25),
                    (0.0, 0.75),
                    (0.75, 0.0),
                    (1.25, 1.0),
                    (1.75, 1.0),
                    (2.0, 1.25),
                    (2.0, 1.75),
                    (1.75, 2.0),
                    (1.25, 2.0),
                    (1.0, 1.75),
                    (1.0, 1.25),
                    (1.25, 1.0),
                ],
                {"iters": 1},
            ),
            (
                ss.catmull_rom_smooth,
                [
                    (0.0, 0.0),
                    (1.5, -0.375),
                    (3.0, 0.0),
                    (3.375, 1.5),
                    (3.0, 3.0),
                    (1.5, 3.375),
                    (0.0, 3.0),
                    (-0.375, 1.5),
                    (0.0, 0.0),
                    (1.0, 1.0),
                    (1.5, 0.875),
                    (2.0, 1.0),
                    (2.125, 1.5),
                    (2.0, 2.0),
                    (1.5, 2.125),
                    (1.0, 2.0),
                    (0.875, 1.5),
                    (1.0, 1.0),
                ],
                {"subdivs": 2},
            ),
        ],
    )
    def test_smoothing_poly(
        self,
        poly: Polygon,
        method: Callable[..., GTypeVar],
        expected: list[tuple[float, float]],
        kwargs: dict[str, Any],
    ):
        smoothed = method(poly, **kwargs)
        c_list = list(smoothed.exterior.coords) + [
            coord for hole in smoothed.interiors for coord in hole.coords
        ]
        assert_allclose(c_list, expected)


def test_input_error():
    with pytest.raises(ss.InputeTypeError):
        ss.taubin_smooth(123)
