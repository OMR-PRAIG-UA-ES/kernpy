from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from enum import Enum, auto
import copy
from typing import List, Dict, Set, Union, Optional
from unittest import result

TOKEN_SEPARATOR = '@'
DECORATION_SEPARATOR = '·'
GRAPHIC_TOKEN_SEPARATOR = ':'
HEADERS = {"**mens", "**kern", "**text", "**harm", "**mxhm", "**root", "**dyn", "**dynam", "**fing"}
CORE_HEADERS = {"**kern", "**mens"}
SPINE_OPERATIONS = {"*-", "*+", "*^", "*v", "*x"}
TERMINATOR = "*-"
EMPTY_TOKEN = "*"
ERROR_TOKEN = "Z"


# We don't use inheritance here for all elements but enum, because we don't need any polymorphism mechanism, just a grouping one
# TODO Poner todos los tipos - p.ej. también comandos de layout - slurs, etc...
class TokenCategory(Enum):
    """
    Options for the category of a token.

    This is used to determine what kind of token should be exported.

    The categories are sorted the specific order they are compared to sorthem. But hierarchical order must be defined in other data structures.
    """
    STRUCTURAL = auto()  # header, spine operations
    HEADER = auto()  # **kern, **mens, **text, **harm, **mxhm, **root, **dyn, **dynam, **fing
    SPINE_OPERATION = auto()
    CORE = auto() # notes, rests, chords, etc.
    ERROR = auto()
    NOTE_REST = auto()
    NOTE = auto()
    DURATION = auto()
    PITCH = auto()
    ALTERATION = auto()
    DECORATION = auto()
    REST = auto()
    CHORD = auto()
    EMPTY = auto()  # placeholders, null interpretation
    SIGNATURES = auto()
    CLEF = auto()
    TIME_SIGNATURE = auto()
    METER_SYMBOL = auto()
    KEY_SIGNATURE = auto()
    KEY_TOKEN = auto()
    ENGRAVED_SYMBOLS = auto()
    OTHER_CONTEXTUAL = auto()
    BARLINES = auto()
    COMMENTS = auto()
    FIELD_COMMENTS = auto()
    LINE_COMMENTS = auto()
    DYNAMICS = auto()
    HARMONY = auto()
    FINGERING = auto()
    LYRICS = auto()
    INSTRUMENTS = auto()
    IMAGE_ANNOTATIONS = auto()
    BOUNDING_BOXES = auto()
    LINE_BREAK = auto()
    OTHER = auto()
    MHXM = auto()
    ROOT = auto()

    def __lt__(self, other):
        """
        Compare two TokenCategory.
        Args:
            other (TokenCategory): The other category to compare.

        Returns (bool): True if this category is lower than the other, False otherwise.

        Examples:
            >>> TokenCategory.STRUCTURAL < TokenCategory.CORE
            True
            >>> TokenCategory.STRUCTURAL < TokenCategory.STRUCTURAL
            False
            >>> TokenCategory.CORE < TokenCategory.STRUCTURAL
            False
            >>> sorted([TokenCategory.STRUCTURAL, TokenCategory.CORE])
            [TokenCategory.STRUCTURAL, TokenCategory.CORE]
        """
        if isinstance(other, TokenCategory):
            return self.value < other.value
        return NotImplemented

    @classmethod
    def all(cls) -> Set[TokenCategory]:
        f"""
        Get all categories in the hierarchy.

        Returns:
            Set[TokenCategory]: The set of all categories in the hierarchy.
            
        Examples:
            >>> import kernpy as kp
            >>> kp.TokenCategory.all()
            set([<TokenCategory.MHXM: 29>, <TokenCategory.COMMENTS: 19>, <TokenCategory.BARLINES: 18>, <TokenCategory.CORE: 2>, <TokenCategory.BOUNDING_BOXES: 27>, <TokenCategory.NOTE_REST: 3>, <TokenCategory.NOTE: 4>, <TokenCategory.ENGRAVED_SYMBOLS: 16>, <TokenCategory.SIGNATURES: 11>, <TokenCategory.REST: 8>, <TokenCategory.METER_SYMBOL: 14>, <TokenCategory.HARMONY: 23>, <TokenCategory.KEY_SIGNATURE: 15>, <TokenCategory.EMPTY: 10>, <TokenCategory.PITCH: 6>, <TokenCategory.LINE_COMMENTS: 21>, <TokenCategory.FINGERING: 24>, <TokenCategory.DECORATION: 7>, <TokenCategory.OTHER: 28>, <TokenCategory.INSTRUMENTS: 26>, <TokenCategory.STRUCTURAL: 1>, <TokenCategory.FIELD_COMMENTS: 20>, <TokenCategory.LYRICS: 25>, <TokenCategory.CLEF: 12>, <TokenCategory.DURATION: 5>, <TokenCategory.DYNAMICS: 22>, <TokenCategory.CHORD: 9>, <TokenCategory.TIME_SIGNATURE: 13>, <TokenCategory.OTHER_CONTEXTUAL: 17>])
        """
        return set([t for t in TokenCategory])

    @classmethod
    def tree(cls):
        """
        Return a string representation of the category hierarchy
        Returns (str): The string representation of the category hierarchy

        Examples:
            >>> import kernpy as kp
            >>> print(kp.TokenCategory.tree())
            .
            ├── TokenCategory.STRUCTURAL
            ├── TokenCategory.CORE
            │   ├── TokenCategory.NOTE_REST
            │   │   ├── TokenCategory.DURATION
            │   │   ├── TokenCategory.NOTE
            │   │   │   ├── TokenCategory.PITCH
            │   │   │   └── TokenCategory.DECORATION
            │   │   └── TokenCategory.REST
            │   ├── TokenCategory.CHORD
            │   └── TokenCategory.EMPTY
            ├── TokenCategory.SIGNATURES
            │   ├── TokenCategory.CLEF
            │   ├── TokenCategory.TIME_SIGNATURE
            │   ├── TokenCategory.METER_SYMBOL
            │   └── TokenCategory.KEY_SIGNATURE
            ├── TokenCategory.ENGRAVED_SYMBOLS
            ├── TokenCategory.OTHER_CONTEXTUAL
            ├── TokenCategory.BARLINES
            ├── TokenCategory.COMMENTS
            │   ├── TokenCategory.FIELD_COMMENTS
            │   └── TokenCategory.LINE_COMMENTS
            ├── TokenCategory.DYNAMICS
            ├── TokenCategory.HARMONY
            ├── TokenCategory.FINGERING
            ├── TokenCategory.LYRICS
            ├── TokenCategory.INSTRUMENTS
            ├── TokenCategory.BOUNDING_BOXES
            └── TokenCategory.OTHER
        """
        return TokenCategoryHierarchyMapper.tree()

    @classmethod
    def is_child(cls, *, child: TokenCategory, parent: TokenCategory) -> bool:
        """
        Check if the child category is a child of the parent category.

        Args:
            child (TokenCategory): The child category.
            parent (TokenCategory): The parent category.

        Returns (bool): True if the child category is a child of the parent category, False otherwise.
        """
        return TokenCategoryHierarchyMapper.is_child(parent=parent, child=child)

    @classmethod
    def children(cls, target: TokenCategory) -> Set[TokenCategory]:
        """
        Get the children of the target category.

        Args:
            target (TokenCategory): The target category.

        Returns (List[TokenCategory]): The list of child categories of the target category.
        """
        return TokenCategoryHierarchyMapper.children(parent=target)

    @classmethod
    def valid(cls, *, include: Optional[Set[TokenCategory]] = None, exclude: Optional[Set[TokenCategory]] = None) -> Set[TokenCategory]:
        """
        Get the valid categories based on the include and exclude sets.

        Args:
            include (Optional[Set[TokenCategory]]): The set of categories to include. Defaults to None. \
                If None, all categories are included.
            exclude (Optional[Set[TokenCategory]]): The set of categories to exclude. Defaults to None. \
                If None, no categories are excluded.

        Returns (Set[TokenCategory]): The list of valid categories based on the include and exclude sets.
        """
        return TokenCategoryHierarchyMapper.valid(include=include, exclude=exclude)

    @classmethod
    def leaves(cls, target: TokenCategory) -> Set[TokenCategory]:
        """
        Get the leaves of the subtree of the target category.

        Args:
            target (TokenCategory): The target category.

        Returns (List[TokenCategory]): The list of leaf categories of the target category.
        """
        return TokenCategoryHierarchyMapper.leaves(target=target)

    @classmethod
    def nodes(cls, target: TokenCategory) -> Set[TokenCategory]:
        """
        Get the nodes of the subtree of the target category.

        Args:
            target (TokenCategory): The target category.

        Returns (List[TokenCategory]): The list of node categories of the target category.
        """
        return TokenCategoryHierarchyMapper.nodes(parent=target)

    @classmethod
    def match(cls,
              target: TokenCategory, *,
              include: Optional[Set[TokenCategory]] = None,
              exclude: Optional[Set[TokenCategory]] = None) -> bool:
        """
        Check if the target category matches the include and exclude sets.

        Args:
            target (TokenCategory): The target category.
            include (Optional[Set[TokenCategory]]): The set of categories to include. Defaults to None. \
                If None, all categories are included.
            exclude (Optional[Set[TokenCategory]]): The set of categories to exclude. Defaults to None. \
                If None, no categories are excluded.

        Returns (bool): True if the target category matches the include and exclude sets, False otherwise.
        """
        return TokenCategoryHierarchyMapper.match(category=target, include=include, exclude=exclude)

    def __str__(self):
        """
        Get the string representation of the category.

        Returns (str): The string representation of the category.
        """
        return self.name


