from shapely.geometry import LineString

import shapelysmooth as ss

line = LineString([(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)])

def test_taubin_smooth():
    smoothed = ss.taubin_smooth(line)
    assert smoothed.length < line.length

def test_chaikin_smooth():
    smoothed = ss.chaikin_smooth(line)
    assert smoothed.length < line.length

def test_catmull_rom_smooth():
    smoothed = ss.catmull_rom_smooth(line)
    assert smoothed.length < line.length