import os

"""
The absolute path
"""
AP = os.path.dirname(os.path.realpath(__file__))


def fahrenheitToCelsius(data):
    """
    Convert a value from Fahrenheit to Celsius
    :param data: str
    :return: str
    """
    return (data - 32) / 1.8
