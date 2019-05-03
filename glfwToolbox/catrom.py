# coding=utf-8
"""
CATMULL-ROM CURVE
Catmull Rom curve definition.

GLFW-TOOLBOX
Toolbox for GLFW Graphic Library.

MIT License
Copyright (c) 2019 Pablo Pizarro R.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import math


def __checkValidVertex(vertex):
    """
    Check vertex is valid.

    :param vertex:
    :return:
    """
    assert isinstance(vertex, list), 'Vertex {0} is not a list'.format(vertex)
    assert len(vertex) != 1, 'Vertex {0} cannot be a number'.format(vertex)
    assert len(vertex) == 2, 'Vertex [{0}] invalid'.format(','.join(str(x) for x in vertex))


def getSpline(vertices, fps):
    """
    Create a CatMull Rom spline from vertices.

    :param vertices:
    :param fps:
    :return:
    """
    for i in vertices:
        __checkValidVertex(i)
    crs = []
    for x in range(0, len(vertices) - 3):
        points = [vertices[x], vertices[x + 1], vertices[x + 2], vertices[x + 3]]
        t = 0
        while t < len(points) - 3.0:
            p1 = 1
            p2 = 2
            p3 = 3
            p0 = 0

            t = t - math.floor(t)
            tt = t * t
            ttt = tt * t

            q1 = -ttt + 2.0 * tt - t
            q2 = 3.0 * ttt - 5.0 * tt + 2.0
            q3 = -3.0 * ttt + 4.0 * tt + t
            q4 = ttt - tt
            tx = 0.5 * (points[p0][0] * q1 + points[p1][0] * q2 + points[p2][0] * q3 + points[p3][0] * q4)
            ty = 0.5 * (points[p0][1] * q1 + points[p1][1] * q2 + points[p2][1] * q3 + points[p3][1] * q4)

            crs.append([tx, ty])
            t += 1 / fps
    return crs


def getSplineFixed(vertices, fps):
    """
    Create spline fixed.

    :param vertices: Lista de vertices
    :type vertices: list
    :param fps: Velocidad de avance
    :type fps: float
    :return:
    """
    v = vertices.copy()
    v.insert(0, vertices[0])
    v.append(vertices[-1])
    return getSpline(v, fps)
