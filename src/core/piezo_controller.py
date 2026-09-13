import numpy as np
from numba import njit, prange

@njit(parallel=True, fastmath=True)
def calculate_solid_state_piezo_dynamics(strain_array, input_voltage_matrix, mode):
    """
    Multi-core parallel CPU kernel processing solid-state crystal responses.
    Mode 0: Stress-to-Cooling (Peltier Harvest Loop)
    Mode 1: Voltage-to-Acoustic-Deflection (Reverse Vectoring Loop)
    """
    length = len(strain_array)
    output_metrics = np.zeros(length, dtype=np.float32)
    
    for i in prange(length):
        if mode == 0:
            # Mode 0: Convert mechanical bending strain directly to Peltier cooling watts
            harvested_volts = np.abs(strain_array[i]) * 0.15
            cooling_watts = harvested_volts * 2.4  # Peltier efficiency multiplier
            output_metrics[i] = cooling_watts
        else:
            # Mode 1: Convert input hex logic voltage to physical boundary layer deflection mm
            applied_voltage = input_voltage_matrix[i]
            boundary_deflection_mm = applied_voltage * 0.045  # Micro-inch crystalline expansion
            output_metrics[i] = boundary_deflection_mm
            
    return output_metrics

class PiezoThermoelectricController:
    """
    Manages solid-state PZT crystal arrays for concurrent exhaust cooling 
    and acoustic boundary layer steering.
    """
    def __init__(self):
        self.voltage_steps = np.linspace(0.0, 1.0, 16)

    def evaluate_piezo_matrix(self, strain_bus: np.ndarray, hex_voltage_bus: np.ndarray, execution_mode: int) -> dict:
        """Processes crystal responses and outputs the native 16-state hexadecimal state."""
        results = calculate_solid_state_piezo_dynamics(strain_bus, hex_voltage_bus, execution_mode)
        mean_value = np.mean(results)
        
        # Normalize and map states directly to the 0.0V-1.0V backplane bus
        normalized_index = min(1.0, max(0.0, mean_value / 50.0 if execution_mode == 0 else mean_value / 0.05))
        closest_idx = (np.abs(self.voltage_steps - normalized_index)).argmin()
        hex_voltage_state = hex(closest_idx)[2:].upper()

        status_string = "PIEZO_COOLING_ACTIVE" if execution_mode == 0 else "ACOUSTIC_VECTORING_ENGAGED"

        return {
            "origin": "PIEZO_THERMOELECTRIC_CONTROLLER",
            "active_mode": status_string,
            "calculated_mean_magnitude": mean_value,
            "hex_voltage_state": f"0.{hex_voltage_state}V",
            "structural_conformity": True
        }
