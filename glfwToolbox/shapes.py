# coding=utf-8
"""
SHAPES
Basic Shapes.

author: Daniel Calderon
modified by: @ppizarror

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

# Library imports
from glfwToolbox.easy_shaders import toGPUShape as _toGPUShape
import glfwToolbox.tripy as _tripy
from glfwToolbox.mathlib import _normal_3_points as _normal3
from glfwToolbox.advanced_shapes import AdvancedGPUShape as _AdvancedGPUShape


# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices, texture_file_name=None):
        self.vertices = vertices
        self.indices = indices
        self.textureFileName = texture_file_name


def createAxis(length=1.0):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -length, 0.0, 0.0, 0.0, 0.0, 0.0,
        length, 0.0, 0.0, 1.0, 0.0, 0.0,

        0.0, -length, 0.0, 0.0, 0.0, 0.0,
        0.0, length, 0.0, 0.0, 1.0, 0.0,

        0.0, 0.0, -length, 0.0, 0.0, 0.0,
        0.0, 0.0, length, 0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1,
        2, 3,
        4, 5]

    return Shape(vertices, indices)


def createRainbowTriangle():
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
        0.0, 0.5, 0.0, 0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return Shape(vertices, indices)


def createRainbowQuad():
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.0, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.0, 1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)


def createColorQuad(r, g, b):
    # Defining locations and colors for each vertex of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0, r, g, b,
        0.5, -0.5, 0.0, r, g, b,
        0.5, 0.5, 0.0, r, g, b,
        -0.5, 0.5, 0.0, r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)


def createTextureQuad(image_filename, nx=1, ny=1):
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions        texture
        -0.5, -0.5, 0.0, 0, 0,
        0.5, -0.5, 0.0, nx, 0,
        0.5, 0.5, 0.0, nx, ny,
        -0.5, 0.5, 0.0, 0, ny]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    textureFileName = image_filename

    return Shape(vertices, indices, textureFileName)


def createRainbowCube():
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions         colors
        -0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.5, 1.0, 1.0, 1.0,

        -0.5, -0.5, -0.5, 1.0, 1.0, 0.0,
        0.5, -0.5, -0.5, 0.0, 1.0, 1.0,
        0.5, 0.5, -0.5, 1.0, 0.0, 1.0,
        -0.5, 0.5, -0.5, 1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def createColorCube(r, g, b):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -0.5, -0.5, 0.5, r, g, b,
        0.5, -0.5, 0.5, r, g, b,
        0.5, 0.5, 0.5, r, g, b,
        -0.5, 0.5, 0.5, r, g, b,

        -0.5, -0.5, -0.5, r, g, b,
        0.5, -0.5, -0.5, r, g, b,
        0.5, 0.5, -0.5, r, g, b,
        -0.5, 0.5, -0.5, r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def createTextureCube(image_filename):
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+
        -0.5, -0.5, 0.5, 0, 0,
        0.5, -0.5, 0.5, 1, 0,
        0.5, 0.5, 0.5, 1, 1,
        -0.5, 0.5, 0.5, 0, 1,

        # Z-
        -0.5, -0.5, -0.5, 0, 0,
        0.5, -0.5, -0.5, 1, 0,
        0.5, 0.5, -0.5, 1, 1,
        -0.5, 0.5, -0.5, 0, 1,

        # X+
        0.5, -0.5, -0.5, 0, 0,
        0.5, 0.5, -0.5, 1, 0,
        0.5, 0.5, 0.5, 1, 1,
        0.5, -0.5, 0.5, 0, 1,

        # X-
        -0.5, -0.5, -0.5, 0, 0,
        -0.5, 0.5, -0.5, 1, 0,
        -0.5, 0.5, 0.5, 1, 1,
        -0.5, -0.5, 0.5, 0, 1,

        # Y+
        -0.5, 0.5, -0.5, 0, 0,
        0.5, 0.5, -0.5, 1, 0,
        0.5, 0.5, 0.5, 1, 1,
        -0.5, 0.5, 0.5, 0, 1,

        # Y-
        -0.5, -0.5, -0.5, 0, 0,
        0.5, -0.5, -0.5, 1, 0,
        0.5, -0.5, 0.5, 1, 1,
        -0.5, -0.5, 0.5, 0, 1
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices, image_filename)


def createRainbowNormalsCube():
    sq3 = 0.57735027

    # Defining the location and colors of each vertex  of the shape
    vertices = [
        -0.5, -0.5, 0.5, 1.0, 0.0, 0.0, -sq3, -sq3, sq3,
        0.5, -0.5, 0.5, 0.0, 1.0, 0.0, sq3, -sq3, sq3,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0, sq3, sq3, sq3,
        -0.5, 0.5, 0.5, 1.0, 1.0, 1.0, -sq3, sq3, sq3,

        -0.5, -0.5, -0.5, 1.0, 1.0, 0.0, -sq3, -sq3, -sq3,
        0.5, -0.5, -0.5, 0.0, 1.0, 1.0, sq3, -sq3, -sq3,
        0.5, 0.5, -0.5, 1.0, 0.0, 1.0, sq3, sq3, -sq3,
        -0.5, 0.5, -0.5, 1.0, 1.0, 1.0, -sq3, sq3, -sq3]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2, 2, 3, 0,
               4, 5, 6, 6, 7, 4,
               4, 5, 1, 1, 0, 4,
               6, 7, 3, 3, 2, 6,
               5, 6, 2, 2, 1, 5,
               7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def createColorNormalsCube(r, g, b):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions         colors   normals
        # Z+
        -0.5, -0.5, 0.5, r, g, b, 0, 0, 1,
        0.5, -0.5, 0.5, r, g, b, 0, 0, 1,
        0.5, 0.5, 0.5, r, g, b, 0, 0, 1,
        -0.5, 0.5, 0.5, r, g, b, 0, 0, 1,

        # Z-
        -0.5, -0.5, -0.5, r, g, b, 0, 0, -1,
        0.5, -0.5, -0.5, r, g, b, 0, 0, -1,
        0.5, 0.5, -0.5, r, g, b, 0, 0, -1,
        -0.5, 0.5, -0.5, r, g, b, 0, 0, -1,

        # X+
        0.5, -0.5, -0.5, r, g, b, 1, 0, 0,
        0.5, 0.5, -0.5, r, g, b, 1, 0, 0,
        0.5, 0.5, 0.5, r, g, b, 1, 0, 0,
        0.5, -0.5, 0.5, r, g, b, 1, 0, 0,

        # X-
        -0.5, -0.5, -0.5, r, g, b, -1, 0, 0,
        -0.5, 0.5, -0.5, r, g, b, -1, 0, 0,
        -0.5, 0.5, 0.5, r, g, b, -1, 0, 0,
        -0.5, -0.5, 0.5, r, g, b, -1, 0, 0,

        # Y+
        -0.5, 0.5, -0.5, r, g, b, 0, 1, 0,
        0.5, 0.5, -0.5, r, g, b, 0, 1, 0,
        0.5, 0.5, 0.5, r, g, b, 0, 1, 0,
        -0.5, 0.5, 0.5, r, g, b, 0, 1, 0,

        # Y-
        -0.5, -0.5, -0.5, r, g, b, 0, -1, 0,
        0.5, -0.5, -0.5, r, g, b, 0, -1, 0,
        0.5, -0.5, 0.5, r, g, b, 0, -1, 0,
        -0.5, -0.5, 0.5, r, g, b, 0, -1, 0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)


def createTextureNormalsCube(image_filename):
    # Defining locations,texture coordinates and normals for each vertex of the shape
    vertices = [
        #   positions            tex coords   normals
        # Z+
        -0.5, -0.5, 0.5, 0, 0, 0, 0, 1,
        0.5, -0.5, 0.5, 1, 0, 0, 0, 1,
        0.5, 0.5, 0.5, 1, 1, 0, 0, 1,
        -0.5, 0.5, 0.5, 0, 1, 0, 0, 1,
        # Z-
        -0.5, -0.5, -0.5, 0, 0, 0, 0, -1,
        0.5, -0.5, -0.5, 1, 0, 0, 0, -1,
        0.5, 0.5, -0.5, 1, 1, 0, 0, -1,
        -0.5, 0.5, -0.5, 0, 1, 0, 0, -1,

        # X+
        0.5, -0.5, -0.5, 0, 0, 1, 0, 0,
        0.5, 0.5, -0.5, 1, 0, 1, 0, 0,
        0.5, 0.5, 0.5, 1, 1, 1, 0, 0,
        0.5, -0.5, 0.5, 0, 1, 1, 0, 0,
        # X-
        -0.5, -0.5, -0.5, 0, 0, -1, 0, 0,
        -0.5, 0.5, -0.5, 1, 0, -1, 0, 0,
        -0.5, 0.5, 0.5, 1, 1, -1, 0, 0,
        -0.5, -0.5, 0.5, 0, 1, -1, 0, 0,
        # Y+
        -0.5, 0.5, -0.5, 0, 0, 0, 1, 0,
        0.5, 0.5, -0.5, 1, 0, 0, 1, 0,
        0.5, 0.5, 0.5, 1, 1, 0, 1, 0,
        -0.5, 0.5, 0.5, 0, 1, 0, 1, 0,
        # Y-
        -0.5, -0.5, -0.5, 0, 0, 0, -1, 0,
        0.5, -0.5, -0.5, 1, 0, 0, -1, 0,
        0.5, -0.5, 0.5, 1, 1, 0, -1, 0,
        -0.5, -0.5, 0.5, 0, 1, 0, -1, 0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices, image_filename)


def __vertexUnpack3(vertex):
    """
    Extend vertex to 3 dimension.

    :param vertex:
    :return:
    """
    if len(vertex) == 2:
        vertex = vertex + (0,)
    return vertex


def createColorPlaneFromCurve(curve, triangulate, r, g, b, center=None):
    """
    Creates a plane from a curve and a center.

    :param curve: Curve vertex list
    :param triangulate: Create plane from curve triangulation
    :param center: Center position
    :param r: Red color
    :param g: Green color
    :param b: Blue color
    :return: Merged shape
    :rtype: AdvancedGPUShape
    """
    shapes = []

    # Use delaunay triangulation
    if triangulate:
        k = []
        for i in curve:
            k.append((i[0], i[1]))
        tri = _tripy.earclip(k)
        for i in tri:
            x1, y1 = i[0]
            x2, y2 = i[1]
            x3, y3 = i[2]
            shape = createTriangleColor((x1, y1, 0), (x2, y2, 0), (x3, y3, 0), r, g, b)
            shapes.append(_toGPUShape(shape))
    else:
        if center is None:
            center = curve[0]
        for i in range(0, len(curve) - 1):
            x1, y1 = curve[i]
            x2, y2 = curve[(i + 1) % len(curve)]
            c1, c2 = center
            shape = createTriangleColor((x1, y1, 0), (x2, y2, 0), (c1, c2, 0), r, g, b)
            shapes.append(_toGPUShape(shape))
    return _AdvancedGPUShape(shapes)


def create4VertexTexture(image_filename, p1, p2, p3, p4, nx=1, ny=1):
    """
    Creates a 4-vertex poly with texture.

    :param image_filename: Image
    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param p4: Vertex (x,y,z)
    :param nx: Texture coord pos
    :param ny: Texture coord pos
    :return:
    """
    # Extend
    p1 = __vertexUnpack3(p1)
    p2 = __vertexUnpack3(p2)
    p3 = __vertexUnpack3(p3)
    p4 = __vertexUnpack3(p4)

    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    x4, y4, z4 = p4

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        x1, y1, z1, 0, 0,
        x2, y2, z2, nx, 0,
        x3, y3, z3, nx, ny,
        x4, y4, z4, 0, ny
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices, image_filename)


def create4VertexTextureNormal(image_filename, p1, p2, p3, p4, nx=1, ny=1):
    """
    Creates a 4-vertex poly with texture.

    :param image_filename: Image
    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param p4: Vertex (x,y,z)
    :param nx: Texture coord pos
    :param ny: Texture coord pos
    :return:
    """
    # Extend
    p1 = __vertexUnpack3(p1)
    p2 = __vertexUnpack3(p2)
    p3 = __vertexUnpack3(p3)
    p4 = __vertexUnpack3(p4)

    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    x4, y4, z4 = p4

    # Calculate the normal
    normal = _normal3(p3, p2, p1)

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        x1, y1, z1, 0, 0, normal.get_x(), normal.get_y(), normal.get_z(),
        x2, y2, z2, nx, 0, normal.get_x(), normal.get_y(), normal.get_z(),
        x3, y3, z3, nx, ny, normal.get_x(), normal.get_y(), normal.get_z(),
        x4, y4, z4, 0, ny, normal.get_x(), normal.get_y(), normal.get_z()
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices, image_filename)


def create4VertexColor(p1, p2, p3, p4, r, g, b):
    """
    Creates a 4-vertex poly with color.

    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param p4: Vertex (x,y,z)
    :param r: Red color
    :param g: Green color
    :param b: Blue color
    :return:
    """
    # Extend
    p1 = __vertexUnpack3(p1)
    p2 = __vertexUnpack3(p2)
    p3 = __vertexUnpack3(p3)
    p4 = __vertexUnpack3(p4)

    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    x4, y4, z4 = p4

    # Defining locations and color
    vertices = [
        # X, Y,  Z, R, G, B,
        x1, y1, z1, r, g, b,
        x2, y2, z2, r, g, b,
        x3, y3, z3, r, g, b,
        x4, y4, z4, r, g, b
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0
    ]

    return Shape(vertices, indices)


def create4VertexColorNormal(p1, p2, p3, p4, r, g, b):
    """
    Creates a 4-vertex figure with color and normals.

    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param p4: Vertex (x,y,z)
    :param r: Red color
    :param g: Green color
    :param b: Blue color
    :return:
    """
    # Extend
    p1 = __vertexUnpack3(p1)
    p2 = __vertexUnpack3(p2)
    p3 = __vertexUnpack3(p3)
    p4 = __vertexUnpack3(p4)

    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    x4, y4, z4 = p4

    # Calculate the normal
    normal = _normal3(p3, p2, p1)

    # Defining locations and color
    vertices = [
        # X, Y,  Z, R, G, B,
        x1, y1, z1, r, g, b, normal.get_x(), normal.get_y(), normal.get_z(),
        x2, y2, z2, r, g, b, normal.get_x(), normal.get_y(), normal.get_z(),
        x3, y3, z3, r, g, b, normal.get_x(), normal.get_y(), normal.get_z(),
        x4, y4, z4, r, g, b, normal.get_x(), normal.get_y(), normal.get_z()
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0
    ]

    return Shape(vertices, indices)


def createTriangleTexture(image_filename, p1, p2, p3, nx=1, ny=1):
    """
    Creates a triangle with textures.

    :param image_filename: Image
    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param nx: Texture coord pos
    :param ny: Texture coord pos
    :return:
    """
    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        # X, Y,  Z,   U,   V
        x1, y1, z1, (nx + ny) / 2, nx,
        x2, y2, z2, 0.0, 0.0,
        x3, y3, z3, ny, 0.0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2
    ]

    return Shape(vertices, indices, image_filename)


def createTriangleTextureNormal(image_filename, p1, p2, p3, nx=1, ny=1):
    """
    Creates a triangle with textures.

    :param image_filename: Image
    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param nx: Texture coord pos
    :param ny: Texture coord pos
    :return:
    """
    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3

    # Calculate the normal
    normal = _normal3(p3, p2, p1)

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        # X, Y,  Z,   U,   V
        x1, y1, z1, (nx + ny) / 2, nx, normal.get_x(), normal.get_y(), normal.get_z(),
        x2, y2, z2, 0.0, 0.0, normal.get_x(), normal.get_y(), normal.get_z(),
        x3, y3, z3, ny, 0.0, normal.get_x(), normal.get_y(), normal.get_z()
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2
    ]

    return Shape(vertices, indices, image_filename)


def createTriangleColor(p1, p2, p3, r, g, b):
    """
    Creates a triangle with color.

    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param r: Red color
    :param g: Green color
    :param b: Blue color
    :return:
    """
    # Extend
    p1 = __vertexUnpack3(p1)
    p2 = __vertexUnpack3(p2)
    p3 = __vertexUnpack3(p3)

    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3

    # Defining locations and color
    vertices = [
        # X, Y,  Z, R, G, B,
        x1, y1, z1, r, g, b,
        x2, y2, z2, r, g, b,
        x3, y3, z3, r, g, b,
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2
    ]

    return Shape(vertices, indices)


def createTriangleColorNormal(p1, p2, p3, r, g, b):
    """
    Creates a triangle with color.

    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param r: Red color
    :param g: Green color
    :param b: Blue color
    :return:
    """
    # Extend
    p1 = __vertexUnpack3(p1)
    p2 = __vertexUnpack3(p2)
    p3 = __vertexUnpack3(p3)

    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3

    # Calculate the normal
    normal = _normal3(p3, p2, p1)

    # Defining locations and color
    vertices = [
        # X, Y,  Z, R, G, B,
        x1, y1, z1, r, g, b, normal.get_x(), normal.get_y(), normal.get_z(),
        x2, y2, z2, r, g, b, normal.get_x(), normal.get_y(), normal.get_z(),
        x3, y3, z3, r, g, b, normal.get_x(), normal.get_y(), normal.get_z()
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2
    ]

    return Shape(vertices, indices)
