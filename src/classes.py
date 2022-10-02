"""
Contains the classes/data-structures used to ingest csv data.
"""


from datetime import date


class WeeklyData:
    """
    Contains weekly sales information stored by period
    and methods to produce percentage changes across periods.
    """

    def __init__(self):
        self.current: dict = None
        self.previous: dict = None

    def add_data(
        self,
        period_id: int,
        period_name: str,
        week_commencement_date: date,
        gross_sales: float,
        units_sold: int
    ):
        """
        Add current or previous data for the week.
        """
        period_dict = {
            'period_id': period_id,
            'week_commencement_date': week_commencement_date,
            'gross_sales': gross_sales,
            'units_sold': units_sold
        }

        if period_name == 'current':
            self.current = period_dict

        elif period_name == 'previous':
            self.previous = period_dict

        else:
            raise ValueError(
                "period_name not recognised. Expected 'current' or 'previous'.")
