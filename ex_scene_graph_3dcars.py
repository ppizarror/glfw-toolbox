# coding=utf-8
"""
EXAMPLE-SCENE-GRAPH-3D-CARS
Drawing 3D cars via scene graph.

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

import glfwToolbox.transformations as tr2
import glfwToolbox.shapes as bs
import glfwToolbox.scene_graph as sg
import glfwToolbox.easy_shaders as es


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True


# We will use the global controller as communication with the callback function
controller = Controller()


# noinspection PyUnusedLocal,PyShadowingNames
def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


def create_car(r, g, b):
    """
    Create car model.

    :param r:
    :param g:
    :param b:
    :return:
    """
    gpu_black_quad = es.to_gpu_shape(bs.create_color_cube(0, 0, 0))
    gpu_chasis_quad = es.to_gpu_shape(bs.create_color_cube(r, g, b))

    # Cheating a single wheel
    wheel = sg.SceneGraphNode('wheel')
    wheel.transform = tr2.scale(0.2, 0.8, 0.2)
    wheel.childs += [gpu_black_quad]

    wheel_rotation = sg.SceneGraphNode('wheel_rotation')
    wheel_rotation.childs += [wheel]

    # Instanciating 2 wheels, for the front and back parts
    front_wheel = sg.SceneGraphNode('front_wheel')
    front_wheel.transform = tr2.translate(0.3, 0, -0.3)
    front_wheel.childs += [wheel_rotation]

    back_wheel = sg.SceneGraphNode('back_wheel')
    back_wheel.transform = tr2.translate(-0.3, 0, -0.3)
    back_wheel.childs += [wheel_rotation]

    # Creating the chasis of the car
    chasis = sg.SceneGraphNode('chasis')
    chasis.transform = tr2.scale(1, 0.7, 0.5)
    chasis.childs += [gpu_chasis_quad]

    # All pieces together
    car = sg.SceneGraphNode('car')
    car.childs += [chasis]
    car.childs += [front_wheel]
    car.childs += [back_wheel]

    return car


if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, '3D cars via scene graph', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    mvcPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(mvcPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.to_gpu_shape(bs.create_axis(7))
    redCarNode = create_car(1, 0, 0)
    blueCarNode = create_car(0, 0, 1)

    blueCarNode.transform = np.matmul(tr2.rotation_z(-np.pi / 4), tr2.translate(3.0, 0, 0.5))

    # Using the same view and projection matrices in the whole application
    projection = tr2.perspective(45, float(width) / float(height), 0.1, 100)
    glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    view = tr2.look_at(
        np.array([5, 5, 7]),
        np.array([0, 0, 0]),
        np.array([0, 0, 1])
    )
    glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, 'view'), 1, GL_TRUE, view)

    # Mainloop
    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        if controller.showAxis:
            glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "model"), 1, GL_TRUE, tr2.identity())
            mvcPipeline.draw_shape(gpuAxis, GL_LINES)

        # Moving the red car and rotating its wheels
        redCarNode.transform = tr2.translate(3 * np.sin(glfw.get_time()), 0, 0.5)
        redWheelRotationNode = sg.find_node(redCarNode, 'wheel_rotation')
        redWheelRotationNode.transform = tr2.rotation_y(-10 * glfw.get_time())

        # Uncomment to print the red car position on every iteration
        # print(sg.find_position(redCarNode, 'car'))

        # Drawing the Car
        sg.draw_scene_graph_node(redCarNode, mvcPipeline)
        sg.draw_scene_graph_node(blueCarNode, mvcPipeline)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
