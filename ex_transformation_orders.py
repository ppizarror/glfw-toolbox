# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
Playing with the matrix multiplications order
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations2 as tr2
import basic_shapes as bs
import easy_shaders as es

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
INT_BYTES = 4

# Mode
SH_TRANSFORM            = 0
SH_TRANSFORM_TRANSPOSED = 1
SH_MVP                  = 2
SH_MVP_TRANSPOSED       = 3

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.mode = SH_TRANSFORM


# we will use the global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_1:
        print("Using Simple Transform Shader Program")
        controller.mode = SH_TRANSFORM

    elif key == glfw.KEY_2:
        print("Using Simple Transform Shader Program with transposed matrices")
        controller.mode = SH_TRANSFORM_TRANSPOSED
    
    elif key == glfw.KEY_3:
        print("Using Simple Model View Projection Shader Program")
        controller.mode = SH_MVP

    elif key == glfw.KEY_4:
        print("Using Simple Model View Projection Shader Program with transposed matrices")
        controller.mode = SH_MVP_TRANSPOSED

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

    window = glfw.create_window(width, height, "Cube", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
    transformPipeline = es.SimpleTransformShaderProgram()
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuCube = es.toGPUShape(bs.createRainbowCube())
    gpuAxis = es.toGPUShape(bs.createAxis(3))

    t0 = glfw.get_time()
    camera_theta = np.pi/4

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta += 2* dt

        camX = 10 * np.sin(camera_theta)
        camY = 10 * np.cos(camera_theta)

        view = tr2.lookAt(
            np.array([camX,camY,5]),
            np.array([0,0,0]),
            np.array([0,0,1])
        )

        axis = np.array([1,-1,1])
        axis = axis / np.linalg.norm(axis)
        theta = glfw.get_time()

        model_rotation = tr2.rotationA(theta, axis)
        model_traslation = tr2.translate(0.2, 0, 0)

        projection = tr2.ortho(-1, 1, -1, 1, 0.1, 100)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if controller.mode == SH_TRANSFORM:
            # Total transformation is computed in the CPU

            glUseProgram(transformPipeline.shaderProgram)

            cubeTransform = tr2.matmul([projection, view, model_traslation, model_rotation])
            axisTransform = tr2.matmul([projection, view])

            glUniformMatrix4fv(glGetUniformLocation(transformPipeline.shaderProgram, "transform"), 1, GL_TRUE, cubeTransform)
            transformPipeline.drawShape(gpuCube)

            glUniformMatrix4fv(glGetUniformLocation(transformPipeline.shaderProgram, "transform"), 1, GL_TRUE, axisTransform)
            transformPipeline.drawShape(gpuAxis, GL_LINES)

        elif controller.mode == SH_TRANSFORM_TRANSPOSED:
            # Total transformation is computed in the CPU, using trasposed matrices

            glUseProgram(transformPipeline.shaderProgram)

            cubeTransformT = tr2.matmul([model_rotation.T, model_traslation.T, view.T, projection.T])
            axisTransformT = tr2.matmul([view.T, projection.T])

            glUniformMatrix4fv(glGetUniformLocation(transformPipeline.shaderProgram, "transform"), 1, GL_FALSE, cubeTransformT)
            transformPipeline.drawShape(gpuCube)

            glUniformMatrix4fv(glGetUniformLocation(transformPipeline.shaderProgram, "transform"), 1, GL_FALSE, axisTransformT)
            transformPipeline.drawShape(gpuAxis, GL_LINES)

        elif controller.mode == SH_MVP:
            # Total transformation is computed in the GPU

            glUseProgram(mvpPipeline.shaderProgram)

            model = np.matmul(model_traslation, model_rotation)

            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, model)
            mvpPipeline.drawShape(gpuCube)

            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr2.identity())
            mvpPipeline.drawShape(gpuAxis, GL_LINES)

        elif controller.mode == SH_MVP_TRANSPOSED:
            # Total transformation is computed in the GPU

            glUseProgram(mvpPipeline.shaderProgram)

            modelT = np.matmul(model_rotation.T, model_traslation.T)

            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_FALSE, projection.T)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_FALSE, view.T)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_FALSE, modelT)
            mvpPipeline.drawShape(gpuCube)

            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_FALSE, projection.T)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_FALSE, view.T)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_FALSE, tr2.identity())
            mvpPipeline.drawShape(gpuAxis, GL_LINES)

        else:
            print("Invalid Mode")
            raise Exception()

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
