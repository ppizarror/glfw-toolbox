# coding=utf-8
"""
EXAMPLE
Creates a 3D cube.

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
import glfwToolbox.transformations as tr
import glfwToolbox.shapes as shapes
import glfwToolbox.easy_shaders as es
from glfwToolbox.advanced_shapes import AdvancedGPUShape

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
INT_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True


# We will use the global controller as communication with the callback function
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

    # Create window
    width = 600
    height = 600
    window = glfw.create_window(width, height, 'Simple Cube - Modern OpenGL', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Create shader
    colorShaderProgram = es.SimpleTransformShaderProgram()

    # Creating shapes on GPU memory
    gpuCube = es.to_gpu_shape(shapes.create_rainbow_cube())
    cube = AdvancedGPUShape(gpuCube, shader=colorShaderProgram)

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

        theta = glfw.get_time()
        Rx = tr.rotation_x(np.pi / 3)
        Ry = tr.rotation_y(theta)
        transform = np.matmul(Rx, Ry)

        # Drawing the Cube
        cube.apply_temporal_transform(transform)
        cube.draw(transform)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
