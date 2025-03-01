#!/usr/bin/env python3
"""
Contains general operations used throughout the package.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2025"
__credits__ = ["Peter Waddell"]
__version__ = "0.0.1"
__date__ = "2024/11/09"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

import math
from typing import List, Callable, Union

from xyz_manipulation.src.plane import Plane


def normalize(v: List) -> List:
    """
    Returns a normalized version of the input vector (i.e. same direction but
    magnitude of 1).

    Parameters
    ----------
    v : List
        List of three floats: coordinates to the vector that will be normalized.

    Returns
    -------
    List
        List of three floats corresponding to the point after normalization.
    """
    assert (calc_magnitude(v) > 0)
    return [i / calc_magnitude(v) for i in v]


def calc_magnitude(v: List) -> float:
    """
    Returns the magnitude of the input vector.

    Parameters
    ----------
    v : List
        List of  floats: coordinates of the vector.

    Returns
    -------
    float
        Magnitude of the vector.
    """
    return math.sqrt(sum([i ** 2 for i in v]))


def dot(u: List, v: List) -> float:
    """
    Computes the dot product of two vectors.

    Parameters
    ----------
    v : List
        List of  floats: coordinates of the vector.
    u : List
        List of  floats: coordinates of the vector.

    Returns
    -------
    float
        Dot product of the two vectors.
    """
    assert (len(u) == 3 and len(v) == 3)
    result = 0
    for i in range(3):
        result += u[i] * v[i]
    return result


def cross(u: List, v: List) -> List:
    """
    Computes the cross product of two vectors.

    Parameters
    ----------
    v : List
        List of  floats: coordinates of the vector.
    u : List
        List of  floats: coordinates of the vector.

    Returns
    -------
    List
        Cross product of the two vectors.
    """
    return [
        (u[1] * v[2]) - (u[2] * v[1]),
        (u[0] * v[2]) - (u[2] * v[0]),
        (u[0] * v[1]) - (u[1] * v[0])
    ]


def calc_angle_between_vectors(u: List, v: List) -> float:
    """
    Computes the angle between two vectors.

    Parameters
    ----------
    v : List
        List of  floats: coordinates of the vector.
    u : List
        List of  floats: coordinates of the vector.

    Returns
    -------
    float
        Angle between the two vectors, in degrees.
    """
    if calc_magnitude(u) == 0 or calc_magnitude(v) == 0:
        return 0
    return math.degrees(
        math.acos(dot(u, v) / (calc_magnitude(u) * calc_magnitude(v)))
    )


def format_elem(elem: str) -> str:
    """
    Formats an element symbol for a .xyz file by adding an additional spaces
    after the symbol as needed in order to preserve the file's formatting.

    Parameters
    ----------
    elem : str
        String of the element symbol.

    Returns
    -------
    str
        Formatted element symbol.
    """
    assert ((len(elem) <= 2) and (len(elem) > 0))
    if len(elem) == 1:
        return elem + "   "
    return elem + "  "


def format_coord(coord: float) -> str:
    """
    Formats a coordinate for a .xyz file by representing the number to six
    decimal places and adding additional spaces in front as needed.

    The total length of each coordinate string should be 12.

    Parameters
    ----------
    coord : float
        Float of the coordinate to be formatted.

    Returns
    -------
    str
        Formatted coord., ready to add to a line in the translated .xyz file.
    """
    new_coord = "{:.6f}".format(coord)
    spaces_needed = 12 - len(new_coord)
    assert (spaces_needed >= 0)
    result = ""
    for i in range(spaces_needed):
        result += " "
    return result + new_coord


def transform_lines(lines: List,
                     transform: Callable,
                     transformation_arg: Union[List, Plane]) -> str:
    """
    Performs a given transformation on a series of points from lines of a .xyz
    file, formats the result in .xyz file format and returns the new lines.

    Parameters
    ----------
    lines : List
        List of lines from a .xyz file to be transformed.
    transform : Callable
        Function corresponding to the desired transformation.
    transformation_arg : Union[List, Plane]
        Additional argument for the transformation, e.g. angle of rotation.

    Returns
    -------
    List
        List of transformed lines in .xyz file format.
    """
    result_contents = lines[0] + "\n" + lines[1] + "\n"
    for i in range(2, len(lines)):
        split_line = lines[i].split()
        if not split_line:
            continue
        assert (len(split_line) == 4)
        x, y, z = \
            float(split_line[1]), float(split_line[2]), float(split_line[3])
        new_point = transform([x, y, z], transformation_arg)
        new_elem = format_elem(split_line[0])
        result_contents += new_elem + \
                           format_coord(new_point[0]) + \
                           format_coord(new_point[1]) + \
                           format_coord(new_point[2]) + "\n"
    return result_contents
