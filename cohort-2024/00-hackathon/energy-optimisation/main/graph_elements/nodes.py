"""
nodes.py
========

This module defines various types of nodes for an energy network, including:
- A base `Node` class (with support for connections to other nodes).
- A `SinkNode` class representing a consumer (e.g., city).
- A family of source node classes (`SourceNode`, `Solar`, `Wind`, and `Gas`)
  for simulating different types of power generation.

Examples
--------
>>> from nodes import SinkNode, Solar, Wind, Gas
>>> # Create a sink node
>>> city_node = SinkNode(node_id="CityA", time_range=24, cartesian_coordinates=(0, 0), econ_coefficient=1.2)
>>> # Create a solar node
>>> solar_node = Solar(name="SolarFarm1", time_range=24, cartesian_coordinates=(1, 1))
>>> 
>>> # Access demand or power output
>>> demand_hour_0 = city_node.get_demand(0)
>>> solar_power_hour_0 = solar_node.get_power_output(0)
"""

import numpy as np
from abc import abstractmethod
from simulations.simulator_base import SimulatorBase
from simulations.source_simulators import GasPowerSimulator, WindPowerSimulator, SolarPowerSimulator
from simulations.sink_simulators import CityPowerDemandSimulator


class Node:
    """
    A basic node in the energy network.

    This class serves as the foundational node entity in the network,
    storing identifying information, geographic coordinates, and
    connections to other nodes.

    Parameters
    ----------
    node_id : Hashable
        A unique identifier for the node (e.g., string, int).
    time_range : int
        The number of hours over which the simulation or data collection runs.
    cartesian_coordinates : tuple of float
        The x, y coordinates of this node's location in a 2D plane.

    Attributes
    ----------
    node_id : Hashable
        The node's unique identifier.
    time_range : int
        The total hours in the simulation.
    cartesian_coordinates : tuple of float
        The (x, y) location of this node.
    connections : list
        A list of Connection objects leading from this node to other nodes.
    connections_ids : list
        A list of the connected nodes' identifiers.
    """

    def __init__(self, node_id, time_range, cartesian_coordinates):
        """
        Initialize a Node with an ID, time range, and 2D coordinates.

        Parameters
        ----------
        node_id : Hashable
            A unique identifier for this node.
        time_range : int
            The number of hours for which the simulation is run.
        cartesian_coordinates : tuple of float
            The x, y coordinates of this node in the network.
        """
        self.node_id = node_id
        self.time_range = time_range
        self.cartesian_coordinates = cartesian_coordinates
        self.connections = []
        self.connections_ids = []

    def set_connection(self, connection, node_id):
        """
        Establish a connection from this node to another node.

        Parameters
        ----------
        connection : Connection
            An object representing the connection properties to another node
            (e.g., capacity, distance, or transmission coefficient).
        node_id : Hashable
            The identifier of the node being connected to.

        Returns
        -------
        None
        """
        self.connections.append(connection)
        self.connections_ids.append(node_id)


class SinkNode(Node):
    """
    Represents a power demand location (e.g., city, town).

    A sink node simulates or records hourly power demand data. It uses
    a `CityPowerDemandSimulator` internally to generate a demand profile.

    Parameters
    ----------
    node_id : Hashable
        A unique identifier for the sink node.
    time_range : int
        The number of hours over which the simulation or data collection runs.
    cartesian_coordinates : tuple of float
        The x, y coordinates of this node's location in a 2D plane.
    econ_coefficient : float
        A penalty or weighting factor applied when power supply fails
        to meet demand (used in economic calculations).

    Attributes
    ----------
    simulator : CityPowerDemandSimulator
        An instance of the city demand simulator.
    econ_coefficient : float
        The penalty factor for supply deficits.
    demand_profile : ndarray
        The hourly power demand in MW for each hour of the simulation.
    """

    def __init__(self, node_id, time_range, cartesian_coordinates, econ_coefficient):
        """
        Initialize the sink node with a city demand simulator.

        Parameters
        ----------
        node_id : Hashable
            A unique identifier for the sink node.
        time_range : int
            The number of hours in the simulation.
        cartesian_coordinates : tuple of float
            The x, y coordinates of this node.
        econ_coefficient : float
            The penalty/weighting factor for supply deficits.
        """
        super().__init__(node_id, time_range, cartesian_coordinates)
        self.simulator = CityPowerDemandSimulator(time_range)
        self.simulator.power_demand()
        self.econ_coefficient = econ_coefficient
        self.demand_profile = self.get_demand_series()

    def get_demand(self, hour):
        """
        Retrieve the power demand at a specified hour.

        Parameters
        ----------
        hour : int
            The hour of interest (0-based).

        Returns
        -------
        float
            The demand in MW at the given hour index.
        """
        return self.simulator.get_power_at_index(hour)

    def get_demand_series(self):
        """
        Retrieve the entire demand profile for this sink node.

        Returns
        -------
        ndarray
            Hourly power demand (MW) for each hour in the simulation.
        """
        return self.simulator.hourly_demand

    def node_type(self):
        """
        Identify the node type.

        Returns
        -------
        str
            The string `'sink'` for this node type.
        """
        return 'sink'


