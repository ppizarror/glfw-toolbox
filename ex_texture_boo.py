# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
Texture and transformations
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations2 as tr2
import basic_shapes as bs
import easy_shaders as es


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# global controller as communication with the callback function
controller = Controller()


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


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Boo!", None, None)

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
    gpuBoo = es.toGPUShape(bs.createTextureQuad("boo.png"), GL_REPEAT, GL_NEAREST)
    gpuQuestionBox = es.toGPUShape(bs.createTextureQuad("question_box.png",10,1), GL_REPEAT, GL_NEAREST)

    questionBoxTransform = np.matmul(tr2.translate(0, -0.8, 0), tr2.scale(-2, 0.2, 1))

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        theta = glfw.get_time()
        tx = 0.7 * np.sin(0.5 * theta)
        ty = 0.2 * np.sin(5 * theta)
    
        # derivative of tx give us the direction
        dtx = 0.7 * 0.5 * np.cos(0.5 * theta)
        if dtx > 0:
            reflex = tr2.scale(-1,1,1)
        else:
            reflex = tr2.identity()

        # Drawing the shapes
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
            tr2.matmul([
                tr2.translate(tx, ty, 0),
                tr2.scale(0.5, 0.5, 1.0),
                reflex]))
        pipeline.drawShape(gpuBoo)
        
        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, questionBoxTransform)
        pipeline.drawShape(gpuQuestionBox)


        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()