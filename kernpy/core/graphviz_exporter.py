from __future__ import annotations

import sys
from pathlib import Path
from unicodedata import category

from kernpy.core import Token, SpineOperationToken
from kernpy.core.document import MultistageTree, Node


class GraphvizExporter:
    def export_token(self, token: Token):
        if token is None or token.encoding is None:
            return ''
        else:
            return token.encoding.replace('\"', '\\"').replace('\\', '\\\\')

    @staticmethod
    def node_id(node: Node):
        return f"node{id(node)}"

    def export_to_dot(self, tree: MultistageTree, filename: Path = None):
        """
        Export the given MultistageTree to DOT format.

        Args:
            tree (MultistageTree): The tree to export.
            filename (Path or None): The output file path. If None, prints to stdout.
        """
        file = sys.stdout if filename is None else open(filename, 'w')

        try:
            file.write('digraph G {\n')
            file.write('    node [shape=record];\n')
            file.write('    rankdir=TB;\n')  # Ensure top-to-bottom layout

            # Create subgraphs for each stage
            for stage_index, stage in enumerate(tree.stages):
                if stage:
                    file.write('  {rank=same; ')
                    for node in stage:
                        file.write(f'"{self.node_id(node)}"; ')
                    file.write('}\n')

            # Write nodes and their connections
            self._write_nodes_iterative(tree.root, file)
            self._write_edges_iterative(tree.root, file)

            file.write('}\n')

        finally:
            if filename is not None:
                file.close()  # Close only if we explicitly opened a file

    def _write_nodes_iterative(self, root, file):
        stack = [root]

        while stack:
            node = stack.pop()
            header_label = f'header #{node.header_node.id}' if node.header_node else ''
            last_spine_operator_label = f'last spine op. #{node.last_spine_operator_node.id}' if node.last_spine_operator_node else ''
            category_name = getattr(getattr(getattr(node, "token", None), "category", None), "_name_", "Non defined category")


            top_record_label = f'{{ #{node.id}| stage {node.stage} | {header_label} | {last_spine_operator_label} | {category_name} }}'
            signatures_label = ''
            if node.last_signature_nodes and node.last_signature_nodes.nodes:
                for k, v in node.last_signature_nodes.nodes.items():
                    if signatures_label:
                        signatures_label += '|'
                    signatures_label += f'{k} #{v.id}'

            if isinstance(node.token, SpineOperationToken) and node.token.cancelled_at_stage:
                signatures_label += f'| {{ cancelled at stage {node.token.cancelled_at_stage} }}'

            file.write(f'  "{self.node_id(node)}" [label="{{ {top_record_label} | {signatures_label} | {self.export_token(node.token)} }}"];\n')

            # Add children to the stack to be processed
            for child in reversed(node.children):
                stack.append(child)

    def _write_edges_iterative(self, root, file):
        stack = [root]

        while stack:
            node = stack.pop()
            for child in node.children:
                file.write(f'  "{self.node_id(node)}" -> "{self.node_id(child)}";\n')
                stack.append(child)
