"""
A script for parsing and analysing sales_brand and sales_data csv files.
Outputs a JSON file with weekly percentage growth information.
"""

import csv
from datetime import datetime
import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from src.classes import WeeklyData

DATA_FOLDER_PATH = Path(__file__).parent.parent / Path("data")


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


def run() -> bool:
    """
    Please update this function with a function that can run your
    solution end to end, producing an output file in the output/
    directory.
    """

    sales_brand_data = parse_sales_brand_csv(
        DATA_FOLDER_PATH / Path("sales_brand.csv"))

    sales_product_data = parse_sales_product_csv(
        DATA_FOLDER_PATH / Path("sales_product.csv"))

    return True


if __name__ == "__main__":
    run()
