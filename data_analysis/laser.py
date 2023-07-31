def get_data(self, protocol: str) -> list[str]:
    """
    Split the laser sensor's protocol into a list of easily retrievable values.

    Args:
        protocol (str): [Date Information] followed by 13 Bytes in hex.

    Returns:
        list[str]: A list containing the bytes without the date time information.
    """
    _, data = protocol.split("]")
    return data.split()


def is_valid(self, protocol: str) -> bool:
    """
    Check if a given protocol is valid.

    Args:
        protocol (str): [Date Information] followed by 13 Bytes in hex.

    Returns:
        bool: Return true if the protocol is valid.
    """
    data = self.get_data(protocol)
    checksum = data[-1]
    total_sum = 0

    for byte in data[:-1]:
        total_sum += int(byte, base=16)

    return total_sum == checksum


def get_distance(self, protocol: str) -> int:
    """
    Find the distance measured given the protocol of the laser sensor's output.

    Args:
        protocol (str): [Date Information] followed by 13 Bytes in hex.

    Returns:
        int: Distance measured.
    """
    # if not self.is_valid(protocol):
    #     return -1

    data = self.get_data(protocol)
    distance = "".join(data[7:10])
    return int(distance, base=16)
