"""
Code is for analyzing true hypnogram graphs; testing accuracy between predicted and actual hypnograms
"""
import mne
import yasa
import matplotlib.pyplot as plt


# Load EDF Hypnogram Annotations

def load_annotations(hypnogram_file):
    annotations = mne.read_annotations(hypnogram_file)
    return annotations


# Display Annotation Information

def print_annotations(annotations):
    print("\nSleep Annotations\n")

    for onset, duration, description in zip(
            annotations.onset,
            annotations.duration,
            annotations.description):

        print(
            f"Time: {onset:8.1f}s | "
            f"Duration: {duration:5.1f}s | "
            f"{description}"
        )


# Convert annotations into stage labels

def create_stage_list(annotations):

    stage_map = {
        "Sleep stage W": "W",
        "Sleep stage 1": "N1",
        "Sleep stage 2": "N2",
        "Sleep stage 3": "N3",
        "Sleep stage 4": "N3",      # Merge N3 + N4
        "Sleep stage R": "REM"
    }

    stages = []

    for duration, desc in zip(
            annotations.duration,
            annotations.description):

        if desc not in stage_map:
            continue

        epochs = int(duration / 30)

        stages.extend([stage_map[desc]] * epochs)

    return stages



# Convert to YASA Hypnogram

def create_hypnogram(stage_list):

    hyp = yasa.Hypnogram(
        stage_list,
        n_stages=5
    )

    return hyp



# Display Hypnogram

def display_hypnogram(hypnogram):
    hypnogram.plot_hypnogram()

    plt.title("Ground Truth Sleep Stages")

    plt.show()