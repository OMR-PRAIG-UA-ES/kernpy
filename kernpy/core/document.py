from copy import copy
from collections import deque, defaultdict
from abc import ABC, abstractmethod

from kernpy.core import MetacommentToken


class SignatureNodes:
    """
    SignatureNodes class.

    This class is used to store the last signature nodes of a tree.
    It is used to keep track of the last signature nodes.
    """
    def __init__(self):
        """
        Create an instance of SignatureNodes.

        Examples:
            >>> signature_nodes = SignatureNodes()
            >>> signature_nodes.nodes
            {}
        """
        self.nodes = {}  # key = Signature descendant token class (KeyToken, MeterSymbolToken, etc...) , value = node
        # - this way, we can add several tokens without repetitions

    def clone(self):
        """
        Create a deep copy of the SignatureNodes instance.
        Returns: A new instance of SignatureNodes with nodes copied.

        """
        result = SignatureNodes()
        result.nodes = copy(self.nodes)
        return result

    def update(self, node):
        self.nodes[node.token.__class__.__name__] = node


class TreeTraversalInterface(ABC):
    @abstractmethod
    def visit(self, node):
        pass


class Node:
    NextID = 1 # static counter
    """
    Node class.

    This class represents a node in a tree.
    The `Node` class is responsible for storing the main information of the **kern file.
    """
    def __init__(self, stage, token, parent, last_spine_operator_node, last_signature_nodes: SignatureNodes,
                 header_node):
        """
        Create an instance of Node.

        Args:
            stage: The stage of the node in the tree. The stage is similar to a row in the **kern file.
            token: The specific token of the node. The token can be a `KeyToken`, `MeterSymbolToken`, etc...
            parent: A reference to the parent `Node`. If the parent is the root, the parent is None.
            last_spine_operator_node: The last spine operator node.
            last_signature_nodes: A reference to the last `SignatureNodes` instance.
            header_node:
        """
        self.id = Node.NextID
        Node.NextID += 1
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

    FIRST_MEASURE = 1

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

    def get_first_measure(self) -> int:
        """
        Get the index of the first measure of the document.

        Returns: (Int) The index of the first measure of the document.

        Raises: Exception - If the document has no measures.

        Examples:
            >>> document = kernpy.read('score.krn')
            >>> document.get_first_measure()
            1
        """
        if len(self.measure_start_tree_stages) == 0:
            raise Exception('No measures found')

        return self.FIRST_MEASURE

    def measures_count(self) -> int:
        """
        Get the index of the last measure of the document.

        Returns: (Int) The index of the last measure of the document.

        Raises: Exception - If the document has no measures.

        Examples:
            >>> document = kernpy.read('score.krn')
            >>> document.measures_count()
            10
            >>> for i in range(document.get_first_measure(), document.measures_count() + 1):
            >>>   options = kernpy.ExportOptions(from_measure=i, to_measure=i+4)
        """
        if len(self.measure_start_tree_stages) == 0:
            raise Exception('No measures found')

        return len(self.measure_start_tree_stages) - 1  # starting from 1 (remove the root)

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

    @staticmethod
    def tokens_to_encodings(tokens: list):
        """
        Get the encodings of a list of tokens.

        The method is equivalent to the following code:
            >>> tokens = yourModule.get_all_tokens()
            >>> [token.encoding for token in tokens if token.encoding is not None]

        Args:
            tokens: list - A list of tokens.

        Returns: list[str] - A list of token encodings.

        Examples:
            >>> tokens = document.get_all_tokens()
            >>> Document.tokens_to_encodings(tokens)
            ['!!!COM: Coltrane', '!!!voices: 1', '!!!OPR: Blue Train']
        """
        encodings = [token.encoding for token in tokens if token.encoding is not None]
        return encodings

    def get_all_tokens(self, filter_by_categories=None):
        """
        Args:
            filter_by_categories: A list of categories to filter the tokens. If None, all tokens are returned.

        Returns:
            list - A list of tokens.


        """
        traversal = TokensTraversal(False, filter_by_categories)
        self.tree.dfs(traversal)
        return traversal.tokens

    def get_all_tokens_encodings(self, filter_by_categories = None):
        tokens = self.get_all_tokens(filter_by_categories)
        return Document.tokens_to_encodings(tokens)

    def get_unique_tokens(self, filter_by_categories = None) -> list:
        """
        Get unique tokens.

        Args:
            filter_by_categories: A list of categories to filter the tokens. If None, all tokens are returned.

        Returns:
            list - A list of unique tokens.

        """
        traversal = TokensTraversal(True, filter_by_categories)
        self.tree.dfs(traversal)
        return traversal.tokens

    def get_unique_token_encodings(self, filter_by_categories = None) -> list:
        """
        Get unique token encodings.

        Args:
            filter_by_categories: A list of categories to filter the tokens. If None, all tokens are returned.

        Returns: list[str] - A list of unique token encodings.

        """
        tokens = self.get_unique_tokens(filter_by_categories)
        return Document.tokens_to_encodings(tokens)

    def get_voices(self, clean=False):
        """
        Get the voices of the document.

        Args
            clean: Remove the first '!' from the voice name.

        Returns: A list of voices.

        Examples:
            >>> document.get_voices()
            ['!sax', '!piano', '!bass']
            >>> document.get_voices(clean=True)
            ['sax', 'piano', 'bass']
            >>> document.get_voices(clean=False)
            ['!sax', '!piano', '!bass']
        """
        from kernpy.core import TokenCategory
        voices = []
        voices = self.get_all_tokens(filter_by_categories=[TokenCategory.INSTRUMENTS])

        if clean:
            voices = [voice[1:] for voice in voices]
        return voices

    @classmethod
    def to_concat(cls, content_a: 'Document', content_b: 'Document') -> str:
        raise NotImplementedError

    def __iter__(self):
        """
        Get the indexes to export all the document.

        Returns: An iterator with the indexes to export the document.
        """
        return iter(range(self.get_first_measure(), self.measures_count() + 1))

    def __next__(self):
        """
        Get the next index to export the document.

        Returns: The next index to export the document.
        """
        return next(iter(range(self.get_first_measure(), self.measures_count() + 1)))


# tree traversal utils
class MetacommentsTraversal(TreeTraversalInterface):
    def __init__(self):
        self.metacomments = []

    def visit(self, node):
        if isinstance(node.token, MetacommentToken):
            self.metacomments.append(node.token)


class TokensTraversal(TreeTraversalInterface):
    def __init__(self, non_repeated: bool, filter_by_categories):
        """
        Create an instance of `TokensTraversal`.
        Args:
            non_repeated: If True, only unique tokens are returned. If False, all tokens are returned.
            filter_by_categories: A list of categories to filter the tokens. If None, all tokens are returned.
        """
        self.tokens = []
        self.seen_encodings = []
        self.non_repeated = non_repeated
        self.filter_by_categories = filter_by_categories

    def visit(self, node):
        if (node.token
            and (not self.non_repeated or node.token.encoding not in self.seen_encodings)
            and (self.filter_by_categories is None or node.token.category in self.filter_by_categories)
        ):
            self.tokens.append(node.token)
            if self.non_repeated:
                self.seen_encodings.append(node.token.encoding)
