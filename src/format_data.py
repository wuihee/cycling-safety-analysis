"""
Throughout this project, I collected data from the sensors through different
means, from which the data was stored in different formats. The idea of this
module is to reformat each set of data in a fixed structure. Distance
measurements by each sensor should be stored in a text file, each line
representing a point of measurement. Each line should be formatted as such:

TIME DISTANCE SIGNAL_STRENGTH

where, time, distance, and signal strength are values separated by a space.
"""

import os
import pathlib

from format import laser, tof

os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Basic TOF indoors and outdoors test by software stored in excel files.
TOF_INDOORS_RAW_DATA = pathlib.Path("./raw_data/tof_basic_tests/indoors")
TOF_OUTDOORS_RAW_DATA = pathlib.Path("./raw_data/tof_basic_tests/outdoors")
TOF_INDOORS_DATA = pathlib.Path("./data/tof_basic_tests/indoors")
TOF_OUTDOORS_DATA = pathlib.Path("./data/tof_basic_tests/outdoors")
tof.format_excel(TOF_INDOORS_RAW_DATA, TOF_INDOORS_DATA)
tof.format_excel(TOF_OUTDOORS_RAW_DATA, TOF_OUTDOORS_DATA)

# Basic outdoors test with shade by Raspberry Pi stored in text file.
TOF_WITH_SHADE_RAW_DATA = pathlib.Path("./raw_data/tof_basic_tests/with_shade")
TOF_WITH_SHADE_DATA = pathlib.Path("./data/tof_basic_tests/with_shade")
tof.format_text(TOF_WITH_SHADE_RAW_DATA, TOF_WITH_SHADE_DATA)

# Basic laser indoor test by software stored in text file.
LASER_INDOORS_RAW_DATA = pathlib.Path("./raw_data/laser_basic_tests/indoors")
LASER_INDOORS_DATA = pathlib.Path("./data/laser_basic_tests/indoors")
laser.format_protocol_data(LASER_INDOORS_RAW_DATA, LASER_INDOORS_DATA)

# Basic laser outdoor test by Raspberry Pi stored in text file.
LASER_OUTDOORS_RAW_DATA = pathlib.Path("./raw_data/laser_basic_tests/outdoors")
LASER_OUTDOORS_DATA = pathlib.Path("./data/laser_basic_tests/outdoors")
tof.format_text(LASER_OUTDOORS_RAW_DATA, LASER_OUTDOORS_DATA)

# Outdoors stationary test by software stored in text file.
LASER_CYCLING_TEST_RAW_DATA = pathlib.Path("./raw_data/laser_outdoor_tests/")
LASER_CYCLING_TEST_DATA = pathlib.Path("./data/laser_outdoor_tests")
laser.format_ascii_data(LASER_CYCLING_TEST_RAW_DATA, LASER_CYCLING_TEST_DATA)
