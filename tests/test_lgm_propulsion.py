import pytest
import os
import numpy as np
from src.core.generate_thruster_mesh import LgmThrusterPodGenerator
from src.core.lgm_controller import LgmEcosystemController

def test_procedural_lgm_canister_mesh_generation(tmpdir):
    generator = LgmThrusterPodGenerator()
    generator.output_dir = str(tmpdir)
    
    scad_file = generator.generate_canister_geometry()
    assert os.path.exists(scad_file)
    with open(scad_file, "r") as f:
        content = f.read()
    assert "cylinder" in content
    assert "cube" in content

def test_lgm_precision_stacking_logic():
    controller = LgmEcosystemController()
    mock_telemetry_bus = np.array([0.1, 0.5, 0.9], dtype=np.float32)
    
    # Evaluate under an LGM-35 high-multiplier setup
    result = controller.bridge_lgm_spec_array(mock_telemetry_bus, spec_multiplier=1.0)
    
    assert result["origin"] == "LGM_ECOSYSTEM_CONTROLLER"
    assert result["mean_voltage_signal"] == pytest.approx(0.5, abs=1e-4)
    assert result["hex_voltage_state"] == "0.8V"  # 0.5V maps directly to intermediate State 8
