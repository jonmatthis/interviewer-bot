import re
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

def parse_archgraph(file_path):
    nodes = {}
    dependencies = []

    with open(file_path, 'r') as file:
        for line in file:
            # Parse node declaration
            node_match = re.match(r'node\s+(\w+)\s+<([^>]+)>\s+"([^"]+)";', line)
            if node_match:
                node_id, node_type, node_label = node_match.groups()
                nodes[node_id] = {'type': node_type, 'label': node_label, 'properties': {}}
                continue

            # Parse node properties
            prop_match = re.match(r'node\s+(\w+)\s+\(([^)]+)\)\s+{([^}]*)}', line)
            if prop_match:
                node_id, node_type, props_str = prop_match.groups()
                properties = dict(re.findall(r'\s*(\w+)\s*=\s*(\w+)', props_str))
                nodes[node_id]['properties'].update(properties)

            # Parse dependency declaration
            dependency_match = re.match(r'dependency\s+(\w+)\s+->\s+(\w+)(?:\s+"([^"]+)")?;', line)
            if dependency_match:
                source, target, label = dependency_match.groups()
                dependencies.append((source, target, label))

    return nodes, dependencies

def draw_graph(nodes, dependencies, node_font_size=14, edge_font_size=12):
    G = nx.DiGraph()

    # Add nodes to the graph
    for node_id, node_info in nodes.items():
        prop_str = ', '.join(f'{k}={v}' for k, v in node_info['properties'].items())
        if prop_str:
            prop_str = f'{{{prop_str}}}'
        G.add_node(node_id, label=f'{node_info["label"]}\n<{node_info["type"]}>\n{prop_str}')

    # Add dependencies to the graph
    for source, target, label in dependencies:
        G.add_edge(source, target, label=label)

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=node_font_size)
    
    # Draw edge labels
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True) if d['label'] is not None}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=edge_font_size)

    # Show the graph
    plt.show()

if __name__ == '__main__':
    script_path = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_path, 'interviewer_bot.ag')

    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found.")
        sys.exit(1)

    nodes, dependencies = parse_archgraph(input_file)
    draw_graph(nodes, dependencies, node_font_size=18, edge_font_size=14)
