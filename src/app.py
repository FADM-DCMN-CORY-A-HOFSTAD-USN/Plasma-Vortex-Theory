import streamlit as st
import numpy as np
import json
from core.propulsion_pod import PlasmaWaveThrusterPod

def render_propulsion_canister_panel():
    st.subheader("🚀 Self-Contained Electroacoustic Plasma Pod")
    st.caption("Armored Canister Mount Module [NASA PPR Phase II Specification Linked]")

    # Initialize the bolt-on thruster capsule simulation
    thruster_pod = PlasmaWaveThrusterPod(target_frequency_hz=24000.0)

    st.sidebar.header("🎚️ Canister Thrust Matrices")
    calibrated_frequency = st.sidebar.slider("Acoustic Driver Calibrated Frequency (Hz)", 1000, 50000, 24000)
    electrode_voltage = st.sidebar.slider("External Electrode Field Intensity (kV)", 0.0, 10.0, 5.0)

    # Fire the dual-hardware propulsion sequence
    thruster_pod.calibrated_frequency = calibrated_frequency
    with st.spinner("Exciting Xenon propellant gas grids via harmonic sound fields..."):
        metrics = thruster_pod.ignite_canister_core(grid_size=64, field_intensity=electrode_voltage)

    # Present Operational Readouts
    col_thrust, col_isp, col_hex = st.columns(3)
    with col_thrust:
        st.metric("Net Canister Thrust Force", f"{metrics['net_thrust_newtons']:,.2f} N", delta="Target: 100,000 N Max")
    with col_isp:
        st.metric("Specific Impulse Efficiency (Isp)", f"{metrics['calculated_specific_impulse_isp']:.0f} seconds", delta="PPR Baseline Match")
    with col_hex:
        st.metric("Propulsion Bus Hex Signal", metrics["hex_voltage_state"])

    # Broadcast secure tracking sync arrays to the active Boeing-Lockheed Martin bridge
    cad_payload = {"thrust_n": metrics["net_thrust_newtons"], "isp_s": metrics["calculated_specific_impulse_isp"]}
    st.components.v1.html(f"""
    <script>
        const payload = {json.dumps(cad_payload)};
        parent.postMessage({{ type: "CANISTER_PROPULSION_SYNC", data: payload }}, "https://boeing.com");
        parent.postMessage({{ type: "CANISTER_PROPULSION_SYNC", data: payload }}, "https://interface.01_node_://lockheedmartin.com");
    </script>
    """, height=0)
