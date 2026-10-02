"""
city_power_demand_simulator.py
==============================

This module provides functionality to simulate 24-hour power demand 
for a given region in GWh using a 'duck curve' approach. It also provides 
a convenient method to visualize the simulated demand. 

The main class, `CityPowerDemandSimulator`, inherits from a base class 
`SimulatorBase` and allows users to generate hourly power demand data 
and plot it for inspection. 

Examples
--------
>>> from city_power_demand_simulator import CityPowerDemandSimulator
>>> simulator = CityPowerDemandSimulator(time_range=24)
>>> demand = simulator.power_demand()
>>> simulator.plot_data(demand)
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import random
from .simulator_base import SimulatorBase


class CityPowerDemandSimulator(SimulatorBase):
    """
    A simulator for power demand across various regions.

    This class simulates the hourly power demand for a typical 24-hour 
    period (or any specified number of hours) using region-specific 
    annual consumption data and a 'duck curve' shape. It applies 
    stochastic variations and ensures a minimum demand threshold.

    Parameters
    ----------
    time_range : int, optional
        The number of hours to simulate (default is 24).

    Attributes
    ----------
    time_range : int
        The total duration (in hours) for which power demand is simulated.
    hourly_demand : ndarray of shape (time_range,)
        The resulting array of hourly power demand values (in GWh). 
        Generated after calling `power_demand`.

    Examples
    --------
    >>> simulator = CityPowerDemandSimulator()
    >>> demand = simulator.power_demand()
    >>> simulator.plot_data(demand)
    """

    def __init__(self, time_range=24):
        """
        Initialize the power demand simulator.

        Parameters
        ----------
        time_range : int, optional
            The number of hours to simulate. Defaults to 24.
        """
        self.time_range = time_range
        self.hourly_demand = None

    def power_demand(self):
        """
        Generate the hourly power demand levels.

        This method:
            1. Selects a random region from a predefined list with 
               annual consumption data (in GWh).
            2. Computes the average hourly demand for that region.
            3. Generates a "duck curve" to shape demand variation 
               throughout the day.
            4. Applies random noise to simulate stochastic variations.
            5. Enforces a minimum demand threshold to avoid unrealistically 
               low values.

        Returns
        -------
        ndarray
            An array of shape (time_range,) representing the hourly 
            power demand in GWh.

        Examples
        --------
        >>> simulator = CityPowerDemandSimulator()
        >>> demand = simulator.power_demand()
        >>> demand.shape
        (24,)
        """
        # Annual electricity consumption in GWh
        annual_demand_gwh = {
            "East Midlands": 19_459,
            "East of England": 26_130,
            "Greater London": 39_337,
            "North East": 10_573,
            "North West": 31_519,
            "South East": 37_655,
            "South West": 23_551,
            "Yorkshire and The Humber": 21_865,
            "West Midlands": 22_839,
            "Scotland": 24_976,
            "Wales": 13_524,
            "England": 232_927,
            "Great Britain": 274_801
        }

        # 1. Select a random region
        region = random.choice(list(annual_demand_gwh.keys()))

        # 2. Calculate average hourly demand (GWh/hour)
        average_hourly_demand_gwh = annual_demand_gwh[region] / 8760

        # 3. Create a duck curve (peak in the afternoon)
        time = np.linspace(0, np.pi * 2, self.time_range)
        duck_curve = 0.9 + 1.1 * np.sin(time - np.pi/2) ** 3

        # Scale the curve so its mean matches the average hourly demand
        daily_demand = duck_curve / np.mean(duck_curve) * average_hourly_demand_gwh

        # 4. Apply stochastic variation (±5% random noise)
        noise = np.random.normal(1, 0.05, self.time_range)
        hourly_demand = daily_demand * noise

        # 5. Ensure no demand goes below 10% of the mean demand
        min_demand_threshold = 0.1 * average_hourly_demand_gwh
        hourly_demand = np.maximum(hourly_demand, min_demand_threshold) * 1e6

        self.hourly_demand = hourly_demand
        return hourly_demand

    def plot_data(self, hourly_demand):
        """
        Plot the hourly power demand data.

        This method plots the simulated hourly power demand data 
        and saves the plot to a local directory.

        Parameters
        ----------
        hourly_demand : ndarray
            The array of hourly power demand values (in GWh).

        Notes
        -----
        The figure is saved in the `../../data/figures` directory as 
        `power_demand.png`.

        Examples
        --------
        >>> simulator = CityPowerDemandSimulator()
        >>> demand = simulator.power_demand()
        >>> simulator.plot_data(demand)
        """
        savepath = '../../data/figures'
        os.makedirs(savepath, exist_ok=True)

        plt.figure(figsize=(10, 5))
        plt.plot(range(self.time_range), hourly_demand, marker='o', linestyle='-',
                 label='Hourly Power Demand (GWh)')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Power Demand (GWh)')
        plt.title('Hourly Power Demand')
        plt.legend()
        plt.grid(True)

        filepath = os.path.join(savepath, 'power_demand.png')
        plt.savefig(filepath)
        plt.show()

        print("Hourly demand:", hourly_demand)
