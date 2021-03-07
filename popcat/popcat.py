import numpy as np
import os
import sys
from scipy.io import wavfile
from pydub import AudioSegment
from moviepy.editor import ImageClip, concatenate

# Globals
DECIMALS = 2
STEPS = 1 / 10 ** DECIMALS
FPS = 24
FILE = sys.argv[1]
NAME = sys.argv[2]

# Gets ranges of consecutive (based on stepsize and decimals) nums for a 1d array
def get_ranges(data, stepsize=1, decimals=0):
    diffs = np.round(np.diff(data), decimals)
    indices = np.nonzero(diffs != stepsize)[0] + 1
    consecutives = np.split(data, indices)

    ranges = []
    for arr in consecutives:
        ranges.append([arr[0], arr[len(arr)-1] + 1 / 10 ** decimals]) # Get first and last element

    return np.array(ranges)

# Gets the combination of two lists, alternating values
def alternate_lists(list1, list2):
    return np.array([[i, j] for i, j in zip(list1, list2)]).ravel()

def main():
    # Get data from audio file
    rate, signal = wavfile.read(FILE)

    thresh = np.amax(signal) * 0.6 # Set decibal threshold to 60% of highest point
    time = np.arange(0, len(signal) / rate, STEPS)

    peak_times = np.unique(np.round(np.where(signal >= thresh)[0] / rate, DECIMALS))
    peak_ranges = get_ranges(peak_times, stepsize=STEPS, decimals=DECIMALS)

    neutral_times = np.setdiff1d(time, peak_times)
    neutral_ranges = get_ranges(neutral_times, stepsize=STEPS, decimals=DECIMALS)

    # Create video
    peak_lengths = [round(arr[1] - arr[0], DECIMALS) for arr in peak_ranges]
    neutral_lengths = [round(arr[1] - arr[0], DECIMALS) for arr in neutral_ranges]

    path = os.path.dirname(os.path.abspath(__file__))
    open_clips = [ImageClip(path + "/images/popcatopen.jpg").set_duration(length) for length in peak_lengths]
    closed_clips = [ImageClip(path + "/images/popcatclosed.jpg").set_duration(length) for length in neutral_lengths]

    audio = AudioSegment.from_wav(FILE)
    audio.export("audio.mp3", format="mp3")

    clips = alternate_lists(closed_clips, open_clips)
    final_clip = concatenate(clips)
    final_clip.write_videofile("test.mp4", audio="audio.mp3", fps=FPS)
    os.remove("audio.mp3")