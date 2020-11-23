# coding=utf-8
"""
LIGHTS
Basic lights implementation.

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

from OpenGL.GL import glUseProgram as _glUseProgram
from OpenGL.GL import glUniform3f as _glUniform3f
from OpenGL.GL import glGetUniformLocation as _glGetUniformLocation
from OpenGL.GL import glUniform1ui as _glUniform1ui
from OpenGL.GL import glUniform1f as _glUniform1f


class Light(object):
    def __init__(self, position, color, shader=None, shininess=100, constant_attenuation=0.001, linear_attenuation=0.1,
                 qudratic_attenuation=0.01):
        """
        Constructor.

        :param shader: Shader class
        :param position: Light position
        :type position: list
        :param color: Color of the light
        :type color: list
        :param shininess: Shininess
        :type shininess: float
        :param constant_attenuation: Light constant attenuation
        :type constant_attenuation: float
        :param linear_attenuation: Light linear attenuation
        :type linear_attenuation: float
        :param qudratic_attenuation: Light quadratic attenuation
        :type qudratic_attenuation: float
        """
        assert isinstance(color, list), 'Color is not a list'
        assert len(color) == 3, 'Color must have 3 components'
        assert isinstance(position, list), 'Position is not a list'
        assert len(position) == 3, 'Position must have 3 components'
        self._shader = shader
        self._position = position
        self._color = color
        self._shininess = shininess
        self._cAtt = constant_attenuation
        self._lAtt = linear_attenuation
        self._qAtt = qudratic_attenuation
        self._enabled = True

    def move_position(self, dx=0, dy=0, dz=0):
        """
        Move light position.

        :param dx:
        :param dy:
        :param dz:
        :return:
        """
        self._position[0] += dx
        self._position[1] += dy
        self._position[2] += dz

    def set_position(self, x, y, z):
        """
        Set light position

        :param x:
        :param y:
        :param z:
        :return:
        """
        self._position[0] = x
        self._position[1] = y
        self._position[2] = z

    def change_color(self, r, g, b):
        """
        Change light color.

        :param r:
        :param g:
        :param b:
        :return:
        """
        self._color[0] = r
        self._color[1] = g
        self._color[2] = b

    def enable(self):
        """
        Enable light.

        :return:
        """
        self._enabled = True

    def disable(self):
        """
        Disable light.

        :return:
        """
        self._enabled = False

    def set_shader(self, shader):
        """
        Change the light shader.

        :param shader: Shader program
        :return:
        """
        self._shader = shader

    def place(self):
        """
        Place light on engine.

        :return:
        """
        if not self._enabled or self._shader is None:
            return
        _glUseProgram(self._shader.shaderProgram)
        _glUniform3f(_glGetUniformLocation(self._shader.shaderProgram, 'lightColor'),
                     self._color[0], self._color[1], self._color[2])
        _glUniform3f(_glGetUniformLocation(self._shader.shaderProgram, 'lightPos'),
                     self._position[0], self._position[1], self._position[2])
        _glUniform1ui(_glGetUniformLocation(self._shader.shaderProgram, 'shininess'), self._shininess)
        _glUniform1f(_glGetUniformLocation(self._shader.shaderProgram, 'constantAttenuation'), self._cAtt)
        _glUniform1f(_glGetUniformLocation(self._shader.shaderProgram, 'linearAttenuation'), self._lAtt)
        _glUniform1f(_glGetUniformLocation(self._shader.shaderProgram, 'quadraticAttenuation'), self._qAtt)
