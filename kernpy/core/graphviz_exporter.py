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
            file.write('    node [shape=record];\n');
            file.write('    rankdir=TB;\n')  # Ensure the overall layout is top to bottom
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
        header_label = f'header #{node.header_node.id}' if node.header_node else ''
        last_spine_operator_label = f'last spine op. #{node.last_spine_operator_node.id}' if node.last_spine_operator_node else ''

        top_record_label = f'{{ #{node.id}| {header_label} | {last_spine_operator_label}}}'
        signatures_label = ''
        if node.last_signature_nodes and node.last_signature_nodes.nodes:
            for k, v in node.last_signature_nodes.nodes.items():
                if signatures_label:
                    signatures_label += '|'
                #signatures_label += f'{{ {k} {v};\n"'
                signatures_label += f'{k} #{v.id}'

        file.write(f'  "{self.node_id(node)}" [label="{{ {top_record_label} | {signatures_label} | {self.export_token(node.token)} }}"];\n')
        for child in node.children:
            self._write_nodes(child, file)

    def _write_edges(self, node, file):
        for child in node.children:
            file.write(f'  "{self.node_id(node)}" -> "{self.node_id(child)}";\n')
            self._write_edges(child, file)
