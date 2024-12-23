import aocd
import networkx
from typing import DefaultDict
from tqdm import tqdm as progress

import cli


sample_data = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
data = sample_data if cli.sample else aocd.data

connections = DefaultDict[str, list[str]](lambda: [])
for l in data.splitlines():
    [f, t] = l.split("-")
    connections[f].append(t)
    connections[t].append(f)

################################################################################################
# Problem 1
t_devices = list(filter(lambda d: d[0] == "t", connections.keys()))

three_networks: set[tuple[str, str, str]] = set()
for first_device in progress(t_devices):
    for second_device in connections[first_device]:
        for third_device in connections[second_device]:
            if third_device == first_device:
                continue

            if first_device not in connections[third_device]:
                continue

            network = tuple(sorted([first_device, second_device, third_device]))
            three_networks.add(network)

print(f"Problem 1: {len(three_networks)}")


################################################################################################
# Problem 2
graph = networkx.Graph()
for f, ts in connections.items():
    for t in ts:
        graph.add_edge(f, t)

largest_network = max(networkx.find_cliques(graph), key=len)
print(f"Problem 1: {",".join(sorted(largest_network))}")
