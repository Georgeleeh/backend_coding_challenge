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

    def __percentage_change(self, target: str):
        # functionally an if-elif-else stack but no need for elifs because it returns
        if self.current is None and self.previous is not None:
            return -100.0
        if self.current is not None and self.previous is None:
            return None

        curr = self.current[target]
        prev = self.previous[target]
        perc = (curr - prev) / prev * 100

        return round(perc, 2)

    @property
    def gross_sales_percentage_growth(self) -> float:
        """
        Returns the percentage growth for gross_sales to 2 d.p.
        """
        return self.__percentage_change('gross_sales')

    @property
    def units_sold_percentage_growth(self) -> float:
        """
        Returns the percentage growth for units_sold to 2 d.p.
        """
        return self.__percentage_change('units_sold')
