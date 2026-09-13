import pytest
import os
import numpy as np
from src.core.generate_vector_nozzle import ResonantVectorNozzleGenerator
from src.core.vector_controller import ResonantVectorController

def test_procedural_nozzle_mesh_io(tmpdir):
    generator = ResonantVectorNozzleGenerator(fundamental_frequency_hz=13.72)
    generator.output_dir = str(tmpdir)
    
    scad_file = generator.compile_nozzle_mesh()
    assert os.path.exists(scad_file)
    with open(scad_file, "r") as f:
        content = f.read()
    assert "cylinder" in content
    assert "cube" in content

def test_resonant_vector_efficiency_tracking():
    controller = ResonantVectorController(fundamental_frequency=13.72)
    
    # Test perfect resonant tunnel matches (12500.0mm at fundamental node)
    perfect_length_bus = np.array([12500.0, 12500.0, 12500.0], dtype=np.float32)
    
    result = controller.process_vector_adjustment_bus(perfect_length_bus, current_pitch_deg=15.0)
    
    assert result["origin"] == "RESONANT_VECTOR_CONTROLLER"
    assert result["nozzle_wave_efficiency_ratio"] > 0.90
    assert result["bridge_interlock_status"] == "NOMINAL_VECTOR_STABLE"
    assert result["hex_voltage_state"] in ["0.EV", "0.FV"]
