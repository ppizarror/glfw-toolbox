# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
A simple scene graph class and functionality
v2.0 - Enhanced to work on 3D environments
"""

from OpenGL.GL import *
import numpy as np

import glfwToolbox.transformations as _tr
from glfwToolbox.easy_shaders import GPUShape as _GPUShape


# A simple class to handle a scene graph
# Each node represents a group of objects
# Each leaf represents a basic figure (GPUShape)
# To identify each node properly, it MUST have a unique name
class SceneGraphNode:
    def __init__(self, _name):
        self.name = _name
        self.transform = _tr.identity()
        self.childs = []


def find_node(node, _name):
    """
    :param node:
    :param _name:
    :return:
    """
    # The name was not found in this path
    if isinstance(node, _GPUShape):
        return None

    # This is the requested node
    if node.name == _name:
        return node

    # All childs are checked for the requested name
    else:
        for child in node.childs:
            found_node = find_node(child, _name)
            if found_node is not None:
                return found_node

    # No child of this node had the requested name
    return None


def find_transform(node, _name, parent_transform=_tr.identity()):
    """
    :param node:
    :param _name:
    :param parent_transform:
    :return:
    """
    # The name was not found in this path
    if isinstance(node, _GPUShape):
        return None

    new_transform = np.matmul(parent_transform, node.transform)

    # This is the requested node
    if node.name == _name:
        return new_transform

    # All childs are checked for the requested name
    else:
        for child in node.childs:
            found_transform = find_transform(child, _name, new_transform)
            if isinstance(found_transform, (np.ndarray, np.generic)):
                return found_transform

    # No child of this node had the requested name
    return None


def find_position(node, _name, parent_transform=_tr.identity()):
    """
    :param node:
    :param _name:
    :param parent_transform:
    :return:
    """
    found_transform = find_transform(node, _name, parent_transform)

    if isinstance(found_transform, (np.ndarray, np.generic)):
        zero = np.array([[0, 0, 0, 1]], dtype=np.float32).T
        found_position = np.matmul(found_transform, zero)
        return found_position

    return None


def draw_scene_graph_node(node, pipeline, parent_transform=_tr.identity()):
    """
    :param node:
    :param pipeline:
    :param parent_transform:
    :return:
    """
    assert (isinstance(node, SceneGraphNode))

    # Composing the transformations through this path
    new_transform = np.matmul(parent_transform, node.transform)

    # If the child node is a leaf, it should be a GPUShape.
    # Hence, it can be drawn with drawShape
    if len(node.childs) == 1 and isinstance(node.childs[0], _GPUShape):
        leaf = node.childs[0]
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'model'), 1, GL_TRUE, new_transform)
        pipeline.draw_shape(leaf)

    # If the child node is not a leaf, it MUST be a SceneGraphNode,
    # so this draw function is called recursively
    else:
        for child in node.childs:
            draw_scene_graph_node(child, pipeline, new_transform)
