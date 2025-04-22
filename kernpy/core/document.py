from __future__ import annotations

from copy import copy, deepcopy
from collections import deque, defaultdict
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Dict, Union
from collections.abc import Sequence
from queue import Queue

from kernpy.core import TokenCategory, CORE_HEADERS, TERMINATOR
from kernpy.core import MetacommentToken, AbstractToken, HeaderToken
from .transposer import transpose, Direction, NotationEncoding, AVAILABLE_INTERVALS
from .tokens import NoteRestToken, Subtoken
from .transposer import IntervalsByName


class SignatureNodes:
    """
    SignatureNodes class.

    This class is used to store the last signature nodes of a tree.
    It is used to keep track of the last signature nodes.

    Attributes: nodes (dict): A dictionary that stores the last signature nodes. This way, we can add several tokens
    without repetitions. - The key is the signature descendant token class (KeyToken, MeterSymbolToken, etc...) - The
    value = node

    """

    def __init__(self):
        """
        Create an instance of SignatureNodes. Initialize the nodes as an empty dictionary.

        Examples:
            >>> signature_nodes = SignatureNodes()
            >>> signature_nodes.nodes
            {}
        """
        self.nodes = {}

    def clone(self):
        """
        Create a deep copy of the SignatureNodes instance.
        Returns: A new instance of SignatureNodes with nodes copied.

        # TODO: This method is equivalent to the following code:
        # from copy import deepcopy
        # signature_nodes_to_copy = SignatureNodes()
        # ...
        # result = deepcopy(signature_nodes_to_copy)
        # It should be tested.
        """
        result = SignatureNodes()
        result.nodes = copy(self.nodes)
        return result

    def update(self, node):
        self.nodes[node.token.__class__.__name__] = node


class TreeTraversalInterface(ABC):
    """
    TreeTraversalInterface class.

    This class is used to traverse the tree. The `TreeTraversalInterface` class is responsible for implementing
    the `visit` method.
    """

    @abstractmethod
    def visit(self, node):
        pass


