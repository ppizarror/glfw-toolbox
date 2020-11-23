# coding=utf-8
"""
MOUSE
Mouse events.

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

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
INT_BYTES = 4


# A class to control the application
class Controller:
    def __init__(self):
        self.leftClickOn = False
        self.theta = 0.0
        self.mousePos = (0.0, 0.0)


# we will use the global controller as communication with the callback function
controller = Controller()


# noinspection PyUnusedLocal,PyShadowingNames
def on_key(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            sys.exit()


# noinspection PyUnusedLocal,PyShadowingNames
def cursor_pos_callback(window, _x, _y):
    global controller
    controller.mousePos = (_x, _y)


# noinspection PyShadowingNames,PyUnusedLocal
def mouse_button_callback(window, button, action, mods):
    global controller

    """
    glfw.MOUSE_BUTTON_1: left click
    glfw.MOUSE_BUTTON_2: right click
    glfw.MOUSE_BUTTON_3: scroll click
    """

    if action == glfw.PRESS or action == glfw.REPEAT:
        if button == glfw.MOUSE_BUTTON_1:
            controller.leftClickOn = True
            print('Mouse click - button 1')
        if button == glfw.MOUSE_BUTTON_2:
            print('Mouse click - button 2:', glfw.get_cursor_pos(window))
        if button == glfw.MOUSE_BUTTON_3:
            print('Mouse click - button 3')
    elif action == glfw.RELEASE:
        if button == glfw.MOUSE_BUTTON_1:
            controller.leftClickOn = False


# noinspection PyUnusedLocal,PyShadowingNames
def scroll_callback(window, _x, _y):
    print('Mouse scroll:', _x, _y)


if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, 'Handling mouse events', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Connecting callback functions to handle mouse events:
    # - Cursor moving over the window
    # - Mouse buttons input
    # - Mouse scroll
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    # Create shader
    basicShader = es.SimpleTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Creating shapes on GPU memory
    blueQuad = shapes.create_color_quad(0, 0, 1)
    redQuad = shapes.create_color_quad(1, 0, 0)
    yellowQuad = shapes.create_color_quad(1, 1, 0)
    greenQuad = shapes.create_color_quad(0, 1, 0)

    # Create objects
    obj_quad_blue = AdvancedGPUShape(es.to_gpu_shape(blueQuad), shader=basicShader)
    obj_quad_red = AdvancedGPUShape(es.to_gpu_shape(redQuad), shader=basicShader)
    obj_quad_yellow = AdvancedGPUShape(es.to_gpu_shape(yellowQuad), shader=basicShader)
    obj_quad_green = AdvancedGPUShape(es.to_gpu_shape(greenQuad), shader=basicShader)

    # Apply permanent transforms
    obj_quad_red.translate(tx=0.5)
    obj_quad_red.uniform_scale(0.5)

    # Polyfon fill mode
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Get time
    t0 = glfw.get_time()

    # Mainloop
    while not glfw.window_should_close(window):

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # While left click is pressed, we have continous rotation movement
        if controller.leftClickOn:
            controller.theta += 4 * dt
            if controller.theta >= 2 * np.pi:
                controller.theta -= 2 * np.pi

        # Drawing the rotating red quad
        obj_quad_red.apply_temporal_transform(tr.rotation_z(controller.theta))
        obj_quad_red.draw()

        # Getting the mouse location in opengl coordinates
        mousePosX = 2 * (controller.mousePos[0] - width / 2) / width
        mousePosY = 2 * (height / 2 - controller.mousePos[1]) / height

        # Draw green quad
        obj_quad_green.apply_temporal_transform(np.matmul(
            tr.uniform_scale(0.5),
            tr.translate(mousePosX, mousePosY, 0)
        ))
        obj_quad_green.draw()

        # This is another way to work with keyboard inputs
        # Here we request the state of a given key
        if glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS:
            obj_quad_blue.apply_temporal_transform(np.matmul(
                tr.uniform_scale(0.2),
                tr.translate(-0.6, 0.4, 0.0)
            ))
            obj_quad_blue.draw()

        # All "non-pressed" keys are in release state
        if glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.RELEASE:
            obj_quad_yellow.apply_temporal_transform(np.matmul(
                tr.uniform_scale(0.2),
                tr.translate(-0.6, 0.6, 0.0)
            ))
            obj_quad_yellow.draw()

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
