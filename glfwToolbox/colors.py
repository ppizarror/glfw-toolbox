# coding=utf-8
"""
COLORS
Color auxiliary functions.

GLFW-TOOLBOX
Toolbox for GLFW Graphic Library.

MIT License
Copyright (c) 2019 Pablo Pizarro R.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import matplotlib.pyplot as _plt
import numpy as _np

# Matplotlib colormap
_COLOR_COLORMAP_R = _np.linspace(0, 1)
# noinspection PyUnresolvedReferences
_COLOR_COLORMAP_HSV = _plt.cm.hsv(_COLOR_COLORMAP_R)

# Gradient color factors
_COLOR_GRADIENT_RFACTOR = [-1029.86559098, 2344.5778132, -1033.38786418, -487.3693808,
                           298.50245209, 167.25393272]
_COLOR_GRADIENT_GFACTOR = [551.32444915, -1098.30287507, 320.71732031, 258.50778539,
                           193.11772901, 30.32958789]
_COLOR_GRADIENT_BFACTOR = [222.95535971, -1693.48546233, 2455.80348727, -726.44075478,
                           -69.61151887, 67.591787]


def _clamp(n):
    return min(255, max(0, n))


def generic_gradient(x, rfactors=None, gfactors=None, bfactors=None):
    """
    Return the r,g,b values along the predefined gradient for
    x in the range [0.0, 1.0].
    """
    if rfactors is None:
        rfactors = _COLOR_GRADIENT_RFACTOR
    if gfactors is None:
        gfactors = _COLOR_GRADIENT_GFACTOR
    if bfactors is None:
        bfactors = _COLOR_GRADIENT_BFACTOR
    n = len(rfactors)
    r = _clamp(int(sum(rfactors[i] * (x ** (n - 1 - i)) for i in range(n))))
    g = _clamp(int(sum(gfactors[i] * (x ** (n - 1 - i)) for i in range(n))))
    b = _clamp(int(sum(bfactors[i] * (x ** (n - 1 - i)) for i in range(n))))
    return float(r) / 255, float(g) / 255, float(b) / 255


def color_hsv(x):
    """
    Return color from colormap.

    :param x: Value from 0 to 1
    :return:
    """
    if x < 0 or x > 1:
        raise Exception('x must be numerical bewteen 0 and 1')
    for i in range(len(_COLOR_COLORMAP_R)):
        if x <= _COLOR_COLORMAP_R[i]:
            return _COLOR_COLORMAP_HSV[i]
