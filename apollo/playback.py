"""Methods for monitoring iTunes playback"""

import subprocess

from enum import Enum


def is_itunes_running():
    """ Checks if iTunes is running.

    :return: whether iTunes is running (bool)
    """
    status = subprocess.check_output(['osascript', '-e', 'application "iTunes" is running'])
    is_running = b'true' == status.strip()  # Strip newline
    return is_running


class PlayStatus(Enum):
    STOPPED = 0
    PLAY = 1
    PAUSE = 2
    FORWARD = 3
    REWIND = 4
    UNKNOWN = 5


def get_play_status():
    """ Get the current playback status from iTunes.

    :return: the current status (PlayStatus)
    """
    # Get status via applescript
    status = subprocess.check_output(['osascript', '-e', 'tell application "iTunes" to get player state'])

    # Strip newline
    status = status.strip()

    if status == b'stopped':
        return PlayStatus.STOPPED
    elif status == b'playing':
        return PlayStatus.PLAY
    elif status == b'paused':
        return PlayStatus.PAUSE
    elif status == b'fast forwarding':
        return PlayStatus.FORWARD
    elif status == b'rewinding':
        return PlayStatus.REWIND
    else:
        print("Unknown play status: {}".format(status))
        return PlayStatus.UNKNOWN


def get_play_time():
    """ Get the current time for the current track. If no track is currently
        playing, returns 0.

    :return: the current time, in seconds (float)
    """
    # Get time from iTunes
    t = subprocess.check_output(['osascript', '-e', 'tell app "itunes" to player position'])

    t = t.strip()  # Strip newline

    if t == b'missing value':
        return 0

    return float(t)


def get_current_track_file():
    """ Get the path to the current track.

    :return: the path (bytes)
    """
    # TODO Fix for when no track is loaded (i.e. just after launch)
    track = subprocess.check_output(['osascript', '-e', "tell application \"iTunes\" to get location of current track"])
    track = track.strip()[18:].replace(b":", b"/")  # TODO breaks when colon in name

    return track
