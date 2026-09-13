#!/usr/bin/env python3
import os
from solid import scad_render, cylinder, cube, union, difference, translate, rotate

class FinalPiezoThrusterPodGenerator:
    """
    Procedurally compiles the entire production-ready LGM Canister Pod.
    Embeds dedicated internal slots for solid-state PZT crystal sub-plates.
    """
    def __init__(self, fundamental_frequency_hz: float = 13.72):
        self.speed_of_sound_m_s = 343.0
        self.frequency = fundamental_frequency_hz
        
        # Calculate resonant half-wavelength dimension for the exhaust path
        self.wavelength_mm = (self.speed_of_sound_m_s / self.frequency) * 1000.0
        self.nozzle_length_mm = self.wavelength_mm / 2.0  
        
        self.cylinder_diameter_mm = 12500.0  # 12.5-meter Montana Core Baseline
        self.cylinder_radius_mm = self.cylinder_diameter_mm / 2.0
        self.output_dir = "gantry_templates"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def compile_production_canister_mesh(self) -> str:
        """Assembles the complete hull geometry with integrated solid-state crystal slots."""
        # 1. Main 12.5m Vortex Resonance Cylinder Body
        resonance_body = cylinder(r=self.cylinder_radius_mm, h=8000, segments=120)
        inner_vacuum_bore = cylinder(r=self.cylinder_radius_mm - 300, h=8004, segments=120)
        
        # 2. Forward F-15/F-22 Style Variable Ramp Compression Intake
        variable_intake = translate([0, 0, -1500])(
            cube([self.cylinder_diameter_mm + 1000, 4000, 3000], center=True)
        )
        
        # 3. Trailing Resonant Exhaust Tunnel Shell
        nozzle_shell = cylinder(r=self.cylinder_radius_mm, h=self.nozzle_length_mm, segments=120)
        
        # 4. Embedded PZT Crystalline Array Mounting Slots (Radial Matrix)
        pzt_slot_width = 1200.0
        pzt_slot_depth = 150.0
        pzt_slot_height = 2000.0
        
        piezo_cutouts = union()
        for angle in range(0, 360, 45):  # 8 radial control vectors
            piezo_cutouts += rotate([0, 0, angle])(
                translate([self.cylinder_radius_mm - 200, 0, self.nozzle_length_mm * 0.3])(
                    cube([pzt_slot_depth, pzt_slot_width, pzt_slot_height], center=True)
                )
            )

        # Merge modules and hollow out the internal exhaust gas flow path
        nozzle_with_slots = difference()(
            nozzle_shell,
            cylinder(r=self.cylinder_radius_mm - 300, h=self.nozzle_length_mm + 4, segments=120),
            piezo_cutouts
        )

        complete_hardware_pod = difference()(
            union()(resonance_body, variable_intake, translate([0, 0, 8000])(nozzle_with_slots)),
            translate([0, 0, -2])(inner_vacuum_bore)
        )
        
        output_file_path = os.path.join(self.output_dir, "production_lgm_canister_pod.scad")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(f"// --- UNIVAC IX AUTOMATED SOLID-STATE PIEZO MESH ---\n")
            f.write(f"// Target Fundamental Frequency: {self.frequency} Hz\n")
            f.write(scad_render(complete_hardware_pod))
            
        return output_file_path

if __name__ == "__main__":
    generator = FinalPiezoThrusterPodGenerator(fundamental_frequency_hz=13.72)
    generator.compile_production_canister_mesh()
