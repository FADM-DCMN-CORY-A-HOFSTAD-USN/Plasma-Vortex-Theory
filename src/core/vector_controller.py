import numpy as np
from numba import njit, prange

@njit(parallel=True, fastmath=True)
def optimize_acoustic_exhaust_deflection(frequency, current_length, pitch_angle_deg):
    """
    Multi-core parallel CPU engine. Calculates standing wave preservation ratios
    during mechanical 2D vector nozzle mechanical pitch adjustments.
    """
    speed_of_sound = 343.0
    wavelength = speed_of_sound / frequency
    ideal_resonant_length = wavelength / 2.0
    
    # Calculate dimensional deviation error caused by mechanical nozzle movement
    length_meters = current_length / 1000.0
    length_deviation = np.abs(ideal_resonant_length - length_meters)
    
    # Standing wave attenuation factor increases if tunnel skews off harmonic peaks
    attenuation_factor = 1.0 - (length_deviation * np.cos(np.radians(pitch_angle_deg)))
    if attenuation_factor < 0.0:
        attenuation_factor = 0.0
        
    return attenuation_factor

class ResonantVectorController:
    def __init__(self, fundamental_frequency: float = 13.72):
        self.freq = fundamental_frequency
        self.voltage_steps = np.linspace(0.0, 1.0, 16)

    def process_vector_adjustment_bus(self, active_lengths_mm: np.ndarray, current_pitch_deg: float) -> dict:
        """Evaluates wave preservation metrics across the active nozzle stream arrays."""
        length = len(active_lengths_mm)
        attenuation_signals = np.zeros(length, dtype=np.float32)
        
        for i in prange(length):
            attenuation_signals[i] = optimize_acoustic_exhaust_deflection(self.freq, active_lengths_mm[i], current_pitch_deg)
            
        mean_efficiency = np.mean(attenuation_signals)
        
        # Enforce hard safety shutdown if acoustic dampening drops below critical limits
        if mean_efficiency < 0.75:
            status = "CRITICAL_ACOUSTIC_DAMPENING_WARNING"
            voltage_out = 0.0
        else:
            status = "NOMINAL_VECTOR_STABLE"
            voltage_out = mean_efficiency

        closest_idx = (np.abs(self.voltage_steps - voltage_out)).argmin()
        hex_voltage_state = hex(closest_idx)[2:].upper()

        return {
            "origin": "RESONANT_VECTOR_CONTROLLER",
            "nozzle_wave_efficiency_ratio": mean_efficiency,
            "hex_voltage_state": f"0.{hex_voltage_state}V",
            "bridge_interlock_status": status,
            "structural_conformity": True if mean_efficiency >= 0.75 else False
        }
