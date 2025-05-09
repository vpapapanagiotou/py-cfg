from pathlib import Path
from typing import Generator, List

from pycfg.parsetree import TreeNode
from pycfg.symbol import Symbol


def traverse_1(root: TreeNode) -> Generator[TreeNode, None, None]:
    for node in root.children:
        yield from traverse_1(node)
    yield root


def create_dot_code(root: TreeNode) -> List[str]:
    count = 0
    for node in traverse_1(root):
        node.index = count
        count += 1

    dot_nodes = list()
    dot_leaves = list()
    dot_edges = list()
    for node in traverse_1(root):
        if len(node.children) == 0:
            dot_leaves.append(f'<n{node.index}> {node}')
        else:
            dot_nodes.append(f'  n{node.index} [label="{node}"]')
            for child in node.children:
                if len(child.children) == 0:
                    dot_edges.append(f'  n{node.index} -> s:n{child.index}')
                else:
                    dot_edges.append(f'  n{node.index} -> n{child.index}')
    dot_leaves_str = "|".join(dot_leaves)

    dot = list()
    dot.append('digraph G {')
    # dot.append('  node [shape="box"]')
    dot.append('')
    for dot_node in dot_nodes:
        dot.append(dot_node)
    dot.append('')
    dot.append(f'  s [shape="record", label="{dot_leaves_str}"]')
    dot.append('')
    for dot_edge in dot_edges:
        dot.append(dot_edge)
    dot.append('}')

    return dot


def save_dot_code(file: Path, dot_code: List[str]):
    with open(file, 'w') as fh:
        for line in dot_code:
            fh.write(line + '\n')


if __name__ == "__main__":
    root = TreeNode(Symbol('a'))
    root.append_children([Symbol('b1'), Symbol('b2')])
    root.children[1].append_child(Symbol('c'))

    dot_code = create_dot_code(root)
    save_dot_code(Path('../dot-files/test.txt'), dot_code)
    print('\n'.join(dot_code))