class SourceNode(Node):
    """
    Base class for power-generating nodes (sources).

    This class initializes a generic simulator (from `SimulatorBase`) 
    and stores overall LCOE and total power output arrays. Subclasses
    override the simulator with a specific power source simulator.

    Parameters
    ----------
    node_id : Hashable
        A unique identifier for the source node.
    time_range : int
        The number of hours in the simulation.
    cartesian_coordinates : tuple of float
        The (x, y) location of this node.

    Attributes
    ----------
    simulator : SimulatorBase
        The generic power generation simulator instance.
    lcoe : ndarray
        The array of levelized cost of electricity (in $/MWh) for each hour.
    total_power : ndarray
        The array of generated power (in MW) for each hour.
    """

    def __init__(self, node_id, time_range, cartesian_coordinates):
        """
        Initialize a source node with a base simulator.

        Parameters
        ----------
        node_id : Hashable
            A unique identifier for this source node.
        time_range : int
            The number of hours for which the simulation is run.
        cartesian_coordinates : tuple of float
            The (x, y) location for this node.
        """
        super().__init__(node_id, time_range, cartesian_coordinates)
        self.simulator = SimulatorBase(time_range)
        # Abstract method call: child classes normally override the simulator
        # But we call it here to populate arrays if possible
        self.simulator.power_output()

        self.lcoe = self.get_lcoe_output_series()
        self.total_power = self.get_power_output_series()

    def get_power_output(self, hour):
        """
        Retrieve the power output at a given hour.

        Parameters
        ----------
        hour : int
            The hour index.

        Returns
        -------
        float
            Power output (MW) at the specified hour.
        """
        return self.total_power[hour]

    def get_lcoe_output(self, hour):
        """
        Retrieve the LCOE at a given hour.

        Parameters
        ----------
        hour : int
            The hour index.

        Returns
        -------
        float
            Levelized Cost of Electricity (in $/MWh) at that hour.
        """
        return self.lcoe[hour]

    def get_power_output_series(self):
        """
        Get the entire power output series.

        Returns
        -------
        ndarray
            Hourly power output array (in MW).
        """
        return self.simulator.power_outputs

    def get_lcoe_output_series(self):
        """
        Get the entire LCOE series.

        Returns
        -------
        ndarray
            Hourly LCOE array (in $/MWh).
        """
        return self.simulator.cost_outputs


class Solar(SourceNode):
    """
    A solar power source node.

    Inherits from `SourceNode` but overrides the simulator with
    a `SolarPowerSimulator`.

    Parameters
    ----------
    name : Hashable
        A unique identifier for this solar node.
    time_range : int
        Number of hours in the simulation.
    cartesian_coordinates : tuple of float
        The (x, y) coordinates for this node.

    Attributes
    ----------
    simulator : SolarPowerSimulator
        The solar-specific simulator for power generation.
    """

    def __init__(self, name, time_range, cartesian_coordinates):
        """
        Initialize a solar node with a solar-specific simulator.

        Parameters
        ----------
        name : Hashable
            A unique identifier for this solar node.
        time_range : int
            Number of hours for the simulation.
        cartesian_coordinates : tuple of float
            (x, y) coordinates of the node.
        """
        super().__init__(name, time_range, cartesian_coordinates)
        self.simulator = SolarPowerSimulator(time_range)
        self.simulator.power_output()


class Wind(SourceNode):
    """
    A wind power source node (onshore or offshore).

    Inherits from `SourceNode` but overrides the simulator with
    a `WindPowerSimulator`.

    Parameters
    ----------
    name : Hashable
        A unique identifier for the wind node.
    time_range : int
        The number of hours for the simulation.
    cartesian_coordinates : tuple of float
        The (x, y) coordinates for this node.
    offshore : bool
        If True, this node represents an offshore wind farm; if False,
        an onshore wind farm.

    Attributes
    ----------
    simulator : WindPowerSimulator
        The wind-specific simulator (onshore or offshore) for power generation.
    """

    def __init__(self, name, time_range, cartesian_coordinates, offshore):
        """
        Initialize a wind node with a wind-specific simulator.

        Parameters
        ----------
        name : Hashable
            A unique identifier for this wind node.
        time_range : int
            The number of hours in the simulation.
        cartesian_coordinates : tuple of float
            (x, y) coordinates of the node.
        offshore : bool
            True if this is an offshore wind node, otherwise onshore.
        """
        super().__init__(name, time_range, cartesian_coordinates)
        self.simulator = WindPowerSimulator(time_range, offshore)
        self.simulator.power_output()


class Gas(SourceNode):
    """
    A gas-powered source node.

    Inherits from `SourceNode` but overrides the simulator with
    a `GasPowerSimulator`.

    Parameters
    ----------
    name : Hashable
        A unique identifier for the gas node.
    time_range : int
        The number of hours for the simulation.
    cartesian_coordinates : tuple of float
        (x, y) coordinates of the node.

    Attributes
    ----------
    simulator : GasPowerSimulator
        The gas-specific simulator for power generation.
    """

    def __init__(self, name, time_range, cartesian_coordinates):
        """
        Initialize a gas node with a gas-specific simulator.

        Parameters
        ----------
        name : Hashable
            A unique identifier for this gas node.
        time_range : int
            The number of hours for the simulation.
        cartesian_coordinates : tuple of float
            (x, y) coordinates of the node.
        """
        super().__init__(name, time_range, cartesian_coordinates)
        self.simulator = GasPowerSimulator(time_range)
        self.simulator.power_output()
