"""
A script for parsing and analysing sales_brand and sales_data csv files.
Outputs a JSON file with weekly percentage growth information.
"""

import csv
from datetime import datetime
import json
import os
from pathlib import Path
import sys
from typing import OrderedDict

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from src.classes import WeeklyData


DATA_FOLDER_PATH = Path(__file__).parent.parent / Path("data")
OUTPUT_FOLDER_PATH = Path(__file__).parent.parent / Path("output")


def parse_sales_brand_csv(csv_filename: str) -> dict:
    """
    Parse a sales_brand csv file into a dictionary of WeeklyData objects.
    This structure allows for easy filtering by brand, then week.
    """

    brands = {}

    with open(csv_filename, mode='r', encoding='utf-8') as file:

        csv_file = csv.DictReader(file)

        for line in csv_file:

            # force variable types for each line item
            line_brand_id = int(line['brand_id'])
            line_brand_name = str(line['brand'])
            line_period_id = int(line['period_id'])
            line_period_name = str(line['period_name'])
            line_week_commencing_date = datetime.strptime(
                line['week_commencing_date'], "%d/%m/%Y").date()
            line_gross_sales = float(line['gross_sales'])
            line_units_sold = int(line['units_sold'])

            formatted_week_day_month = line_week_commencing_date.strftime(
                "%d/%m"
            )

            # if the brand is new, add to the brands dict
            if line_brand_name not in brands:
                brands[line_brand_name] = {
                    "brand_id": line_brand_id,
                    "brand_name": line_brand_name,
                    "weekly_data": {}
                }

            # if the week has no data, create a new class instance and add it to the dict
            if formatted_week_day_month not in brands[line_brand_name]['weekly_data']:
                brands[line_brand_name]['weekly_data'][formatted_week_day_month] = WeeklyData()

            # create a WeeklyData instance for this line of data
            brands[line_brand_name]['weekly_data'][formatted_week_day_month].add_data(
                line_period_id,
                line_period_name,
                line_week_commencing_date,
                line_gross_sales,
                line_units_sold
            )

    return brands

# parity between brand_id-barcode_no and brand-product_name means these could be combined?
# probably harder to read


def parse_sales_product_csv(csv_filename: str) -> dict:
    """
    Parse a sales_product csv file into a dictionary of WeeklyData objects.
    This structure allows for easy filtering by brand, then week.
    """

    products = {}

    with open(csv_filename, mode='r', encoding='utf-8') as file:

        csv_file = csv.DictReader(file)

        for line in csv_file:

            # force variable types for each line item
            line_barcode_no = int(line['barcode_no'])
            line_product_name = str(line['product_name'])
            line_period_id = int(line['period_id'])
            line_period_name = str(line['period_name'])
            line_week_commencing_date = datetime.strptime(
                line['week_commencing_date'], "%d/%m/%Y").date()
            line_gross_sales = float(line['gross_sales'])
            line_units_sold = int(line['units_sold'])

            formatted_week_day_month = line_week_commencing_date.strftime(
                "%d/%m"
            )

            # if the brand is new, add to the brands dict
            if line_product_name not in products:
                products[line_product_name] = {
                    "barcode_no": line_barcode_no,
                    "product_name": line_product_name,
                    "weekly_data": {}
                }

            # if the week has no data, create a new class instance and add it to the dict
            if formatted_week_day_month not in products[line_product_name]['weekly_data']:
                products[line_product_name]['weekly_data'][formatted_week_day_month] = WeeklyData(
                )

            # create a WeeklyData instance for this line of data
            products[line_product_name]['weekly_data'][formatted_week_day_month].add_data(
                line_period_id,
                line_period_name,
                line_week_commencing_date,
                line_gross_sales,
                line_units_sold
            )

    return products


