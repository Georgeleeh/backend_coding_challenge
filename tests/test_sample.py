"""
Tests covering main.py and classes.py
"""
import sys
import os
import pytest
from src.main import run
from src.classes import WeeklyData

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


def class_test_weekly_data():
    """
    Tests for the class WeeklyData.
    """
    test_weekly_data = WeeklyData()
    assert test_weekly_data.current is None
    assert test_weekly_data.previous is None


def test_skeleton_code_returns_true():
    """
    Example test

    Please replace with your tests
    """

    assert run() is True
