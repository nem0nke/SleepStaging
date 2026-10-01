import yasa
import mne
import pandas as pd
import matplotlib.pyplot as plt

'''
Sleep Staging Documentation

initialize_raw(filename)
- Loads an EDF recording using MNE.
- Reads the EEG recording into memory for processing.
- Prints the sampling frequency (Hz) for verification.
- Parameters:
    filename: Path to the EDF file.
- Returns:
    raw: MNE Raw object containing the EEG recording.


initialize_sleep_staging(raw, eeg_channel, eog_channel=None,
                         emg_channel=None, metadata=None)
- Creates a YASA SleepStaging object.
- Specifies which EEG channel to use for sleep staging.
- Optionally accepts EOG and EMG channels to improve prediction
  accuracy, as well as subject metadata.
- Parameters:
    raw: MNE Raw EEG object.
    eeg_channel: Name of the EEG channel.
    eog_channel: Name of the EOG channel (optional).
    emg_channel: Name of the EMG channel (optional).
    metadata: Dictionary containing subject information
              (optional).
- Returns:
    sls: YASA SleepStaging object.


extract_features(sls)
- Extracts the numerical EEG features used by YASA's machine
  learning model.
- These include spectral power, relative band power, entropy,
  statistical measures, and temporal features computed for each
  30-second epoch.
- Parameters:
    sls: YASA SleepStaging object.
- Returns:
    features: Pandas DataFrame containing one row per epoch and
              feature columns used for sleep stage prediction.


predict_sleep_stage(sls)
- Predicts the sleep stage of every 30-second epoch using YASA's
  pretrained LightGBM classifier.
- Converts the predicted labels into a YASA Hypnogram object for
  visualization and analysis.
- Parameters:
    sls: YASA SleepStaging object.
- Returns:
    hypno: YASA Hypnogram object containing the predicted sleep
           stages.


predict_probability(sls)
- Calculates the probability that each epoch belongs to each sleep
  stage (Wake, N1, N2, N3, REM).
- Each row represents one epoch, and each column represents the
  model's confidence for a particular stage.
- The probabilities for each epoch sum to approximately 1.
- Parameters:
    sls: YASA SleepStaging object.
- Returns:
    predict: Pandas DataFrame containing sleep stage
             probabilities.


display_hypnogram(hypno)
- Displays the predicted hypnogram.
- Visualizes how the predicted sleep stage changes over time
  throughout the recording.
- Parameters:
    hypno: YASA Hypnogram object.
- Returns:
    None
'''

def initialize_raw(filename):
    raw = mne.io.read_raw_edf(filename, preload=True)

    print(raw.info["sfreq"])
    return raw #Raw EDF data

def initialize_sleep_staging(raw, eeg_channel, eog_channel=None, emg_channel=None, metadata=None):

    sls = yasa.SleepStaging(
        raw,
        eeg_name=eeg_channel,
        eog_name=eog_channel,
        emg_name=emg_channel,
        metadata=metadata
    )

    return sls #Sleep Staging instance

def extract_features(sls):

    features = sls.get_features()

    return features #Pandas dataframe



def predict_sleep_stage(sls):

    hypno = sls.predict()

    hypno = yasa.Hypnogram(
        hypno,
        n_stages=5
    )

    return hypno

def predict_probability(sls):

    predict = sls.predict_proba()

    print(predict)
    return predict #Returns probability of sleep each sleep stage



def display_hypnogram(hypno):
    hypno.plot_hypnogram()
    plt.show()