class Node:
    """
    Node class.

    This class represents a node in a tree.
    The `Node` class is responsible for storing the main information of the **kern file.

    Attributes:
        id(int): The unique id of the node.
        token(Optional[AbstractToken]): The specific token of the node. The token can be a `KeyToken`, `MeterSymbolToken`, etc...
        parent(Optional['Node']): A reference to the parent `Node`. If the parent is the root, the parent is None.
        children(List['Node']): A list of the children `Node`.
        stage(int): The stage of the node in the tree. The stage is similar to a row in the **kern file.
        last_spine_operator_node(Optional['Node']): The last spine operator node.
        last_signature_nodes(Optional[SignatureNodes]): A reference to the last `SignatureNodes` instance.
        header_node(Optional['Node']): The header node.
    """
    NextID = 1  # static counter

    def __init__(self,
                 stage: int,
                 token: Optional[AbstractToken],
                 parent: Optional['Node'],
                 last_spine_operator_node: Optional['Node'],
                 last_signature_nodes: Optional[SignatureNodes],
                 header_node: Optional['Node']
                 ):
        """
        Create an instance of Node.

        Args:
            stage (int): The stage of the node in the tree. The stage is similar to a row in the **kern file.
            token (Optional[AbstractToken]): The specific token of the node. The token can be a `KeyToken`, `MeterSymbolToken`, etc...
            parent (Optional['Node']): A reference to the parent `Node`. If the parent is the root, the parent is None.
            last_spine_operator_node (Optional['Node']): The last spine operator node.
            last_signature_nodes (Optional[SignatureNodes]): A reference to the last `SignatureNodes` instance.
            header_node (Optional['Node']): The header node.
        """
        self.id = Node.NextID
        Node.NextID += 1
        self.token = token
        self.parent = parent
        self.children = []
        self.stage = stage
        self.header_node = header_node
        if last_signature_nodes is not None:
            self.last_signature_nodes = last_signature_nodes.clone()  #TODO Documentar todo esto - composición
            # self.last_signature_nodes = copy.deepcopy(last_signature_nodes) # TODO: Ver en SignatureNodes.clone
        else:
            self.last_signature_nodes = SignatureNodes()
        self.last_spine_operator_node = last_spine_operator_node

    def count_nodes_by_stage(self) -> List[int]:
        """
        Count the number of nodes in each stage of the tree.

        Examples:
            >>> node = Node(0, None, None, None, None, None)
            >>> ...
            >>> node.count_nodes_by_stage()
            [2, 2, 2, 2, 3, 3, 3, 2]

        Returns:
            List[int]: A list with the number of nodes in each stage of the tree.
        """
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
        """
        Depth-first search (DFS)

        Args:
            tree_traversal (TreeTraversalInterface): The tree traversal interface. Object used to visit the nodes of the tree.
        """
        node = self
        tree_traversal.visit(node)
        for child in self.children:
            child.dfs(tree_traversal)

    def dfs_iterative(self, tree_traversal: TreeTraversalInterface):
        """
        Depth-first search (DFS). Iterative version.

        Args:
            tree_traversal (TreeTraversalInterface): The tree traversal interface. Object used to visit the nodes of the tree.

        Returns: None
        """
        stack = [self]
        while stack:
            node = stack.pop()
            tree_traversal.visit(node)
            stack.extend(reversed(node.children))  # Add children in reverse order to maintain DFS order

    def __eq__(self, other):
        """
        Compare two nodes.

        Args:
            other: The other node to compare.

        Returns: True if the nodes are equal, False otherwise.
        """
        if other is None or not isinstance(other, Node):
            return False

        return self.id == other.id

    def __ne__(self, other):
        """
        Compare two nodes.

        Args:
            other: The other node to compare.

        Returns: True if the nodes are not equal, False otherwise.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Get the hash of the node.

        Returns: The hash of the node.
        """
        return hash(self.id)

    def __str__(self):
        """
        Get the string representation of the node.

        Returns: The string representation of the node.
        """
        return f"{{{self.stage}: {self.token}}}"


class BoundingBoxMeasures:
    """
    BoundingBoxMeasures class.
    """

    def __init__(
            self,
            bounding_box,
            from_measure: int,
            to_measure: int
    ):
        """
        Create an instance of BoundingBoxMeasures.

        Args:
            bounding_box: The bounding box object of the node.
            from_measure (int): The first measure of the score in the BoundingBoxMeasures object.
            to_measure (int): The last measure of the score in the BoundingBoxMeasures object.
        """
        self.from_measure = from_measure
        self.to_measure = to_measure
        self.bounding_box = bounding_box


class MultistageTree:
    """
    MultistageTree class.
    """

    def __init__(self):
        """
        Constructor for MultistageTree class.

        Create an empty Node object to serve as the root, \
        and start the stages list by placing this root node inside a new list.

        """
        self.root = Node(0, None, None, None, None, None)
        self.stages = []  # First stage (0-index) is the root (Node with None token and header_node). The core header is in stage 1.
        self.stages.append([self.root])

    def add_node(
            self,
            stage: int,
            parent: Node,
            token: Optional[AbstractToken],
            last_spine_operator_node: Optional[Node],
            previous_signature_nodes: Optional[SignatureNodes],
            header_node: Optional[Node] = None
    ) -> Node:
        """
        Add a new node to the tree.
        Args:
            stage (int):
            parent (Node):
            token (Optional[AbstractToken]):
            last_spine_operator_node (Optional[Node]):
            previous_signature_nodes (Optional[SignatureNodes]):
            header_node (Optional[Node]):

        Returns: Node - The added node object.

        """
        node = Node(stage, token, parent, last_spine_operator_node, previous_signature_nodes, header_node)
        if stage == len(self.stages):
            self.stages.append([node])
        elif stage > len(self.stages):
            raise ValueError(f'Cannot add node in stage {stage} when there are only {len(self.stages)} stages')
        else:
            self.stages[stage].append(node)

        parent.children.append(node)
        return node

    def dfs(self, visit_method) -> None:
        """
        Depth-first search (DFS)

        Args:
            visit_method (TreeTraversalInterface): The tree traversal interface.

        Returns: None

        """
        self.root.dfs(visit_method)

    def dfs_iterative(self, visit_method) -> None:
        """
        Depth-first search (DFS). Iterative version.

        Args:
            visit_method (TreeTraversalInterface): The tree traversal interface.

        Returns: None

        """
        self.root.dfs_iterative(visit_method)

    def __deepcopy__(self, memo):
        """
        Create a deep copy of the MultistageTree object.
        """
        # Create a new empty MultistageTree object
        new_tree = MultistageTree()

        # Deepcopy the root
        new_tree.root = deepcopy(self.root, memo)

        # Deepcopy the stages list
        new_tree.stages = deepcopy(self.stages, memo)

        return new_tree


