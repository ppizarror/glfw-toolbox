# coding=utf-8
"""
OPENGL
Basic opengl initialization.

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

# Library imports
from __future__ import print_function

# noinspection PyPep8Naming
import OpenGL.GL as _gl

# Constants
_OPENGL_DEFAULT_AMBIENT_COLOR = [0.2, 0.2, 0.2, 1.0]
_OPENGL_DEFAULT_BGCOLOR = [0.0, 0.0, 0.0, 1.0]
_OPENGL_DEFAULT_BGDEPTH = 1.0
_OPENGL_DEFAULT_CONSTANT_ATTENUATION = 1.0
_OPENGL_DEFAULT_DIFFUSE_COLOR = [0.8, 0.8, 0.8, 1.0]
_OPENGL_DEFAULT_FOV = 60
_OPENGL_DEFAULT_LINEAR_ATTENUATION = 0.0
_OPENGL_DEFAULT_QUADRATIC_ATTENUATION = 0.0
_OPENGL_DEFAULT_SPECULAR_COLOR = [1.0, 1.0, 1.0, 1.0]
_OPENGL_DEFAULT_SPOT_CUTOFF = 180.0
_OPENGL_DEFAULT_SPOT_DIRECTION = [0.0, 0.0, -1.0, 1.0]
_OPENGL_DEFAULT_SPOT_EXPONENT = 1.0
_OPENGL_OPENGL_CONFIGS = [False]
_OPENGL_SPOT_DIRECTION_ALL = [1.0, 1.0, 1.0, 1.0]


def init_gl(antialiasing=True, bgcolor=None, bgdepth=_OPENGL_DEFAULT_BGDEPTH, depth=True, lighting=False,
            materialcolor=True, normalized=True, numlights=0, perspectivecorr=False, polyfonfillmode=True, smooth=True,
            surffill=True, textures=False, transparency=False, verbose=False, version=False):
    """
    Inits OpenGL.

    :param antialiasing: Enables antialiasing
    :param bgcolor: Background color
    :param bgdepth: Background depth value
    :param depth: Enables depth
    :param lighting: Enables light
    :param materialcolor: Enables material color
    :param normalized: Enables normalized
    :param numlights: Number of lights
    :param perspectivecorr: Enables perspective correction
    :param polyfonfillmode: Enabled polygon fill
    :param smooth: Enables smooth
    :param surffill: Enables surface fill
    :param textures: Enables textures
    :param transparency: Enables transparency
    :param verbose: Enable verbose
    :param version: Show OpenGL version
    :type antialiasing: bool
    :type bgcolor: list
    :type bgdepth: float, int
    :type depth: bool
    :type lighting: bool
    :type materialcolor: bool
    :type normalized: bool
    :type numlights: int
    :type perspectivecorr: bool
    :type polyfonfillmode: bool
    :type smooth: bool
    :type surffill: bool
    :type textures: bool
    :type transparency: bool
    :type verbose: bool
    :type version: bool
    """

    if bgcolor is None:
        bgcolor = _OPENGL_DEFAULT_BGCOLOR

    def log(msg):
        """
        Print a message on screen.

        :param msg: Message
        :type msg: basestring
        """
        if verbose:
            print('[GL] {0}'.format(msg))

    def log_info(msg):
        """
        Print information on screen
        :param msg:
        :return:
        """
        print('[GL-INFO] {0}'.format(msg))

    log('Init OPENGL')

    # Print OpenGL version
    if version:
        log_info('OpenGL version {0}'.format(_gl.glGetString(_gl.GL_VERSION)))
        log_info('GPU {0}'.format(_gl.glGetString(_gl.GL_VENDOR)))
        log_info('Renderer {0}'.format(_gl.glGetString(_gl.GL_RENDERER)))
        log_info('SLSL version {0}'.format(_gl.glGetString(_gl.GL_SHADING_LANGUAGE_VERSION)))
        log_info('Extensions {0}'.format(_gl.glGetString(_gl.GL_EXTENSIONS)))

    # Set background clear color
    if bgcolor is not None:
        log('Clear color set: {0}'.format(bgcolor))
        _gl.glClearColor(*bgcolor)
    else:
        log('Clear color set default')
        _gl.glClearColor(*_OPENGL_DEFAULT_BGCOLOR)

    # Set clear depth color
    if bgdepth is not None:
        log('Clear depth color set: {0}'.format(bgdepth))
        _gl.glClearDepth(bgdepth)
    else:
        log('Clear depth color set default')
        _gl.glClearDepth(_OPENGL_DEFAULT_BGDEPTH)

    # Enable transparency
    if transparency:
        log('Transparency enabled')
        _gl.glEnable(_gl.GL_BLEND)
        _gl.glBlendFunc(_gl.GL_SRC_ALPHA, _gl.GL_ONE_MINUS_SRC_ALPHA)

    # Smooth
    if smooth:
        log('Enable SMOOTH shade model')
        _gl.glShadeModel(_gl.GL_SMOOTH)

    # Depth test
    if depth:
        log('Enable depth test')
        _gl.glEnable(_gl.GL_DEPTH_TEST)
        _gl.glDepthFunc(_gl.GL_LEQUAL)

    # Antialiasing
    if antialiasing:
        log('Antialiasing enabled')
        _gl.glHint(_gl.GL_POLYGON_SMOOTH_HINT, _gl.GL_NICEST)

    # Enabled normalized normal
    if normalized:
        log('Normalized normal enabled')
        _gl.glEnable(_gl.GL_NORMALIZE)

    # Enable offset fill
    if surffill:
        log('Enabled polygon offset fill')
        _gl.glEnable(_gl.GL_POLYGON_OFFSET_FILL)

    # Enable lighting
    if lighting:
        log('Enable lighting')
        _gl.glEnable(_gl.GL_LIGHTING)
        if numlights > 0:
            for light in range(int(numlights)):
                log('Light {0} enabled'.format(light))
                eval('_gl.glEnable(_gl.GL_LIGHT{0})'.format(light))
        _OPENGL_OPENGL_CONFIGS[0] = True

    # Polygon fill mode
    if polyfonfillmode:
        log('Enabled polygoon fill by both sides')
        _gl.glPolygonMode(_gl.GL_FRONT_AND_BACK, _gl.GL_FILL)

    # Enable color material
    if materialcolor:
        log('Enabled color material')
        _gl.glEnable(_gl.GL_COLOR_MATERIAL)

    # Enable perspective correction
    if perspectivecorr:
        log('Enabled pespective correction')
        _gl.glHint(_gl.GL_PERSPECTIVE_CORRECTION_HINT, _gl.GL_NICEST)

    # Enable textures
    if textures:
        log('Textures enabled')
        _gl.glEnable(_gl.GL_TEXTURE_2D)
        _gl.glLightModeli(_gl.GL_LIGHT_MODEL_COLOR_CONTROL, _gl.GL_SEPARATE_SPECULAR_COLOR)

    log('OpenGL init finished')


def clear_buffer():
    """
    Clear buffer
    :return:
    """
    _gl.glClear(_gl.GL_COLOR_BUFFER_BIT | _gl.GL_DEPTH_BUFFER_BIT)
