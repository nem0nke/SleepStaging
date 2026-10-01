import numpy as np
import pyedflib
import matplotlib.pyplot as plt

'''
Function Documentation:

initialize_eeg(filename)
- Loads an EDF EEG recording from the specified file.
- Extracts the EEG signal, channel labels, and sampling frequency.
- Returns:
    signal: EEG amplitude values
    labels: EEG channel names
    fs: sampling frequency (Hz)


display_eeg(signal, fs)
- Displays raw EEG data


compute_fft(signal, fs)
- Applies a Fast Fourier Transform (FFT) to convert the EEG signal
  from the time domain into the frequency domain.
- Calculates the power spectrum to measure signal strength at each frequency.
- Returns:
    freq: frequency values (Hz)
    power: power spectrum values


display_fft(freq, power)
- Displays the EEG power spectrum.
- Plots frequency (Hz) against power to visualize frequency components
  present in the EEG signal.


band_setup(freq, power)
- Separates the power spectrum into standard EEG frequency bands:
    Delta (0.5-4 Hz)
    Theta (4-8 Hz)
    Alpha (8-13 Hz)
    Beta (13-30 Hz)
    Gamma (30-45 Hz)
- Returns:
    band_power: dictionary containing power values for each frequency band


histogram_display(band_power)
- Creates histograms showing the distribution of power values
  within each EEG frequency band.


estimate_sleep_stage(band_power) TO BE DEPRECIATED BY YASA
- Estimates sleep stage activity based on EEG band power.
- Currently uses simple frequency-based approximations:
    Awake: Alpha + Beta
    N1: Theta
    N3: Delta
    REM: Beta
'''

print("Bello world")

#Initialize Freq
def initialize_eeg(filename):
    f = pyedflib.EdfReader(filename)
    s = f.readSignal(0)
    labels = f.getSignalLabels()
    fs = f.getSampleFrequency(0)

    return s, labels, fs

def display_eeg(s, fs):
    samples = int(fs * 10)

    
    plt.figure(figsize=(15, 4))

    plt.plot(s[:samples])

    plt.title("EEG Signal (For First 10 Seconds)")
    plt.xlabel("Sample Number")
    plt.ylabel("Amplitude")
    plt.show()

#(Fast) Fourier Transform Setup
def compute_fft(s, fs):
    fourier_transform = np.fft.rfft(s)

    # Frequency values
    freq = np.fft.rfftfreq(len(s), d=1/fs)

    # Convert FFT into Power Spectrum
    power = np.abs(fourier_transform)**2

    return freq, power

def display_fft(freq, power):
    plt.figure(figsize=(15,4))

    plt.plot(freq, power)

    plt.xlim(0,50)

    plt.title("Power Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power")

    plt.grid(True)

    plt.show() #Power Spectrum

#EEG Band Setup
'''
Delta (0.5 - 4 Hz): Slowest brain waves; associated with deep, dreamless sleep, restorative functions, and sometimes pathological states while awake.
Theta (4 - 8 Hz): Linked to light meditation, deep relaxation, intuition, and early sleep stages.
Alpha (8 - 13 Hz): Represents relaxed, alert wakefulness (e.g., closing your eyes) and a calm, focused state.
Beta (13 - 30 Hz): Associated with active thinking, problem-solving, and a state of active focus or alertness.
Gamma (>30 Hz): The fastest waves; linked to high-level cognitive processing, sensory perception, and focused concentration.
'''

def band_setup(freq, power):
    bands = {
        "Delta": (0.5,4),
        "Theta": (4,8),
        "Alpha": (8,13),
        "Beta": (13,30),
        "Gamma": (30,45)
    }

    band_power = {}
    sleep_power = {}

    for band, (low, high) in bands.items():

        mask = (freq >= low) & (freq < high)

        band_power[band] = power[mask]
        sleep_power[band] = np.sum(power[mask])


    #print("\nBand Powers\n")

    for band in band_power:

        print(f"{band}: {band_power[band].sum():.2f}")

    return band_power


#Histogram (Band powers)

def histogram_display(band_power):
    plt.figure(figsize=(12,8))

    for i, band in enumerate(band_power):

        plt.subplot(3,2,i+1)

        plt.hist(band_power[band], bins=20)

        plt.title(band)
        plt.xlabel("Power")
        plt.ylabel("Count")

    plt.tight_layout()
    plt.show()

#Divides band powers among sleep stages
'''
Awake:
Alpha + Beta

Non-REM:
N1 - Theta
N2 - ??? (WILL NEED TO BE DISCUSSED)
N3 - Delta

REM
Beta
'''

#band_power[band] = np.sum(power[mask])
def estimate_sleep_stage(band_power): #TO BE DEPRECIATED
    sleep_stage_power = {
        "Awake": np.sum(band_power["Alpha"]) + np.sum(band_power["Beta"]),
        "N1": np.sum(band_power["Theta"]),
        #"N2" : (WILL NEED TO FIURE THIS OUT)
        "N3": np.sum(band_power["Delta"]),
        "REM": np.sum(band_power["Beta"])   # temporary approximation
    }

    plt.figure(figsize=(8,5))

    plt.bar(
        sleep_stage_power.keys(),
        sleep_stage_power.values()
    )

    plt.title("Estimated Sleep Stage Strength")
    plt.xlabel("Sleep Stage")
    plt.ylabel("Total Power")


    plt.tight_layout()
    plt.show()
