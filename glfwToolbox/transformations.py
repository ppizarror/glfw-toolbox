# coding=utf-8
"""
TRANSFORMATIONS
Transformation matrices for computer graphics.

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
import numpy as np


def identity():
    """
    Identity matrix.

    :return:
    """
    return np.identity(4, dtype=np.float32)


def uniform_scale(s):
    """
    Uniform scale transformation.

    :param s:
    :return:
    """
    return np.array([
        [s, 0, 0, 0],
        [0, s, 0, 0],
        [0, 0, s, 0],
        [0, 0, 0, 1]], dtype=np.float32)


def scale(sx, sy, sz):
    """
    Scale matrix.

    :param sx:
    :param sy:
    :param sz:
    :return:
    """
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]], dtype=np.float32)


def rotation_x(theta):
    """
    Rotation around x.

    :param theta:
    :return:
    """
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [1, 0, 0, 0],
        [0, cos_theta, -sin_theta, 0],
        [0, sin_theta, cos_theta, 0],
        [0, 0, 0, 1]], dtype=np.float32)


def rotation_y(theta):
    """
    Rotation around y.

    :param theta:
    :return:
    """
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [cos_theta, 0, sin_theta, 0],
        [0, 1, 0, 0],
        [-sin_theta, 0, cos_theta, 0],
        [0, 0, 0, 1]], dtype=np.float32)


def rotation_z(theta):
    """
    Rotation around z.

    :param theta:
    :return:
    """
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [cos_theta, -sin_theta, 0, 0],
        [sin_theta, cos_theta, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]], dtype=np.float32)


def rotation_a(theta, axis):
    """
    Rotation around axis.

    :param theta:
    :param axis:
    :return:
    """
    s = np.sin(theta)
    c = np.cos(theta)

    assert axis.shape == (3,)

    x = axis[0]
    y = axis[1]
    z = axis[2]

    return np.array([
        # First row
        [c + (1 - c) * x * x,
         (1 - c) * x * y - s * z,
         (1 - c) * x * z + s * y,
         0],
        # Second row
        [(1 - c) * x * y + s * z,
         c + (1 - c) * y * y,
         (1 - c) * y * z - s * x,
         0],
        # Third row
        [(1 - c) * x * z - s * y,
         (1 - c) * y * z + s * x,
         c + (1 - c) * z * z,
         0],
        # Fourth row
        [0, 0, 0, 1]], dtype=np.float32)


def translate(tx, ty, tz):
    """
    Translate matrix.

    :param tx:
    :param ty:
    :param tz:
    :return:
    """
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]], dtype=np.float32)


def shearing(xy, yx, xz, zx, yz, zy):
    """
    Shearing matrix.

    :param xy:
    :param yx:
    :param xz:
    :param zx:
    :param yz:
    :param zy:
    :return:
    """
    return np.array([
        [1, xy, xz, 0],
        [yx, 1, yz, 0],
        [zx, zy, 1, 0],
        [0, 0, 0, 1]], dtype=np.float32)


def matmul(mats):
    """
    Matrix multiplication.

    :param mats:
    :return:
    """
    out = mats[0]
    for i in range(1, len(mats)):
        out = np.matmul(out, mats[i])
    return out


def frustum(left, right, bottom, top, near, far):
    """
    Frustrum viewing matrix.

    :param left:
    :param right:
    :param bottom:
    :param top:
    :param near:
    :param far:
    :return:
    """
    r_l = right - left
    t_b = top - bottom
    f_n = far - near
    return np.array([
        [2 * near / r_l,
         0,
         (right + left) / r_l,
         0],
        [0,
         2 * near / t_b,
         (top + bottom) / t_b,
         0],
        [0,
         0,
         -(far + near) / f_n,
         -2 * near * far / f_n],
        [0,
         0,
         -1,
         0]], dtype=np.float32)


def perspective(fovy, aspect, near, far):
    """
    Perspective viewing matrix.

    :param fovy:
    :param aspect:
    :param near:
    :param far:
    :return:
    """
    half_height = np.tan(np.pi * fovy / 360) * near
    half_width = half_height * aspect
    return frustum(-half_width, half_width, -half_height, half_height, near, far)


def ortho(left, right, bottom, top, near, far):
    """
    Orthographic viewing matrix.

    :param left:
    :param right:
    :param bottom:
    :param top:
    :param near:
    :param far:
    :return:
    """
    r_l = right - left
    t_b = top - bottom
    f_n = far - near
    return np.array([
        [2 / r_l,
         0,
         0,
         -(right + left) / r_l],
        [0,
         2 / t_b,
         0,
         -(top + bottom) / t_b],
        [0,
         0,
         -2 / f_n,
         -(far + near) / f_n],
        [0,
         0,
         0,
         1]], dtype=np.float32)


def look_at(eye, at, up):
    """
    Look at operator.

    :param eye:
    :param at:
    :param up:
    :return:
    """
    forward = (at - eye)
    forward = forward / np.linalg.norm(forward)

    side = np.cross(forward, up)
    side = side / np.linalg.norm(side)

    new_up = np.cross(side, forward)
    new_up = new_up / np.linalg.norm(new_up)

    return np.array([
        [side[0], side[1], side[2], -np.dot(side, eye)],
        [new_up[0], new_up[1], new_up[2], -np.dot(new_up, eye)],
        [-forward[0], -forward[1], -forward[2], np.dot(forward, eye)],
        [0, 0, 0, 1]
    ], dtype=np.float32)
