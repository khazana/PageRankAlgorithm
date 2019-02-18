# PageRankAlgorithm
This project contains three python files: 1)zipf_law.py 2)simple_webgraph.py 3)focused_webgraph.py 4)pagerank.py.

1)Zip_law.py contains the code which gives the loglog plot of Rank Vs Frequency of trigrams collected from the documents provided in BFS.txt. Running it also saves a text file called Trigrams.txt which is a file consisting of trigrams and their frequencies in sorted order. It also gives the plot in a file called Zipf.png.

2)simple_webgraph.py takes BFS.txt as input and generates a graph with links from BFS.txt as nodes and incoming links as edges. It saves this graph in dictionary format as G1.txt. It also prints the graph's statistics.

3)focused_webgraph.py takes FOCUSED.txt as input and generates a graph with links from FOCUSED.txt as nodes and incoming links as edges. This links are extracted based on relevancy, a node will have incoming or outgoing links only if those links are very relevant to that node. It saves this graph in dictionary format as G2.txt. It also prints the graph's statistics.

4)pagerank.py contains the function to compute page rank values and print the sum and L2 norm values in sorted order. The 'compute_rank()' function has to be included in the simple_webgraph.py or focused_webgraph.py, depending on whose values are required to use it. It doesn't handle rank sinks similar to the pseudocode implemented in the book 'Search Engines' (W. Bruce Croft, Donald Metzler, Trevor Strohman). The default surprise parameter is chosen as '0.15'.

## Libraries used
urllib.request, nltk, Beautiful soup, httplib2, collections, numpy, itertools, string, re, os, matplotlib.pyplot

## Installation
 
You need BFS.txt and FOCUS.txt saved in the same directory as this project to run it. This project requires Python 3. There are a few packages which have to be installed to be able to run the code. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install them as follows:


```bash
pip install numpy
pip install urllib
pip install bs4 
pip install nltk
pip install httplib2
pip install collections
pip install matplotlib
```

## Usage

```bash
python zipf_law.py 
python simple_webgraph.py
python focused_webgraph.py 
python pagerank.py
```

