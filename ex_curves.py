# coding=utf-8
"""
EXAMPLE-CURVES
Simple example that creates a plane using Catmull-Rom curve.

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

# Library imports
import glfw
from OpenGL.GL import *
import numpy as np
import sys

from glfwToolbox.advanced_shapes import AdvancedGPUShape
from glfwToolbox.mathlib import Point3
import glfwToolbox.camera as cam
import glfwToolbox.catrom as catrom
import glfwToolbox.easy_shaders as es
import glfwToolbox.shapes as bs
import glfwToolbox.transformations as tr2
from glfwToolbox.tripy import earclip


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# Global controller as communication with the callback function
controller = Controller()

# Create camera
camera = cam.CameraR(r=3, center=Point3())
camera.set_r_vel(0.1)


# noinspection PyUnusedLocal
def on_key(window_obj, key, scancode, action, mods):
    global controller

    if action == glfw.REPEAT or action == glfw.PRESS:
        # Move the camera position
        if key == glfw.KEY_LEFT:
            camera.rotate_phi(-4)
        elif key == glfw.KEY_RIGHT:
            camera.rotate_phi(4)
        elif key == glfw.KEY_UP:
            camera.rotate_theta(-4)
        elif key == glfw.KEY_DOWN:
            camera.rotate_theta(4)
        elif key == glfw.KEY_A:
            camera.close()
        elif key == glfw.KEY_D:
            camera.far()

        # Move the center of the camera
        elif key == glfw.KEY_I:
            camera.move_center_x(-0.05)
        elif key == glfw.KEY_K:
            camera.move_center_x(0.05)
        elif key == glfw.KEY_J:
            camera.move_center_y(-0.05)
        elif key == glfw.KEY_L:
            camera.move_center_y(0.05)
        elif key == glfw.KEY_U:
            camera.move_center_z(-0.05)
        elif key == glfw.KEY_O:
            camera.move_center_z(0.05)

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        sys.exit()


def create_color_plane_from_curve(_curve, triangulate, r, g, b, center=None):
    """
    Creates a plane from a curve and a center.

    :param _curve: Curve vertex list
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
        for i in _curve:
            k.append((i[0], i[1]))
        tri = earclip(k)
        for i in tri:
            x1, y1 = i[0]
            x2, y2 = i[1]
            x3, y3 = i[2]
            shape = bs.create_triangle_color((x1, y1, 0), (x2, y2, 0), (x3, y3, 0), r, g, b)
            shapes.append(es.to_gpu_shape(shape))
    else:
        if center is None:
            center = _curve[0]
        for i in range(0, len(_curve) - 1):
            x1, y1 = _curve[i]
            x2, y2 = _curve[(i + 1) % len(_curve)]
            c1, c2 = center
            shape = bs.create_triangle_color((x1, y1, 0), (x2, y2, 0), (c1, c2, 0), r, g, b)
            shapes.append(es.to_gpu_shape(shape))
    return AdvancedGPUShape(shapes)


if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 800

    window = glfw.create_window(width, height, 'Curves', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colores
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Create models
    gpuAxis = es.to_gpu_shape(bs.create_axis(1))
    obj_axis = AdvancedGPUShape(gpuAxis, shader=colorShaderProgram)

    # Create one side of the wall
    vertices = [[1, 0], [0.9, 0.4], [0.5, 0.5], [0, 0.5]]
    curve = catrom.get_spline_fixed(vertices, 10)

    obj_planeL = create_color_plane_from_curve(curve, False, 0.6, 0.6, 0.6, center=(0, 0))
    obj_planeL.uniform_scale(1.1)
    obj_planeL.rotation_x(np.pi / 2)
    obj_planeL.rotation_z(-np.pi / 2)
    obj_planeL.translate(0.5, 0, 0)
    obj_planeL.set_shader(colorShaderProgram)

    # Create other side of the wall
    obj_planeR = obj_planeL.clone()
    obj_planeR.translate(-1, 0, 0)

    # Textured plane
    s1 = (0.5, 0, 0)
    s2 = (-0.5, 0, 0)
    s3 = (-0.5, 0.55, 0)
    s4 = (0.5, 0.55, 0)
    gpuTexturePlane = es.to_gpu_shape(bs.create4_vertex_texture('example_data/bricks.jpg', s1, s2, s3, s4), GL_REPEAT, GL_LINEAR)
    obj_planeS = AdvancedGPUShape(gpuTexturePlane, shader=textureShaderProgram)
    obj_planeS.rotation_x(np.pi / 2)

    # Bottom plane
    s1 = (0.5, 0, 0)
    s2 = (-0.5, 0, 0)
    s3 = (-0.5, 0.55, 0)
    s4 = (0.5, 0.55, 0)
    gpuTexturePlane = es.to_gpu_shape(bs.create4_vertex_texture('example_data/boo.png', s1, s2, s3, s4), GL_REPEAT, GL_LINEAR)
    obj_planeB = AdvancedGPUShape(gpuTexturePlane, shader=textureShaderProgram)
    obj_planeB.rotation_z(np.pi)
    obj_planeB.scale(1, 2, 1)

    # Create camera target
    obj_camTarget = AdvancedGPUShape(es.to_gpu_shape(bs.create_color_cube(1, 0, 0.5)), shader=colorShaderProgram)
    obj_camTarget.uniform_scale(0.05)

    # Main loop
    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Create projection
        # projection = tr2.ortho(-1, 1, -1, 1, 0.1, 100)
        projection = tr2.perspective(45, float(width) / float(height), 0.1, 100)

        # Get camera view matrix
        view = camera.get_view()

        # Update target cube object
        t = tr2.translate(camera.get_center_x(), camera.get_center_y(), camera.get_center_z())
        obj_camTarget.apply_temporal_transform(t)

        # Draw objects
        obj_axis.draw(view, projection, mode=GL_LINES)
        obj_camTarget.draw(view, projection)
        obj_planeL.draw(view, projection)
        obj_planeR.draw(view, projection)
        obj_planeS.draw(view, projection)
        obj_planeB.draw(view, projection)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen
        glfw.swap_buffers(window)

    glfw.terminate()