NON_CORE_CATEGORIES = {
    TokenCategory.STRUCTURAL,
    TokenCategory.SIGNATURES,
    TokenCategory.EMPTY,
    TokenCategory.IMAGE_ANNOTATIONS,
    TokenCategory.BARLINES,
    TokenCategory.COMMENTS,
}

BEKERN_CATEGORIES = {
    TokenCategory.STRUCTURAL,
    TokenCategory.CORE,
    TokenCategory.SIGNATURES,
    TokenCategory.BARLINES,
    TokenCategory.IMAGE_ANNOTATIONS,
}


class TokenCategoryHierarchyMapper:
    """
    Mapping of the TokenCategory hierarchy.

    This class is used to define the hierarchy of the TokenCategory. Useful related methods are provided.
    """
    """
    The hierarchy of the TokenCategory is a recursive dictionary that defines the parent-child relationships \
        between the categories. It's a tree.
    """
    _hierarchy_typing = Dict[TokenCategory, '_hierarchy_typing']
    hierarchy: _hierarchy_typing = {
        TokenCategory.STRUCTURAL: {
            TokenCategory.HEADER: {},  # each leave must be an empty dictionary
            TokenCategory.SPINE_OPERATION: {},
        },
        TokenCategory.CORE: {
            TokenCategory.NOTE_REST: {
                TokenCategory.DURATION: {},
                TokenCategory.NOTE: {
                    TokenCategory.PITCH: {},
                    TokenCategory.DECORATION: {},
                    TokenCategory.ALTERATION: {},
                },
                TokenCategory.REST: {},
            },
            TokenCategory.CHORD: {},
            TokenCategory.EMPTY: {},
            TokenCategory.ERROR: {},
        },
        TokenCategory.SIGNATURES: {
            TokenCategory.CLEF: {},
            TokenCategory.TIME_SIGNATURE: {},
            TokenCategory.METER_SYMBOL: {},
            TokenCategory.KEY_SIGNATURE: {},
            TokenCategory.KEY_TOKEN: {},
        },
        TokenCategory.ENGRAVED_SYMBOLS: {},
        TokenCategory.OTHER_CONTEXTUAL: {},
        TokenCategory.BARLINES: {},
        TokenCategory.COMMENTS: {
            TokenCategory.FIELD_COMMENTS: {},
            TokenCategory.LINE_COMMENTS: {},
        },
        TokenCategory.DYNAMICS: {},
        TokenCategory.HARMONY: {},
        TokenCategory.FINGERING: {},
        TokenCategory.LYRICS: {},
        TokenCategory.INSTRUMENTS: {},
        TokenCategory.IMAGE_ANNOTATIONS: {
            TokenCategory.BOUNDING_BOXES: {},
            TokenCategory.LINE_BREAK: {},
        },
        TokenCategory.OTHER: {},
        TokenCategory.MHXM: {},
        TokenCategory.ROOT: {},
    }

    @classmethod
    def _is_child(cls, parent: TokenCategory, child: TokenCategory, *, tree: '_hierarchy_typing') -> bool:
        """
        Recursively check if `child` is in the subtree of `parent`.

        Args:
            parent (TokenCategory): The parent category.
            child (TokenCategory): The category to check.
            tree (_hierarchy_typing): The subtree to check.

        Returns:
            bool: True if `child` is a descendant of `parent`, False otherwise.
        """
        # Base case: the parent is empty.
        if len(tree.keys()) == 0:
            return False

        # Recursive case: explore the direct children of the parent.
        return any(
            direct_child == child or cls._is_child(direct_child, child, tree=tree[parent])
            for direct_child in tree.get(parent, {})
        )
        # Vectorized version of the following code:
        #direct_children = tree.get(parent, dict())
        #for direct_child in direct_children.keys():
        #    if direct_child == child or cls._is_child(direct_child, child, tree=tree[parent]):
        #        return True

    @classmethod
    def is_child(cls, parent: TokenCategory, child: TokenCategory) -> bool:
        """
        Recursively check if `child` is in the subtree of `parent`. If `parent` is the same as `child`, return True.

        Args:
            parent (TokenCategory): The parent category.
            child (TokenCategory): The category to check.

        Returns:
            bool: True if `child` is a descendant of `parent`, False otherwise.
        """
        if parent == child:
            return True
        return cls._is_child(parent, child, tree=cls.hierarchy)

    @classmethod
    def children(cls, parent: TokenCategory) -> Set[TokenCategory]:
        """
        Get the direct children of the parent category.

        Args:
            parent (TokenCategory): The parent category.

        Returns:
            Set[TokenCategory]: The list of children categories of the parent category.
        """
        return set(cls.hierarchy.get(parent, {}).keys())

    @classmethod
    def _nodes(cls, tree: _hierarchy_typing) -> Set[TokenCategory]:
        """
        Recursively get all nodes in the given hierarchy tree.
        """
        nodes = set(tree.keys())
        for child in tree.values():
            nodes.update(cls._nodes(child))
        return nodes

    @classmethod
    def _find_subtree(cls, tree: '_hierarchy_typing', parent: TokenCategory) -> Optional['_hierarchy_typing']:
        """
        Recursively find the subtree for the given parent category.
        """
        if parent in tree:
            return tree[parent]  # Return subtree if parent is found at this level
        for child, sub_tree in tree.items():
            result = cls._find_subtree(sub_tree, parent)
            if result is not None:
                return result
        return None  # Return None if parent is not found. It won't happer never


    @classmethod
    def nodes(cls, parent: TokenCategory) -> Set[TokenCategory]:
        """
        Get the all nodes of the subtree of the parent category.

        Args:
            parent (TokenCategory): The parent category.

        Returns:
            List[TokenCategory]: The list of nodes of the subtree of the parent category.
        """
        subtree = cls._find_subtree(cls.hierarchy, parent)
        return cls._nodes(subtree) if subtree is not None else set()

    @classmethod
    def valid(cls,
              include: Optional[Set[TokenCategory]] = None,
              exclude: Optional[Set[TokenCategory]] = None) -> Set[TokenCategory]:
        """
        Get the valid categories based on the include and exclude sets.

        Args:
            include (Optional[Set[TokenCategory]]): The set of categories to include. Defaults to None. \
                If None, all categories are included.
            exclude (Optional[Set[TokenCategory]]): The set of categories to exclude. Defaults to None. \
                If None, no categories are excluded.

        Returns (Set[TokenCategory]): The list of valid categories based on the include and exclude sets.
        """
        include = cls._validate_include(include)
        exclude = cls._validate_exclude(exclude)

        included_nodes = set.union(*[(cls.nodes(cat) | {cat}) for cat in include]) if len(include) > 0 else include
        excluded_nodes = set.union(*[(cls.nodes(cat) | {cat}) for cat in exclude]) if len(exclude) > 0 else exclude
        return included_nodes - excluded_nodes

    @classmethod
    def _leaves(cls, tree: '_hierarchy_typing') -> Set[TokenCategory]:
        """
        Recursively get all leaves (nodes without children) in the hierarchy tree.
        """
        if not tree:
            return set()
        leaves = {node for node, children in tree.items() if not children}
        for node, children in tree.items():
            leaves.update(cls._leaves(children))
        return leaves

    @classmethod
    def leaves(cls, target: TokenCategory) -> Set[TokenCategory]:
        """
        Get the leaves of the subtree of the target category.

        Args:
            target (TokenCategory): The target category.

        Returns (List[TokenCategory]): The list of leaf categories of the target category.
        """
        tree = cls._find_subtree(cls.hierarchy, target)
        return cls._leaves(tree)


    @classmethod
    def _match(cls, category: TokenCategory, *,
               include: Set[TokenCategory],
               exclude: Set[TokenCategory]) -> bool:
        """
        Check if a category matches include/exclude criteria.
        """
        # Include the category itself along with its descendants.
        target_nodes = cls.nodes(category) | {category}

        valid_categories = cls.valid(include=include, exclude=exclude)

        # Check if any node in the target set is in the valid categories.
        return len(target_nodes & valid_categories) > 0

    @classmethod
    def _validate_include(cls, include: Optional[Set[TokenCategory]]) -> Set[TokenCategory]:
        """
        Validate the include set.
        """
        if include is None:
            return cls.all()
        if isinstance(include, (list, tuple)):
            include = set(include)
        elif not isinstance(include, set):
            include = {include}
        if not all(isinstance(cat, TokenCategory) for cat in include):
            raise ValueError('Invalid category: include and exclude must be a set of TokenCategory.')
        return include

    @classmethod
    def _validate_exclude(cls, exclude: Optional[Set[TokenCategory]]) -> Set[TokenCategory]:
        """
        Validate the exclude set.
        """
        if exclude is None:
            return set()
        if isinstance(exclude, (list, tuple)):
            exclude = set(exclude)
        elif not isinstance(exclude, set):
            exclude = {exclude}
        if not all(isinstance(cat, TokenCategory) for cat in exclude):
            raise ValueError(f'Invalid category: category must be a {TokenCategory.__name__}.')
        return exclude


    @classmethod
    def match(cls, category: TokenCategory, *,
              include: Optional[Set[TokenCategory]] = None,
              exclude: Optional[Set[TokenCategory]] = None) -> bool:
        """
        Check if the category matches the include and exclude sets.
            If include is None, all categories are included. \
            If exclude is None, no categories are excluded.

        Args:
            category (TokenCategory): The category to check.
            include (Optional[Set[TokenCategory]]): The set of categories to include. Defaults to None. \
                If None, all categories are included.
            exclude (Optional[Set[TokenCategory]]): The set of categories to exclude. Defaults to None. \
                If None, no categories are excluded.

        Returns (bool): True if the category matches the include and exclude sets, False otherwise.

        Examples:
            >>> TokenCategoryHierarchyMapper.match(TokenCategory.NOTE, include={TokenCategory.NOTE_REST})
            True
            >>> TokenCategoryHierarchyMapper.match(TokenCategory.NOTE, include={TokenCategory.NOTE_REST}, exclude={TokenCategory.REST})
            True
            >>> TokenCategoryHierarchyMapper.match(TokenCategory.NOTE, include={TokenCategory.NOTE_REST}, exclude={TokenCategory.NOTE})
            False
            >>> TokenCategoryHierarchyMapper.match(TokenCategory.NOTE, include={TokenCategory.CORE}, exclude={TokenCategory.DURATION})
            True
            >>> TokenCategoryHierarchyMapper.match(TokenCategory.DURATION, include={TokenCategory.CORE}, exclude={TokenCategory.DURATION})
            False
        """
        include = cls._validate_include(include)
        exclude = cls._validate_exclude(exclude)

        return cls._match(category, include=include, exclude=exclude)

    @classmethod
    def all(cls) -> Set[TokenCategory]:
        """
        Get all categories in the hierarchy.

        Returns:
            Set[TokenCategory]: The set of all categories in the hierarchy.
        """
        return cls._nodes(cls.hierarchy)

    @classmethod
    def tree(cls) -> str:
        """
        Return a string representation of the category hierarchy,
        formatted similar to the output of the Unix 'tree' command.

        Example output:
            .
            ├── STRUCTURAL
            ├── CORE
            │   ├── NOTE_REST
            │   │   ├── DURATION
            │   │   ├── NOTE
            │   │   │   ├── PITCH
            │   │   │   └── DECORATION
            │   │   └── REST
            │   ├── CHORD
            │   └── EMPTY
            ├── SIGNATURES
            │   ├── CLEF
            │   ├── TIME_SIGNATURE
            │   ├── METER_SYMBOL
            │   └── KEY_SIGNATURE
            ├── ENGRAVED_SYMBOLS
            ├── OTHER_CONTEXTUAL
            ├── BARLINES
            ├── COMMENTS
            │   ├── FIELD_COMMENTS
            │   └── LINE_COMMENTS
            ├── DYNAMICS
            ├── HARMONY
            ...
        """
        def build_tree(tree: Dict[TokenCategory, '_hierarchy_typing'], prefix: str = "") -> [str]:
            lines_buffer = []
            items = list(tree.items())
            count = len(items)
            for index, (category, subtree) in enumerate(items):
                connector = "└── " if index == count - 1 else "├── "
                lines_buffer.append(prefix + connector + str(category))
                extension = "    " if index == count - 1 else "│   "
                lines_buffer.extend(build_tree(subtree, prefix + extension))
            return lines_buffer

        lines = ["."]
        lines.extend(build_tree(cls.hierarchy))
        return "\n".join(lines)


