import matplotlib.pyplot as plt
from astropy.io import fits
from pathlib import Path
import numpy as np

# SETUP: Adjust this if your data is in a different folder
DATA_DIR = Path("data/pds") 

def plot_bennu_map(filename, title, cmap="magma"):
    """
    Reads a Bennu FITS table, FILTERS OUT BAD DATA, and creates a scatter map.
    """
    filepath = DATA_DIR / filename
    
    if not filepath.exists():
        print(f"❌ File not found: {filename}")
        return

    print(f"--- Processing: {title} ---")
    
    with fits.open(filepath) as hdul:
        try:
            data = hdul[1].data
        except IndexError:
            return

        lat = data['LATITUDE']
        lon = data['LONGITUDE']
        val = data['VALUE']

        # --- THE FIX: Filter out the -9999 "No Data" values ---
        # Real spectral data is usually > -100.
        valid_mask = val > -9000
        
        lat_clean = lat[valid_mask]
        lon_clean = lon[valid_mask]
        val_clean = val[valid_mask]
        
        print(f"Original points: {len(val)}")
        print(f"Valid points: {len(val_clean)}")
        print(f"Real Data Range -> Min: {val_clean.min():.4f}, Max: {val_clean.max():.4f}")

        # Plotting
        plt.figure(figsize=(12, 6))
        
        # We use the CLEAN data now
        scatter = plt.scatter(lon_clean, lat_clean, c=val_clean, cmap=cmap, s=1, alpha=0.8)
        
        plt.colorbar(scatter, label="Band Depth / Strength")
        plt.title(f"Bennu Nightingale Site: {title}")
        plt.xlabel("Longitude (deg)")
        plt.ylabel("Latitude (deg)")
        plt.grid(True, linestyle='--', alpha=0.5)
        
        # SAVE
        output_filename = f"map_{title.split()[0]}.png"
        plt.savefig(output_filename, dpi=150)
        print(f"✅ Saved clean map to: {output_filename}\n")
        plt.close()

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    print("Starting Cleaned Table Analysis...\n")

    # 1. Plot Organic Carbon (Space Gum)
    plot_bennu_map(
        "l_1600mm_sp_ovirs_recb_bandarea3200to3600nm_nightingale_wavc_0000n00000.fits", 
        "Organic Carbon (3.4 micron)", 
        cmap="plasma"
    )

    # 2. Plot Water (Hydration)
    plot_bennu_map(
        "l_1600mm_sp_ovirs_recb_oh2740nm_nightingale_wavc_0000n00000.fits", 
        "Hydration (2.7 micron)", 
        cmap="viridis"
    )
    
    print("Analysis Complete.")