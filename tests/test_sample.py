"""
Tests covering main.py and classes.py
"""
from datetime import date
import sys
import os
import pytest
from src.main import run
from src.classes import WeeklyData

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


def test_class_weekly_data():
    """
    Tests for the class WeeklyData.
    """
    test_weekly_data = WeeklyData()
    assert test_weekly_data.current is None
    assert test_weekly_data.previous is None

    test_weekly_data.add_data(
        period_id=2,
        period_name="current",
        week_commencement_date=date(2022, 7, 4),
        gross_sales=200,
        units_sold=20
    )

    assert isinstance(test_weekly_data.current, dict)

    test_weekly_data.add_data(
        period_id=1,
        period_name="previous",
        week_commencement_date=date(2021, 7, 4),
        gross_sales=100,
        units_sold=10
    )

    assert isinstance(test_weekly_data.previous, dict)

    with pytest.raises(ValueError):
        test_weekly_data.add_data(
            period_id=3,
            period_name="next",
            week_commencement_date=date(2023, 7, 4),
            gross_sales=600,
            units_sold=60
        )


def test_skeleton_code_returns_true():
    """
    Example test

    Please replace with your tests
    """

    assert run() is True
