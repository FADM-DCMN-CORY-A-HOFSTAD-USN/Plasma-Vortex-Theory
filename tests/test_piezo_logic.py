import pytest
import numpy as np
from src.core.piezo_controller import PiezoThermoelectricController

def test_piezo_energy_harvesting_cooling():
    controller = PiezoThermoelectricController()
    
    # Emulate massive physical hull bending strains under sound loads
    mock_strain_bus = np.array([120.0, 150.0, 110.0], dtype=np.float32)
    empty_voltage = np.zeros(3, dtype=np.float32)
    
    output = controller.evaluate_piezo_matrix(mock_strain_bus, empty_voltage, execution_mode=0)
    
    assert output["origin"] == "PIEZO_THERMOELECTRIC_CONTROLLER"
    assert output["active_mode"] == "PIEZO_COOLING_ACTIVE"
    # Ensure active cooling magnitude scales correctly with mechanical input force
    assert output["calculated_mean_magnitude"] > 30.0  

def test_reverse_piezo_boundary_deflection():
    controller = PiezoThermoelectricController()
    
    # Input high hexadecimal logic voltage parameters (0.9375V step equivalent)
    mock_voltage_bus = np.array([0.9375, 0.9375, 0.9375], dtype=np.float32)
    empty_strain = np.zeros(3, dtype=np.float32)
    
    output = controller.evaluate_piezo_matrix(empty_strain, mock_voltage_bus, execution_mode=1)
    
    assert output["active_mode"] == "ACOUSTIC_VECTORING_ENGAGED"
    # Micro-inch structural deflections must remain bounded under sub-millimetric scales
    assert 0.01 <= output["calculated_mean_magnitude"] <= 0.05
