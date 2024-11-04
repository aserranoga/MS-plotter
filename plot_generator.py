import matplotlib.pyplot as plt
import numpy as np
import os


# Configuration (you can modify these as needed)
mass_spectrum_files = [
    "/Volumes/Bode/Bruker-Compact-1-Repro/2024-07-15/data_reprocessed/Bode - ASG4_69_hIL4_PBS - MassSpectrum.xy",
    "/Volumes/Bode/Bruker-Compact-1-Repro/2024-07-15/data_reprocessed/Bode - ASG4_69_hIL4_PBS - MassSpectrum - Deconvoluted.xy",
    "/Volumes/Bode/Bruker-Compact-1-Repro/2024-07-15/data_reprocessed/Bode - ASG4_69_hIL4_PBS - MassSpectrum - Deconvoluted.xy",
    "/Volumes/Bode/Bruker-Compact-1-Repro/2024-07-15/data_reprocessed/Bode - ASG4_69_hIL4_PBS - MassSpectrum - Deconvoluted.xy",
    # Add more file paths here as needed
]

# Optional x-axis limits for each file (or None for automatic limits)
x_limits_list = [
    (1000, 2000),  # x-axis limits for spectrum1.xy
    (5000, 20000),  # x-axis limits for spectrum2.xy
    (14900, 15000),  # x-axis limits for spectrum3.xy
    (14900, 15000),  # x-axis limits for spectrum3.xy
    # Add limits for additional files or set to None to use default limits
]

# Custom titles for each spectrum
titles = [
    "Mass spectrum - Measured",
    "Mass spectrum - Deconvoluted",
    "Mass spectrum - Deconvoluted",
    "Mass spectrum - Simulated",
    # Add titles for additional files as needed
]

# Optional parameters for peak finding (customized for each spectrum)
peak_ranges = [100.0, 3.0, 4.0, 6.0]  # Different peak ranges for each spectrum
num_peaks_list = [3, 1, 1, 1]  # Number of peaks to label for each spectrum

# Load .xy files
def load_mass_spectrum(file_path):
    """Load mass spectrum data from an .xy file with space-separated values."""
    with open(file_path, 'r') as f:
        data = [tuple(map(float, line.split())) for line in f]
    return zip(*data)  # Returns two lists: x and y

# Peak finding function
def find_peaks_within_range(x, y, peak_range, num_peaks):
    """Find the highest peaks in the spectrum within the specified range."""
    peaks = [(x[i], y[i]) for i in range(1, len(y) - 1) if y[i] > y[i - 1] and y[i] > y[i + 1]]
    peaks.sort(key=lambda p: p[1], reverse=True)

    labeled_peaks = []
    for peak in peaks:
        peak_x, _ = peak
        if not any(abs(peak_x - lp[0]) <= peak_range for lp in labeled_peaks):
            labeled_peaks.append(peak)
            if len(labeled_peaks) >= num_peaks:
                break
    return labeled_peaks

def configure_font_properties():
    """Define font properties for the plots."""
    return {
        'font': {'family': 'Arial', 'weight': 'normal', 'size': 8},     # General font properties
        'x_label': {'family': 'Arial', 'weight': 'normal', 'size': 6},  # X axis label
        'tick': {'size': 6}                                             # X tick font properties
    }

# Plotting function
def plot_mass_spectra(files, x_limits_list):
    """Plot multiple mass spectra with vertical stacking, each with its own x-axis limits."""
    num_files = len(files)
    fig, axes = plt.subplots(num_files, 1, figsize=(10 / 2.54, 2.5 * num_files / 2.54), sharey=False)

    if num_files == 1:
        axes = [axes]  # Ensure axes is a list if there's only one subplot

    # Define font properties for Arial, 6pt, regular
    font_properties = {'family': 'Arial', 'weight': 'normal', 'size': 8} # General font properties
    x_label_font_properties = {'family': 'Arial', 'weight': 'normal', 'size': 6}  # X axis label
    x_tick_font_properties = {'family': 'Arial', 'weight': 'normal', 'size': 6}  # X tick font properties

    for i, (file_path, ax) in enumerate(zip(files, axes)):
        # Load data
        x, y = load_mass_spectrum(file_path)

        # Plot each spectrum on its own subplot
        ax.plot(x, y, color='black', linewidth=0.5)

        # Apply individual x-axis limits if specified
        if x_limits_list[i] is not None:
            ax.set_xlim(x_limits_list[i])

        # Hide the y-axis
        ax.get_yaxis().set_visible(False)
        
        # Remove the spines (box) around the plot
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Set axis line widths
        ax.spines['bottom'].set_linewidth(0.5)  # Bottom spine

        # Label x and y axes
        ax.set_xlabel("m/z", fontdict=x_label_font_properties)

        # Use the custom title for each subplot
        ax.set_title(titles[i], fontdict=font_properties)

        # Optional grid for clarity
        # ax.grid(True, linestyle="--", linewidth=0.5)

        # Set tick label font properties
        ax.tick_params(axis='x', labelsize=6, labelfontfamily='Arial', width=0.5)

        # ** Peak finding and labeling implementation **
        # Find and annotate peaks with individual parameters
        peaks = find_peaks_within_range(x, y, peak_range=peak_ranges[i], num_peaks=num_peaks_list[i])
        for peak_x, peak_y in peaks:
            ax.annotate(f'{peak_x:.2f}', xy=(peak_x, peak_y), xytext=(peak_x, peak_y + 0.1 * max(y)),
                        textcoords='data', fontsize=6, color='black',
                        arrowprops=dict(arrowstyle='->', color='black', lw=0.5))

    plt.tight_layout()
    plt.show()

# Call the plotting function with the list of files and x-axis limits
plot_mass_spectra(mass_spectrum_files, x_limits_list)
