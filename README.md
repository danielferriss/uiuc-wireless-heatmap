# Uiuc Wireless Heatmap

This project gets wireless data connections for university properties from their api and makes a heatmap showing this data.

Example Image:
![StillHeatmap](https://github.com/danielferriss/uiuc-wireless-heatmap/blob/master/examples/recentmap.png)

You can get animated heatmaps of a day as well.

![HeatmapBuildingScale](https://github.com/danielferriss/uiuc-wireless-heatmap/blob/master/examples/2019-01-23.gif)

The weight of the heatmap points can either be scaled building by building, which is showed in the previous video, or by the maximum number of connected devices on campus, shown here:

![HeatmapMaxScale](https://github.com/danielferriss/uiuc-wireless-heatmap/blob/master/examples/2019-01-23-max-scale.gif)

The difference between these options is that when scaled by building every point will cycle through a weight from its minimum value to 1. In other words, every building will change color from transparent to bright red every day, with bright red being its busiest time.

## Prerequisites

Packages required:
* urllib.request
* json
* math
* folium

## Usage
To get a still heatmap of the most recent data use most_recent.ipynb
To get an animated heatmap of a certain day use day_data.ipynb and change the date to whatever you would like to get data for.

## Examples
Examples for the wednesday before our cold day, the cold day, and the wednesday after can be found in the examples folder. There is a version for both ways of scaling weights.
PLEASE NOTE: When running the exmaples in browser you must disable any adblocker or HTML5 video blocker as they will not allow the animation to run.

## Built With

* [urllib](https://docs.python.org/3/library/urllib.request.html) - Used to grab data from api endpoint
* [json](https://docs.python.org/3/library/json.html) - Used to parse json data
* [folium](https://python-visualization.github.io/folium/) - Used to generate heatmaps



## Author

* **Daniel Ferriss** - [website](https://danielferriss.com)