class PitchRest:
    """
    Represents a name or a rest in a note.

    The name is represented using the International Standard Organization (ISO) name notation.
    The first line below the staff is the C4 in G clef. The above C is C5, the below C is C3, etc.

    The Humdrum Kern format uses the following name representation:
    'c' = C4
    'cc' = C5
    'ccc' = C6
    'cccc' = C7

    'C' = C3
    'CC' = C2
    'CCC' = C1

    The rests are represented by the letter 'r'. The rests do not have name.

    This class do not limit the name ranges.


    In the following example, the name is represented by the letter 'c'. The name of 'c' is C4, 'cc' is C5, 'ccc' is C6.
    ```
    **kern
    *clefG2
    2c          // C4
    2cc         // C5
    2ccc        // C6
    2C          // C3
    2CC         // C2
    2CCC        // C1
    *-
    ```
    """
    C4_PITCH_LOWERCASE = 'c'
    C4_OCATAVE = 4
    C3_PITCH_UPPERCASE = 'C'
    C3_OCATAVE = 3
    REST_CHARACTER = 'r'

    VALID_PITCHES = 'abcdefg' + 'ABCDEFG' + REST_CHARACTER

    def __init__(self, raw_pitch: str):
        """
        Create a new PitchRest object.

        Args:
            raw_pitch (str): name representation in Humdrum Kern format

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest = PitchRest('DDD')
        """
        if raw_pitch is None or len(raw_pitch) == 0:
            raise ValueError(f'Empty name: name can not be None or empty. But {raw_pitch} was provided.')

        self.encoding = raw_pitch
        self.pitch, self.octave = self.__parse_pitch_octave()

    def __parse_pitch_octave(self) -> (str, int):
        if self.encoding == PitchRest.REST_CHARACTER:
            return PitchRest.REST_CHARACTER, None

        if self.encoding.islower():
            min_octave = PitchRest.C4_OCATAVE
            octave = min_octave + (len(self.encoding) - 1)
            pitch = self.encoding[0].lower()
            return pitch, octave

        if self.encoding.isupper():
            max_octave = PitchRest.C3_OCATAVE
            octave = max_octave - (len(self.encoding) - 1)
            pitch = self.encoding[0].lower()
            return pitch, octave

        raise ValueError(f'Invalid name: name {self.encoding} is not a valid name representation.')

    def is_rest(self) -> bool:
        """
        Check if the name is a rest.

        Returns:
            bool: True if the name is a rest, False otherwise.

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest.is_rest()
            False
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest.is_rest()
            True
        """
        return self.octave is None

    @staticmethod
    def pitch_comparator(pitch_a: str, pitch_b: str) -> int:
        """
        Compare two pitches of the same octave.

        The lower name is 'a'. So 'a' < 'b' < 'c' < 'd' < 'e' < 'f' < 'g'

        Args:
            pitch_a: One name of 'abcdefg'
            pitch_b: Another name of 'abcdefg'

        Returns:
            -1 if pitch1 is lower than pitch2
            0 if pitch1 is equal to pitch2
            1 if pitch1 is higher than pitch2

        Examples:
            >>> PitchRest.pitch_comparator('c', 'c')
            0
            >>> PitchRest.pitch_comparator('c', 'd')
            -1
            >>> PitchRest.pitch_comparator('d', 'c')
            1
        """
        if pitch_a < pitch_b:
            return -1
        if pitch_a > pitch_b:
            return 1
        return 0

    def __str__(self):
        return f'{self.encoding}'

    def __repr__(self):
        return f'[PitchRest: {self.encoding}, name={self.pitch}, octave={self.octave}]'

    def __eq__(self, other: 'PitchRest') -> bool:
        """
        Compare two pitches and rests.

        Args:
            other (PitchRest): The other name to compare

        Returns (bool):
            True if the pitches are equal, False otherwise

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest == pitch_rest2
            True
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('ccc')
            >>> pitch_rest == pitch_rest2
            False
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest == pitch_rest2
            False
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest == pitch_rest2
            True

        """
        if not isinstance(other, PitchRest):
            return False
        if self.is_rest() and other.is_rest():
            return True
        if self.is_rest() or other.is_rest():
            return False
        return self.pitch == other.pitch and self.octave == other.octave

    def __ne__(self, other: 'PitchRest') -> bool:
        """
        Compare two pitches and rests.
        Args:
            other (PitchRest): The other name to compare

        Returns (bool):
            True if the pitches are different, False otherwise

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest != pitch_rest2
            False
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('ccc')
            >>> pitch_rest != pitch_rest2
            True
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest != pitch_rest2
            True
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest != pitch_rest2
            False
        """
        return not self.__eq__(other)

    def __gt__(self, other: 'PitchRest') -> bool:
        """
        Compare two pitches.

        If any of the pitches is a rest, the comparison raise an exception.

        Args:
            other (PitchRest): The other name to compare

        Returns (bool): True if this name is higher than the other, False otherwise

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('d')
            >>> pitch_rest > pitch_rest2
            False
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest > pitch_rest2
            False
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('b')
            >>> pitch_rest > pitch_rest2
            True
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest > pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest > pitch_rest2
            Traceback (most recent call last):
            ValueError: ...


        """
        if self.is_rest() or other.is_rest():
            raise ValueError(f'Invalid comparison: > operator can not be used to compare name of a rest.\n\
            self={repr(self)} > other={repr(other)}')

        if self.octave > other.octave:
            return True
        if self.octave == other.octave:
            return PitchRest.pitch_comparator(self.pitch, other.pitch) > 0
        return False

    def __lt__(self, other: 'PitchRest') -> bool:
        """
        Compare two pitches.

        If any of the pitches is a rest, the comparison raise an exception.

        Args:
            other: The other name to compare

        Returns:
            True if this name is lower than the other, False otherwise

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('d')
            >>> pitch_rest < pitch_rest2
            True
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest < pitch_rest2
            False
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('b')
            >>> pitch_rest < pitch_rest2
            False
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest < pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest < pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...

        """
        if self.is_rest() or other.is_rest():
            raise ValueError(f'Invalid comparison: < operator can not be used to compare name of a rest.\n\
            self={repr(self)} < other={repr(other)}')

        if self.octave < other.octave:
            return True
        if self.octave == other.octave:
            return PitchRest.pitch_comparator(self.pitch, other.pitch) < 0
        return False

    def __ge__(self, other: 'PitchRest') -> bool:
        """
        Compare two pitches. If any of the PitchRest is a rest, the comparison raise an exception.
        Args:
            other (PitchRest): The other name to compare

        Returns (bool):
            True if this name is higher or equal than the other, False otherwise

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('d')
            >>> pitch_rest >= pitch_rest2
            False
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest >= pitch_rest2
            True
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('b')
            >>> pitch_rest >= pitch_rest2
            True
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest >= pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest >= pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...


        """
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other: 'PitchRest') -> bool:
        """
        Compare two pitches. If any of the PitchRest is a rest, the comparison raise an exception.
        Args:
            other (PitchRest): The other name to compare

        Returns (bool): True if this name is lower or equal than the other, False otherwise

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('d')
            >>> pitch_rest <= pitch_rest2
            True
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest <= pitch_rest2
            True
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('b')
            >>> pitch_rest <= pitch_rest2
            False
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest <= pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest <= pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...

        """
        return self.__lt__(other) or self.__eq__(other)


