# -*- coding: utf-8 -*-
"""
common.py
Briefly describe the functionality and purpose of the file.

This file is part of KimariDraw.
KimariDraw is a Python script that processes Multiwfn spectral data and plots various spectra.

@author:
Kimariyb (kimariyb@163.com)

@license:
Licensed under the MIT License.
For details, see the LICENSE file.

@Data:
2023-08-31
"""

import math
import os


def count_degree(expected, max_value, min_value, symmetrical=False):
    """
    Calculate the maximum and minimum degrees of the expected scale,
    which are multiples of the estep.

    Args:
        expected (float): The desired interval of the scale.
        max_value (float): The maximum value of the data.
        min_value (float): The minimum value of the data.
        symmetrical (bool, optional): Whether to enable symmetrical scale.
            Defaults to False.

    Returns:
        tuple: The maximum and minimum degrees (maxi, mini).

    """
    # The final effect is to take 1 unit up when max/expected belongs to the interval (-1, Infinity),
    # otherwise take 2 units. Similarly, take 1 unit down when min/expected belongs to the interval (-Infinity,1),
    # otherwise take 2 units.
    maxi = int(max_value / expected + 1) * expected
    mini = int(min_value / expected - 1) * expected

    # If max and min are exactly on the scale lines, the logic above would take one extra unit up or down.
    if max_value == 0:
        maxi = 0
    if min_value == 0:
        mini = 0

    if symmetrical and maxi * mini <= 0:
        tm = max(abs(maxi), abs(mini))
        maxi = tm
        mini = -tm

    return maxi, mini


def auto_lim(max_value, min_value, is_deviation=False):
    """
    Automatically generate a neat xlim or ylim based on the maximum and minimum values.
    The lim includes the maximum value and minimum value of the x or y axis,
    as well as the x or y axis tick locator.

    Args:
        max_value (float): The maximum value of x or y data.
        min_value (float): The minimum value of x or y data.
        is_deviation (bool, optional): Whether to allow deviation.
            Defaults to False.

    Returns:
        list: Auto lim list [lim_min, lim_max, locator].

    """
    # Initialize the desired number of scale intervals
    split_number = 4

    # Initialize a magic array and calculate the initial interval (temp_gap) and scaling factor (multiple)
    magic_array = [2, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100]
    temp_gap = (max_value - min_value) / split_number
    multiple = 10 ** (math.floor(math.log10(temp_gap) - 1))
    expected = next((val * multiple for val in magic_array if val > temp_gap / multiple), None)

    # Calculate the maximum and minimum degrees of the expected scale
    maxi, mini = count_degree(expected, max_value, min_value)

    if not is_deviation:
        while True:
            temp_split_number = round((maxi - mini) / expected)

            # Update the maximum and minimum values based on conditions
            if (maxi == 0 or mini - min_value <= maxi - max_value) and temp_split_number < split_number:
                # Update the minimum value (move left)
                mini -= expected
            else:
                # Update the maximum value (move right)
                maxi += expected

            # Exit the loop when the desired number of splits is reached
            if temp_split_number == split_number:
                break

            if temp_split_number > split_number:
                # Find the index of the current magic number
                magic_idx = next((i for i, val in enumerate(magic_array) if val * multiple == expected), None)

                # If the index exists and is not the last one, update the expected value and the maximum
                # and minimum values
                if magic_idx is not None and magic_idx < len(magic_array) - 1:
                    # Update the expected value (increase)
                    expected = magic_array[magic_idx + 1] * multiple
                    # Update the maximum and minimum values
                    maxi, mini = count_degree(expected, max_value, min_value)
                else:
                    break
            else:
                # Find the index of the current magic number
                magic_idx = next((i for i, val in enumerate(magic_array) if val * multiple == expected), None)

                # If the index exists and is not the first one, update the expected value and the
                # maximum and minimum values
                if magic_idx is not None and magic_idx > 0:
                    # Update the expected value (decrease)
                    expected = magic_array[magic_idx - 1] * multiple
                    # Update the maximum and minimum values
                    maxi, mini = count_degree(expected, max_value, min_value)
                else:
                    break

    interval = (maxi - mini) / split_number
    lim = [mini, maxi, interval]

    return lim


def validate(file):
    """
    判断输入的文件是否为 toml 文件

    Args:
        file(str): toml 文件的路径
    """
    # 首先判断输入的是否为 toml 文件，如果不是，则抛出异常。并在屏幕上打印不支持该文件
    if not file.endswith(".toml"):
        raise ValueError("Error: Unsupported file format. Only TOML files are supported.\n")

    # 判断输入的 toml 文件是否存在，如果不存在，则抛出异常。并在屏幕上打印未找到该文件
    if not os.path.isfile(file):
        raise FileNotFoundError("Error: File not found.\n")
