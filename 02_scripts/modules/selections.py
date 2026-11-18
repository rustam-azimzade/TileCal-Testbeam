import pandas as pd


class SELECTIONS:
    def __init__(self, events):
        self.__events = events
        logger.debug('SELECTIONS module is correctly initialized')

    def coordinates(self):
        events = pd.DataFrame()
        variable_name = ""
        condition_mask = 30 <= events[variable_name] <= -30
        selected_events = events.loc[condition_mask]
