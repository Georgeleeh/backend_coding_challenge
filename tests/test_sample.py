"""
Tests covering main.py and classes.py
"""
from datetime import date
from pathlib import Path
import sys
import os
import pytest
from src.main import run, parse_sales_brand_csv, parse_sales_product_csv
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

    gross_sales_percentage_growth = test_weekly_data.gross_sales_percentage_growth
    assert isinstance(gross_sales_percentage_growth, float)
    assert gross_sales_percentage_growth == 100.0

    units_sold_percentage_growth = test_weekly_data.units_sold_percentage_growth
    assert isinstance(units_sold_percentage_growth, float)
    assert units_sold_percentage_growth == 100.0

    # set the current weekly_data to None to test previous data but no current data
    test_weekly_current = test_weekly_data.current
    test_weekly_data.current = None
    units_sold_percentage_growth = test_weekly_data.units_sold_percentage_growth
    assert units_sold_percentage_growth == -100.0

    # set the previous weekly_data to None to test current data but no previous data
    test_weekly_data.current = test_weekly_current
    test_weekly_data.previous = None
    units_sold_percentage_growth = test_weekly_data.units_sold_percentage_growth
    assert units_sold_percentage_growth == None


def test_parse_sales_product_csv():
    sales_product_csv_filepath = Path(
        __file__).parent / Path('test_sales_product.csv')
    assert sales_product_csv_filepath.exists()
    parsed_csv = parse_sales_product_csv(sales_product_csv_filepath.as_posix())

    # check that 3 products are present
    assert isinstance(parsed_csv, dict)
    assert len(parsed_csv) == 3

    # check variable types are correct
    assert isinstance(parsed_csv['Product A'], dict)
    assert isinstance(parsed_csv['Product A']['barcode_no'], int)
    assert isinstance(parsed_csv['Product A']['product_name'], str)
    assert isinstance(parsed_csv['Product A']['weekly_data'], dict)

    # check correct number of weekly data entries
    assert len(parsed_csv['Product A']['weekly_data']) == 2
    assert len(parsed_csv['Product B']['weekly_data']) == 1
    assert len(parsed_csv['Product C']['weekly_data']) == 1

    # check variable types are correct
    assert isinstance(parsed_csv['Product A']
                      ['weekly_data']['04/07'].current, dict)
    assert isinstance(parsed_csv['Product A']['weekly_data']
                      ['04/07'].current['gross_sales'], float)
    assert isinstance(parsed_csv['Product A']['weekly_data']
                      ['04/07'].current['units_sold'], int)

    # check values are correct
    assert parsed_csv['Product A']['weekly_data']['04/07'].previous['units_sold'] == 20
    assert parsed_csv['Product A']['weekly_data']['04/07'].current['units_sold'] == 30
    assert parsed_csv['Product A']['weekly_data']['18/07'].current['units_sold'] == 40
    assert parsed_csv['Product B']['weekly_data']['18/07'].previous['units_sold'] == 50
    assert parsed_csv['Product C']['weekly_data']['25/07'].current['units_sold'] == 38


def test_parse_sales_brand_csv():
    """
    Tests the csv ingect function for sales_brand csv files.
    """
    sales_brand_csv_filepath = Path(
        __file__).parent / Path('test_sales_brand.csv')
    assert sales_brand_csv_filepath.exists()
    parsed_csv = parse_sales_brand_csv(sales_brand_csv_filepath.as_posix())

    # check that 3 brands are present
    assert isinstance(parsed_csv, dict)
    assert len(parsed_csv) == 3

    # check variable types are correct
    assert isinstance(parsed_csv['Brand A'], dict)
    assert isinstance(parsed_csv['Brand A']['brand_id'], int)
    assert isinstance(parsed_csv['Brand A']['brand_name'], str)
    assert isinstance(parsed_csv['Brand A']['weekly_data'], dict)

    # check correct number of weekly data entries
    assert len(parsed_csv['Brand A']['weekly_data']) == 3
    assert len(parsed_csv['Brand B']['weekly_data']) == 1
    assert len(parsed_csv['Brand C']['weekly_data']) == 1

    # check variable types are correct
    assert isinstance(parsed_csv['Brand A']
                      ['weekly_data']['04/07'].current, dict)
    assert isinstance(parsed_csv['Brand A']['weekly_data']
                      ['04/07'].current['gross_sales'], float)
    assert isinstance(parsed_csv['Brand A']['weekly_data']
                      ['04/07'].current['units_sold'], int)

    # check values are correct
    assert parsed_csv['Brand A']['weekly_data']['04/07'].previous['units_sold'] == 20
    assert parsed_csv['Brand A']['weekly_data']['04/07'].current['units_sold'] == 30
    assert parsed_csv['Brand A']['weekly_data']['18/07'].current['units_sold'] == 40
    assert parsed_csv['Brand B']['weekly_data']['18/07'].previous['units_sold'] == 50
    assert parsed_csv['Brand C']['weekly_data']['25/07'].current['units_sold'] == 38


def test_skeleton_code_returns_true():
    """
    Example test

    Please replace with your tests
    """

    assert run() is True
