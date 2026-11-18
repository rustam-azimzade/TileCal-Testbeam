
class Events:
    def __init__(self):
        # MODULES
        self._selections = None
        self._eda = None

    @property
    def eda(self):
        if self._eda is None:
            from .eda import EDA  # import here to avoid circular import
            self._eda = EDA(self)
        return self._eda

    @property
    def selections(self):
        if self._selections is None:
            from .selections import SELECTIONS  # import here to avoid circular import
            self._selections = SELECTIONS(self)
        return self._selections
