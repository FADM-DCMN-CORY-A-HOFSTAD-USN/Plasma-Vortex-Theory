import numpy as np
from numba import njit, prange

@njit(parallel=True, fastmath=True)
def calculate_fuel_offset_matrix(pressure_array, uv_intensity, base_fuel_flow):
    """
    Multi-core parallel CPU kernel tracking propellant mass reductions.
    Computes how much chemical fuel is saved by active photoionization grids.
    """
    length = len(pressure_array)
    optimized_flow_rates = np.zeros(length, dtype=np.float32)
    
    for i in prange(length):
        # Calculate compression efficiency from the variable ramp intake
        compression_factor = pressure_array[i] / 101.325  # Normalized against 1 atm
        
        # High ionization scales exhaust velocity, reducing mass flow rate demands
        mass_flow_reduction = 0.05 * compression_factor + (uv_intensity * 0.12)
        
        # Enforce maximum safety limits (Cap reduction at 85% to protect flight lines)
        safe_reduction = min(0.85, mass_flow_reduction)
        optimized_flow_rates[i] = base_fuel_flow * (1.0 - safe_reduction)
        
    return optimized_flow_rates

class PropulsionEfficiencyController:
    """
    Manages fuel-optimization vectors by blending atmospheric intake compression 
    ratios with cold plasma photoionization multipliers.
    """
    def __init__(self):
        self.voltage_steps = np.linspace(0.0, 1.0, 16)

    def optimize_bridge_thrust_efficiency(
        self, 
        simulated_pressures: np.ndarray, 
        uv_lux_intensity: float, 
        nominal_flow_kg_s: float
    ) -> dict:
        """Evaluates live fuel savings and maps the output to native 16-state hex logic."""
        optimized_flows = calculate_fuel_offset_matrix(simulated_pressures, uv_lux_intensity, nominal_flow_kg_s)
        
        mean_optimized_flow = np.mean(optimized_flows)
        total_fuel_saved_pct = ((nominal_flow_kg_s - mean_optimized_flow) / nominal_flow_kg_s) * 100.0
        
        # Convert performance metrics to native 0.0V-1.0V voltage levels
        normalized_index = min(1.0, max(0.0, total_fuel_saved_pct / 100.0))
        closest_idx = (np.abs(self.voltage_steps - normalized_index)).argmin()
        hex_voltage_state = hex(closest_idx)[2:].upper()

        return {
            "origin": "PROPULSION_EFFICIENCY_CONTROLLER",
            "mean_optimized_mass_flow_kg_s": mean_optimized_flow,
            "chemical_fuel_mass_saved_percentage": total_fuel_saved_pct,
            "hex_voltage_state": f"0.{hex_voltage_state}V",
            "structural_conformity": True
        }
