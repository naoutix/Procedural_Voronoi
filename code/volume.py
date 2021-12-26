#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple test script to load voxel data.
"""
import re
import os
import sys
import numpy


def write_ITK_metaimage(volume, name, order=None):
    """
    Writes a ITK metaimage file, which can be viewed by Paraview.
    See http://www.itk.org/Wiki/ITK/MetaIO/Documentation

    Generates a raw file containing the volume, and an associated mhd
    metaimge file.

    TODO: Order should not be given as an argument, but guessed from the
    layout of the numpy array (possibly modified).

    TODO: Use compressed raw binary to save space. Should be possible, but
    given the lack of documentation it is a pain in the ass.

    Parameters
    ----------
    volume : numpy.array
        Input 3D image. Must be numpy.float32
    name : string
        Name of the metaimage file.
    """
    if order is None:
        order = [2, 1, 0]
    assert len(volume.shape) == 3
    print("* Writing ITK metaimage " + name + "...")
    # Write volume data
    with open(name + ".raw", "wb") as raw_file:
        raw_file.write(bytearray(volume.astype(volume.dtype).flatten()))
    # Compute meta data
    if volume.dtype == numpy.float32:
        typename = 'MET_FLOAT'
    elif volume.dtype == numpy.uint8:
        typename = 'MET_CHAR'
    else:
        raise RuntimeError("Incorrect element type: " + volume.dtype)
    # Write meta data
    with open(name + ".mhd", "w") as meta_file:
        basename = os.path.basename(name)
        meta_file.write("ObjectType = Image\nNDims = 3\n")
        meta_file.write(
            "DimSize = " + str(volume.shape[order[0]]) + " " +
            str(volume.shape[order[1]]) + " " +
            str(volume.shape[order[2]]) + "\n")
        meta_file.write(
            "ElementType = {0}\nElementDataFile = {1}.raw\n".format(
                typename, basename))


def read_itk_metaimage(filename, order=[2, 1, 0]):
    """
    Read voxel data saved as a pair of .mhd/.raw files.
    Assume the binary data is stored as uint8.

    Additional documentation:
    http://www.itk.org/Wiki/ITK/MetaIO/Documentation

    Parameters
    ----------
        filename : str
            Name of the file to load (with or withour extension)
        order : list, optional
            Storage order in the .raw file.
    """
    if order is None:
        order = [2, 1, 0]
    name = os.path.splitext(filename)[0]
    # Open meta data file
    with open(name + ".mhd", "r") as mhdfile:
        s = mhdfile.read()
    # Read grid dimensions
    m = re.search('DimSize = ([0-9]*) ([0-9]*) ([0-9]*)', s)
    shape = (int(m.group(order[0] + 1)), int(m.group(order[1] + 1)), int(m.group(order[2] + 1)))
    # Read data file name
    m = re.search('ElementDataFile = (.*).raw', s)
    my_dir = os.path.dirname(name)
    assert os.path.join(my_dir, m.group(1)) == name
    # Read data type
    m = re.search('ElementType = (.*)', s)
    elem_type = m.group(1)
    if elem_type == 'MET_FLOAT':
        num_type = numpy.float32
    elif elem_type == 'MET_CHAR':
        num_type = numpy.uint8
    else:
        raise RuntimeError("Incorrect element type: " + elem_type)
    # Read actual data
    with open(name + ".raw", "rb") as rawfile:
        volume = numpy.frombuffer(bytearray(rawfile.read()), dtype=num_type)
    return volume.reshape(shape)


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else 'volume.mhd'
    volume = read_itk_metaimage(filename)
    print(volume.shape)
    print("volume = {0}%".format(100 * volume.sum() / volume.size))
