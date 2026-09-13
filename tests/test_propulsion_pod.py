import pytest
import numpy as np
from src.core.propulsion_pod import PlasmaWaveThrusterPod

def test_electroacoustic_canister_nominal_ignition():
    # Instantiate the bolt-on thruster engine core
    pod = PlasmaWaveThrusterPod(target_frequency_hz=24000.0)
    
    # Run a test loop using standard nominal parameters
    metrics = pod.ignite_canister_core(grid_size=32, field_intensity=4.0)
    
    assert metrics["origin"] == "CANISTER_THRUSTER_POD"
    assert metrics["calculated_specific_impulse_isp"] == 5000.0
    assert metrics["propulsion_status"] == "NOMINAL_PROPULSION_STABLE"
    assert metrics["structural_conformity"] is True

def test_electroacoustic_overthrust_limit():
    pod = PlasmaWaveThrusterPod(target_frequency_hz=48000.0)
    
    # Force extreme high external voltage field inputs
    metrics = pod.ignite_canister_core(grid_size=32, field_intensity=12.0)
    
    assert metrics["net_thrust_newtons"] <= 100000.0  # Confirm system handles limits safely
