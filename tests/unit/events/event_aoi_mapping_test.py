# Copyright (c) 2023-2024 The pymovements Project Authors
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
"""Test all GazeDataFrame functionality."""
import polars as pl
import pytest
from polars.testing import assert_frame_equal

import pymovements as pm

EXPECTED_DF = {
    'char': pl.DataFrame(
        [
            (0, 1, 'fixation', 1988147, 1988322, 175, 207.40908813476562, 151.54261779785156, ''),
            (0, 1, 'fixation', 1988351, 1988546, 195, 167.1040802001953, 147.58265686035156, ''),
            (0, 1, 'fixation', 1988592, 1988736, 144, 251.90138244628906, 152.11585998535156, ''),
            (0, 1, 'fixation', 1988788, 1989013, 225, 375.60797119140625, 156.98583984375, ''),
            (0, 1, 'fixation', 1989060, 1989170, 110, 447.34954833984375, 153.80810546875, ''),
            (0, 1, 'fixation', 1989202, 1989424, 222, 513.2999877929688, 157.17892456054688, ''),
            (0, 1, 'fixation', 1989461, 1989585, 124, 581.2647705078125, 159.6696014404297, ''),
            (0, 1, 'fixation', 1989640, 1989891, 251, 707.7650756835938, 163.16627502441406, ''),
            (0, 1, 'fixation', 1989929, 1990049, 120, 787.0628051757812, 163.24462890625, ''),
            (0, 1, 'fixation', 1990078, 1990304, 226, 846.222900390625, 166.44009399414062, ''),
            (0, 1, 'fixation', 1990356, 1990652, 296, 978.3326416015625, 163.44142150878906, ''),
            (0, 1, 'fixation', 1990751, 1990926, 175, 180.8477325439453, 208.05738830566406, ''),
            (0, 1, 'fixation', 1990961, 1991140, 179, 150.49110412597656, 211.2177734375, ''),
            (0, 1, 'fixation', 1991189, 1991317, 128, 239.65658569335938, 211.82479858398438, ''),
            (0, 1, 'fixation', 1991353, 1991495, 142, 302.7160949707031, 216.57412719726562, ''),
            (0, 1, 'fixation', 1991527, 1991715, 188, 375.2423400878906, 219.38729858398438, ''),
            (0, 1, 'fixation', 1991745, 1991899, 154, 427.5083923339844, 217.13418579101562, 'y'),
            (0, 1, 'fixation', 1991950, 1992230, 280, 600.10498046875, 213.44769287109375, ''),
            (0, 1, 'fixation', 1992284, 1992569, 285, 725.8087158203125, 222.2129364013672, ''),
            (0, 1, 'fixation', 1992611, 1992757, 146, 791.149658203125, 221.16598510742188, ''),
            (0, 1, 'fixation', 1992792, 1992969, 177, 848.5045166015625, 221.47415161132812, ''),
            (0, 1, 'fixation', 1993004, 1993238, 234, 932.0889282226562, 221.6782989501953, ''),
            (0, 1, 'fixation', 1993274, 1993510, 236, 1024.1549072265625, 221.48606872558594, ''),
            (0, 1, 'fixation', 1993610, 1993716, 106, 200.10841369628906, 264.7196350097656, ''),
            (0, 1, 'fixation', 1993752, 1993948, 196, 157.9243621826172, 268.237548828125, ''),
            (0, 1, 'fixation', 1993982, 1994193, 211, 241.02406311035156, 271.51885986328125, ''),
            (0, 1, 'fixation', 1994223, 1994383, 160, 296.4459533691406, 273.27764892578125, ''),
            (0, 1, 'fixation', 1994436, 1994710, 274, 435.92181396484375, 286.8061828613281, ''),
            (0, 1, 'fixation', 1994761, 1994900, 139, 522.0599975585938, 286.7850036621094, ''),
            (0, 1, 'fixation', 1994957, 1995109, 152, 606.8084716796875, 285.356201171875, ''),
            (0, 1, 'fixation', 1995156, 1995323, 167, 688.3916625976562, 284.9291687011719, ''),
            (0, 1, 'fixation', 1995374, 1995532, 158, 770.3402709960938, 289.7440185546875, ''),
            (0, 1, 'fixation', 1995558, 1995805, 247, 825.5753784179688, 287.0762023925781, ''),
            (0, 1, 'fixation', 1995841, 1995988, 147, 880.3533935546875, 283.3432312011719, ''),
            (0, 1, 'fixation', 1996026, 1996198, 172, 938.55029296875, 281.8595275878906, ''),
            (0, 1, 'fixation', 1996245, 1996412, 167, 1022.4404907226562, 278.0517883300781, ''),
            (0, 1, 'fixation', 1996517, 1996758, 241, 157.65289306640625, 323.64007568359375, ''),
            (0, 1, 'fixation', 1996804, 1997014, 210, 223.5668182373047, 337.4715576171875, ''),
            (0, 1, 'fixation', 1997043, 1997190, 147, 274.8675537109375, 344.57501220703125, ''),
            (0, 1, 'fixation', 1997223, 1997438, 215, 368.62640380859375, 349.6805419921875, ''),
            (0, 1, 'fixation', 1997488, 1997653, 165, 460.4620361328125, 359.3228759765625, ''),
            (0, 1, 'fixation', 1997678, 1997905, 227, 432.24078369140625, 357.230712890625, ''),
            (0, 1, 'fixation', 1997954, 1998254, 300, 521.3893432617188, 356.7348937988281, ''),
            (0, 1, 'fixation', 1998285, 1998512, 227, 477.1824645996094, 357.98638916015625, ''),
            (0, 1, 'fixation', 1998562, 1998790, 228, 577.8619995117188, 364.3253173828125, ''),
            (0, 1, 'fixation', 1998838, 1999070, 232, 703.7059936523438, 360.56610107421875, ''),
            (0, 1, 'fixation', 1999125, 1999382, 257, 830.8821411132812, 355.1527099609375, ''),
            (0, 1, 'fixation', 1999436, 1999625, 189, 952.5884399414062, 352.0815734863281, ''),
            (0, 1, 'fixation', 1999663, 1999819, 156, 1009.4426879882812, 342.19873046875, ''),
            (0, 1, 'fixation', 1999922, 2000103, 181, 157.89505004882812, 413.232421875, ''),
            (0, 1, 'fixation', 2000129, 2000245, 116, 184.9940185546875, 409.1675109863281, ''),
            (0, 1, 'fixation', 2000295, 2000455, 160, 272.43975830078125, 416.96087646484375, ''),
            (0, 1, 'fixation', 2000514, 2000641, 127, 389.37188720703125, 417.5953063964844, ''),
            (0, 1, 'fixation', 2000677, 2000894, 217, 446.2220153808594, 419.3307189941406, 'c'),
            (0, 1, 'fixation', 2000930, 2001173, 243, 526.5098266601562, 423.3586120605469, 's'),
            (0, 1, 'fixation', 2001208, 2001459, 251, 612.4912719726562, 425.6646728515625, 'g'),
            (0, 1, 'fixation', 2001495, 2001712, 217, 708.4536743164062, 423.4444885253906, 'e'),
            (0, 1, 'fixation', 2001746, 2001930, 184, 773.7962036132812, 423.0291748046875, 'r'),
            (0, 1, 'fixation', 2002003, 2002122, 119, 857.3724975585938, 422.3450012207031, 'p'),
            (0, 1, 'fixation', 2002160, 2002306, 146, 936.1646118164062, 418.0686950683594, 's'),
            (0, 1, 'fixation', 2002308, 2002442, 134, 940.3585205078125, 416.9755554199219, 's'),
            (0, 1, 'fixation', 2002495, 2002603, 108, 1034.3890380859375, 409.68255615234375, ''),
            (0, 1, 'fixation', 2002709, 2002831, 122, 134.06097412109375, 491.251220703125, ''),
            (0, 1, 'fixation', 2002863, 2003003, 140, 161.3858184814453, 482.514892578125, ''),
            (0, 1, 'fixation', 2003042, 2003424, 382, 211.2224578857422, 483.4208984375, ''),
            (0, 1, 'fixation', 2003453, 2003657, 204, 283.94683837890625, 485.6600036621094, ''),
            (0, 1, 'fixation', 2003721, 2003917, 196, 422.4142150878906, 484.2720947265625, ' '),
            (0, 1, 'fixation', 2003968, 2004074, 106, 509.65234375, 480.1925354003906, 'n'),
            (0, 1, 'fixation', 2004132, 2004331, 199, 610.8610229492188, 484.6025085449219, 'g'),
            (0, 1, 'fixation', 2004399, 2004687, 288, 717.8470458984375, 486.0269775390625, ''),
            (0, 1, 'fixation', 2004714, 2004878, 164, 785.6884765625, 481.4891052246094, ''),
            (0, 1, 'fixation', 2004931, 2005109, 178, 896.4055786132812, 480.51898193359375, ''),
            (0, 1, 'fixation', 2005138, 2005287, 149, 933.6119995117188, 481.8833312988281, ''),
        ],
        schema=[
            'text_id',
            'page_id',
            'name',
            'onset',
            'offset',
            'duration',
            'location_x',
            'location_y',
            'area_of_interest',
        ],
        orient='row',
    ),
    'word': pl.DataFrame(
        [
            (0, 1, 'fixation', 1988147, 1988322, 175, 207.40908813476562, 151.54261779785156, ''),
            (0, 1, 'fixation', 1988351, 1988546, 195, 167.1040802001953, 147.58265686035156, ''),
            (0, 1, 'fixation', 1988592, 1988736, 144, 251.90138244628906, 152.11585998535156, ''),
            (0, 1, 'fixation', 1988788, 1989013, 225, 375.60797119140625, 156.98583984375, ''),
            (0, 1, 'fixation', 1989060, 1989170, 110, 447.34954833984375, 153.80810546875, ''),
            (0, 1, 'fixation', 1989202, 1989424, 222, 513.2999877929688, 157.17892456054688, ''),
            (0, 1, 'fixation', 1989461, 1989585, 124, 581.2647705078125, 159.6696014404297, ''),
            (0, 1, 'fixation', 1989640, 1989891, 251, 707.7650756835938, 163.16627502441406, ''),
            (0, 1, 'fixation', 1989929, 1990049, 120, 787.0628051757812, 163.24462890625, ''),
            (0, 1, 'fixation', 1990078, 1990304, 226, 846.222900390625, 166.44009399414062, ''),
            (0, 1, 'fixation', 1990356, 1990652, 296, 978.3326416015625, 163.44142150878906, ''),
            (0, 1, 'fixation', 1990751, 1990926, 175, 180.8477325439453, 208.05738830566406, ''),
            (0, 1, 'fixation', 1990961, 1991140, 179, 150.49110412597656, 211.2177734375, ''),
            (0, 1, 'fixation', 1991189, 1991317, 128, 239.65658569335938, 211.82479858398438, ''),
            (0, 1, 'fixation', 1991353, 1991495, 142, 302.7160949707031, 216.57412719726562, ''),
            (0, 1, 'fixation', 1991527, 1991715, 188, 375.2423400878906, 219.38729858398438, ''),
            (
                0, 1, 'fixation', 1991745, 1991899, 154,
                427.5083923339844, 217.13418579101562, 'pymovements:',
            ),
            (0, 1, 'fixation', 1991950, 1992230, 280, 600.10498046875, 213.44769287109375, ''),
            (0, 1, 'fixation', 1992284, 1992569, 285, 725.8087158203125, 222.2129364013672, ''),
            (0, 1, 'fixation', 1992611, 1992757, 146, 791.149658203125, 221.16598510742188, ''),
            (0, 1, 'fixation', 1992792, 1992969, 177, 848.5045166015625, 221.47415161132812, ''),
            (0, 1, 'fixation', 1993004, 1993238, 234, 932.0889282226562, 221.6782989501953, ''),
            (0, 1, 'fixation', 1993274, 1993510, 236, 1024.1549072265625, 221.48606872558594, ''),
            (0, 1, 'fixation', 1993610, 1993716, 106, 200.10841369628906, 264.7196350097656, ''),
            (0, 1, 'fixation', 1993752, 1993948, 196, 157.9243621826172, 268.237548828125, ''),
            (0, 1, 'fixation', 1993982, 1994193, 211, 241.02406311035156, 271.51885986328125, ''),
            (0, 1, 'fixation', 1994223, 1994383, 160, 296.4459533691406, 273.27764892578125, ''),
            (0, 1, 'fixation', 1994436, 1994710, 274, 435.92181396484375, 286.8061828613281, ''),
            (0, 1, 'fixation', 1994761, 1994900, 139, 522.0599975585938, 286.7850036621094, ''),
            (0, 1, 'fixation', 1994957, 1995109, 152, 606.8084716796875, 285.356201171875, ''),
            (0, 1, 'fixation', 1995156, 1995323, 167, 688.3916625976562, 284.9291687011719, ''),
            (0, 1, 'fixation', 1995374, 1995532, 158, 770.3402709960938, 289.7440185546875, ''),
            (0, 1, 'fixation', 1995558, 1995805, 247, 825.5753784179688, 287.0762023925781, ''),
            (0, 1, 'fixation', 1995841, 1995988, 147, 880.3533935546875, 283.3432312011719, ''),
            (0, 1, 'fixation', 1996026, 1996198, 172, 938.55029296875, 281.8595275878906, ''),
            (0, 1, 'fixation', 1996245, 1996412, 167, 1022.4404907226562, 278.0517883300781, ''),
            (0, 1, 'fixation', 1996517, 1996758, 241, 157.65289306640625, 323.64007568359375, ''),
            (0, 1, 'fixation', 1996804, 1997014, 210, 223.5668182373047, 337.4715576171875, ''),
            (0, 1, 'fixation', 1997043, 1997190, 147, 274.8675537109375, 344.57501220703125, ''),
            (0, 1, 'fixation', 1997223, 1997438, 215, 368.62640380859375, 349.6805419921875, ''),
            (0, 1, 'fixation', 1997488, 1997653, 165, 460.4620361328125, 359.3228759765625, ''),
            (0, 1, 'fixation', 1997678, 1997905, 227, 432.24078369140625, 357.230712890625, ''),
            (0, 1, 'fixation', 1997954, 1998254, 300, 521.3893432617188, 356.7348937988281, ''),
            (0, 1, 'fixation', 1998285, 1998512, 227, 477.1824645996094, 357.98638916015625, ''),
            (0, 1, 'fixation', 1998562, 1998790, 228, 577.8619995117188, 364.3253173828125, ''),
            (0, 1, 'fixation', 1998838, 1999070, 232, 703.7059936523438, 360.56610107421875, ''),
            (0, 1, 'fixation', 1999125, 1999382, 257, 830.8821411132812, 355.1527099609375, ''),
            (0, 1, 'fixation', 1999436, 1999625, 189, 952.5884399414062, 352.0815734863281, ''),
            (0, 1, 'fixation', 1999663, 1999819, 156, 1009.4426879882812, 342.19873046875, ''),
            (0, 1, 'fixation', 1999922, 2000103, 181, 157.89505004882812, 413.232421875, ''),
            (0, 1, 'fixation', 2000129, 2000245, 116, 184.9940185546875, 409.1675109863281, ''),
            (0, 1, 'fixation', 2000295, 2000455, 160, 272.43975830078125, 416.96087646484375, ''),
            (0, 1, 'fixation', 2000514, 2000641, 127, 389.37188720703125, 417.5953063964844, ''),
            (0, 1, 'fixation', 2000677, 2000894, 217, 446.2220153808594, 419.3307189941406, 'processes'),  # noqa:E501
            (0, 1, 'fixation', 2000930, 2001173, 243, 526.5098266601562, 423.3586120605469, 'processes'),  # noqa:E501
            (0, 1, 'fixation', 2001208, 2001459, 251, 612.4912719726562, 425.6646728515625, 'along'),  # noqa:E501
            (0, 1, 'fixation', 2001495, 2001712, 217, 708.4536743164062, 423.4444885253906, 'entire'),  # noqa:E501
            (0, 1, 'fixation', 2001746, 2001930, 184, 773.7962036132812, 423.0291748046875, 'entire'),  # noqa:E501
            (
                0, 1, 'fixation', 2002003, 2002122, 119,
                857.3724975585938, 422.3450012207031, 'preprocessing',
            ),
            (
                0, 1, 'fixation', 2002160, 2002306, 146,
                936.1646118164062, 418.0686950683594, 'preprocessing',
            ),
            (
                0, 1, 'fixation', 2002308, 2002442, 134,
                940.3585205078125, 416.9755554199219, 'preprocessing',
            ),
            (0, 1, 'fixation', 2002495, 2002603, 108, 1034.3890380859375, 409.68255615234375, ''),
            (0, 1, 'fixation', 2002709, 2002831, 122, 134.06097412109375, 491.251220703125, ''),
            (0, 1, 'fixation', 2002863, 2003003, 140, 161.3858184814453, 482.514892578125, ''),
            (0, 1, 'fixation', 2003042, 2003424, 382, 211.2224578857422, 483.4208984375, ''),
            (0, 1, 'fixation', 2003453, 2003657, 204, 283.94683837890625, 485.6600036621094, ''),
            (0, 1, 'fixation', 2003721, 2003917, 196, 422.4142150878906, 484.2720947265625, ' '),
            (0, 1, 'fixation', 2003968, 2004074, 106, 509.65234375, 480.1925354003906, 'Python'),
            (0, 1, 'fixation', 2004132, 2004331, 199, 610.8610229492188, 484.6025085449219, 'package'),  # noqa:E501
            (0, 1, 'fixation', 2004399, 2004687, 288, 717.8470458984375, 486.0269775390625, ''),
            (0, 1, 'fixation', 2004714, 2004878, 164, 785.6884765625, 481.4891052246094, ''),
            (0, 1, 'fixation', 2004931, 2005109, 178, 896.4055786132812, 480.51898193359375, ''),
            (0, 1, 'fixation', 2005138, 2005287, 149, 933.6119995117188, 481.8833312988281, ''),
        ],
        schema=[
            'text_id',
            'page_id',
            'name',
            'onset',
            'offset',
            'duration',
            'location_x',
            'location_y',
            'area_of_interest',
        ],
        orient='row',
    ),
}


