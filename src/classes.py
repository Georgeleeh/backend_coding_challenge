"""
Contains the classes/data-structures used to ingest csv data.
"""


class WeeklyData:
    """
    Contains weekly sales information stored by period
    and methods to produce percentage changes across periods.
    """

    def __init__(self):
        self.current: dict = None
        self.previous: dict = None