def output_json(
    brand_data: dict,
    product_data: dict,
    output_filename: str = 'results.json'
    ) -> dict:
    """
    Create an json file containing ordered weekly growth data for all brands and products.
    """
    output = OrderedDict({
        "PRODUCT": [],
        "BRAND": []
    })

    json_file_path = OUTPUT_FOLDER_PATH / Path(output_filename)

    # sort brand_data_keys before iterating and inserting into OrderedDict
    for brand_name in sorted(brand_data.keys()):

        brand_id = brand_data[brand_name]["brand_id"]
        brand_name = brand_data[brand_name]["brand_name"]

        # used to hold entries with no current weekly data
        # so they can be appended after
        no_current_weekly_data = []

        # sort weekly_data keys before iterating and inserting
        for week_key in sorted(
                brand_data[brand_name]["weekly_data"].keys()):
            weekly_data = brand_data[brand_name]["weekly_data"][week_key]

            if weekly_data.current_week_commencement_date(iso=True) is not None:
                output["BRAND"].append({
                    "brand_id": brand_id,
                    "brand_name": brand_name,
                    "current_week_commencing_date":
                    weekly_data.current_week_commencement_date(iso=True),
                    "previous_week_commencing_date":
                    weekly_data.previous_week_commencement_date(iso=True),
                    "perc_gross_sales_growth": weekly_data.gross_sales_percentage_growth,
                    "perc_unit_sales_growth": weekly_data.units_sold_percentage_growth
                })
            else:
                no_current_weekly_data.append({
                    "brand_id": brand_id,
                    "brand_name": brand_name,
                    "current_week_commencing_date":
                    weekly_data.current_week_commencement_date(iso=True),
                    "previous_week_commencing_date":
                    weekly_data.previous_week_commencement_date(iso=True),
                    "perc_gross_sales_growth": weekly_data.gross_sales_percentage_growth,
                    "perc_unit_sales_growth": weekly_data.units_sold_percentage_growth
                })

        # append entries with no current weekly data
        for item in no_current_weekly_data:
            output["BRAND"].append(item)

    for product_name in sorted(product_data.keys()):

        barcode_no = product_data[product_name]["barcode_no"]
        product_name = product_data[product_name]["product_name"]

        sorted_weekly_data_keys = sorted(
            product_data[product_name]["weekly_data"].keys())

        # used to hold entries with no current weekly data
        # so they can be appended after
        no_current_weekly_data = []

        for week_key in sorted_weekly_data_keys:
            weekly_data = product_data[product_name]["weekly_data"][week_key]

            if weekly_data.current_week_commencement_date(iso=True) is not None:

                output["PRODUCT"].append({
                    "barcode_no": barcode_no,
                    "product_name": product_name,
                    "current_week_commencing_date":
                    weekly_data.current_week_commencement_date(iso=True),
                    "previous_week_commencing_date":
                    weekly_data.previous_week_commencement_date(iso=True),
                    "perc_gross_sales_growth": weekly_data.gross_sales_percentage_growth,
                    "perc_unit_sales_growth": weekly_data.units_sold_percentage_growth
                })

            else:

                no_current_weekly_data.append({
                    "barcode_no": barcode_no,
                    "product_name": product_name,
                    "current_week_commencing_date":
                    weekly_data.current_week_commencement_date(iso=True),
                    "previous_week_commencing_date":
                    weekly_data.previous_week_commencement_date(iso=True),
                    "perc_gross_sales_growth": weekly_data.gross_sales_percentage_growth,
                    "perc_unit_sales_growth": weekly_data.units_sold_percentage_growth
                })

        # append entries with no current weekly data
        for item in no_current_weekly_data:
            output["PRODUCT"].append(item)

    with open(json_file_path.as_posix(), "w", encoding='utf-8') as outfile:
        json.dump(output, outfile)

    return output


def run() -> bool:
    """
    This is the main entry point to the program.
    The parsing and output functions are called from here.
    """

    sales_brand_data = parse_sales_brand_csv(
        DATA_FOLDER_PATH / Path("sales_brand.csv"))

    sales_product_data = parse_sales_product_csv(
        DATA_FOLDER_PATH / Path("sales_product.csv"))

    output_json(brand_data=sales_brand_data, product_data=sales_product_data)

    return True


if __name__ == "__main__":
    run()
