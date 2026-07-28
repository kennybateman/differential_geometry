
import numpy as np
from scipy.optimize import curve_fit
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import subprocess
from src.curve import *
from src.surface import *
from src.graphing import *

class MatplotGraphing:

    def plot_and_save(filepath, x_y_data, curve=None, label='', curve_name=''):
        x_data = x_y_data[:,0]
        y_data = x_y_data[:,1]
    
        x_line = np.linspace(min(x_data), max(x_data), 500) # default resolution of 500 for now
        _, ax = plt.subplots()
        ax.plot(x_data, y_data, 'o', label=label)
        if curve:
            ax.plot(x_line, curve(x_line), '-', label=curve_name)

        ax.legend()
        plt.savefig(filepath, dpi=300)