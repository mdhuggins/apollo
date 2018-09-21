"""WAV utilities"""

import wave
import sys
import subprocess

import numpy as np


def convert_to_wav(source_path, output_path):
    """ Converts an audio file to WAV.

    :param source_path: the file to convert (bytes/str)
    :param output_path: where to save the WAV output (bytes/str)
    :return: None
    """
    convert = subprocess.check_output(['ffmpeg',
                                       '-y',
                                       '-loglevel', 'error',
                                       '-i', source_path,
                                       '-ar', '22050',
                                       output_path])


def load_wav(filepath, t_start=0, t_end=sys.maxsize, only_22k=True):
    """Load a wave file, which must be 22050Hz and 16bit and must be either
    mono or stereo. Adapted from Eran Egozy's 21M.387 version.
    Inputs:
        filepath: audio file
        t_start, t_end:  (optional) subrange of file to load (in seconds)
        only_22k: if True (default), assert if sample rate is different from 22050.
    Returns:
        a numpy floating-point array with a range of [-1, 1]
    """

    wf = wave.open(filepath)
    num_channels, sampwidth, fs, end, comptype, compname = wf.getparams()

    # for now, we will only accept 16 bit files at 22k
    assert (sampwidth == 2)
    # assert(fs == 22050)

    # start frame, end frame, and duration in frames
    f_start = int(t_start * fs)
    f_end = min(int(t_end * fs), end)
    frames = f_end - f_start

    wf.setpos(f_start)
    raw_bytes = wf.readframes(frames)

    # convert raw data to numpy array, assuming int16 arrangement
    samples = np.fromstring(raw_bytes, dtype=np.int16)

    # convert from integer type to floating point, and scale to [-1, 1]
    samples = samples.astype(np.float)
    samples *= (1 / 32768.0)

    if num_channels == 1:
        return samples

    elif num_channels == 2:
        return 0.5 * (samples[0::2] + samples[1::2])

    else:
        raise ValueError('Can only handle mono or stereo wave files')
