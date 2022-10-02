"""
Tests covering main.py and classes.py
"""
from datetime import date
import json
from pathlib import Path
import sys
import os
import pytest
from src.main import run, parse_sales_brand_csv, parse_sales_product_csv, output_json
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
    assert test_weekly_data.current_week_commencement_date() is None
    assert test_weekly_data.previous_week_commencement_date() is None

    test_weekly_data.add_data(
        period_id=2,
        period_name="current",
        week_commencement_date=date(2022, 7, 4),
        gross_sales=200,
        units_sold=20
    )

    assert isinstance(test_weekly_data.current, dict)
    assert isinstance(test_weekly_data.current_week_commencement_date(), date)
    assert isinstance(
        test_weekly_data.current_week_commencement_date(iso=True), str)

    test_weekly_data.add_data(
        period_id=1,
        period_name="previous",
        week_commencement_date=date(2021, 7, 4),
        gross_sales=100,
        units_sold=10
    )

    assert isinstance(test_weekly_data.previous, dict)
    assert isinstance(test_weekly_data.previous_week_commencement_date(), date)
    assert isinstance(
		test_weekly_data.previous_week_commencement_date(iso=True), str)

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
    """
    Tests the csv ingest function for sales_product csv files.
    """
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
    Tests the csv ingest function for sales_brand csv files.
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


def test_output_json():
    """
    Tests the JSON output using test csv files, outputting a json,
    and reading it back in to check for correctness and sortedness.
    """

    # parse a test sales_brand csv file
    sales_brand_csv_filepath = Path(
		__file__).parent / Path('test_sales_brand.csv')

    parsed_brand_csv = parse_sales_brand_csv(
        sales_brand_csv_filepath.as_posix())

    # parse a test sales_product csv file
    sales_product_csv_filepath = Path(
        __file__).parent / Path('test_sales_product.csv')

    parsed_product_csv = parse_sales_product_csv(
        sales_product_csv_filepath.as_posix())

    output = output_json(brand_data=parsed_brand_csv, product_data=parsed_product_csv,
	                     output_filename='test_results.json')

    # first check the output of the output_json function
    # this should mirror the structure and content of the json file
    assert isinstance(output, dict)

    # check the json file was created in the specified location
    test_json_output_path = Path(
	    __file__).parent.parent / Path('output/test_results.json')
    assert test_json_output_path.exists()

    # read the created json file back in to check
    test_json_file = open(test_json_output_path.as_posix(),
	                      mode='r', encoding='utf-8')
    test_json_data = json.load(test_json_file)

    # check it is read in as a dict with content
    assert isinstance(test_json_data, dict)
    assert test_json_data.get("BRAND") is not None
    assert test_json_data.get("PRODUCT") is not None
    assert len(test_json_data["PRODUCT"]) == 4
    assert len(test_json_data["BRAND"]) == 5

    # check entries are sorted by brand_name
    test_json_brand_entries = [entry['brand_name']
                               for entry in test_json_data["BRAND"]]
    assert test_json_brand_entries == sorted(test_json_brand_entries)

    # check entries are sorted by product_name
    test_json_product_entries = [entry['product_name']
                                 for entry in test_json_data["PRODUCT"]]
    assert test_json_product_entries == sorted(test_json_product_entries)

    # check entries are sorted by current week
    test_json_current_weeks = [entry['current_week_commencing_date']
                               for entry in test_json_data["BRAND"] if entry['brand_name'] == 'Brand A']

    # entries with no current week come last
    assert test_json_current_weeks[-1] is None
    assert test_json_current_weeks[:-1] == sorted(test_json_current_weeks[:-1])

    # remove the test results file when we're done
    test_json_output_path.unlink()


def test_main_returns_true():
    """
    Example test

    Please replace with your tests
    """

    assert run() is True
