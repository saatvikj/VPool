# VPool

VPool is a python implementation for the project titled "Optimization problems in vehicle route network design" developed at IIIT Delhi as part of my undergraduate thesis. The project aims at tackling the problem of inefficient vehicle sharing systems currently present in public transport domain and mobility on demand systems by suggesting changes in the way route planning and ride combining for sharing based systems is done while assuring optimization in several other domains.

## Workflow

The problem is tackled in a 3 phase approach:
* Problem modelling in terms of graph.
* Application of graph algorithms to get desired solution.
* Optimization of different domains on obtained solution.

## Dependencies

Python libraries required for running the code:

```
numpy
pandas
gurobipy
osrm
datetime
networkx
```

## Running the code

In order to run the code, first obtain either a pickled format or csv format of the dataset you are going to run it on and then type the command:
```
python driver_script.py -option
```
Where option is 1 for pickle file and 2 for csv file.
It is to be noted that csv file should be in NYC Taxi Data format only.
