#!/usr/bin/env python3
"""
CSV V2.6 Continuous SPARC Rotation Curve & Data Export Engine
Generates smooth velocity profiles from r = 0.5 kpc to outer halo bounds.
"""

import math

G = 6.67430e-11
c = 299792458.0
rho_0 = 5.0e-22
K_c = 1.0 / (8.0 * math.pi)
a0_csv = (K_c ** 2) * c * math.sqrt(2.0 * G * rho_0)

kpc_to_m = 3.08567758e19
km_to_m = 1000.0

# Representative galaxy baryonic mass profiles (M_bar(r) in solar masses)
def sample_baryon_mass(r_kpc, gal_type):
    if gal_type == "Dwarf":
        return 1.2e9 * (r_kpc / (r_kpc + 1.5))
    elif gal_type == "LSB":
        return 3.5e9 * (r_kpc / (r_kpc + 2.0))
    elif gal_type == "Spiral":
        return 4.5e10 * (r_kpc / (r_kpc + 3.0))
    elif gal_type == "Giant":
        M_sun = 1.98847e30
        return 1.8e11 * (r_kpc / (r_kpc + 5.0))
    return 1.0e10

def generate_curves():
    print("==============================================================================")
    print(" CSV V2.6 CONTINUOUS ROTATION CURVE EXPORT ENGINE")
    print("==============================================================================")
    
    galaxies = [("DDO_154_Dwarf", "Dwarf"), ("NGC_3109_LSB", "LSB"), ("NGC_3198_Spiral", "Spiral"), ("UGC_2885_Giant", "Giant")]
    
    for gal_name, gtype in galaxies:
        filename = f"{gal_name}_predicted_curve.csv"
        print(f" Exporting continuous profile for {gal_name} -> {filename}")
        
        with open(filename, "w") as f:
            f.write("Radius_kpc,V_Newton_kms,V_CSV_Pred_kms,g_bar_ms2,g_csv_ms2\n")
            for r in range(1, 51):
                r_kpc = float(r)
                r_m = r_kpc * kpc_to_m
                M_b = sample_baryon_mass(r_kpc, gtype) * 1.98847e30
                
                g_bar = (G * M_b) / (r_m ** 2)
                v_newt = math.sqrt(g_bar * r_m) / km_to_m
                
                g_csv = g_bar / (1.0 - math.exp(-math.sqrt(g_bar / a0_csv)))
                v_csv = math.sqrt(g_csv * r_m) / km_to_m
                
                f.write(f"{r_kpc:.1f},{v_newt:.2f},{v_csv:.2f},{g_bar:.6e},{g_csv:.6e}\n")
    
    print("==============================================================================")
    print(" All continuous rotation profiles exported successfully as CSV files.")
    print("==============================================================================")

if __name__ == "__main__":
    generate_curves()
