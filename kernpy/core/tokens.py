from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from enum import Enum, auto
import copy
from typing import List, Dict, Set, Union, Optional

TOKEN_SEPARATOR = '@'
DECORATION_SEPARATOR = '·'
HEADERS = {"**mens", "**kern", "**text", "**harm", "**mxhm", "**root", "**dyn", "**dynam", "**fing"}
CORE_HEADERS = {"**kern", "**mens"}
SPINE_OPERATIONS = {"*-", "*+", "*^", "*v", "*x"}
TERMINATOR = "*-"


# We don't use inheritance here for all elements but enum, because we don't need any polymorphism mechanism, just a grouping one
# TODO Poner todos los tipos - p.ej. también comandos de layout - slurs, etc...
class TokenCategory(Enum):
    """
    Options for the category of a token.

    This is used to determine what kind of token should be exported.

    The categories are not sorted in any particular order. Hierarchical order must be defined in other data structures.
    """
    STRUCTURAL = auto()  # header, spine operations
    CORE = auto() # notes, rests, chords, etc.
    NOTE_REST = auto()
    NOTE = auto()
    PITCH = auto()
    DURATION = auto()
    DECORATION = auto()
    REST = auto()
    CHORD = auto()
    EMPTY = auto()  # placeholders, null interpretation
    SIGNATURES = auto()
    CLEF = auto()
    TIME_SIGNATURE = auto()
    METER_SYMBOL = auto()
    KEY_SIGNATURE = auto()
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
    BOUNDING_BOXES = auto()
    OTHER = auto()


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
        TokenCategory.STRUCTURAL: {},  # each leave must be an empty dictionary
        TokenCategory.CORE: {
            TokenCategory.NOTE_REST: {
                TokenCategory.DURATION: {},
                TokenCategory.NOTE: {
                    TokenCategory.PITCH: {},
                    TokenCategory.DECORATION: {}},
                TokenCategory.REST: {},
            },
            TokenCategory.CHORD: {},
            TokenCategory.EMPTY: {},
        },
        TokenCategory.SIGNATURES: {
            TokenCategory.CLEF: {},
            TokenCategory.TIME_SIGNATURE: {},
            TokenCategory.METER_SYMBOL: {},
            TokenCategory.KEY_SIGNATURE: {},
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
        TokenCategory.BOUNDING_BOXES: {},
        TokenCategory.OTHER: {},
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
        Recursively check if `child` is in the subtree of `parent`.

        Args:
            parent (TokenCategory): The parent category.
            child (TokenCategory): The category to check.

        Returns:
            bool: True if `child` is a descendant of `parent`, False otherwise.
        """
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

        # Build the union of each include/exclude category and its descendants. O(n**2) but n is small.
        included_nodes = set.union(*[(cls.nodes(cat) | {cat}) for cat in include]) if len(include) > 0 else include
        excluded_nodes = set.union(*[(cls.nodes(cat) | {cat}) for cat in exclude]) if len(exclude) > 0 else exclude

        # Valid categories are those in the include set that are not excluded.
        valid_categories = included_nodes - excluded_nodes

        # Check if any node in the target set is in the valid categories.
        return len(target_nodes & valid_categories) > 0


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
        # Check include
        if include is None:
            include = cls.all()
        else:
            if isinstance(include, (list, tuple)):
                include = set(include)
            elif not isinstance(include, set):
                include = {include}
            if not all(isinstance(cat, TokenCategory) for cat in include):
                raise ValueError('Invalid category: include and exclude must be a set of TokenCategory.')

        # Check exclude
        if exclude is None:
            exclude = set()
        else:
            if isinstance(exclude, (list, tuple)):
                exclude = set(exclude)
            elif not isinstance(exclude, set):
                exclude = {exclude}
            if not all(isinstance(cat, TokenCategory) for cat in exclude):
                raise ValueError('Invalid category: category must be a TokenCategory.')

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
    Subtoken class

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
    def export(self) -> str:
        """
        Exports the token.

        Returns:
            str: The encoding of the token.

        Examples:
            >>> token = AbstractToken('*clefF4', TokenCategory.SIGNATURES)
            >>> token.export()
            '*clefF4'
        """
        pass

    def __str__(self):
        """
        Returns the string representation of the token.

        Returns (str): The string representation of the token.
        """
        return self.export()


class ErrorToken(AbstractToken):
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
        super().__init__(encoding, TokenCategory.EMPTY)
        self.error = error
        self.line = line

    def export(self) -> str:
        return ''  # TODO Qué exportamos?

    def __str__(self):
        """
        Information about the error token.

        Returns (str) The information about the error token.
        """
        return f'Error token found at line {self.line} with encoding "{self.encoding}". Description: {self.error}'


class MetacommentToken(AbstractToken):
    """
    MetacommentToken class stores the metacomments of the score.
    Usually these are comments starting with `!!`.

    """

    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.LINE_COMMENTS)

    def export(self) -> str:
        return self.encoding


class InstrumentToken(AbstractToken):
    """
    InstrumentToken class stores the instruments of the score.

    These tokens usually look like `*I"Organo`.
    """

    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.INSTRUMENTS)

    def export(self) -> str:
        return self.encoding


class FieldCommentToken(AbstractToken):
    """
    FieldCommentToken class stores the metacomments of the score.
    Usually these are comments starting with `!!!`.

    """

    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.FIELD_COMMENTS)

    def export(self) -> str:
        return self.encoding


class HeaderToken(AbstractToken):
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
        super().__init__(encoding, TokenCategory.STRUCTURAL)
        self.spine_id = spine_id

    def export(self) -> str:
        extended_header = '**e' + self.encoding[2:]  # remove the **, and append the e
        return extended_header


class SpineOperationToken(AbstractToken):
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
        super().__init__(encoding, TokenCategory.STRUCTURAL)
        self.cancelled_at_stage = None

    def export(self) -> str:
        return self.encoding

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

    def export(self) -> str:
        return self.encoding


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

    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.SIGNATURES)


class ClefToken(SignatureToken):
    """
    ClefToken class.
    """

    def __init__(self, encoding):
        super().__init__(encoding)


class TimeSignatureToken(SignatureToken):
    """
    TimeSignatureToken class.
    """

    def __init__(self, encoding):
        super().__init__(encoding)


class MeterSymbolToken(SignatureToken):
    """
    MeterSymbolToken class.
    """

    def __init__(self, encoding):
        super().__init__(encoding)


class KeySignatureToken(SignatureToken):
    """
    KeySignatureToken class.
    """

    def __init__(self, encoding):
        super().__init__(encoding)


class KeyToken(SignatureToken):
    """
    KeyToken class.
    """

    def __init__(self, encoding):
        super().__init__(encoding)


class CompoundToken(Token):
    def __init__(self, encoding: str, category: TokenCategory, subtokens: List[Subtoken]):
        """
        Args:
            encoding (str): The complete unprocessed encoding
            category (TokenCategory): The token category, one of 'TokenCategory'
            subtokens (List[Subtoken]): The individual elements of the token. Also of type 'TokenCategory' but \
                in the hierarchy they must be children of the current token.
        """
        super().__init__(encoding, category)
        self.subtokens = subtokens

    def export(self) -> str:
        result = ''
        for subtoken in self.subtokens:
            if len(result) > 0:
                result += TOKEN_SEPARATOR

            result += subtoken.encoding
        return result


class NoteRestToken(Token):
    """
    NoteRestToken class.

    Attributes:
        pitch_duration_subtokens (list): The subtokens for the pitch and duration
        decoration_subtokens (list): The subtokens for the decorations
    """

    def __init__(
            self,
            encoding: str,
            pitch_duration_subtokens,
            decoration_subtokens
    ):
        """
        NoteRestToken constructor.

        Args:
            encoding (str): The complete unprocessed encoding
            pitch_duration_subtokens: The subtokens for the pitch and duration
            decoration_subtokens: The subtokens for the decorations. Individual elements of the token, of type Subtoken
        """
        super().__init__(encoding, TokenCategory.CORE)
        if not pitch_duration_subtokens or len(pitch_duration_subtokens) == 0:
            raise ValueError('Empty name-duration subtokens')

        self.pitch_duration_subtokens = pitch_duration_subtokens
        self.decoration_subtokens = decoration_subtokens

        try:
            self.duration = None
            # TODO: Refactor this
            #duration_token = ''.join([n for n in self.encoding if n.isnumeric()])
            #if duration_token is None or len(duration_token) == 0:
            #    self.duration = None
            #else:
            #    self.duration = DurationFactory.create_duration(duration_token)
        except Exception:
            self.duration = None

        try:
            self.pitch = None
            # TODO: Refactor this
            #pitch_rest_token = ''.join([n for n in self.encoding if n in PitchRest.VALID_PITCHES])
            #if pitch_rest_token is None or len(pitch_rest_token) == 0:
            #    self.pitch = None
            #else:
            #    self.pitch = PitchRest(pitch_rest_token)
        except Exception:
            self.pitch = None
        # TODO: Ahora entran muchos tokens diferentes, filtrar solo los de name

    def export(self) -> str:
        result = ''
        for subtoken in self.pitch_duration_subtokens:
            if len(result) > 0:
                result += TOKEN_SEPARATOR

            result += subtoken.encoding

        decorations = set()
        # we order them and avoid repetitions
        for subtoken in self.decoration_subtokens:
            decorations.add(subtoken)
        for decoration in sorted(decorations):
            result += DECORATION_SEPARATOR
            result += decoration
        return result


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
            notes_tokens (Sequence[Token]): The subtokens for the notes. Individual elements of the token, of type Subtoken
        """
        super().__init__(encoding, category)
        self.notes_tokens = notes_tokens

    def export(self) -> str:
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


class BoundingBoxToken(AbstractToken):
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

    def export(self) -> str:
        return self.encoding


class MHXMToken(AbstractToken):
    """
    MHXMToken class.
    """
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.OTHER)

    # TODO: Implement constructor
    def export(self) -> str:
        return self.encoding
