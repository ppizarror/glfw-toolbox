# coding=utf-8
"""
EXAMPLE-LIGHTING-TEXTURE
Showing lighting effects over a textured object: Flat, Gauraud and Phong

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
from glfwToolbox.lights import Light

LIGHT_FLAT = 0
LIGHT_GOURAUD = 1
LIGHT_PHONG = 2


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.lightingModel = LIGHT_PHONG


# We will use the global controller as communication with the callback function
controller = Controller()


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyShadowingNames
def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon
    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis
    elif key == glfw.KEY_Q:
        controller.lightingModel = LIGHT_FLAT
    elif key == glfw.KEY_W:
        controller.lightingModel = LIGHT_GOURAUD
    elif key == glfw.KEY_E:
        controller.lightingModel = LIGHT_PHONG
    elif key == glfw.KEY_ESCAPE:
        sys.exit()


if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, 'Lighting + Textures demo', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Different shader programs for different lighting strategies
    textureFlatPipeline = es.SimpleTextureFlatShaderProgram()
    textureGouraudPipeline = es.SimpleTextureGouraudShaderProgram()
    texturePhongPipeline = es.SimpleTexturePhongShaderProgram()

    # This shader program does not consider lighting
    colorPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.to_gpu_shape(shapes.create_axis(4))
    gpuTextureCube = es.to_gpu_shape(shapes.create_texture_normals_cube('example_data/bricks.jpg'), GL_REPEAT,
                                     GL_LINEAR)

    t0 = glfw.get_time()
    camera_theta = np.pi / 4

    # Create light
    obj_light = Light(position=[5, 5, 5], color=[1, 1, 1])

    # Mainloop
    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            camera_theta -= 2 * dt

        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            camera_theta += 2 * dt

        projection = tr.perspective(45, float(width) / float(height), 0.1, 100)

        camX = 3 * np.sin(camera_theta)
        camY = 3 * np.cos(camera_theta)

        viewPos = np.array([camX, camY, 2])

        view = tr.look_at(
            viewPos,
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )
        model = tr.identity()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # The axis is drawn without lighting effects
        if controller.showAxis:
            glUseProgram(colorPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(colorPipeline.shaderProgram, 'projection'), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(colorPipeline.shaderProgram, 'view'), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(colorPipeline.shaderProgram, 'model'), 1, GL_TRUE, tr.identity())
            colorPipeline.draw_shape(gpuAxis, GL_LINES)

        # Selecting the lighting shader program
        if controller.lightingModel == LIGHT_FLAT:
            lightingPipeline = textureFlatPipeline
        elif controller.lightingModel == LIGHT_GOURAUD:
            lightingPipeline = textureGouraudPipeline
        elif controller.lightingModel == LIGHT_PHONG:
            lightingPipeline = texturePhongPipeline
        else:
            raise Exception()

        obj_light.set_shader(lightingPipeline)
        glUseProgram(lightingPipeline.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, 'projection'), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, 'view'), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, 'model'), 1, GL_TRUE, model)

        # Setting all uniform shader variables
        obj_light.place()

        # Drawing
        lightingPipeline.draw_shape(gpuTextureCube)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
