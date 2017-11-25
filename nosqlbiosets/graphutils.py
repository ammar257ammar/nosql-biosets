""" Methods to return and save graphs in Cytoscape.js, D3js, GML
 and GraphML formats """
import json

import networkx


# Return NetworkX graphs in Cytoscape.js JSON format
# https://stackoverflow.com/questions/45342470/
# how-to-show-a-network-generated-by-networkx-in-cytoscape-js
def networkx2cytoscape_json(networkxgraph):
    cygraph = dict()
    cygraph["nodes"] = []
    cygraph["edges"] = []
    for node in networkxgraph.nodes():
        nx = dict()
        nx["data"] = {}
        nx["data"]["id"] = node
        nx["data"]["label"] = node
        cygraph["nodes"].append(nx.copy())
    for edge in networkxgraph.edges():
        nx = dict()
        nx["data"] = {}
        nx["data"]["id"] = edge[0] + edge[1]
        nx["data"]["source"] = edge[0]
        nx["data"]["target"] = edge[1]
        cygraph["edges"].append(nx)
    return cygraph


def networkx2d3_json(networkxgraph):
    d3 = dict()
    d3["nodes"] = []
    d3["links"] = []
    for node in networkxgraph.nodes():
        nx = dict()
        nx["id"] = node
        nx["label"] = node
        d3["nodes"].append(nx.copy())
    for edge in networkxgraph.edges():
        nx = dict()
        nx["source"] = edge[0]
        nx["target"] = edge[1]
        d3["links"].append(nx)
    return d3


# Save NetworkX graph in a format based on the selected file extension
# If the file name ends with .xml suffix [GraphML](
#    https://en.wikipedia.org/wiki/GraphML) format is selected,
# If the file name ends with .d3.json extension graph is saved in
# a form easier to read with [D3js](d3js.org),
# If the file name ends with .json extension graph is saved in
# [Cytoscape.js](js.cytoscape.org) graph format,
# Otherwise it is saved in GML format
def save_graph(graph, outfile):
    if outfile.endswith(".xml"):
        networkx.write_graphml(graph, outfile)
    elif outfile.endswith(".d3js.json"):
        cygraph = networkx2d3_json(graph)
        json.dump(cygraph, open(outfile, "w"), indent=4)
    elif outfile.endswith(".json"):
        cygraph = networkx2cytoscape_json(graph)
        json.dump(cygraph, open(outfile, "w"), indent=4)
    else:  # Assume GML format
        networkx.write_gml(graph, outfile)