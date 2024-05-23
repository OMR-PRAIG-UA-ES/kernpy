import string

from kernpy.core import Token
from kernpy.core.document import MultistageTree, Node


class GraphvizExporter():
    def export_token(self, token: Token) -> string:
        if token is None or token.encoding is None:
            return ''
        else:
            return token.encoding.replace('\"', '\\"').replace('\\', '\\\\')

    @staticmethod
    def node_id(node: Node) -> string:
        return f"node{id(node)}"

    def export_to_dot(self, tree: MultistageTree, filename):
        with open(filename, 'w') as file:
            file.write('digraph G {\n')
            file.write('  rankdir=TB;\n')  # Ensure the overall layout is top to bottom
            # Create subgraphs for each stage
            for stage_index, stage in enumerate(tree.stages):
                if stage:
                    file.write(f'  {{rank=same; ')
                    for node in stage:
                        file.write(f'"{self.node_id(node)}"; ')
                    file.write('}\n')

            # Write nodes and their connections
            self._write_nodes(tree.root, file)
            self._write_edges(tree.root, file)

            file.write('}\n')

    def _write_nodes(self, node, file):
        file.write(f'  "{self.node_id(node)}" [label="{self.export_token(node.token)}"];\n')
        for child in node.children:
            self._write_nodes(child, file)

    def _write_edges(self, node, file):
        for child in node.children:
            file.write(f'  "{self.node_id(node)}" -> "{self.node_id(child)}";\n')
            self._write_edges(child, file)
