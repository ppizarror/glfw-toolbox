# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
Interactions with keyboard and mouse via GLFW/python

More information at:
https://www.glfw.org/docs/latest/input_guide.html

How to convert GLFW/C calls to GLFW/python
https://pypi.org/project/glfw/
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import transformations as tr
import sys


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


def on_key(window, key, scancode, action, mods):

    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            sys.exit()


def cursor_pos_callback(window, x, y):
    global controller
    controller.mousePos = (x,y)


def mouse_button_callback(window, button, action, mods):

    global controller

    """
    glfw.MOUSE_BUTTON_1: left click
    glfw.MOUSE_BUTTON_2: right click
    glfw.MOUSE_BUTTON_3: scroll click
    """

    if (action == glfw.PRESS or action == glfw.REPEAT):
        if (button == glfw.MOUSE_BUTTON_1):
            controller.leftClickOn = True
            print("Mouse click - button 1")

        if (button == glfw.MOUSE_BUTTON_2):
            print("Mouse click - button 2:", glfw.get_cursor_pos(window))

        if (button == glfw.MOUSE_BUTTON_3):
            print("Mouse click - button 3")

    elif (action ==glfw.RELEASE):
        if (button == glfw.MOUSE_BUTTON_1):
            controller.leftClickOn = False


def scroll_callback(window, x, y):

    print("Mouse scroll:", x, y)


def basicShaderProgram():

    # Defining shaders for our pipeline
    vertex_shader = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    uniform mat4 transform;

    void main()
    {
        fragColor = color;
        gl_Position = transform * vec4(position, 1.0f);
    }
    """

    fragment_shader = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor, 1.0f);
    }
    """

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    return shaderProgram


# A simple class container to reference a shape on GPU memory
class GPUShape:
    def __init__(self):
        self.vao = 0
        self.vbo = 0
        self.ebo = 0
        self.size = 0


def drawShape(shaderProgram, shape, transform):

    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # updating the new transform attribute
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_FALSE, transform)

    # Describing how the data is stored in the VBO
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    
    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # This line tells the active shader program to render the active element buffer with the given size
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)


def createQuad(r, g, b):

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape    
    vertexData = np.array([
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r, g, b,
         0.5,  0.5, 0.0,  r, g, b,
        -0.5,  0.5, 0.0,  r, g, b
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Handling mouse events", None, None)

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


    # Using the simple shader program from basic_shapes and
    # telling OpenGL to use our shader program
    shaderProgram = basicShaderProgram()
    glUseProgram(shaderProgram)


    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Creating shapes on GPU memory
    blueQuad = createQuad(0,0,1)
    redQuad = createQuad(1,0,0)
    yellowQuad = createQuad(1,1,0)
    greenQuad = createQuad(0,1,0)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    t0 = glfw.get_time()

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
        drawShape(shaderProgram, redQuad, tr.matmul([
            tr.uniformScale(0.5),
            tr.translate(0.5, 0.0, 0.0),
            tr.rotationZ(controller.theta)
        ]))

        # Getting the mouse location in opengl coordinates
        mousePosX = 2 * (controller.mousePos[0] - width/2) / width
        mousePosY = 2 * (height/2 - controller.mousePos[1]) / height
 
        drawShape(shaderProgram, greenQuad, np.matmul(
            tr.uniformScale(0.3),
            tr.translate(mousePosX, mousePosY, 0)
        ))

        # This is another way to work with keyboard inputs
        # Here we request the state of a given key
        if (glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS):
            drawShape(shaderProgram, blueQuad, np.matmul(
                tr.uniformScale(0.2),
                tr.translate(-0.6, 0.4, 0.0)
            ))

        # All "non-pressed" keys are in release state
        if (glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.RELEASE):
            drawShape(shaderProgram, yellowQuad, np.matmul(
                tr.uniformScale(0.2),
                tr.translate(-0.6, 0.6, 0.0)
            ))

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()