class Duration(ABC):
    """
    Represents the duration of a note or a rest.

    The duration is represented using the Humdrum Kern format.
    The duration is a number that represents the number of units of the duration.

    The duration of a whole note is 1, half note is 2, quarter note is 4, eighth note is 8, etc.

    The duration of a note is represented by a number. The duration of a rest is also represented by a number.

    This class do not limit the duration ranges.

    In the following example, the duration is represented by the number '2'.
    ```
    **kern
    *clefG2
    2c          // whole note
    4c          // half note
    8c          // quarter note
    16c         // eighth note
    *-
    ```
    """

    def __init__(self, raw_duration):
        self.encoding = str(raw_duration)

    @abstractmethod
    def modify(self, ratio: int):
        pass

    @abstractmethod
    def __deepcopy__(self, memo=None):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass

    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def __ge__(self, other):
        pass

    @abstractmethod
    def __le__(self, other):
        pass

    @abstractmethod
    def __str__(self):
        pass


class DurationFactory:
    @staticmethod
    def create_duration(duration: str) -> Duration:
        return DurationClassical(int(duration))


class DurationMensural(Duration):
    """
    Represents the duration in mensural notation of a note or a rest.
    """

    def __init__(self, duration):
        super().__init__(duration)
        self.duration = duration

    def __eq__(self, other):
        raise NotImplementedError()

    def modify(self, ratio: int):
        raise NotImplementedError()

    def __deepcopy__(self, memo=None):
        raise NotImplementedError()

    def __gt__(self, other):
        raise NotImplementedError()

    def __lt__(self, other):
        raise NotImplementedError()

    def __le__(self, other):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def __ge__(self, other):
        raise NotImplementedError()

    def __ne__(self, other):
        raise NotImplementedError()


