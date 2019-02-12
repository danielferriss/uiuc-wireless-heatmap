# uiuc-wireless-heatmap

The python file in this repository contains functions to get data and form it into the correct input style for heatmaps.
You can see how to create a heatmap of the most recent data by running most_recent.ipynb
You can see how to create an animated heatmaps of a day's worth of data by running day_data.ipynb

There are animated heatmap examples in the examples folder. There are two heatmaps for each example day.
The one that has max-scale in its name scales the weight of each point by the highest number of connected devices in a day. The other file scales each building by its own highest device count. This means that the max scale buildings may not show much of an effect throughout the day if they are insignificant in comparison to the more used buildings, while for the non-max-scaled map each building will go from a weight of 0 to a weight of 1 every day.

##########IMPORTANT NOTE ##########
When running the example animated heatmaps in browser you MUST disable adblock and and html5 video blockers. Otherwise the heatmap will not display!
