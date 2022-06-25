import matplotlib.pyplot as plot
import matplotlib.ticker as mtick
import numpy as np


def calculate_darea(desired_array, reference_array):
    """
    Calculates delta area as da = (area2 - area1) / area1

    :param desired_array: To get area2
    :param reference_array: To get area1
    :return: delta area
    """
    last_area = np.count_nonzero(desired_array)
    reference_area = np.count_nonzero(reference_array)
    delta_area = (last_area - reference_area) / reference_area
    return delta_area


def get_delta_area_list(x, y):
    """
    Get lists of dates and delta areas with respect to first image

    :param x: dates data
    :param y: image list
    :return: (list_of_dates, list_of_delta_areas)
    """
    dates = []
    areas = []
    y_prev = y[0]
    for value in range(0, len(x)):
        dates.append(x[value][0])
        areas.append(calculate_darea(y[value], y_prev) * 100)
    return dates, areas


def plot_dareas(dates, areas):
    """
    Plot delta areas vs dates
    :param dates: list of dates for x axis
    :param areas: list of areas for y axis
    :return:
    """
    fig, ax = plot.subplots()
    ax.bar(dates, areas, width=1, edgecolor="white", linewidth=0.7)
    ax.set(title="Area increment with respect to first year", xlabel="year", ylabel="area increment")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plot.show()
    return
