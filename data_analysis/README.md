# Data Analysis

A secondary objective I had for this project was to keep my code clean and modular. This was not only to maintain the integrity of my code, but to train myself to write code in a disciplined manner.

I definitely felt that at some points, this level of modularization was unnecessary and a little redundant. However, as someone not used to writing clean code, I took this upon myself as a learning experience.

## Code

While creating my Jupyter Notebooks to display the data collected, I quickly ran into the problem of having my notebooks fill up with huge chunks of auxilliary code unrelated to the data analysis. As a result, I decided to split the auxilliary code into separate modules, and import them when needed. This kept the code in my Notebooks minimal and allowed the focus to remain on the data analysis. I will be describing the functions and challenges of each module.

### [`format`](./data_analysis/format/)

One of the biggest difficulties in keeping my code modular was dealing with the different ways the data collected was formatted. For instance, the code extracted from the WaveShare's software was found in an excel file, whereas when I used a Raspberry Pi, I had the data output to a text file. Therefore, I needed a fixed format in which the data was stored, so I could extract every file of data using the same function, instead of creating a new function for every new format. I created a module `format` that contianed auxilliary functions to format all data collected into a consistent format, and store them in a text file.

Each line in the text file would contain time, distance, and signal strength separate by a space, where -1 represents null values. For example:

```text
13:20:45 3540 -1
```

### [`format_data.py`](./data_analysis/format_data.py)

I then imported the `format` module and used it to format the data I wanted in this script.

### [`data_loader.py`](./data_analysis/data_loader.py)

Once I had a fix format which all the data was stored, I needed a way to easily extract the data. I hated to see my Notebooks cluttered with ugly code to in the process of extracting the data. `data.py` contains two classes: `FolderData`, which is concerned with storing the data from folders and `DataLoader` which helps to extract the data from files and folders.

For example, if I wanted to extract an entire folder of distance measurements for each distance interval, I would use `FolderData`.

```python
from data import FolderData

data = FolderData(PATH_TO_FOLDER)
distances = data.distances
```

Or, if I wanted to extract data from a file only, I would use the `load_data_from_file` function.

```python
import data_loader

timings, distances, signal_strengths = data_loader.load_data_from_file(PATH_TO_FILE)
```

### [`basic_graphs.py`](./data_analysis/basic_graphs.py)

For both the TOF and laser sensor, I wanted to plot the same graphs many times for comparison and analysis. Thus, it only made sense to create a module with resuable code to do this. `basic_graphs.py` contained the code that let me easily graph the data collected during the basic tests.

For example, if I wanted to plot a scatter plot of all the distances measured for a stationary test, I would use the `plot_scatter` method of `BasicGraphs`.

```python
import matplotlib.pyplot as plt

import basic_graphs
from data_loader import FolderData

data = FolderData(PATH_TO_FOLDER)

fig, ax = plt.subplots(figsize=(6, 5))
basic_graphs.plot_scatter(ax, data.distances, title="Scatter Plot of All Data")
```

![Sample Scatter Plot](./images/sample_scatter_plot.png)

### [`outdoor_graphs.py`](./data_analysis/outdoor_graphs.py)

On the other hand, `outdoor_graphs.py` let helped me to graph data collected in the outdoor experiements. For example, after I collected a list of points from cycling on the road and wanted to plot a scatter, I would use the `scatter_time_vs_distance` function.

```python
import matplotlib.pyplot as plt

import data_loader
import outdoor_graphs

timing, distance, signal_strength = data_loader.load_data_from_file(PATH_TO_FILE)

fig, ax = plt.subplots(figsize=(13, 5))
outdoor_graphs.scatter_time_vs_distance(ax, timing, distance, title="Scatter Plot of Time vs Distance")
```

![Sample Time vs Distance Scatter](./images/sample_time_vs_distance_scatter.png)

### [`data_cleaner.py`](./data_analysis/data_cleaner.py)

Next, I often needed to clean the data I collected in various ways. For example, cleaning the spurious data points collected by the TOF sensor.

```python
import data_cleaner

cleaned_distances = data_cleaner.clean_spurious_data(distances)
```

![Sample Cleaned Scatter](./images/sample_cleaned_scatter.png)

### [`preprocessing.py`](./data_analysis/preprocessing.py)

Finally, the preprocessing module handles the processing of data. and includes auxlliary functions to find the mean, standard deviation, etc. of an array of data.
