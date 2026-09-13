import pytest
import numpy as np
from src.core.propulsion_efficiency import PropulsionEfficiencyController

def test_propulsion_efficiency_fuel_reduction():
    controller = PropulsionEfficiencyController()
    
    # Emulate incoming pre-compressed gas streams (3 atmospheres of pressure)
    mock_pressure_bus = np.array([303.975, 303.975, 303.975], dtype=np.float32)
    
    # Evaluate under a high-intensity UV photoionization field (5.0 units)
    efficiency_data = controller.optimize_bridge_thrust_efficiency(
        simulated_pressures=mock_pressure_bus,
        uv_lux_intensity=5.0,
        nominal_flow_kg_s=10.0
    )
    
    assert efficiency_data["origin"] == "PROPULSION_EFFICIENCY_CONTROLLER"
    # Ensure fuel consumption significantly drops when UV-C systems are engaged
    assert efficiency_data["chemical_fuel_mass_saved_percentage"] > 50.0
    assert efficiency_data["hex_voltage_state"] == "0.BV"  # Significant reduction maps to high hex state
