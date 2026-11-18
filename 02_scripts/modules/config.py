import numpy as np
from matplotlib.ticker import ScalarFormatter
from dataclasses import dataclass

@dataclass
class Config:
    DATA_PATH = "../01_src/data"

    COLORS = {
        # ATLAS / Okabe-Ito
        "atlas:red": "#D55E00",
        "atlas:blue": "#0072B2",
        "atlas:lightBlue": "#56B4E9",
        "atlas:orange": "#E69F00",
        "atlas:yellow": "#F0E442",
        "atlas:green": "#009E73",
        "atlas:purple": "#CC79A7",

        # Petroff
        "petroff:blue": "#3f90da",
        "petroff:orange": "#ffa90d",
        "petroff:red": "#bc1e00",
        "petroff:gray": "#94a4a2",
        "petroff:purple": "#832db5",
        "petroff:brown": "#a96b59",
        "petroff:orange2": "#e76300",
        "petroff:tan": "#b8ab6f",
        "petroff:gray2": "#707480",
        "petroff:lightBlue": "#92dadd",

        # Neutral
        "black": "#000000",
        "dark_gray": "#404040",
        "gray": "#808080",
        "light_gray": "#B0B0B0",
        "white": "#FFFFFF",
    }

    PLOT_SIZE = (11.111, 8.333)
    BOXPLOTS_PLOT_SIZE = (15, 6)
    CORRELATION_MATRIX_PLOT_SIZE = (24, 20)
    PREDICTIONS_PLOT_SIZE = (8.5, 10)
    PREDICTIONS_PLOT_RATIO_UPPER = 6
    PREDICTIONS_PLOT_RATIO_LOWER = 1
    RANKING_PLOT_SIZE = (15, 17)
    ABLATION_PLOT_SIZE = (20, 6)
    TECHNICAL_INFO_LOCATION = (0.05, 0.95)

    POWER_LIMITS = (-2, 4)

    FONT_SIZE = 18
    BIG_FONT_SIZE = 24
    SMALL_FONT_SIZE = 6
    EXTRA_SMALL_FONT_SIZE = 3

    BIN_EDGES = np.linspace(0, 1, 40)
    BINS = 100

    RUNS_DESCRIPTION = {
        "2510758": {
            "particle_type": "Hadrons",
            "energy": "50",
            "impact_angle": "20",
            "cell": "A-4",
            "delta_Z": "0",
        },
    }
    RECONSTRUCTION_METHOD_ENCODINGS = ["fit", "opt"]
    MODULE_ENCODINGS = {
        "A02": "LBA65",
        "C01": "M0C",
        "C02": "LBC65",
        "E03": "EBC65",
    }
    CHANNELS_NUMBER = 48
    NON_OPERATIONAL_CHANNEL_INDICES = {
        "A02": {},
        "C01": {},
        "C02": {31, 32, 43},
        "E03": {},
    }

    UNIT_SYSTEMS = {
        "energy": {
            "eV": 1.0,
            "keV": 1e3,
            "MeV": 1e6,
            "GeV": 1e9,
            "TeV": 1e12,
        },
        "time": {
            "ps": 1e-3,
            "ns": 1.0,
            "us": 1e3,
            "ms": 1e6,
            "s": 1e9,
            "min": 60e9,
            "h": 3600e9,
        },
    }