@pytest.fixture(name='dataset')
def dataset_fixture():
    dataset = pm.Dataset('ToyDataset', 'toy_dataset')
    dataset.download()
    dataset.load()
    dataset.pix2deg()
    dataset.pos2vel()
    dataset.detect_events('ivt')
    dataset.compute_event_properties(('location', {'position_column': 'pixel'}))
    yield dataset


@pytest.mark.parametrize(
    ('aoi_column'),
    [
        'word',
        'char',
    ],
)
def test_gaze_to_aoi_mapping_char_width_height(aoi_column, dataset):
    aoi_df = pm.stimulus.text.from_file(
        'tests/files/toy_text_1_1_aoi.csv',
        aoi_column=aoi_column,
        start_x_column='top_left_x',
        start_y_column='top_left_y',
        width_column='width',
        height_column='height',
        page_column='page',
    )

    dataset.events[0].map_to_aois(aoi_df)
    assert_frame_equal(dataset.events[0].frame, EXPECTED_DF[aoi_column])


@pytest.mark.parametrize(
    ('aoi_column'),
    [
        'word',
        'char',
    ],
)
def test_gaze_to_aoi_mapping_char_end(aoi_column, dataset):
    aoi_df = pm.stimulus.text.from_file(
        'tests/files/toy_text_1_1_aoi.csv',
        aoi_column=aoi_column,
        start_x_column='top_left_x',
        start_y_column='top_left_y',
        end_x_column='bottom_left_x',
        end_y_column='bottom_left_y',
        page_column='page',
    )

    dataset.events[0].map_to_aois(aoi_df)
    assert_frame_equal(dataset.events[0].frame, EXPECTED_DF[aoi_column])


