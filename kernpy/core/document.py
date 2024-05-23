from copy import copy
from collections import deque, defaultdict

from kernpy.core import MetacommentToken


class SignatureNodes:
    def __init__(self):
        self.nodes = {}  # key = Signature descendant token class (KeyToken, MeterSymbolToken, etc...) , value = node
        # - this way, we can add several tokens without repetitions

    def clone(self):
        result = SignatureNodes()
        result.nodes = copy(self.nodes)
        return result

    def update(self, node):
        self.nodes[not node.token.__class__.__name__] = node


from abc import ABC, abstractmethod


class TreeTraversalInterface(ABC):
    @abstractmethod
    def visit(self, node):
        pass


class Node:
    def __init__(self, stage, token, parent, last_spine_operator_node, last_signature_nodes: SignatureNodes,
                 header_node):
        self.token = token
        self.parent = parent
        self.children = []
        self.stage = stage
        self.header_node = header_node
        if last_signature_nodes:
            self.last_signature_nodes = last_signature_nodes.clone()  #TODO Documentar todo esto - composición
        else:
            self.last_signature_nodes = SignatureNodes()
        self.last_spine_operator_node = last_spine_operator_node

    def count_nodes_by_stage(self):
        level_counts = defaultdict(int)
        queue = deque([(self, 0)])  # (node, level)
        # breadth-first search (BFS)
        while queue:
            node, level = queue.popleft()
            level_counts[level] += 1
            for child in node.children:
                queue.append((child, level + 1))

        # Convert the level_counts dictionary to a list of counts
        max_level = max(level_counts.keys())
        counts_by_level = [level_counts[level] for level in range(max_level + 1)]

        return counts_by_level

    def dfs(self, tree_traversal: TreeTraversalInterface):
        node = self
        tree_traversal.visit(node)
        for child in self.children:
            child.dfs(tree_traversal)


class BoundingBoxMeasures:
    def __init__(self, bounding_box, from_measure, to_measure):
        self.from_measure = from_measure
        self.to_measure = to_measure
        self.bounding_box = bounding_box


class MultistageTree:
    def __init__(self):
        self.root = Node(0, None, None, None, None, None)
        self.stages = []
        self.stages.append([self.root])

    def add_node(self, stage, parent, token, last_spine_operator_node, previous_signature_nodes,
                 header_node=None) -> Node:
        node = Node(stage, token, parent, last_spine_operator_node, previous_signature_nodes, header_node)
        if stage == len(self.stages):
            self.stages.append([node])
        elif stage > len(self.stages):
            raise Exception(f'Cannot add node in stage {stage} for max. {len(self.stages)} stages')
        else:
            self.stages[stage].append(node)
        parent.children.append(node)
        return node

    def dfs(self, visit_method):
        self.root.dfs(visit_method)


class Document:
    def __init__(self, tree: MultistageTree):
        self.tree = tree  # each stage of the tree corresponds to a row in the **kern file
        self.measure_start_tree_stages = []  # starting from 1. Rows after removing empty lines and line comments
        self.page_bounding_boxes = {}
        self.header_stage = None  # the stage that contains the heders

    def get_header_stage(self):
        if self.header_stage:
            return self.tree.stages[self.header_stage]
        else:
            raise Exception('No header stage found')

    def get_leaves(self):
        return self.tree.stages[len(self.tree.stages) - 1]

    def get_spine_count(self):
        if self.header_stage:
            return len(self.tree.stages[self.header_stage])
        else:
            raise Exception('No header stage found')

    def get_metacomments(self, KeyComment=None, clear=False) -> list:
        """
        Get all metacomments in the document

        Args:
            KeyComment: Filter by a specific metacomment key: e.g. Use 'COM' to get only comments starting with\
                '!!!COM: '. If None, all metacomments are returned.
            clear: If True, the metacomment key is removed from the comment. E.g. '!!!COM: Coltrane' -> 'Coltrane'.\
                If False, the metacomment key is kept. E.g. '!!!COM: Coltrane' -> '!!!COM: Coltrane'. \
                The clear functionality is equivalent to the following code:
                ```python
                comment = '!!!COM: Coltrane'
                clean_comment = comment.replace(f"!!!{KeyComment}: ", "")
                ```
                Other formats are not supported.

        Returns: A list of metacomments.

        Examples:
            >>> document.get_metacomments()
            ['!!!COM: Coltrane', '!!!voices: 1', '!!!OPR: Blue Train']
            >>> document.get_metacomments(KeyComment='COM')
            ['!!!COM: Coltrane']
            >>> document.get_metacomments(KeyComment='COM', clear=True)
            ['Coltrane']
            >>> document.get_metacomments(KeyComment='non_existing_key')
            []
        """
        traversal = MetacommentsTraversal()
        self.tree.dfs(traversal)
        result = []
        for metacomment in traversal.metacomments:
            if KeyComment is None or metacomment.encoding.startswith(f"!!!{KeyComment}"):
                new_comment = metacomment.encoding
                if clear:
                    new_comment = metacomment.encoding.replace(f"!!!{KeyComment}: ", "")
                result.append(new_comment)

        return result

    def tokens_to_encodings(self, tokens):
        encodings = [token.encoding for token in tokens if token.encoding is not None]
        return encodings

    def get_all_tokens(self, filter_by_categories = None):
        traversal = TokensTraversal(False, filter_by_categories)
        self.tree.dfs(traversal)
        return traversal.tokens

    def get_all_tokens_encodings(self, filter_by_categories = None):
        tokens = self.get_all_tokens(filter_by_categories)
        return self.tokens_to_encodings(tokens)

    def get_unique_tokens(self, filter_by_categories = None):
        traversal = TokensTraversal(True, filter_by_categories)
        self.tree.dfs(traversal)
        return traversal.tokens

    def get_unique_token_encodings(self, filter_by_categories = None):
        tokens = self.get_unique_tokens(filter_by_categories)
        return self.tokens_to_encodings(tokens)


# tree traversal utils
class MetacommentsTraversal(TreeTraversalInterface):
    def __init__(self):
        self.metacomments = []

    def visit(self, node):
        if isinstance(node.token, MetacommentToken):
            self.metacomments.append(node.token)


class TokensTraversal(TreeTraversalInterface):
    def __init__(self, non_repeated: bool, filter_by_categories):
        self.tokens = []
        self.seen_encodings = []
        self.non_repeated = non_repeated
        self.filter_by_categories = filter_by_categories

    def visit(self, node):
        if node.token and (not self.non_repeated or node.token.encoding not in self.seen_encodings):
            self.tokens.append(node.token)
            if self.non_repeated:
                self.seen_encodings.append(node.token.encoding)
