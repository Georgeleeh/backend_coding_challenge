"""
A script for parsing and analysing sales_brand and sales_data csv files.
Outputs a JSON file with weekly percentage growth information.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from src.classes import WeeklyData


def run():
    """
    Please update this function with a function that can run your
    solution end to end, producing an output file in the output/
    directory.
    """

    print("Hello World")

    return True


if __name__ == "__main__":
    run()