def test_map_to_aois_raises_value_error():
    aoi_df = pm.stimulus.text.from_file(
        'tests/files/toy_text_1_1_aoi.csv',
        aoi_column='char',
        start_x_column='top_left_x',
        start_y_column='top_left_y',
        width_column='width',
        height_column='height',
        page_column='page',
    )
    gaze_df = pm.gaze.io.from_csv(
        'tests/files/judo1000_example.csv',
        **{'separator': '\t'},
        position_columns=['x_left', 'y_left', 'x_right', 'y_right'],
    )

    with pytest.raises(ValueError) as excinfo:
        gaze_df.map_to_aois(aoi_df, eye='right', gaze_type='')
    msg, = excinfo.value.args
    assert msg == 'neither position nor pixel in gaze dataframe, one needed for mapping'


def test_map_to_aois_raises_value_error_missing_width_height(dataset):
    aoi_df = pm.stimulus.text.from_file(
        'tests/files/toy_text_1_1_aoi.csv',
        aoi_column='char',
        start_x_column='top_left_x',
        start_y_column='top_left_y',
        page_column='page',
    )
    with pytest.raises(ValueError) as excinfo:
        dataset.events[0].map_to_aois(aoi_df)
    msg, = excinfo.value.args
    assert msg == 'either aoi_dataframe.width or aoi_dataframe.end_x_column have to be not None'
