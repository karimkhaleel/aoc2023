from graphviz import Digraph


def create_circuit_graph(input_text):
    dot = Digraph(comment="Circuit Diagram")
    dot.attr(rankdir="LR")

    dot.attr("node", shape="box")

    nodes = set()
    edges = set()

    for line in input_text.strip().split("\n"):
        if "->" not in line:
            continue

        left, right = line.split("->")
        left = left.strip()
        right = right.strip()

        if " AND " in left:
            op = "AND"
            inputs = left.split(" AND ")
        elif " OR " in left:
            op = "OR"
            inputs = left.split(" OR ")
        elif " XOR " in left:
            op = "XOR"
            inputs = left.split(" XOR ")
        else:
            continue

        for input_node in inputs:
            input_node = input_node.strip()
            if input_node not in nodes:
                if input_node.startswith(("x", "y")):
                    dot.node(input_node, input_node, color="blue")
                else:
                    dot.node(input_node, input_node)
                nodes.add(input_node)

        if right not in nodes:
            if right.startswith("z"):
                dot.node(right, right, color="red")
            else:
                dot.node(right, right)
            nodes.add(right)

        op_node = f"{inputs[0]}_{op}_{inputs[1]}"
        dot.node(op_node, op, shape="ellipse")

        for input_node in inputs:
            input_node = input_node.strip()
            edge = (input_node, op_node)
            if edge not in edges:
                dot.edge(input_node, op_node)
                edges.add(edge)

        edge = (op_node, right)
        if edge not in edges:
            dot.edge(op_node, right)
            edges.add(edge)

    return dot


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        circuit_text = f.read()

    dot = create_circuit_graph(circuit_text)

    dot.render("dg", view=True, format="pdf", engine="dot")
