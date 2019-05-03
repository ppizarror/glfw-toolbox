# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
Indirect color example
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import sys

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
INT_BYTES = 4

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Simple Triangle - Modern OpenGL", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Defining the triangle and its colors at each vertex
    #            positions        colors
    triangle = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                 0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                 0.0,  0.5, 0.0, 0.0, 0.0, 1.0]

    triangle = numpy.array(triangle, dtype = numpy.float32)

    # Defining shaders for our pipeline
    vertex_shader = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 newColor;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """

    fragment_shader = """
    #version 130
    in vec3 newColor;

    out vec4 outColor;
    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # Each shape must be attached to a Vertex Buffer Object (VBO)
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, len(triangle) * INT_BYTES, triangle, GL_STATIC_DRAW)

    # Setting up the location of the attributes position and color from the VBO
    # A vertex attribute has 3 integers for the position (each is 4 bytes),
    # and 3 numbers to represent the color (each is 4 bytes),
    # Henceforth, we have 3*4 + 3*4 = 24 bytes
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # It renders a scene using the active shader program (pipeline) and the active VBA (shapes)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
