# VPool

VPool is a python implementation for the project titled "Optimization problems in vehicle route network design" developed at IIIT Delhi as part of my undergraduate thesis. The project aims at tackling the problem of inefficient vehicle sharing systems currently present in public transport domain and mobility on demand systems by suggesting changes in the way route planning and ride combining for sharing based systems is done while assuring optimization in several other domains.

## Workflow

The problem is tackled in a 3 phase approach:
* Problem modelling in terms of graph.
* Application of graph algorithms to get desired solution.
* Optimization of different domains on obtained solution.

## Dependencies

The code runs an instance of the python wrapper of the Gurobi mathematical programming solver, you will need to obtain your own license and get access to the python wrapper.

Some basic python libraries required for running the code (add ons and backend requirements to these are listed in requirements.txt):

```
numpy
pandas
gurobipy
datetime
networkx
folium
```

The code requires an instance of osrm running on your local system with the open street data of the area you are looking to run it on. A good starters guide to setting up and running an osrm instance on localhost is available at [this](https://reckoningrisk.com/coding/2017/OSRM-server/) link. If you instead want to use the demo server, follow the following steps-
* Navigate to utilities > ride_utility.py
* Change 127.0.0.1:5000 in request string everywhere to router.project-osrm.org

However, since this is a public server, there are no assurances of it working for all requests due to limit exhaustion, server load etc.
## Running the code

In order to run the code, first obtain either a pickled format or csv format of the dataset you are going to run it on, and then type the command:
```
pip install -r requirements.txt
python driver_script.py option input_filepath output_filepath 
```
Where option is 1 for pickle file and 2 for csv file, input_filepath is full path of the data file (no spaces), output_filepath is an optional argument which would enable to pickle the graph and distance data obtained during the run of the code.
It is to be noted that csv file should be in NYC Taxi Data format only.