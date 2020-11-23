# coding=utf-8
"""
EXAMPLE-TEXTURE-BOO
Texture example.

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

import glfw
from OpenGL.GL import *
import numpy as np
import sys

import glfwToolbox.transformations as tr
import glfwToolbox.shapes as shapes
import glfwToolbox.easy_shaders as es
from glfwToolbox.advanced_shapes import AdvancedGPUShape


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

    window = glfw.create_window(width, height, 'Boo!', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # A simple shader program with position and texture coordinates as inputs.
    pipeline = es.SimpleTextureTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Creating shapes on GPU memory
    gpuBoo = es.to_gpu_shape(shapes.create_texture_quad('example_data/boo.png'), GL_REPEAT, GL_NEAREST)
    gpuQuestionBox = es.to_gpu_shape(shapes.create_texture_quad('example_data/question_box.png', 10, 1), GL_REPEAT,
                                     GL_NEAREST)

    # Create objets
    obj_boo = AdvancedGPUShape(gpuBoo, shader=pipeline)
    obj_question = AdvancedGPUShape(gpuQuestionBox, shader=pipeline)

    # Apply object transform
    obj_question.scale(sx=-2, sy=0.2)
    obj_question.translate(ty=-0.8)

    # Mainloop
    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()

        # OpenGL polygon mode
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        theta = glfw.get_time()
        tx = 0.7 * np.sin(0.5 * theta)
        ty = 0.2 * np.sin(5 * theta)

        # Derivative of tx give us the direction
        dtx = 0.7 * 0.5 * np.cos(0.5 * theta)
        if dtx > 0:
            reflex = tr.scale(-1, 1, 1)
        else:
            reflex = tr.identity()

        # Create booObj transformation
        booT = tr.matmul([tr.translate(tx, ty, 0), tr.scale(0.5, 0.5, 1.0), reflex])
        obj_boo.apply_temporal_transform(booT)

        # Draw shapes
        obj_boo.draw()
        obj_question.draw()

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
