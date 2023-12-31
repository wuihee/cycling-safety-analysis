from pathlib import Path

from cycling_safety_analysis.format import jrt_bb2x, raspberry_pi, tof

# Base Directories
BASE_RAW_DATA = Path("./data/raw")
BASE_DATA = Path("./data/processed")

# Formatting TOF Basic Tests
TOF_BASE_RAW = BASE_RAW_DATA / "tof_basic_tests"
TOF_BASE_DATA = BASE_DATA / "tof_basic_tests"
tof_in_raw_pairs = [
    (TOF_BASE_RAW / "indoors", TOF_BASE_DATA / "indoors"),
    (TOF_BASE_RAW / "outdoors", TOF_BASE_DATA / "outdoors"),
    (TOF_BASE_RAW / "with_shade", TOF_BASE_DATA / "with_shade"),
]
for raw, data in tof_in_raw_pairs:
    if "with_shade" in str(raw):
        raspberry_pi.format_text(raw, data)
    else:
        tof.format_excel(raw, data)

# Formatting Laser Basic Tests
LASER_BASE_RAW = BASE_RAW_DATA / "laser_basic_tests"
LASER_BASE_DATA = BASE_DATA / "laser_basic_tests"
laser_in_raw_pairs = [
    (LASER_BASE_RAW / "indoors", LASER_BASE_DATA / "indoors"),
    (LASER_BASE_RAW / "outdoors", LASER_BASE_DATA / "outdoors"),
]
for raw, data in laser_in_raw_pairs:
    if "indoors" in str(raw):
        jrt_bb2x.format_protocol_data(raw, data)
    else:
        raspberry_pi.format_text(raw, data)

# Formatting Laser Outdoor Tests
jrt_bb2x.format_ascii_data(
    BASE_RAW_DATA / "laser_outdoor_tests", BASE_DATA / "laser_outdoor_tests"
)

# Formatting LIDAR Basic Tests
LIDAR_BASE_RAW = BASE_RAW_DATA / "lidar_basic_tests"
LIDAR_BASE_DATA = BASE_DATA / "lidar_basic_tests"
lidar_in_raw_pairs = [
    (LIDAR_BASE_RAW / "indoors", LIDAR_BASE_DATA / "indoors"),
    (LIDAR_BASE_RAW / "outdoors", LIDAR_BASE_DATA / "outdoors"),
]
for raw, data in lidar_in_raw_pairs:
    raspberry_pi.format_text(raw, data)

# Formatting Ultrasonic Basic Tests
ULTRASONIC_BASE_RAW = BASE_RAW_DATA / "ultrasonic_basic_tests"
ULTRASONIC_BASE_DATA = BASE_DATA / "ultrasonic_basic_tests"
ultrasonic_in_raw_pairs = [
    (ULTRASONIC_BASE_RAW / "indoors", ULTRASONIC_BASE_DATA / "indoors"),
    (ULTRASONIC_BASE_RAW / "outdoors", ULTRASONIC_BASE_DATA / "outdoors"),
]
for raw, data in ultrasonic_in_raw_pairs:
    raspberry_pi.format_text(raw, data)
