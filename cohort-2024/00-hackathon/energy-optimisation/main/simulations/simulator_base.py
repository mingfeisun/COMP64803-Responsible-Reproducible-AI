"""
simulator_base.py
=================

This module defines a base class, `SimulatorBase`, for simulating power 
outputs and associated costs over a specified time range. The class 
includes functionality for generating skewed random numbers, plotting 
power data, and accessing specific hourly cost/power/demand values.

Classes
-------
SimulatorBase
    The abstract base class for all power generator simulations.

Examples
--------
>>> from simulator_base import SimulatorBase
>>> # Since SimulatorBase is abstract, you would typically inherit from it:
>>> class ExampleSimulator(SimulatorBase):
...     def power_output(self):
...         # Implement the abstract method here
...         pass
"""

from abc import abstractmethod
import numpy as np
import matplotlib.pyplot as plt


class SimulatorBase:
    """
    Simulator base class for source node power simulation.

    This abstract class provides attributes and methods common to
    all power source simulators, including:
      - a time range for the simulation,
      - arrays for power output and associated costs,
      - methods for plotting and data retrieval.

    Parameters
    ----------
    time_range : int, optional
        The number of hours over which to generate simulator values.
        Defaults to 24.

    Attributes
    ----------
    time_range : int
        The number of hours for the simulation.
    power_outputs : ndarray or None
        Array of power output values over the time range (in kW).
        Populated by the child class's `power_output` method.
    cost_outputs : ndarray or None
        Array of the power costs over the time range (in USD).
        Populated by the child class's `power_output` method.
    capital_cost : float or None
        The initial infrastructure cost (in USD), if applicable.
    power_demands : ndarray or None
        Array of the power demand values over the time range, if relevant
        (for simulation classes that handle demand as well).
    """

    def __init__(self, time_range: int = 24):
        """
        Initialize the simulator base class.

        Parameters
        ----------
        time_range : int, optional
            The number of hours for which the simulation runs. 
            Defaults to 24.
        """
        self.time_range = time_range
        self.power_outputs = None
        self.cost_outputs = None
        self.capital_cost = None
        self.power_demands = None

    @staticmethod
    def skewed_random(low: int, high: int, skew_factor: float = 0.65) -> int:
        """
        Generate a skewed random number, favoring higher values within a range.

        Uses a Beta distribution to skew towards higher values in the
        specified range.

        Parameters
        ----------
        low : int
            The minimum value of the generated random number.
        high : int
            The maximum value of the generated random number.
        skew_factor : float, optional
            Determines the skew of the distribution. 
            A higher skew factor (> 0.5) biases towards the higher end of the range.
            Default is 0.65.

        Returns
        -------
        int
            A randomly generated integer within the specified range.
        """
        return int(
            low
            + (high - low)
            * np.random.beta(skew_factor * 5, (1 - skew_factor) * 5)
        )

    def plot_power_data(self, title: str, label: str, savepath: str):
        """
        Plot the power output data and save the figure.

        This method creates a simple line plot of hourly power output 
        over the specified time range. It also prints the total capital 
        cost, hourly cost array, and hourly power output array to the console.

        Parameters
        ----------
        title : str
            The title of the plot.
        label : str
            The label for the power output line on the plot legend.
        savepath : str
            The filesystem path to save the plot image as a PNG file.

        Notes
        -----
        This method expects that `self.power_outputs`, `self.cost_outputs`, 
        and `self.capital_cost` have been populated by the subclass’s 
        `power_output` method before being called. Otherwise, it may 
        produce incorrect or empty plots.
        """
        plt.figure(figsize=(10, 5))
        plt.plot(
            range(self.time_range),
            self.power_outputs,
            marker='o',
            linestyle='-',
            label=label
        )
        plt.xlabel('Hour')
        plt.ylabel('Power Output (kW)')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.savefig(savepath, format='png')
        plt.close()  # Closes the figure to free memory and avoid display issues

        # Print cost and power output information
        print(f"Total Capital Cost: ${self.capital_cost:,}")
        print(f"Hourly Cost Array: {self.cost_outputs}")
        print(f"Hourly Power Output Array: {self.power_outputs}")

    @abstractmethod
    def power_output(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Compute the output for a given simulator (to be implemented by subclass).

        Subclasses must define how power output and costs are calculated.

        Returns
        -------
        tuple of (np.ndarray, np.ndarray)
            A tuple of arrays corresponding to:
              - The power output over the time range (in kW).
              - The associated power cost over the time range (in USD).
        """
        pass

    def get_cost_at_index(self, hour: int) -> float:
        """
        Retrieve the cost at a specific hour index.

        Parameters
        ----------
        hour : int
            The hour index within the simulation time range.

        Returns
        -------
        float
            The cost at the specified hour index.

        Raises
        ------
        IndexError
            If the provided hour index is out of bounds.
        """
        return self.cost_outputs[hour]

    def get_power_at_index(self, hour: int) -> float:
        """
        Retrieve the power output at a specific hour index.

        Parameters
        ----------
        hour : int
            The hour index within the simulation time range.

        Returns
        -------
        float
            The power output (in kW) at the specified hour index.

        Raises
        ------
        IndexError
            If the provided hour index is out of bounds.
        """
        return self.power_outputs[hour]

    def get_power_demand_at_index(self, hour: int) -> float:
        """
        Retrieve the power demand at a specific hour index.

        This is relevant only for simulators that also track 
        demand values (e.g., consumer-side simulations).

        Parameters
        ----------
        hour : int
            The hour index within the simulation time range.

        Returns
        -------
        float
            The power demand at the specified hour index.

        Raises
        ------
        IndexError
            If the provided hour index is out of bounds or if
            `power_demands` is None.
        """
        return self.power_demands[hour]

    def get_costs(self, power, lcoe): 
        return power * lcoe 