# coding=utf-8
"""
ADVANCED SHAPES
Advenced shapes definition

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

# Library imports
from glfwToolbox.easy_shaders import GPUShape as _GPUShape
from OpenGL.GL import GL_POLYGON as _GL_POLYGON
from OpenGL.GL import glUniformMatrix4fv as _glUniformMatrix4fv
from OpenGL.GL import glGetUniformLocation as _glGetUniformLocation
from OpenGL.GL import GL_TRUE as _GL_TRUE
from OpenGL.GL import GL_TRIANGLES as _GL_TRIANGLES
from OpenGL.GL import glUseProgram as _glUseProgram
import glfwToolbox.transformations as _tr


class AdvancedGPUShape(object):
    def __init__(self, shapes, model=_tr.identity(), enabled=True, shader=None, mode=None):
        """
        Constructor.

        :param shapes: List or GPUShape object
        :param model: Basic model transformation matrix
        :param enabled: Indicates if the shape is enabled or not
        :param shader: Shader program
        """
        if not isinstance(shapes, list):
            shapes = [shapes]
        for i in range(len(shapes)):
            if not isinstance(shapes[i], _GPUShape):
                raise Exception('Object {0} of shapes list is not GPUShape instance'.format(i))
        if mode is None:
            mode = _GL_TRIANGLES

        self._shapes = shapes
        self._model = model
        self._modelPrev = None
        self._enabled = enabled
        self._shader = shader
        self._drawMode = mode

    def set_shader(self, shader):
        """
        Set shader.

        :param shader:
        :return:
        """
        self._shader = shader

    def translate(self, tx=0, ty=0, tz=0):
        """
        Translate model.

        :param tx:
        :param ty:
        :param tz:
        :return:
        """
        self._model = _tr.matmul([_tr.translate(tx, ty, tz), self._model])

    def scale(self, sx=1, sy=1, sz=1):
        """
        Scale model.

        :param sx:
        :param sy:
        :param sz:
        :return:
        """
        self._model = _tr.matmul([_tr.scale(sx, sy, sz), self._model])

    def uniform_scale(self, s=1):
        """
        Uniform scale model.

        :param s:
        :return:
        """
        self._model = _tr.matmul([_tr.uniform_scale(s), self._model])

    def rotation_x(self, theta=0):
        """
        Rotate model.

        :param theta:
        :return:
        """
        self._model = _tr.matmul([_tr.rotation_x(theta), self._model])

    def rotation_y(self, theta=0):
        """
        Rotate model.

        :param theta:
        :return:
        """
        self._model = _tr.matmul([_tr.rotation_y(theta), self._model])

    def rotation_z(self, theta=0):
        """
        Rotate model.

        :param theta:
        :return:
        """
        self._model = _tr.matmul([_tr.rotation_z(theta), self._model])

    def rotation_a(self, theta, axis):
        """
        Rotate model.

        :param theta:
        :param axis:
        :return:
        """
        self._model = _tr.matmul([_tr.rotation_a(theta, axis), self._model])

    def shearing(self, xy=0, yx=0, xz=0, zx=0, yz=0, zy=0):
        """
        Apply shear to model.

        :param xy:
        :param yx:
        :param xz:
        :param zx:
        :param yz:
        :param zy:
        :return:
        """
        self._model = _tr.matmul([_tr.shearing(xy, yx, xz, zx, yz, zy), self._model])

    def apply_temporal_transform(self, t):
        """
        Apply temporal transform to model until drawing.

        :param t:
        :return:
        """
        self._modelPrev = self._model
        self._model = _tr.matmul([t, self._model])

    def draw(self, view=None, projection=None, mode=None, shader=None, usemodel=True):
        """
        Draw model.

        :param view:
        :param projection:
        :param mode:
        :param shader:
        :param usemodel:
        :return:
        """
        if not self._enabled:
            return
        if mode is None:
            if self._drawMode is None:
                mode = _GL_POLYGON
            else:
                mode = self._drawMode
        if shader is None:
            if self._shader is None:
                raise Exception('MergedShape shader is not set')
            shader = self._shader
        _glUseProgram(shader.shaderProgram)
        if usemodel and shader.keyModel != '':
            _glUniformMatrix4fv(_glGetUniformLocation(shader.shaderProgram, shader.keyModel), 1, _GL_TRUE, self._model)
        if projection is not None and shader.keyProjection != '':
            _glUniformMatrix4fv(_glGetUniformLocation(shader.shaderProgram, shader.keyProjection), 1, _GL_TRUE,
                                projection)
        if view is not None and shader.keyView != '':
            _glUniformMatrix4fv(_glGetUniformLocation(shader.shaderProgram, shader.keyView), 1, _GL_TRUE, view)
        for i in self._shapes:
            shader.draw_shape(i, mode)
        if self._modelPrev is not None:
            self._model = self._modelPrev
            self._modelPrev = None

    def disable(self):
        """
        Disable the model.

        :return:
        """
        self._enabled = False

    def enable(self):
        """
        Enable the model.

        :return:
        """
        self._enabled = True

    def clone(self):
        """
        Clone the model.

        :return:
        """
        return AdvancedGPUShape(self._shapes.copy(), self._model, enabled=self._enabled, shader=self._shader)
