#!/usr/bin/env python3
import os
from solid import scad_render, cylinder, cube, union, difference, translate, rotate

class ResonantVectorNozzleGenerator:
    """
    Procedurally compiles an exhaust tunnel whose dimensions match the resonant
    wavelengths of the engine, integrated with F-22 Raptor style 2D thrust vectoring flaps.
    """
    def __init__(self, fundamental_frequency_hz: float = 13.72):
        self.speed_of_sound_m_s = 343.0
        self.frequency = fundamental_frequency_hz
        
        # Calculate precise resonant half-wavelength dimension (scaled to millimeters)
        self.wavelength_mm = (self.speed_of_sound_m_s / self.frequency) * 1000.0
        self.tunnel_length_mm = self.wavelength_mm / 2.0  # fundamental n=1 resonance node
        
        # Hard anchor diameter bound to the 12.5-meter Montana spec
        self.tunnel_diameter_mm = 12500.0
        self.output_dir = "gantry_templates"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def compile_nozzle_mesh(self) -> str:
        """Generates the acoustically-tuned exhaust chamber and 2D vectoring vector flaps."""
        # 1. Main Resonant Tunnel Core Shell
        outer_shell = cylinder(r=(self.tunnel_diameter_mm / 2.0) + 250, h=self.tunnel_length_mm, segments=120)
        inner_bore = cylinder(r=self.tunnel_diameter_mm / 2.0, h=self.tunnel_length_mm + 4, segments=120)
        
        # 2. Upper and Lower Lockheed Raptor-style 2D Vectoring Flaps
        upper_flap = translate([0, (self.tunnel_diameter_mm / 2.0), self.tunnel_length_mm])(
            rotate([5, 0, 0])(cube([self.tunnel_diameter_mm, 400, 2000], center=True))
        )
        lower_flap = translate([0, -(self.tunnel_diameter_mm / 2.0), self.tunnel_length_mm])(
            rotate([-5, 0, 0])(cube([self.tunnel_diameter_mm, 400, 2000], center=True))
        )
        
        complete_nozzle = difference()(
            union()(outer_shell, upper_flap, lower_flap),
            translate([0, 0, -2])(inner_bore)
        )
        
        output_path = os.path.join(self.output_dir, "resonant_vector_nozzle.scad")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"// --- UNIVAC IX AUTOMATED WAVE-TUNNEL MATRIX ---\n")
            f.write(f"// Target Fundamental Resonance: {self.frequency} Hz\n")
            f.write(f"// Calculated Tunnel Length   : {self.tunnel_length_mm:.4f} mm\n")
            f.write(scad_render(complete_nozzle))
            
        return output_path

if __name__ == "__main__":
    # Deploys standard 13.72Hz motor acoustic node calibration tracking matching BB-67 core harmonics
    generator = ResonantVectorNozzleGenerator(fundamental_frequency_hz=13.72)
    print(f"[+] Resonant vector nozzle SCAD generated at: {generator.compile_nozzle_mesh()}")