class DurationClassical(Duration):
    """
    Represents the duration in classical notation of a note or a rest.
    """

    def __init__(self, duration: int):
        """
        Create a new Duration object.

        Args:
            duration (str): duration representation in Humdrum Kern format

        Examples:
            >>> duration = DurationClassical(2)
            True
            >>> duration = DurationClassical(4)
            True
            >>> duration = DurationClassical(32)
            True
            >>> duration = DurationClassical(1)
            True
            >>> duration = DurationClassical(0)
            False
            >>> duration = DurationClassical(-2)
            False
            >>> duration = DurationClassical(3)
            False
            >>> duration = DurationClassical(7)
            False
        """
        super().__init__(duration)
        if not DurationClassical.__is_valid_duration(duration):
            raise ValueError(f'Bad duration: {duration} was provided.')

        self.duration = int(duration)

    def modify(self, ratio: int):
        """
        Modify the duration of a note or a rest of the current object.

        Args:
            ratio (int): The factor to modify the duration. The factor must be greater than 0.

        Returns (DurationClassical): The new duration object with the modified duration.

        Examples:
            >>> duration = DurationClassical(2)
            >>> new_duration = duration.modify(2)
            >>> new_duration.duration
            4
            >>> duration = DurationClassical(2)
            >>> new_duration = duration.modify(0)
            Traceback (most recent call last):
            ...
            ValueError: Invalid factor provided: 0. The factor must be greater than 0.
            >>> duration = DurationClassical(2)
            >>> new_duration = duration.modify(-2)
            Traceback (most recent call last):
            ...
            ValueError: Invalid factor provided: -2. The factor must be greater than 0.
        """
        if not isinstance(ratio, int):
            raise ValueError(f'Invalid factor provided: {ratio}. The factor must be an integer.')
        if ratio <= 0:
            raise ValueError(f'Invalid factor provided: {ratio}. The factor must be greater than 0.')

        return copy.deepcopy(DurationClassical(self.duration * ratio))

    def __deepcopy__(self, memo=None):
        if memo is None:
            memo = {}

        new_instance = DurationClassical(self.duration)
        new_instance.duration = self.duration
        return new_instance

    def __str__(self):
        return f'{self.duration}'

    def __eq__(self, other: 'DurationClassical') -> bool:
        """
        Compare two durations.

        Args:
            other (DurationClassical): The other duration to compare

        Returns (bool): True if the durations are equal, False otherwise


        Examples:
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(2)
            >>> duration == duration2
            True
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(4)
            >>> duration == duration2
            False
        """
        if not isinstance(other, DurationClassical):
            return False
        return self.duration == other.duration

    def __ne__(self, other: 'DurationClassical') -> bool:
        """
        Compare two durations.

        Args:
            other (DurationClassical): The other duration to compare

        Returns (bool):
            True if the durations are different, False otherwise

        Examples:
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(2)
            >>> duration != duration2
            False
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(4)
            >>> duration != duration2
            True
        """
        return not self.__eq__(other)

    def __gt__(self, other: 'DurationClassical') -> bool:
        """
        Compare two durations.

        Args:
            other: The other duration to compare

        Returns (bool):
            True if this duration is higher than the other, False otherwise

        Examples:
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(4)
            >>> duration > duration2
            False
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(2)
            >>> duration > duration2
            True
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(4)
            >>> duration > duration2
            False
        """
        if not isinstance(other, DurationClassical):
            raise ValueError(f'Invalid comparison: > operator can not be used to compare duration with {type(other)}')
        return self.duration > other.duration

    def __lt__(self, other: 'DurationClassical') -> bool:
        """
        Compare two durations.

        Args:
            other (DurationClassical): The other duration to compare

        Returns (bool):
            True if this duration is lower than the other, False otherwise

        Examples:
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(4)
            >>> duration < duration2
            True
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(2)
            >>> duration < duration2
            False
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(4)
            >>> duration < duration2
            False
        """
        if not isinstance(other, DurationClassical):
            raise ValueError(f'Invalid comparison: < operator can not be used to compare duration with {type(other)}')
        return self.duration < other.duration

    def __ge__(self, other: 'DurationClassical') -> bool:
        """
        Compare two durations.

        Args:
            other (DurationClassical): The other duration to compare

        Returns (bool):
            True if this duration is higher or equal than the other, False otherwise

        Examples:
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(4)
            >>> duration >= duration2
            False
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(2)
            >>> duration >= duration2
            True
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(4)
            >>> duration >= duration2
            True
        """
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other: 'DurationClassical') -> bool:
        """
        Compare two durations.

        Args:
            other (DurationClassical): The other duration to compare

        Returns:
            True if this duration is lower or equal than the other, False otherwise

        Examples:
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(4)
            >>> duration <= duration2
            True
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(2)
            >>> duration <= duration2
            False
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(4)
            >>> duration <= duration2
            True
        """
        return self.__lt__(other) or self.__eq__(other)

    @classmethod
    def __is_valid_duration(cls, duration: int) -> bool:
        try:
            duration = int(duration)
            if duration is None or duration <= 0:
                return False

            return duration > 0 and (duration % 2 == 0 or duration == 1)
        except ValueError:
            return False


