import matplotlib.pyplot as plt
from utils import cd_to_parent_dir

cd_to_parent_dir()

distances = []

with open("tof_data.txt") as file:
    for data in file:
        t, distance = data.split()
        distances.append(int(distance))

plt.plot(distances)
plt.show()
