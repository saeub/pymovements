# Copyright (c) 2022-2023 The pymovements Project Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""This module provides an interface to the GazeBase dataset."""
from pymovements.base import Experiment
from pymovements.datasets.base import PublicDataset


class GazeBase(PublicDataset):
    """GazeBase dataset :cite:p:`GazeBase`.

    This dataset includes monocular (left eye) eye tracking data from 322 participants captured over
    a period of 37 months. Participants attended up to 9 rounds during this time frame, with each
    round consisting of two contiguous sessions.

    Eye movements are recorded at a sampling frequency of 1000 Hz using an EyeLink 1000 video-based
    eye tracker and are provided as positional data in degrees of visual angle.

    In each of the two sessions per round, participants are instructed to complete a series of
    tasks, including a fixation task (FIX), a horizontal saccade task (HSS), a random saccade task
    (RAN), a reading task (TEX), two free viewing video tasks (VD1 and VD2) and a gaze-driven gaming
    task (BLG).

    Check the respective paper for details :cite:p:`GazeBase`.
    """
    _mirrors = [
        'https://figshare.com/ndownloader/files/',
    ]

    _resources = [
        {
            'resource': '27039812',
            'filename': 'GazeBase_v2_0.zip',
            'md5': 'cb7eb895fb48f8661decf038ab998c9a',
        },
    ]

    _experiment = Experiment(
        screen_width_px=1680,
        screen_height_px=1050,
        screen_width_cm=47.4,
        screen_height_cm=29.7,
        distance_cm=55,
        origin='lower left',
        sampling_rate=1000,
    )

    _filename_regex = (
        r'S_(?P<round_id>\d)(?P<subject_id>\d+)'
        r'_S(?P<session_id>\d+)'
        r'_(?P<task_name>.+).csv'
    )

    _filename_regex_dtypes = {
        'round_id': int,
        'subject_id': int,
        'session_id': int,
    }

    _column_map = {
        'n': 'time',
        'x': 'x_left_dva',
        'y': 'y_left_dva',
        'val': 'validity',
        'xT': 'x_target_dva',
        'yT': 'y_target_dva',
    }

    _read_csv_kwargs = {
        'columns': list(_column_map.keys()),
        'new_columns': list(_column_map.values()),
    }

    def __init__(self, **kwargs):
        super().__init__(
            experiment=self._experiment,
            filename_regex=self._filename_regex,
            filename_regex_dtypes=self._filename_regex_dtypes,
            custom_read_kwargs=self._read_csv_kwargs,
            **kwargs,
        )