class Subtoken:
    """
    Subtoken class. Thhe subtokens are the smallest units of categories. ComplexToken objects are composed of subtokens.

    Attributes:
        encoding: The complete unprocessed encoding
        category: The subtoken category, one of SubTokenCategory
    """
    DECORATION = None

    def __init__(self, encoding: str, category: TokenCategory):
        """
        Subtoken constructor

        Args:
            encoding (str): The complete unprocessed encoding
            category (TokenCategory): The subtoken category. \
                It should be a child of the main 'TokenCategory' in the hierarchy.

        """
        self.encoding = encoding
        self.category = category

    def __str__(self):
        """
        Returns the string representation of the subtoken.

        Returns (str): The string representation of the subtoken.
        """
        return self.encoding

    def __eq__(self, other):
        """
        Compare two subtokens.

        Args:
            other (Subtoken): The other subtoken to compare.
        Returns (bool): True if the subtokens are equal, False otherwise.
        """
        if not isinstance(other, Subtoken):
            return False
        return self.encoding == other.encoding and self.category == other.category

    def __ne__(self, other):
        """
        Compare two subtokens.

        Args:
            other (Subtoken): The other subtoken to compare.
        Returns (bool): True if the subtokens are different, False otherwise.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Returns the hash of the subtoken.

        Returns (int): The hash of the subtoken.
        """
        return hash((self.encoding, self.category))

class AbstractToken(ABC):
    """
    An abstract base class representing a token.

    This class serves as a blueprint for creating various types of tokens, which are
    categorized based on their TokenCategory.

    Attributes:
        encoding (str): The original representation of the token.
        category (TokenCategory): The category of the token.
        hidden (bool): A flag indicating whether the token is hidden. Defaults to False.
    """

    def __init__(self, encoding: str, category: TokenCategory):
        """
        AbstractToken constructor

        Args:
            encoding (str): The original representation of the token.
            category (TokenCategory): The category of the token.
        """
        self.encoding = encoding
        self.category = category
        self.hidden = False

    @abstractmethod
    def export(self, **kwargs) -> str:
        """
        Exports the token.

        Keyword Arguments:
            filter_categories (Optional[Callable[[TokenCategory], bool]]): A function that takes a TokenCategory and returns a boolean
                indicating whether the token should be included in the export. If provided, only tokens for which the
                function returns True will be exported. Defaults to None. If None, all tokens will be exported.

        Returns:
            str: The encoded token representation, potentially filtered if a filter_categories function is provided.

        Examples:
            >>> token = AbstractToken('*clefF4', TokenCategory.SIGNATURES)
            >>> token.export()
            '*clefF4'
            >>> token.export(filter_categories=lambda cat: cat in {TokenCategory.SIGNATURES, TokenCategory.SIGNATURES.DURATION})
            '*clefF4'
        """
        pass


    def __str__(self):
        """
        Returns the string representation of the token.

        Returns (str): The string representation of the token without processing.
        """
        return self.export()

    def __eq__(self, other):
        """
        Compare two tokens.

        Args:
            other (AbstractToken): The other token to compare.
        Returns (bool): True if the tokens are equal, False otherwise.
        """
        if not isinstance(other, AbstractToken):
            return False
        return self.encoding == other.encoding and self.category == other.category

    def __ne__(self, other):
        """
        Compare two tokens.

        Args:
            other (AbstractToken): The other token to compare.
        Returns (bool): True if the tokens are different, False otherwise.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Returns the hash of the token.

        Returns (int): The hash of the token.
        """
        return hash((self.export(), self.category))


class Token(AbstractToken, ABC):
    """
    Abstract Token class.
    """

    def __init__(self, encoding, category):
        super().__init__(encoding, category)


class SimpleToken(Token):
    """
    SimpleToken class.
    """

    def __init__(self, encoding, category):
        super().__init__(encoding, category)

    def export(self, **kwargs) -> str:
        """
        Exports the token.

        Args:
            **kwargs: 'filter_categories' (Optional[Callable[[TokenCategory], bool]]): It is ignored in this class.

        Returns (str): The encoded token representation.
        """
        return self.encoding


