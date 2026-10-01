from fft_analysis import (
    initialize_eeg,
    compute_fft,

    display_eeg,
    display_fft,

    band_setup,

    histogram_display
)
from sleep_stage import (
    initialize_raw,
    initialize_sleep_staging,
    extract_features,

    predict_sleep_stage,
    predict_probability,

    display_hypnogram
)

from true_hypnogram import (
    load_annotations,
    print_annotations,
    create_stage_list,
    create_hypnogram,
    display_hypnogram
)

def main():
    #FFT Stuff
    
    #signal, labels, fs = initialize_eeg("chb01_01.edf")
    signal, labels, fs = initialize_eeg("SC4001E0-PSG.edf")

    freq, power = compute_fft(signal, fs)

    band_power = band_setup(freq, power)

    display_eeg(signal, fs)
    display_fft(freq, power)
    histogram_display(band_power)

    # Load EEG

    #YASA stuff
    #raw = initialize_raw("chb01_01.edf")
    raw = initialize_raw("SC4001E0-PSG.edf")

    print("\nRaw Info")
    print(raw.info)

    # Replace with the correct EEG channel name
    eeg_channel = raw.ch_names[0]

    sleep_model = initialize_sleep_staging(
        raw,
        eeg_channel=eeg_channel
    )

    features = extract_features(sleep_model)

    print("\nSleep Features")
    print(features.head())

    hypnogram = predict_sleep_stage(sleep_model)

    probabilities = predict_probability(sleep_model)

    proba = predict_probability(sleep_model)
    print(proba.head())

    print("\nStage Probabilities")
    print(probabilities.head())

    display_hypnogram(hypnogram)

    #True hypnogram fact check (for testing)
    anno = load_annotations("SC4001EC-Hypnogram.edf")
    print_annotations(anno)

    stages = create_stage_list(anno)
    test_hypnogram = create_hypnogram(stages)
    display_hypnogram(test_hypnogram)


if __name__ == "__main__":
    main()