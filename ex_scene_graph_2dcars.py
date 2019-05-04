# coding=utf-8
"""
EXAMPLE-SCENE-GRAPH-2D-CARS
Drawing many cars in 2D using scene_graph.

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
import glfwToolbox.scene_graph as sg
import glfwToolbox.easy_shaders as es


# noinspection PyUnusedLocal,PyShadowingNames
def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    if key == glfw.KEY_ESCAPE:
        sys.exit()
    else:
        print('Unknown key')


def create_car():
    """
    Create car object.

    :return:
    """

    gpu_black_quad = es.to_gpu_shape(shapes.create_color_quad(0, 0, 0))
    gpu_red_quad = es.to_gpu_shape(shapes.create_color_quad(1, 0, 0))

    # Cheating a single wheel
    wheel = sg.SceneGraphNode('wheel')
    wheel.transform = tr.uniform_scale(0.2)
    wheel.childs += [gpu_black_quad]

    wheel_rotation = sg.SceneGraphNode('wheel_rotation')
    wheel_rotation.childs += [wheel]

    # Instanciating 2 wheels, for the front and back parts
    front_wheel = sg.SceneGraphNode('front_wheel')
    front_wheel.transform = tr.translate(0.3, -0.3, 0)
    front_wheel.childs += [wheel_rotation]

    back_wheel = sg.SceneGraphNode('back_wheel')
    back_wheel.transform = tr.translate(-0.3, -0.3, 0)
    back_wheel.childs += [wheel_rotation]

    # Creating the chasis of the car
    chasis = sg.SceneGraphNode('chasis')
    chasis.transform = tr.scale(1, 0.5, 1)
    chasis.childs += [gpu_red_quad]

    car = sg.SceneGraphNode('car')
    car.childs += [chasis]
    car.childs += [front_wheel]
    car.childs += [back_wheel]

    traslated_car = sg.SceneGraphNode('traslated_car')
    traslated_car.transform = tr.translate(0, 0.3, 0)
    traslated_car.childs += [car]

    return traslated_car


def create_cars(n):
    """
    Create cars.

    :param n: Number of cars
    :return:
    """

    # First we scale a car
    scaled_car = sg.SceneGraphNode('traslated_car')
    scaled_car.transform = tr.uniform_scale(0.15)
    scaled_car.childs += [create_car()]  # Re-using the previous function

    _cars = sg.SceneGraphNode('cars')

    base_name = 'scaled_car'
    for i in range(n):
        # A new node is only locating a scaled_car in the scene depending on index i
        new_node = sg.SceneGraphNode(base_name + str(i))
        new_node.transform = tr.translate(0.4 * i - 0.9, 0.9 - 0.4 * i, 0)
        new_node.childs += [scaled_car]

        # Now this car is added to the 'cars' scene graph
        _cars.childs += [new_node]

    return _cars


if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, '2D Cars via scene graph', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Creating shapes on GPU memory
    cars = create_cars(5)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    projection = tr.ortho(-1, 1, -1, 1, 0.1, 10)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'projection'), 1, GL_TRUE, projection)

    view = tr.look_at(
        np.array([0, 0, 2]),
        np.array([0, 0, 0]),
        np.array([0, 1, 0])
    )
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'view'), 1, GL_TRUE, view)

    # Mainloop
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Modifying only a specific node in the scene graph
        wheelRotationNode = sg.find_node(cars, 'wheel_rotation')
        theta = -10 * glfw.get_time()
        wheelRotationNode.transform = tr.rotation_z(theta)

        # Modifying only car 3
        car3 = sg.find_node(cars, 'scaled_car3')
        car3.transform = tr.translate(0.3, 0.5 * np.sin(0.1 * theta), 0)

        # Uncomment to see the position of scaledCar_3, it will fill your terminal
        # print('car3_position =', sg.find_position(cars, 'scaled_car3'))

        # Drawing the Car
        sg.draw_scene_graph_node(cars, pipeline)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