class ErrorToken(SimpleToken):
    """
    Used to wrap tokens that have not been parsed.
    """

    def __init__(
            self,
            encoding: str,
            line: int,
            error: str
    ):
        """
        ErrorToken constructor

        Args:
            encoding (str): The original representation of the token.
            line (int): The line number of the token in the score.
            error (str): The error message thrown by the parser.
        """
        super().__init__(encoding, TokenCategory.ERROR)
        self.error = error
        self.line = line

    def export(self, **kwargs) -> str:
        """
        Exports the error token.

        Returns (str): A string representation of the error token.
        """
        # return ERROR_TOKEN
        return self.encoding  # TODO: add a constant for the error token

    def __str__(self):
        """
        Information about the error token.

        Returns (str) The information about the error token.
        """
        return f'Error token found at line {self.line} with encoding "{self.encoding}". Description: {self.error}'


class MetacommentToken(SimpleToken):
    """
    MetacommentToken class stores the metacomments of the score.
    Usually these are comments starting with `!!`.

    """

    def __init__(self, encoding: str):
        """
        Constructor for the MetacommentToken class.

        Args:
            encoding (str): The original representation of the token.
        """
        super().__init__(encoding, TokenCategory.LINE_COMMENTS)


class InstrumentToken(SimpleToken):
    """
    InstrumentToken class stores the instruments of the score.

    These tokens usually look like `*I"Organo`.
    """

    def __init__(self, encoding: str):
        """
        Constructor for the InstrumentToken

        Args:
            encoding:
        """
        super().__init__(encoding, TokenCategory.INSTRUMENTS)


class FieldCommentToken(SimpleToken):
    """
    FieldCommentToken class stores the metacomments of the score.
    Usually these are comments starting with `!!!`.

    """

    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.FIELD_COMMENTS)


class HeaderToken(SimpleToken):
    """
    HeaderTokens class.
    """

    def __init__(self, encoding, spine_id: int):
        """
        Constructor for the HeaderToken class.

        Args:
            encoding (str): The original representation of the token.
            spine_id (int): The spine id of the token. The spine id is used to identify the token in the score.\
                The spine_id starts from 0 and increases by 1 for each new spine like the following example:
                **kern  **kern  **kern **dyn **text
                0   1   2   3   4
        """
        super().__init__(encoding, TokenCategory.HEADER)
        self.spine_id = spine_id

    def export(self, **kwargs) -> str:
        return self.encoding


class SpineOperationToken(SimpleToken):
    """
    SpineOperationToken class.

    This token represents different operations in the Humdrum kern encoding.
    These are the available operations:
        - `*-`:  spine-path terminator.
        - `*`: null interpretation.
        - `*+`: add spines.
        - `*^`: split spines.
        - `*x`: exchange spines.

    Attributes:
        cancelled_at_stage (int): The stage at which the operation was cancelled. Defaults to None.
    """

    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.SPINE_OPERATION)
        self.cancelled_at_stage = None

    def is_cancelled_at(self, stage) -> bool:
        """
        Checks if the operation was cancelled at the given stage.

        Args:
            stage (int): The stage at which the operation was cancelled.

        Returns:
            bool: True if the operation was cancelled at the given stage, False otherwise.
        """
        if self.cancelled_at_stage is None:
            return False
        else:
            return self.cancelled_at_stage < stage


class BarToken(SimpleToken):
    """
    BarToken class.
    """

    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.BARLINES)


class SignatureToken(SimpleToken):
    """
    SignatureToken class for all signature tokens. It will be overridden by more specific classes.
    """

    def __init__(self, encoding, category=TokenCategory.SIGNATURES):
        super().__init__(encoding, category)


class ClefToken(SignatureToken):
    """
    ClefToken class.
    """

    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.CLEF)


class TimeSignatureToken(SignatureToken):
    """
    TimeSignatureToken class.
    """

    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.TIME_SIGNATURE)


class MeterSymbolToken(SignatureToken):
    """
    MeterSymbolToken class.
    """

    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.METER_SYMBOL)


class KeySignatureToken(SignatureToken):
    """
    KeySignatureToken class.
    """

    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.KEY_SIGNATURE)


class KeyToken(SignatureToken):
    """
    KeyToken class.
    """

    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.KEY_TOKEN)


class ComplexToken(Token, ABC):
    """
    Abstract ComplexToken class. This abstract class ensures that the subclasses implement the export method using\
     the 'filter_categories' parameter to filter the subtokens.

     Passing the argument 'filter_categories' by **kwargs don't break the compatibility with parent classes.

     Here we're trying to get the Liskov substitution principle done...
    """
    def __init__(self, encoding: str, category: TokenCategory):
        """
        Constructor for the ComplexToken

        Args:
            encoding (str): The original representation of the token.
            category (TokenCategory) : The category of the token.
        """
        super().__init__(encoding, category)

    @abstractmethod
    def export(self, **kwargs) -> str:
        """
        Exports the token.

        Keyword Arguments:
            filter_categories (Optional[Callable[[TokenCategory], bool]]): A function that takes a TokenCategory and returns a boolean
                indicating whether the token should be included in the export. If provided, only tokens for which the
                function returns True will be exported. Defaults to None. If None, all tokens will be exported.

        Returns (str): The exported token.
        """
        pass


class CompoundToken(ComplexToken):
    def __init__(self, encoding: str, category: TokenCategory, subtokens: List[Subtoken]):
        """
        Args:
            encoding (str): The complete unprocessed encoding
            category (TokenCategory): The token category, one of 'TokenCategory'
            subtokens (List[Subtoken]): The individual elements of the token. Also of type 'TokenCategory' but \
                in the hierarchy they must be children of the current token.
        """
        super().__init__(encoding, category)

        for subtoken in subtokens:
            if not isinstance(subtoken, Subtoken):
                raise ValueError(f'All subtokens must be instances of Subtoken. Found {type(subtoken)}')

        self.subtokens = subtokens

    def export(self, **kwargs) -> str:
        """
        Exports the token.

        Keyword Arguments:
            filter_categories (Optional[Callable[[TokenCategory], bool]]): A function that takes a TokenCategory and returns a boolean
                indicating whether the token should be included in the export. If provided, only tokens for which the
                function returns True will be exported. Defaults to None. If None, all tokens will be exported.

        Returns (str): The exported token.
        """
        filter_categories_fn = kwargs.get('filter_categories', None)
        parts = []
        for subtoken in self.subtokens:
            # Only export the subtoken if it passes the filter_categories (if provided)
            if filter_categories_fn is None or filter_categories_fn(subtoken.category):
                # parts.append(subtoken.export(**kwargs)) in the future when SubTokens will be Tokens
                parts.append(subtoken.encoding)
        return TOKEN_SEPARATOR.join(parts) if len(parts) > 0 else EMPTY_TOKEN


