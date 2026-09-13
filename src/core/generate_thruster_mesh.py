#!/usr/bin/env python3
import os
from solid import scad_render, cylinder, cube, union, difference

class LgmThrusterPodGenerator:
    """
    Procedurally compiles the 12.5-meter Vortex Resonance Cylinder 
    integrated with an F-15/F-22 variable ramp air intake profile.
    """
    def __init__(self):
        self.cylinder_diameter_mm = 12500.0  # 12.5-meter specification matching BB-67
        self.cylinder_radius_mm = self.cylinder_diameter_mm / 2.0
        self.output_dir = "gantry_templates"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_canister_geometry(self) -> str:
        """Shapes the external armored pod housing containing the F-18 style intake geometry."""
        # 1. Main 12.5m Vortex Resonance Core
        resonance_core = cylinder(r=self.cylinder_radius_mm, h=8000, segments=120)
        inner_vacuum_bore = cylinder(r=self.cylinder_radius_mm - 300, h=8002, segments=120)
        
        # 2. F-15/F-22 Style Variable Ramp Compression Intake Module
        variable_intake_ramp = cube([self.cylinder_diameter_mm + 1000, 4000, 3000], center=True)
        
        # Assemble complete structural canister pod assembly
        complete_canister_pod = difference()(
            union()(
                resonance_core,
                variable_intake_ramp
            ),
            inner_vacuum_bore
        )
        
        output_file_path = os.path.join(self.output_dir, "lgm_canister_propulsion_pod.scad")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write("// --- UNIVAC IX AUTOMATED MULTI-PARTY LGM MODULE MESH ---\n")
            f.write(scad_render(complete_canister_pod))
            
        return output_file_path

if __name__ == "__main__":
    generator = LgmThrusterPodGenerator()
    print(f"[+] Procedural SCAD model built: {generator.generate_canister_geometry()}")
