
import numpy as np
import os
from scipy.optimize import curve_fit
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import subprocess
from src.curve import *
from src.surface import *
from src.graphing import *
import toml



def try_load_toml(param_name, filename, dir, default):
    if os.path.exists(f"{dir}{filename}.toml"):
        return toml.load(f"{dir}{filename}.toml").get(param_name, default)
    return default


def plot_and_save(filepath, x_y_data, curve=None, label='', curve_name=''):
    x_data = x_y_data[:,0]
    y_data = x_y_data[:,1]

    x_line = np.linspace(min(x_data), max(x_data), 5000) # default resolution of 500 for now
    _, ax = plt.subplots()
    ax.plot(x_data, y_data, 'o', label=label)
    if curve:
        ax.plot(x_line, curve(x_line), '-', label=curve_name)

    ax.legend()
    plt.savefig(filepath, dpi=1000)
    

def plot_and_save_3d(filepath, xyz_data):
        measurements = np.array(xyz_data)
        x = measurements[:,0]
        y = measurements[:,1]
        z = measurements[:,2]

        fig, ax = plt.subplots(figsize=(6, 4), facecolor='white')
        ax.set_facecolor('white')  # axes background
        sc = ax.scatter(x, y, c=z)
        fig.colorbar(sc, ax=ax, label="z")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        fig.canvas.draw()

        plt.savefig(filepath, dpi=300)