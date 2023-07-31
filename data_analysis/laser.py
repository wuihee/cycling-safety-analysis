def get_data(protocol: str) -> list[str]:
    """
    Split the laser sensor's protocol into a list of easily retrievable values.

    Args:
        protocol (str): [Date Information] followed by 13 Bytes in hex.

    Returns:
        list[str]: A list containing the bytes without the date time information.
    """
    _, data = protocol.split("]")
    return data.split()


def get_distance(protocol: str) -> int:
    """
    Find the distance measured given the protocol of the laser sensor's output.

    Args:
        protocol (str): [Date Information] followed by 13 Bytes in hex.

    Returns:
        int: Distance measured.
    """
    # if not self.is_valid(protocol):
    #     return -1

    data = get_data(protocol)
    distance = "".join(data[7:10])
    if distance:
        return int(distance, base=16)
    return -1


def replace_intervals_with_distance(raw_data: list[list[str]]) -> list[list[float]]:
    new_data = []
    for interval_data in raw_data:
        new_data.append(replace_protocols_with_distance(interval_data))
    return new_data


def replace_protocols_with_distance(protocols: list[str]) -> list[float]:
    distances = []
    for protocol in protocols:
        distance = round(get_distance(protocol) / 1000, 2)
        distances.append(distance)
    return distances
