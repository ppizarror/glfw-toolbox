# coding=utf-8
"""
SHAPES
Basic Shapes.

author: Daniel Calderon
modified by: @ppizarror

GLFW-TOOLBOX
Toolbox for GLFW Graphic Library.

MIT License
Copyright (c) 2019-2020 Pablo Pizarro R.

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

# Library imports
from glfwToolbox.mathlib import _normal_3_points as _normal3


# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices, texture_file_name=None):
        self.vertices = vertices
        self.indices = indices
        self.textureFileName = texture_file_name


def create_axis(length=1.0, use_neg=True):
    """
    Create axis.

    :param length:
    :param use_neg: If False, Only defined in Positive planes
    :return: Axis object
    """
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -length * use_neg, 0.0, 0.0, 1.0, 0.0, 0.0,
        length, 0.0, 0.0, 1.0, 0.0, 0.0,

        0.0, -length * use_neg, 0.0, 0.0, 1.0, 0.0,
        0.0, length, 0.0, 0.0, 1.0, 0.0,

        0.0, 0.0, -length * use_neg, 0.0, 0.0, 1.0,
        0.0, 0.0, length, 0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1,
        2, 3,
        4, 5]

    return Shape(vertices, indices)


def create_rainbow_triangle():
    """
    :return:
    """
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


def create_rainbow_quad():
    """
    :return:
    """
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


def create_color_quad(r, g, b):
    """
    :param r:
    :param g:
    :param b:
    :return:
    """
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


def create_texture_quad(image_filename, nx=1, ny=1):
    """
    :param image_filename:
    :param nx:
    :param ny:
    :return:
    """
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

    texture_file_name = image_filename

    return Shape(vertices, indices, texture_file_name)


def create_rainbow_cube():
    """
    :return:
    """
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


def create_color_cube(r, g, b):
    """
    :param r:
    :param g:
    :param b:
    :return:
    """
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


def create_texture_cube(image_filename):
    """
    :param image_filename:
    :return:
    """
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


def create_rainbow_normals_cube():
    """
    :return:
    """
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


def create_color_normals_cube(r, g, b):
    """
    :param r:
    :param g:
    :param b:
    :return:
    """
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


def create_texture_normals_cube(image_filename):
    """
    :param image_filename:
    :return:
    """
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


def __vertex_unpack3(vertex):
    """
    Extend vertex to 3 dimension.

    :param vertex:
    :return:
    """
    if len(vertex) == 2:
        vertex = vertex + (0,)
    return vertex


def create4_vertex_texture(image_filename, p1, p2, p3, p4, nx=1, ny=1):
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
    p1 = __vertex_unpack3(p1)
    p2 = __vertex_unpack3(p2)
    p3 = __vertex_unpack3(p3)
    p4 = __vertex_unpack3(p4)

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


def create4_vertex_texture_normal(image_filename, p1, p2, p3, p4, nx=1, ny=1):
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
    p1 = __vertex_unpack3(p1)
    p2 = __vertex_unpack3(p2)
    p3 = __vertex_unpack3(p3)
    p4 = __vertex_unpack3(p4)

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


def create4_vertex_color(p1, p2, p3, p4, r, g, b):
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
    p1 = __vertex_unpack3(p1)
    p2 = __vertex_unpack3(p2)
    p3 = __vertex_unpack3(p3)
    p4 = __vertex_unpack3(p4)

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


def create4_vertex_color_normal(p1, p2, p3, p4, r, g, b):
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
    p1 = __vertex_unpack3(p1)
    p2 = __vertex_unpack3(p2)
    p3 = __vertex_unpack3(p3)
    p4 = __vertex_unpack3(p4)

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


def create_triangle_texture(image_filename, p1, p2, p3, nx=1, ny=1):
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


def create_triangle_texture_normal(image_filename, p1, p2, p3, nx=1, ny=1):
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


def create_triangle_color(p1, p2, p3, r, g, b):
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
    p1 = __vertex_unpack3(p1)
    p2 = __vertex_unpack3(p2)
    p3 = __vertex_unpack3(p3)

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


def create_triangle_color_normal(p1, p2, p3, r, g, b):
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
    p1 = __vertex_unpack3(p1)
    p2 = __vertex_unpack3(p2)
    p3 = __vertex_unpack3(p3)

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