class Document:
    """
    Document class.

    This class store the score content using an agnostic tree structure.

    Attributes:
        tree (MultistageTree): The tree structure of the document where all the nodes are stored. \
            Each stage of the tree corresponds to a row in the Humdrum **kern file encoding.
        measure_start_tree_stages (List[List[Node]]): The list of nodes that corresponds to the measures. \
            Empty list by default.
            The index of the list is starting from 1. Rows after removing empty lines and line comments
        page_bounding_boxes (Dict[int, BoundingBoxMeasures]): The dictionary of page bounding boxes. \
            - key: page number
            - value: BoundingBoxMeasures object
        header_stage (int): The index of the stage that contains the headers. None by default.
    """

    def __init__(self, tree: MultistageTree):
        """
        Constructor for Document class.

        Args:
            tree (MultistageTree): The tree structure of the document where all the nodes are stored.
        """
        self.tree = tree  # TODO: ? Should we use copy.deepcopy() here?
        self.measure_start_tree_stages = []
        self.page_bounding_boxes = {}
        self.header_stage = None

    FIRST_MEASURE = 1

    def get_header_stage(self) -> Union[List[Node], List[List[Node]]]:
        """
        Get the Node list of the header stage.

        Returns: (Union[List[Node], List[List[Node]]]) The Node list of the header stage.

        Raises: Exception - If the document has no header stage.
        """
        if self.header_stage:
            return self.tree.stages[self.header_stage]
        else:
            raise Exception('No header stage found')

    def get_leaves(self) -> List[Node]:
        """
        Get the leaves of the tree.

        Returns: (List[Node]) The leaves of the tree.
        """
        return self.tree.stages[len(self.tree.stages) - 1]

    def get_spine_count(self) -> int:
        """
        Get the number of spines in the document.

        Returns (int): The number of spines in the document.
        """
        return len(self.get_header_stage())  # TODO: test refactor

    def get_first_measure(self) -> int:
        """
        Get the index of the first measure of the document.

        Returns: (Int) The index of the first measure of the document.

        Raises: Exception - If the document has no measures.

        Examples:
            >>> import kernpy as kp
            >>> document, err = kp.read('score.krn')
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
            >>> document, _ = kernpy.read('score.krn')
            >>> document.measures_count()
            10
            >>> for i in range(document.get_first_measure(), document.measures_count() + 1):
            >>>   options = kernpy.ExportOptions(from_measure=i, to_measure=i+4)
        """
        if len(self.measure_start_tree_stages) == 0:
            raise Exception('No measures found')

        return len(self.measure_start_tree_stages)

    def get_metacomments(self, KeyComment: Optional[str] = None, clear: bool = False) -> List[str]:
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
        self.tree.dfs_iterative(traversal)
        result = []
        for metacomment in traversal.metacomments:
            if KeyComment is None or metacomment.encoding.startswith(f"!!!{KeyComment}"):
                new_comment = metacomment.encoding
                if clear:
                    new_comment = metacomment.encoding.replace(f"!!!{KeyComment}: ", "")
                result.append(new_comment)

        return result

    @classmethod
    def tokens_to_encodings(cls, tokens: Sequence[AbstractToken]):
        """
        Get the encodings of a list of tokens.

        The method is equivalent to the following code:
            >>> tokens = kp.get_all_tokens()
            >>> [token.encoding for token in tokens if token.encoding is not None]

        Args:
            tokens (Sequence[AbstractToken]): list - A list of tokens.

        Returns: List[str] - A list of token encodings.

        Examples:
            >>> tokens = document.get_all_tokens()
            >>> Document.tokens_to_encodings(tokens)
            ['!!!COM: Coltrane', '!!!voices: 1', '!!!OPR: Blue Train']
        """
        encodings = [token.encoding for token in tokens if token.encoding is not None]
        return encodings

    def get_all_tokens(self, filter_by_categories: Optional[Sequence[TokenCategory]] = None) -> List[AbstractToken]:
        """
        Args:
            filter_by_categories (Optional[Sequence[TokenCategory]]): A list of categories to filter the tokens. If None, all tokens are returned.

        Returns:
            List[AbstractToken] - A list of all tokens.

        Examples:
            >>> tokens = document.get_all_tokens()
            >>> Document.tokens_to_encodings(tokens)
            >>> [type(t) for t in tokens]
            [<class 'kernpy.core.token.Token'>, <class 'kernpy.core.token.Token'>, <class 'kernpy.core.token.Token'>]
        """
        computed_categories = TokenCategory.valid(include=filter_by_categories)
        traversal = TokensTraversal(False, computed_categories)
        self.tree.dfs_iterative(traversal)
        return traversal.tokens

    def get_all_tokens_encodings(
            self,
            filter_by_categories: Optional[Sequence[TokenCategory]] = None
    ) -> List[str]:
        """
        Args:
            filter_by_categories (Optional[Sequence[TokenCategory]]): A list of categories to filter the tokens. If None, all tokens are returned.


        Returns:
            list[str] - A list of all token encodings.

        Examples:
            >>> tokens = document.get_all_tokens_encodings()
            >>> Document.tokens_to_encodings(tokens)
            ['!!!COM: Coltrane', '!!!voices: 1', '!!!OPR: Blue Train']
        """
        tokens = self.get_all_tokens(filter_by_categories)
        return Document.tokens_to_encodings(tokens)

    def get_unique_tokens(
            self,
            filter_by_categories: Optional[Sequence[TokenCategory]] = None
    ) -> List[AbstractToken]:
        """
        Get unique tokens.

        Args:
            filter_by_categories (Optional[Sequence[TokenCategory]]): A list of categories to filter the tokens. If None, all tokens are returned.

        Returns:
            List[AbstractToken] - A list of unique tokens.

        """
        computed_categories = TokenCategory.valid(include=filter_by_categories)
        traversal = TokensTraversal(True, computed_categories)
        self.tree.dfs_iterative(traversal)
        return traversal.tokens

    def get_unique_token_encodings(
            self,
            filter_by_categories: Optional[Sequence[TokenCategory]] = None
    ) -> List[str]:
        """
        Get unique token encodings.

        Args:
            filter_by_categories (Optional[Sequence[TokenCategory]]): A list of categories to filter the tokens. If None, all tokens are returned.

        Returns: List[str] - A list of unique token encodings.

        """
        tokens = self.get_unique_tokens(filter_by_categories)
        return Document.tokens_to_encodings(tokens)

    def get_voices(self, clean: bool = False):
        """
        Get the voices of the document.

        Args
            clean (bool): Remove the first '!' from the voice name.

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
        voices = self.get_all_tokens(filter_by_categories=[TokenCategory.INSTRUMENTS])

        if clean:
            voices = [voice[1:] for voice in voices]
        return voices

    def clone(self):
        """
        Create a deep copy of the Document instance.

        Returns: A new instance of Document with the tree copied.

        """
        result = Document(copy(self.tree))
        result.measure_start_tree_stages = copy(self.measure_start_tree_stages)
        result.page_bounding_boxes = copy(self.page_bounding_boxes)
        result.header_stage = copy(self.header_stage)

        return result

    def append_spines(self, spines) -> None:
        """
        Append the spines directly to current document tree.

        Args:
            spines(list): A list of spines to append.

        Returns: None

        Examples:
            >>> import kernpy as kp
            >>> doc, _ = kp.read('score.krn')
            >>> spines = [
            >>> '4e\t4f\t4g\t4a\n4b\t4c\t4d\t4e\n=\t=\t=\t=\n',
            >>> '4c\t4d\t4e\t4f\n4g\t4a\t4b\t4c\n=\t=\t=\t=\n',
           >>> ]
           >>> doc.append_spines(spines)
           None
        """
        raise NotImplementedError()
        if len(spines) != self.get_spine_count():
            raise Exception(f"Spines count mismatch: {len(spines)} != {self.get_spine_count()}")

        for spine in spines:
            return

    def add(self, other: 'Document', *, check_core_spines_only: Optional[bool] = False) -> 'Document':
        """
        Concatenate one document to the current document: Modify the current object!

        Args:
            other: The document to concatenate.
            check_core_spines_only: If True, only the core spines (**kern and **mens) are checked. If False, all spines are checked.

        Returns ('Document'): The current document (self) with the other document concatenated.
        """
        if not Document.match(self, other, check_core_spines_only=check_core_spines_only):
            raise Exception(f'Documents are not compatible for addition. '
                            f'Headers do not match with check_core_spines_only={check_core_spines_only}. '
                            f'self: {self.get_header_nodes()}, other: {other.get_header_nodes()}. ')

        current_header_nodes = self.get_header_stage()
        other_header_nodes = other.get_header_stage()

        current_leaf_nodes = self.get_leaves()
        flatten = lambda lst: [item for sublist in lst for item in sublist]
        other_first_level_children = [flatten(c.children) for c in other_header_nodes]  # avoid header stage

        for current_leaf, other_first_level_child in zip(current_leaf_nodes, other_first_level_children, strict=False):
            # Ignore extra spines from other document.
            # But if there are extra spines in the current document, it will raise an exception.
            if current_leaf.token.encoding == TERMINATOR:
                # remove the '*-' token from the current document
                current_leaf_index = current_leaf.parent.children.index(current_leaf)
                current_leaf.parent.children.pop(current_leaf_index)
                current_leaf.parent.children.insert(current_leaf_index, other_first_level_child)

            self.tree.add_node(
                stage=len(self.tree.stages) - 1,  # TODO: check offset 0, +1, -1 ????
                parent=current_leaf,
                token=other_first_level_child.token,
                last_spine_operator_node=other_first_level_child.last_spine_operator_node,
                previous_signature_nodes=other_first_level_child.last_signature_nodes,
                header_node=other_first_level_child.header_node
            )

        return self

    def get_header_nodes(self) -> List[HeaderToken]:
        """
        Get the header nodes of the current document.

        Returns: List[HeaderToken]: A list with the header nodes of the current document.
        """
        return [token for token in self.get_all_tokens(filter_by_categories=None) if isinstance(token, HeaderToken)]

    def get_spine_ids(self) -> List[int]:
        """
                Get the indexes of the current document.

                Returns List[int]: A list with the indexes of the current document.

                Examples:
                    >>> document.get_all_spine_indexes()
                    [0, 1, 2, 3, 4]
                """
        header_nodes = self.get_header_nodes()
        return [node.spine_id for node in header_nodes]

    def frequencies(self, token_categories: Optional[Sequence[TokenCategory]] = None) -> Dict:
        """
        Frequency of tokens in the document.


        Args:
            token_categories (Optional[Sequence[TokenCategory]]): If None, all tokens are considered.
        Returns (Dict):
            A dictionary with the category and the number of occurrences of each token.

        """
        tokens = self.get_all_tokens(filter_by_categories=token_categories)
        frequencies = {}
        for t in tokens:
            if t.encoding in frequencies:
                frequencies[t.encoding]['occurrences'] += 1
            else:
                frequencies[t.encoding] = {
                    'occurrences': 1,
                    'category': t.category.name,
                }

        return frequencies

    def split(self) -> List['Document']:
        """
        Split the current document into a list of documents, one for each **kern spine.
        Each resulting document will contain one **kern spine along with all non-kern spines.

        Returns:
            List['Document']: A list of documents, where each document contains one **kern spine
            and all non-kern spines from the original document.

        Examples:
            >>> document.split()
            [<Document: score.krn>, <Document: score.krn>, <Document: score.krn>]
        """
        raise NotImplementedError
        new_documents = []
        self_document_copy = deepcopy(self)
        kern_header_nodes = [node for node in self_document_copy.get_header_nodes() if node.encoding == '**kern']
        other_header_nodes = [node for node in self_document_copy.get_header_nodes() if node.encoding != '**kern']
        spine_ids = self_document_copy.get_spine_ids()

        for header_node in kern_header_nodes:
            if header_node.spine_id not in spine_ids:
                continue

            spine_ids.remove(header_node.spine_id)

            new_tree = deepcopy(self.tree)
            prev_node = new_tree.root
            while not isinstance(prev_node, HeaderToken):
                prev_node = prev_node.children[0]

            if not prev_node or not isinstance(prev_node, HeaderToken):
                raise Exception(f'Header node not found: {prev_node} in {header_node}')

            new_children = list(filter(lambda x: x.spine_id == header_node.spine_id, prev_node.children))
            new_tree.root = new_children

            new_document = Document(new_tree)

            new_documents.append(new_document)

        return new_documents

    @classmethod
    def to_concat(cls, first_doc: 'Document', second_doc: 'Document', deep_copy: bool = True) -> 'Document':
        """
        Concatenate two documents.

        Args:
            first_doc (Document): The first document.
            second_doc (Document: The second document.
            deep_copy (bool): If True, the documents are deep copied. If False, the documents are shallow copied.

        Returns: A new instance of Document with the documents concatenated.
        """
        first_doc = first_doc.clone() if deep_copy else first_doc
        second_doc = second_doc.clone() if deep_copy else second_doc
        first_doc.add(second_doc)

        return first_doc

    @classmethod
    def match(cls, a: 'Document', b: 'Document', *, check_core_spines_only: Optional[bool] = False) -> bool:
        """
        Match two documents. Two documents match if they have the same spine structure.

        Args:
            a (Document): The first document.
            b (Document): The second document.
            check_core_spines_only (Optional[bool]): If True, only the core spines (**kern and **mens) are checked. If False, all spines are checked.

        Returns: True if the documents match, False otherwise.

        Examples:

        """
        if check_core_spines_only:
            return [token.encoding for token in a.get_header_nodes() if token.encoding in CORE_HEADERS] \
                == [token.encoding for token in b.get_header_nodes() if token.encoding in CORE_HEADERS]
        else:
            return [token.encoding for token in a.get_header_nodes()] \
                == [token.encoding for token in b.get_header_nodes()]


    def to_transposed(self, interval: str, direction: str = Direction.UP.value) -> 'Document':
        """
        Create a new document with the transposed notes without modifying the original document.

        Args:
            interval (str): The name of the interval to transpose. It can be 'P4', 'P5', 'M2', etc. Check the \
             kp.AVAILABLE_INTERVALS for the available intervals.
            direction (str): The direction to transpose. It can be 'up' or 'down'.

        Returns:

        """
        if interval not in AVAILABLE_INTERVALS:
            raise ValueError(
                f"Interval {interval!r} is not available. "
                f"Available intervals are: {AVAILABLE_INTERVALS}"
            )

        if direction not in (Direction.UP.value, Direction.DOWN.value):
            raise ValueError(
                f"Direction {direction!r} is not available. "
                f"Available directions are: "
                f"{Direction.UP.value!r}, {Direction.DOWN.value!r}"
            )

        new_document = self.clone()

        # BFS through the tree
        root = new_document.tree.root
        queue = Queue()
        queue.put(root)

        while not queue.empty():
            node = queue.get()

            if isinstance(node.token, NoteRestToken):
                orig_token = node.token

                new_subtokens = []
                transposed_pitch_encoding = None

                # Transpose each pitch subtoken in the pitch–duration list
                for subtoken in orig_token.pitch_duration_subtokens:
                    if subtoken.category == TokenCategory.PITCH:
                        # transpose() returns a new pitch subtoken
                        tp = transpose(
                            input_encoding=subtoken.encoding,
                            interval=IntervalsByName[interval],
                            direction=direction,
                            input_format=NotationEncoding.HUMDRUM.value,
                            output_format=NotationEncoding.HUMDRUM.value,
                        )
                        new_subtokens.append(Subtoken(tp, subtoken.category))
                        transposed_pitch_encoding = tp
                    else:
                        # leave duration subtokens untouched
                        new_subtokens.append(Subtoken(subtoken.encoding, subtoken.category))

                # Replace the node’s token with a new NoteRestToken
                node.token = NoteRestToken(
                    encoding=transposed_pitch_encoding,
                    pitch_duration_subtokens=new_subtokens,
                    decoration_subtokens=orig_token.decoration_subtokens,
                )

            # enqueue children
            for child in node.children:
                queue.put(child)

        # Return the transposed clone
        return new_document


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
    def __init__(
            self,
            non_repeated: bool,
            filter_by_categories
    ):
        """
        Create an instance of `TokensTraversal`.
        Args:
            non_repeated: If True, only unique tokens are returned. If False, all tokens are returned.
            filter_by_categories: A list of categories to filter the tokens. If None, all tokens are returned.
        """
        self.tokens = []
        self.seen_encodings = []
        self.non_repeated = non_repeated
        self.filter_by_categories = [t for t in TokenCategory] if filter_by_categories is None else filter_by_categories

    def visit(self, node):
        if (node.token
                and (not self.non_repeated or node.token.encoding not in self.seen_encodings)
                and (self.filter_by_categories is None or node.token.category in self.filter_by_categories)
        ):
            self.tokens.append(node.token)
            if self.non_repeated:
                self.seen_encodings.append(node.token.encoding)


class TraversalFactory:
    class Categories(Enum):
        METACOMMENTS = "metacomments"
        TOKENS = "tokens"

    @classmethod
    def create(
            cls,
            traversal_type: str,
            non_repeated: bool,
            filter_by_categories: Optional[Sequence[TokenCategory]]
    ) -> TreeTraversalInterface:
        """
        Create an instance of `TreeTraversalInterface` based on the `traversal_type`.
        Args:
            non_repeated:
            filter_by_categories:
            traversal_type: The type of traversal to use. Possible values are:
                - "metacomments"
                - "tokens"

        Returns: An instance of `TreeTraversalInterface`.
        """
        if traversal_type == cls.Categories.METACOMMENTS.value:
            return MetacommentsTraversal()
        elif traversal_type == cls.Categories.TOKENS.value:
            return TokensTraversal(non_repeated, filter_by_categories)

        raise ValueError(f"Unknown traversal type: {traversal_type}")

