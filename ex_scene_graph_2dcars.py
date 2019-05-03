# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
Drawing many cars in 2D using scene_graph2
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations2 as tr2
import basic_shapes as bs
import scene_graph2 as sg
import easy_shaders as es


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


def createCar():

    gpuBlackQuad = es.toGPUShape(bs.createColorQuad(0,0,0))
    gpuRedQuad = es.toGPUShape(bs.createColorQuad(1,0,0))
    
    # Cheating a single wheel
    wheel = sg.SceneGraphNode("wheel")
    wheel.transform = tr2.uniformScale(0.2)
    wheel.childs += [gpuBlackQuad]

    wheelRotation = sg.SceneGraphNode("wheelRotation")
    wheelRotation.childs += [wheel]

    # Instanciating 2 wheels, for the front and back parts
    frontWheel = sg.SceneGraphNode("frontWheel")
    frontWheel.transform = tr2.translate(0.3,-0.3,0)
    frontWheel.childs += [wheelRotation]

    backWheel = sg.SceneGraphNode("backWheel")
    backWheel.transform = tr2.translate(-0.3,-0.3,0)
    backWheel.childs += [wheelRotation]
    
    # Creating the chasis of the car
    chasis = sg.SceneGraphNode("chasis")
    chasis.transform = tr2.scale(1,0.5,1)
    chasis.childs += [gpuRedQuad]

    car = sg.SceneGraphNode("car")
    car.childs += [chasis]
    car.childs += [frontWheel]
    car.childs += [backWheel]

    traslatedCar = sg.SceneGraphNode("traslatedCar")
    traslatedCar.transform = tr2.translate(0,0.3,0)
    traslatedCar.childs += [car]

    return traslatedCar

def createCars(N):

    # First we scale a car
    scaledCar = sg.SceneGraphNode("traslatedCar")
    scaledCar.transform = tr2.uniformScale(0.15)
    scaledCar.childs += [createCar()] # Re-using the previous function

    cars = sg.SceneGraphNode("cars")

    baseName = "scaledCar"
    for i in range(N):
        # A new node is only locating a scaledCar in the scene depending on index i
        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr2.translate(0.4 * i - 0.9, 0.9 - 0.4 * i, 0)
        newNode.childs += [scaledCar]

        # Now this car is added to the 'cars' scene graph
        cars.childs += [newNode]

    return cars


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Cars via scene graph 2", None, None)

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
    cars = createCars(5)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    projection = tr2.ortho(-1, 1, -1, 1, 0.1, 10)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    view = tr2.lookAt(
            np.array([0,0,2]),
            np.array([0,0,0]),
            np.array([0,1,0])
        )
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Modifying only a specific node in the scene graph
        wheelRotationNode = sg.findNode(cars, "wheelRotation")
        theta = -10 * glfw.get_time()
        wheelRotationNode.transform = tr2.rotationZ(theta)

        # Modifying only car 3
        car3 = sg.findNode(cars, "scaledCar3")
        car3.transform = tr2.translate(0.3, 0.5 * np.sin(0.1 * theta), 0)

        # Uncomment to see the position of scaledCar_3, it will fill your terminal
        #print("car3Position =", sg.findPosition(cars, "scaledCar3"))

        # Drawing the Car
        sg.drawSceneGraphNode(cars, pipeline)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()