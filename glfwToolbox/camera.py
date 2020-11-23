# coding=utf-8
"""
CAMERA
Camera implementations.

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
from glfwToolbox.mathlib import _cos, _sin, _xyz_to_spr, _spr_to_xyz
from glfwToolbox.mathlib import Point3 as _Point3
from glfwToolbox.mathlib import Vector3 as _Vector3
import glfwToolbox.transformations as tr

from OpenGL.GL import glLoadIdentity as _glLoadIdentity
from OpenGL.GLU import gluLookAt as _gluLookAt
import math as _math
import numpy as _np

# Constants
_CAMERA_CENTER_LIMIT_Z_DOWN = -3500
_CAMERA_CENTER_LIMIT_Z_UP = 3500
_CAMERA_CENTER_VEL = 1
_CAMERA_DEFAULT_RVEL = 1
_CAMERA_MIN_THETA_VALUE = 0.000001
_CAMERA_NEGATIVE = -1.0
_CAMERA_POSITIVE = 1.0
_CAMERA_ROUNDED = 2
_CAMERA_SPHERICAL = 0x0fb
_CAMERA_XYZ = 0x0fa


class _Camera(object):
    """
    Abstract camera class.
    """

    def __init__(self):
        """
        Void constructor.
        """
        pass

    def place(self):
        """
        Place camera in world.
        """
        pass

    def get_view(self):
        """
        Get view matrix.
        :rtype: array
        """
        return self._look_at(
            _np.array([self.get_pos_x(), self.get_pos_y(), self.get_pos_z()]),
            _np.array([self.get_center_x(), self.get_center_y(), self.get_center_z()]),
            _np.array([self.get_up_x(), self.get_up_y(), self.get_up_z()])
        )

    def get_pos_x(self):
        """
        Returns x position.

        :rtype: float, int
        """
        pass

    def get_pos_y(self):
        """
        Returns y position.

        :rtype: float, int
        """
        pass

    def get_pos_z(self):
        """
        Returns z position.

        :rtype: float, int
        """
        pass

    def get_center_translation(self):
        """
        Returns center as a translation.

        :return: Translation matrix
        """
        return tr.translate(self.get_center_x(), self.get_center_y(), self.get_center_z())

    def get_center_x(self):
        """
        Returns center x position.

        :rtype: float, int
        """
        pass

    def get_center_y(self):
        """
        Returns center y position.

        :rtype: float, int
        """
        pass

    def get_center_z(self):
        """
        Returns center x position.

        :rtype: float, int
        """
        pass

    def get_up_x(self):
        """
        Return up vector x position.
        :rtype: float, int
        """
        pass

    def get_up_y(self):
        """
        Return up vector y position.
        :rtype: float, int
        """
        pass

    def get_up_z(self):
        """
        Return up vector z position.
        :rtype: float, int
        """
        pass

    def move_x(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to x-position.

        :param direction: X-axis position
        :type direction: float, int
        """
        pass

    def move_y(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to y-position.

        :param direction: Y-axis position
        :type direction: float, int
        """
        pass

    def move_z(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to z-position.

        :param direction: Z-axis position
        :type direction: float, int
        """
        pass

    def set_vel_move_x(self, vel):
        """
        Defines x-axis movement velocity.

        :param vel: X-axis velocity
        :type vel: float, int
        """
        pass

    def set_vel_move_y(self, vel):
        """
        Defines y-axis movement velocity.

        :param vel: Y-axis velocity
        :type vel: float, int
        """
        pass

    def set_vel_move_z(self, vel):
        """
        Defines z-axis movement velocity.

        :param vel: Z-axis velocity
        :type vel: float, int
        """
        pass

    def set_center_vel(self, vel):
        """
        Defines center movement velocity.

        :param vel: Center velocity
        :type vel: float, int
        """
        pass

    def move_center_x(self, dist):
        """
        Moves center x coordinate.

        :param dist: X-distance
        :type dist: float, int
        """
        pass

    def move_center_y(self, dist):
        """
        Moves center y coordinate.

        :param dist: Y-distance
        :type dist: float, int
        """
        pass

    def move_center_z(self, dist):
        """
        Moves center z coordinate.

        :param dist: Z-distance
        :type dist: float, int
        """
        pass

    def rotate_center_z(self, angle):
        """
        Rotate center around z.

        :param angle: Rotation angle
        :type angle: float, int
        """
        pass

    def far(self):
        """
        Camera zoom-out.
        """
        pass

    def close(self):
        """
        Camera zoom-in.
        """
        pass

    def convert_to_xyz(self):
        """
        Convert spheric to cartesian.

        :return: Coordinates
        :rtype: tuple
        """
        pass

    def convert_to_spr(self):
        """
        Convert cartesian to spheric.

        :return: Coordinates
        :rtype: tuple
        """
        pass

    def __str__(self):
        """
        Return camera status.
        """
        pass

    def get_name(self):
        """
        Returns camera name.
        """
        pass

    def set_name(self, n):
        """
        Set camera name
        :param n: Camera name
        """
        pass

    @staticmethod
    def _look_at(_eye, _at, _up):
        """
        Create look at matrix.

        :param _eye:
        :param _at:
        :param _up:
        """
        forward = (_at - _eye)
        forward /= _np.linalg.norm(forward)

        side = _np.cross(forward, _up)
        side /= _np.linalg.norm(side)

        new_up = _np.cross(side, forward)
        new_up /= _np.linalg.norm(new_up)

        return _np.array([
            [side[0], side[1], side[2], -_np.dot(side, _eye)],
            [new_up[0], new_up[1], new_up[2], -_np.dot(new_up, _eye)],
            [-forward[0], -forward[1], -forward[2], _np.dot(forward, _eye)],
            [0, 0, 0, 1]
        ], dtype=_np.float32)


class CameraXYZ(_Camera):
    """
    Camera in XYZ, position (x,y,z), can rotate around z.
    """

    def __init__(self, pos, center=_Point3(0, 0, 0), up=_Point3(0, 0, 1)):
        """
        Constructor.

        :param pos: Position
        :param center: Center coordinate
        :param up: Up vector
        :type pos: float, int
        :type center: float, int
        :type up: float, int
        """
        _Camera.__init__(self)
        if isinstance(pos, _Point3) and isinstance(center, _Point3) and isinstance(up, _Point3):
            self._center = _Vector3(*center.export_to_list())
            self._pos = _Vector3(*pos.export_to_list())
            self._up = _Vector3(*up.export_to_list())
        else:
            raise Exception('pos, center and up must be Point3 type')
        self._angle = 45.0
        self._cameraVel = _Vector3(1.0, 1.0, 1.0)
        self._centerAngle = 0.0
        self._radVel = _CAMERA_CENTER_VEL
        self._name = 'unnamed'
        self._viewVel = _Vector3(1.0, 1.0, 1.0)

        # Normalize vector
        self._up.normalize()

    def place(self):
        """
        Place camera in world.
        """
        _glLoadIdentity()
        _gluLookAt(self._pos.get_x(), self._pos.get_y(), self._pos.get_z(),
                   self._center.get_x(), self._center.get_y(),
                   self._center.get_z(), self._up.get_x(), self._up.get_y(),
                   self._up.get_z())

    def get_pos_x(self):
        """
        Return x position.
        :rtype: float, int
        """
        return self._pos.get_x()

    def get_pos_y(self):
        """
        Return y position.
        :rtype: float, int
        """
        return self._pos.get_y()

    def get_pos_z(self):
        """
        Return z position.
        """
        return self._pos.get_z()

    def get_center_x(self):
        """
        Return center x position.
        :rtype: float, int
        """
        return self._center.get_x()

    def get_center_y(self):
        """
        Return center y position.
        :rtype: float, int
        """
        return self._center.get_y()

    def get_center_z(self):
        """
        Return center x position.
        :rtype: float, int
        """
        return self._center.get_z()

    def get_up_x(self):
        """
        Return up vector x position.
        :rtype: float, int
        """
        return self._up.get_x()

    def get_up_y(self):
        """
        Return up vector y position.
        :rtype: float, int
        """
        return self._up.get_y()

    def get_up_z(self):
        """
        Return up vector z position.
        :rtype: float, int
        """
        return self._up.get_z()

    def move_x(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to x-position.

        :param direction: X-axis position
        :type direction: float, int
        """
        self._pos.set_x(self._pos.get_x() + self._cameraVel.get_x() * direction)

    def move_y(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to y-position.

        :param direction: Y-axis position
        :type direction: float, int
        """
        self._pos.set_y(self._pos.get_y() + self._cameraVel.get_y() * direction)

    def move_z(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to z-position.

        :param direction: Z-axis position
        :type direction: float, int
        """
        self._pos.set_z(self._pos.get_z() + self._cameraVel.get_z() * direction)

    def set_vel_move_x(self, vel):
        """
        Defines x-axis movement velocity.

        :param vel: X-axis velocity
        :type vel: float, int
        """
        self._cameraVel.set_x(vel)

    def set_vel_move_y(self, vel):
        """
        Defines y-axis movement velocity.

        :param vel: Y-axis velocity
        :type vel: float, int
        """
        self._cameraVel.set_y(vel)

    def set_vel_move_z(self, vel):
        """
        Defines z-axis movement velocity.

        :param vel: Z-axis velocity
        """
        self._cameraVel.set_z(vel)

    def set_radial_vel(self, vel):
        """
        Defines radial movement velocity.

        :param vel: Radial velocity
        :type vel: float, int
        """
        self._radVel = vel

    def rotate_x(self, angle):
        """
        Rotate eye position in x-axis.

        :param angle: Rotation angle
        :type angle: float, int
        """
        x = self._pos.get_x()
        y = self._pos.get_y() * _cos(angle) - self._pos.get_z() * _sin(angle)
        z = self._pos.get_y() * _sin(angle) + self._pos.get_z() * _cos(angle)
        self._pos.set_x(x)
        self._pos.set_y(y)
        self._pos.set_z(z)

    def rotate_y(self, angle):
        """
        Rotate eye position in y-axis.

        :param angle: Rotation angle
        :type angle: float, int
        """
        x = self._pos.get_x() * _cos(angle) + self._pos.get_z() * _sin(angle)
        y = self._pos.get_y()
        z = -self._pos.get_x() * _sin(angle) + self._pos.get_z() * _cos(angle)
        self._pos.set_x(x)
        self._pos.set_y(y)
        self._pos.set_z(z)

    def rotate_z(self, angle):
        """
        Rotate eye position in z-axis.

        :param angle: Rotation angle
        :type angle: float, int
        """
        x = self._pos.get_x() * _cos(angle) - self._pos.get_y() * _sin(angle)
        y = self._pos.get_x() * _sin(angle) + self._pos.get_y() * _cos(angle)
        z = self._pos.get_z()
        self._pos.set_x(x)
        self._pos.set_y(y)
        self._pos.set_z(z)

    def move_center_x(self, dist):
        """
        Moves center x coordinate.

        :param dist: X-distance
        :type dist: float, int
        """
        self._center.set_x(self._center.get_x() + dist)

    def move_center_y(self, dist):
        """
        Moves center y coordinate.

        :param dist: Y-distance
        :type dist: float, int
        """
        self._center.set_y(self._center.get_y() + dist)

    def move_center_z(self, dist):
        """
        Moves center z coordinate.

        :param dist: Z-distance
        :type dist: float, int
        """
        if (_CAMERA_CENTER_LIMIT_Z_DOWN <= self._center.get_z() and dist < 0) or \
                (self._center.get_z() <= _CAMERA_CENTER_LIMIT_Z_UP and dist > 0):
            self._center.set_z(self._center.get_z() + dist)

    def rotate_center_z(self, angle):
        """
        Rotate center around z.

        :param angle: Rotation angle
        :type angle: float, int
        """
        rad = _math.sqrt(self._pos.get_x() ** 2 + self._pos.get_y() ** 2)
        self._pos.set_x(rad * _cos(self._angle))
        self._pos.set_y(rad * _sin(self._angle))

    def far(self):
        """
        Camera zoom-out.
        """
        (rad, phi, theta) = _xyz_to_spr(*self._pos.export_to_list())
        rad += self._radVel
        (x, y, z) = _spr_to_xyz(rad, phi, theta)
        self._pos.set_x(x)
        self._pos.set_y(y)
        self._pos.set_z(z)

    def close(self):
        """
        Camera zoom-in.
        """
        (rad, phi, theta) = _xyz_to_spr(*self._pos.export_to_list())
        rad -= self._radVel
        if rad < 0:  # Radius cannot be less than zero
            return
        (x, y, z) = _spr_to_xyz(rad, phi, theta)
        self._pos.set_x(x)
        self._pos.set_y(y)
        self._pos.set_z(z)

    def get_name(self):
        """
        Returns camera name.

        :return: Camera name
        :rtype: basestring
        """
        return self._name

    def set_name(self, n):
        """
        Set camera name.

        :param n: Camera name
        :type n: basestring
        """
        self._name = n

    def convert_to_xyz(self):
        """
        Convert spheric to cartesian.

        :return: Cartesian coordinates
        """
        return self._pos.export_to_tuple()

    def convert_to_spr(self):
        """
        Convert cartesian to spheric.

        :return: Spheric coordinates
        :rtype: tuple
        """
        return _xyz_to_spr(*self._pos.export_to_list())


class CameraR(_Camera):
    """
    Camera in spheric coordinates.
    """

    def __init__(self, r=1.0, phi=45, theta=45, center=_Point3(), up=_Vector3(0, 0, 1)):
        """
        Constructor.

        :param r: Radius
        :param phi: Phi angle
        :param theta: Theta angle
        :param center: Center point
        :param up: Up vector
        :type r: float, int
        :type phi: float, int
        :type theta: float, int
        :type center: Point3
        :type up: Point3
        """
        _Camera.__init__(self)
        if isinstance(center, _Point3):
            if isinstance(up, _Vector3):
                if r > 0:
                    if 0 <= phi <= 360 and 0 <= theta <= 180:
                        self._relpos = _Point3()  # Point added to computed by r*cos*sin
                        self._center = center
                        self._name = 'unnamed'
                        self._phi = phi
                        self._r = r
                        self._rvel = _CAMERA_DEFAULT_RVEL
                        self._theta = theta
                        self._up = up
                    else:
                        raise Exception('Phi angle must be between 0 and 360 degrees, theta must be between 0 and 180')
                else:
                    raise Exception('Radius must be greater than zero')
            else:
                raise Exception('up_vector must be Vector3 type')
        else:
            raise Exception('center must be Point3 type')
        self._max_rad = 0
        self._min_rad = 0

    def set_r_vel(self, vel):
        """
        Defines radial velocity.

        :param vel: Velocity
        :type vel: float, int
        """
        if vel > 0:
            self._rvel = vel
        else:
            raise Exception('Velocity must be greater than zero')

    def place(self):
        """
        Place camera in world.
        """
        _glLoadIdentity()
        _gluLookAt(self._r * _sin(self._theta) * _cos(self._phi) + self._relpos.get_x(),
                   self._r * _sin(self._theta) * _sin(self._phi) + self._relpos.get_y(),
                   self._r * _cos(self._theta) + self._relpos.get_z(),
                   self._center.get_x(), self._center.get_y(), self._center.get_z(),
                   self._up.get_x(), self._up.get_y(),
                   self._up.get_z())

    def get_pos_x(self):
        """
        Return x position.
        :rtype: float, int
        """
        return self._r * _sin(self._theta) * _cos(self._phi)

    def get_pos_y(self):
        """
        Return y position.
        :rtype: float, int
        """
        return self._r * _sin(self._theta) * _sin(self._phi)

    def get_pos_z(self):
        """
        Return z position.
        :rtype: float, int
        """
        return self._r * _cos(self._theta)

    def get_center_x(self):
        """
        Return center x position.
        :rtype: float, int
        """
        return self._center.get_x()

    def get_center_y(self):
        """
        Return center y position.
        :rtype: float, int
        """
        return self._center.get_y()

    def get_center_z(self):
        """
        Return center x position.
        :rtype: float, int
        """
        return self._center.get_z()

    def get_up_x(self):
        """
        Return up vector x position.
        :rtype: float, int
        """
        return self._up.get_x()

    def get_up_y(self):
        """
        Return up vector y position.
        :rtype: float, int
        """
        return self._up.get_y()

    def get_up_z(self):
        """
        Return up vector z position.
        :rtype: float, int
        """
        return self._up.get_z()

    def get_view(self):
        """
        Get view matrix.
        :rtype: array
        """
        return self._look_at(
            _np.array([self.get_pos_x() + self._relpos.get_x(), self.get_pos_y() + self._relpos.get_y(),
                       self.get_pos_z() + self._relpos.get_z()]),
            _np.array([self.get_center_x(), self.get_center_y(), self.get_center_z()]),
            _np.array([self.get_up_x(), self.get_up_y(), self.get_up_z()])
        )

    def __str__(self):
        """
        Returns camera status.

        :return: Camera status
        :rtype: basestring
        """
        x, y, z = self.convert_to_xyz()
        r = _CAMERA_ROUNDED
        msg = 'Camera: {12}\nRadius: {0}\nPhi angle: {1}, Theta angle: {2}\nXYZ eye pos: ({3},{4},{5})\nXYZ center ' \
              'pos: ({6},{7},{8})\nXYZ up vector: ({9},{10},{11})'
        return msg.format(round(self._r, r), round(self._phi, r),
                          round(self._theta, r), round(x, r), round(y, r),
                          round(z, r), round(self._center.get_x(), r),
                          round(self._center.get_y(), r),
                          round(self._center.get_z(), r),
                          round(self._up.get_x(), r), round(self._up.get_y(), r),
                          round(self._up.get_z(), r), self.get_name())

    def set_max_radius(self, r):
        """
        Set max radius.

        :param r: Max radius
        """
        assert r > 0
        assert r > self._min_rad
        self._max_rad = r

    def set_min_radius(self, r):
        """
        Set min radius.

        :param r: Min radius
        """
        assert 0 <= r < self._max_rad
        self._min_rad = r

    def far(self):
        """
        Camera zoom-out.
        """
        self._r += self._rvel
        if self._max_rad != 0:
            self._r = min(self._r, self._max_rad)

    def close(self):
        """
        Camera zoom-in.
        """
        self._r = max(self._r - self._rvel, self._min_rad)

    def rotate_phi(self, angle):
        """
        Rotate phi angle.

        :param angle: Rotation angle
        :type angle: float, int
        """
        self._phi = (self._phi + angle) % 360

    def rotate_theta(self, angle):
        """
        Rotate theta angle.

        :param angle: Rotation angle
        :type angle: float, int
        """
        self._theta = min(max(self._theta + angle, _CAMERA_MIN_THETA_VALUE), 180)

    def convert_to_xyz(self):
        """
        Convert spheric to cartesian.

        :return: Cartesian coodinates
        :rtype: tuple
        """
        return _spr_to_xyz(self._r, self._phi, self._theta)

    def convert_to_spr(self):
        """
        Convert to spheric.

        :return: Coordinates
        :rtype: tuple
        """
        return self._r, self._phi, self._theta

    def move_center_x(self, dist):
        """
        Moves center x coordinate.

        :param dist: X-distance
        :type dist: float, int
        """
        self._center.set_x(self._center.get_x() + dist)

    def move_center_y(self, dist):
        """
        Moves center y coordinate.

        :param dist: Y-distance
        :type dist: float, int
        """
        self._center.set_y(self._center.get_y() + dist)

    def move_x(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to x-position.

        :param direction: X-axis position
        :type direction: float, int
        """
        self._relpos.set_x(self._relpos.get_x() + direction)

    def move_y(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to y-position.

        :param direction: Y-axis position
        :type direction: float, int
        """
        self._relpos.set_y(self._relpos.get_y() + direction)

    def move_z(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to z-position.

        :param direction: Z-axis position
        :type direction: float, int
        """
        self._relpos.set_z(self._relpos.get_z() + direction)

    def move_center_z(self, dist):
        """
        Moves center z coordinate.

        :param dist: Z-distance
        :type dist: float, int
        """
        if (_CAMERA_CENTER_LIMIT_Z_DOWN <= self._center.get_z() and dist < 0) or \
                (self._center.get_z() <= _CAMERA_CENTER_LIMIT_Z_UP and dist > 0):
            self._center.set_z(self._center.get_z() + dist)

    def get_name(self):
        """
        Returns camera name.

        :return: Camera name
        :rtype: basestring
        """
        return self._name

    def set_name(self, n):
        """
        Set camera name.

        :param n: Camera name
        :type n: basestring
        """
        self._name = n

    def get_radius(self):
        """
        Get camera radius.

        :return: Camera radius
        :rtype: float, int
        """
        return self._r

    def set_radius(self, r):
        """
        Set camera radius.

        :param r: Camera radius
        :type r: float, int
        """
        self._r = r

    def get_phi(self):
        """
        Get camera phi angle.

        :return: Phi angle
        :rtype: float, int
        """
        return self._phi

    def set_phi(self, phi):
        """
        Set camera phi.

        :param phi: Phi angle
        :type phi: float, int
        """
        self._phi = phi

    def get_theta(self):
        """
        Returns theta angle.

        :return: Theta angle
        :rtype: float, int
        """
        return self._theta

    def set_theta(self, theta):
        """
        Set theta angle.

        :param theta: Theta angle
        :type theta: float, int
        """
        self._theta = theta