class NoteRestToken(ComplexToken):
    """
    NoteRestToken class.

    Attributes:
        pitch_duration_subtokens (list): The subtokens for the pitch and duration
        decoration_subtokens (list): The subtokens for the decorations
    """

    def __init__(
            self,
            encoding: str,
            pitch_duration_subtokens: List[Subtoken],
            decoration_subtokens: List[Subtoken]
    ):
        """
        NoteRestToken constructor.

        Args:
            encoding (str): The complete unprocessed encoding
            pitch_duration_subtokens (List[Subtoken])y: The subtokens for the pitch and duration
            decoration_subtokens (List[Subtoken]): The subtokens for the decorations. Individual elements of the token, of type Subtoken
        """
        super().__init__(encoding, TokenCategory.NOTE_REST)
        if not pitch_duration_subtokens or len(pitch_duration_subtokens) == 0:
            raise ValueError('Empty name-duration subtokens')

        for subtoken in pitch_duration_subtokens:
            if not isinstance(subtoken, Subtoken):
                raise ValueError(f'All pitch-duration subtokens must be instances of Subtoken. Found {type(subtoken)}')
        for subtoken in decoration_subtokens:
            if not isinstance(subtoken, Subtoken):
                raise ValueError(f'All decoration subtokens must be instances of Subtoken. Found {type(subtoken)}')

        self.pitch_duration_subtokens = pitch_duration_subtokens
        self.decoration_subtokens = decoration_subtokens

    def export(self, **kwargs) -> str:
        """
        Exports the token.

        Keyword Arguments:
            filter_categories (Optional[Callable[[TokenCategory], bool]]): A function that takes a TokenCategory and returns a boolean
                indicating whether the token should be included in the export. If provided, only tokens for which the
                function returns True will be exported. Defaults to None. If None, all tokens will be exported.

        Returns (str): The exported token.

        """
        filter_categories_fn = kwargs.get('filter_categories', None)

        # Filter subcategories
        pitch_duration_tokens = {
            subtoken for subtoken in self.pitch_duration_subtokens
            if filter_categories_fn is None or filter_categories_fn(subtoken.category)
        }
        decoration_tokens = {
            subtoken for subtoken in self.decoration_subtokens
            if filter_categories_fn is None or filter_categories_fn(subtoken.category)
        }
        pitch_duration_tokens_sorted = sorted(pitch_duration_tokens, key=lambda t:  (t.category.value, t.encoding))
        decoration_tokens_sorted     = sorted(decoration_tokens,     key=lambda t:  (t.category.value, t.encoding))

        # Join the sorted subtokens
        pitch_duration_part = TOKEN_SEPARATOR.join([subtoken.encoding for subtoken in pitch_duration_tokens_sorted])
        decoration_part = DECORATION_SEPARATOR.join([subtoken.encoding for subtoken in decoration_tokens_sorted])

        result = pitch_duration_part
        if len(decoration_part):
            result += DECORATION_SEPARATOR + decoration_part

        return result if len(result) > 0 else EMPTY_TOKEN


class ChordToken(SimpleToken):
    """
    ChordToken class.

    It contains a list of compound tokens
    """

    def __init__(self,
                 encoding: str,
                 category: TokenCategory,
                 notes_tokens: Sequence[Token]
                 ):
        """
        ChordToken constructor.

        Args:
            encoding (str): The complete unprocessed encoding
            category (TokenCategory): The token category, one of TokenCategory
            notes_tokens (Sequence[Token]): The subtokens for the notes. Individual elements of the token, of type token
        """
        super().__init__(encoding, category)
        self.notes_tokens = notes_tokens

    def export(self, **kwargs) -> str:
        result = ''
        for note_token in self.notes_tokens:
            if len(result) > 0:
                result += ' '

            result += note_token.export()

        return result


class BoundingBox:
    """
    BoundingBox class.

    It contains the coordinates of the score bounding box. Useful for full-page tasks.

    Attributes:
        from_x (int): The x coordinate of the top left corner
        from_y (int): The y coordinate of the top left corner
        to_x (int): The x coordinate of the bottom right corner
        to_y (int): The y coordinate of the bottom right corner
    """

    def __init__(self, x, y, w, h):
        """
        BoundingBox constructor.

        Args:
            x (int): The x coordinate of the top left corner
            y (int): The y coordinate of the top left corner
            w (int): The width
            h (int): The height
        """
        self.from_x = x
        self.from_y = y
        self.to_x = x + w
        self.to_y = y + h

    def w(self) -> int:
        """
        Returns the width of the box

        Returns:
            int: The width of the box
        """
        return self.to_x - self.from_x

    def h(self) -> int:
        """
        Returns the height of the box

        Returns:
            int: The height of the box
        return self.to_y - self.from_y
        """
        return self.to_y - self.from_y

    def extend(self, bounding_box) -> None:
        """
        Extends the bounding box. Modify the current object.

        Args:
            bounding_box (BoundingBox): The bounding box to extend

        Returns:
            None
        """
        self.from_x = min(self.from_x, bounding_box.from_x)
        self.from_y = min(self.from_y, bounding_box.from_y)
        self.to_x = max(self.to_x, bounding_box.to_x)
        self.to_y = max(self.to_y, bounding_box.to_y)

    def __str__(self) -> str:
        """
        Returns a string representation of the bounding box

        Returns (str): The string representation of the bounding box
        """
        return f'(x={self.from_x}, y={self.from_y}, w={self.w()}, h={self.h()})'

    def xywh(self) -> str:
        """
        Returns a string representation of the bounding box.

        Returns:
            str: The string representation of the bounding box
        """
        return f'{self.from_x},{self.from_y},{self.w()},{self.h()}'


class BoundingBoxToken(Token):
    """
    BoundingBoxToken class.

    It contains the coordinates of the score bounding box. Useful for full-page tasks.

    Attributes:
        encoding (str): The complete unprocessed encoding
        page_number (int): The page number
        bounding_box (BoundingBox): The bounding box
    """

    def __init__(
            self,
            encoding: str,
            page_number: int,
            bounding_box: BoundingBox
    ):
        """
        BoundingBoxToken constructor.

        Args:
            encoding (str): The complete unprocessed encoding
            page_number (int): The page number
            bounding_box (BoundingBox): The bounding box
        """
        super().__init__(encoding, TokenCategory.BOUNDING_BOXES)
        self.page_number = page_number
        self.bounding_box = bounding_box

    def export(self, **kwargs) -> str:
        return self.encoding


class MHXMToken(Token):
    """
    MHXMToken class.
    """
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.MHXM)

    # TODO: Implement constructor
    def export(self, **kwargs) -> str:
        return self.encoding
