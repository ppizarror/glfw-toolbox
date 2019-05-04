# coding=utf-8
"""
EXAMPLE-TEXTURE-CUBE
Texture cube.

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

import glfw
from OpenGL.GL import *
import numpy as np
import sys

from glfwToolbox.advanced_shapes import AdvancedGPUShape
import glfwToolbox.shapes as shapes
import glfwToolbox.easy_shaders as es
import glfwToolbox.transformations as tr
from glfwToolbox.opengl import clear_buffer


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# Global controller as communication with the callback function
controller = Controller()


# noinspection PyUnusedLocal,PyUnusedLocal,PyShadowingNames
def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon
    elif key == glfw.KEY_ESCAPE:
        sys.exit()
    else:
        print('Unknown key')


if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Cube with texture", None, None)

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

    # Creating shapes on GPU memory
    gpuTextureCube = es.to_gpu_shape(shapes.create_texture_cube('example_data/bricks.jpg'), GL_REPEAT, GL_LINEAR)
    gpuAxis = es.to_gpu_shape(shapes.create_axis(100))

    # Create objects
    obj_cube = AdvancedGPUShape(gpuTextureCube, shader=textureShaderProgram)
    obj_axis = AdvancedGPUShape(gpuAxis, shader=colorShaderProgram, mode=GL_LINES)

    # Create projection and view matrix
    projection = tr.ortho(-1, 1, -1, 1, 0.1, 100)
    view = tr.look_at(
        np.array([10, 10, 5]),
        np.array([0, 0, 0]),
        np.array([0, 0, 1])
    )

    # Mainloop
    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        clear_buffer()

        theta = glfw.get_time()
        axis = np.array([1, -1, 1])
        axis = axis / np.linalg.norm(axis)
        obj_cube.apply_temporal_transform(tr.rotation_a(theta, axis))

        # Draw objects
        obj_axis.draw(view, projection)
        obj_cube.draw(view, projection)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
