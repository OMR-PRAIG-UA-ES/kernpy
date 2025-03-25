import os
import unittest
import sys

import kernpy as kp


class TokenCategoryHierarchyTestCase(unittest.TestCase):
    def _is_child(cls, parent, child):
        cls.assertTrue(kp.TokenCategoryHierarchyMapper.is_child(parent=parent, child=child))

    def _is_not_child(cls, parent, child):
        cls.assertFalse(kp.TokenCategoryHierarchyMapper.is_child(parent=parent, child=child))

    def _is_valid_category(cls, include, exclude, expected_categories):
        cls.assertSetEqual(
            expected_categories,
            kp.TokenCategoryHierarchyMapper.valid(include=include, exclude=exclude)
        )

    def test_is_child_of_CORE(self):
        self._is_child(kp.TokenCategory.CORE, kp.TokenCategory.NOTE_REST)
        self._is_child(kp.TokenCategory.CORE, kp.TokenCategory.NOTE)
        self._is_child(kp.TokenCategory.CORE, kp.TokenCategory.REST)
        self._is_child(kp.TokenCategory.CORE, kp.TokenCategory.DURATION)
        self._is_child(kp.TokenCategory.CORE, kp.TokenCategory.CHORD)
        self._is_child(kp.TokenCategory.CORE, kp.TokenCategory.EMPTY)

    def test_is_child_of_SIGNATURES(self):
        self._is_child(kp.TokenCategory.SIGNATURES, kp.TokenCategory.CLEF)
        self._is_child(kp.TokenCategory.SIGNATURES, kp.TokenCategory.TIME_SIGNATURE)
        self._is_child(kp.TokenCategory.SIGNATURES, kp.TokenCategory.METER_SYMBOL)
        self._is_child(kp.TokenCategory.SIGNATURES, kp.TokenCategory.KEY_SIGNATURE)

    def test_not_child_across_branches(self):
        """
        Test that categories from different branches are not related.
        """
        # For example, CLEF (under SIGNATURES) is not a child of CORE.
        self._is_not_child(kp.TokenCategory.CORE, kp.TokenCategory.CLEF)
        # Similarly, dynamics is not a child of comments.
        self._is_not_child(kp.TokenCategory.COMMENTS, kp.TokenCategory.DYNAMICS)

    def test_invalid_parent_type(self):
        self.assertFalse(kp.TokenCategoryHierarchyMapper.is_child("CORE", kp.TokenCategory.NOTE))

    def test_invalid_child_type(self):
        self.assertFalse(kp.TokenCategoryHierarchyMapper.is_child(kp.TokenCategory.CORE, "NOTE"))

    def test_child_of_same_category(self):
        self.assertFalse(kp.TokenCategoryHierarchyMapper.is_child(kp.TokenCategory.CORE, kp.TokenCategory.CORE))
        self.assertFalse(kp.TokenCategoryHierarchyMapper.is_child(kp.TokenCategory.HARMONY, kp.TokenCategory.HARMONY))


    def test_match_included_category(self):
        """Test that a category matches when it's explicitly included."""
        self.assertTrue(
            kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include={kp.TokenCategory.NOTE_REST})
        )

    def test_match_with_exclusion(self):
        """Test that a category is correctly excluded."""
        self.assertFalse(
            kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include={kp.TokenCategory.NOTE_REST}, exclude={kp.TokenCategory.NOTE})
        )

    def test_match_without_includes(self):
        """Test that a category is included when include is None."""
        self.assertTrue(
            kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include=None)
        )

    def test_match_with_exclude_only(self):
        """Test that an excluded category correctly returns False."""
        self.assertFalse(
            kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.DURATION, exclude={kp.TokenCategory.DURATION})
        )

    def test_match_descendant_inclusion(self):
        """Test that a child category correctly matches an ancestor in include set."""
        self.assertTrue(
            kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.PITCH, include={kp.TokenCategory.NOTE_REST})
        )

    def test_match_descendant_exclusion(self):
        """Test that a descendant category is excluded when its ancestor is in exclude set."""
        self.assertFalse(
            kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.PITCH, include={kp.TokenCategory.NOTE_REST}, exclude={kp.TokenCategory.NOTE})
        )

    def test_match_category_not_in_include(self):
        """Test that a category is not matched if it is not in the include set or a descendant."""
        self.assertFalse(
            kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.BARLINES, include={kp.TokenCategory.NOTE_REST})
        )

    def test_match_category_in_exclude_and_include(self):
        """Ensure that exclude takes precedence over include."""
        self.assertFalse(
            kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include={kp.TokenCategory.CORE}, exclude={kp.TokenCategory.NOTE})
        )

    def test_match_accept_passing_only_one_category(self):
        kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include=kp.TokenCategory.NOTE_REST)
        kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include=kp.TokenCategory.CORE)
        kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, exclude=kp.TokenCategory.NOTE_REST)
        kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, exclude=kp.TokenCategory.CORE)

        self.assertTrue(True)  # If no exception is raised, the test passes.

    def test_match_accept_passing_list_or_tuple_of_categories(self):
        kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include=[kp.TokenCategory.NOTE_REST])
        kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include=(kp.TokenCategory.NOTE_REST,))
        kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include=[kp.TokenCategory.NOTE_REST, kp.TokenCategory.CORE])
        kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include=(kp.TokenCategory.NOTE_REST, kp.TokenCategory.CORE))
        kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, exclude=[kp.TokenCategory.NOTE_REST])
        kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, exclude=(kp.TokenCategory.NOTE_REST,))
        kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, exclude=[kp.TokenCategory.NOTE_REST, kp.TokenCategory.CORE])
        kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, exclude=(kp.TokenCategory.NOTE_REST, kp.TokenCategory.CORE))

        self.assertTrue(True)

    def test_match_raises_error_on_invalid_include(self):
        with self.assertRaises(ValueError):
            kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include="NOTE_REST")
        with self.assertRaises(ValueError):
            kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include=[kp.TokenCategory.NOTE_REST, 0])
        with self.assertRaises(ValueError):
            kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include=[kp.TokenCategory.NOTE_REST, "NOTE"])
        with self.assertRaises(ValueError):
            kp.TokenCategoryHierarchyMapper.match(kp.TokenCategory.NOTE, include=[kp.TokenCategory.NOTE_REST, None])

    def test_hierarchy_mapper_children(self):
        expected_children = {
            kp.TokenCategory.NOTE_REST,
            kp.TokenCategory.CHORD,
            kp.TokenCategory.EMPTY,
        }
        self.assertSetEqual(expected_children, kp.TokenCategoryHierarchyMapper.children(kp.TokenCategory.CORE))

    def test_hierarchy_mapper_nodes_CORE(self):
        expected_nodes = {
            kp.TokenCategory.NOTE_REST,
            kp.TokenCategory.NOTE,
            kp.TokenCategory.REST,
            kp.TokenCategory.DURATION,
            kp.TokenCategory.CHORD,
            kp.TokenCategory.EMPTY,
            kp.TokenCategory.DECORATION,
            kp.TokenCategory.PITCH
        }
        self.assertSetEqual(expected_nodes, kp.TokenCategoryHierarchyMapper.nodes(parent=kp.TokenCategory.CORE))

    def test_hierarchy_mapper_nodes_SIGNATURES(self):
        expected_nodes = {
            kp.TokenCategory.CLEF,
            kp.TokenCategory.TIME_SIGNATURE,
            kp.TokenCategory.METER_SYMBOL,
            kp.TokenCategory.KEY_SIGNATURE
        }
        self.assertSetEqual(expected_nodes, kp.TokenCategoryHierarchyMapper.nodes(parent=kp.TokenCategory.SIGNATURES))

    def test_hierarchy_mapper_nodes_NOTE_REST(self):
        expected_nodes = {
            kp.TokenCategory.NOTE,
            kp.TokenCategory.REST,
            kp.TokenCategory.DURATION,
            kp.TokenCategory.PITCH,
            kp.TokenCategory.DECORATION,
        }
        self.assertSetEqual(expected_nodes, kp.TokenCategoryHierarchyMapper.nodes(parent=kp.TokenCategory.NOTE_REST))

    def test_hierarchy_mapper_leaves_CORE(self):
        expected_leaves = {
            kp.TokenCategory.REST,
            kp.TokenCategory.DURATION,
            kp.TokenCategory.CHORD,
            kp.TokenCategory.EMPTY,
            kp.TokenCategory.DECORATION,
            kp.TokenCategory.PITCH
        }
        self.assertSetEqual(expected_leaves, kp.TokenCategoryHierarchyMapper.leaves(target=kp.TokenCategory.CORE))

    def test_hierarchy_mapper_leaves_SIGNATURES(self):
        expected_leaves = {
            kp.TokenCategory.CLEF,
            kp.TokenCategory.TIME_SIGNATURE,
            kp.TokenCategory.METER_SYMBOL,
            kp.TokenCategory.KEY_SIGNATURE
        }
        self.assertSetEqual(expected_leaves, kp.TokenCategoryHierarchyMapper.leaves(target=kp.TokenCategory.SIGNATURES))

    def test_hierarchy_mapper_leaves_NOTE_REST(self):
        expected_leaves = {
            kp.TokenCategory.REST,
            kp.TokenCategory.DURATION,
            kp.TokenCategory.PITCH,
            kp.TokenCategory.DECORATION
        }
        self.assertSetEqual(expected_leaves, kp.TokenCategoryHierarchyMapper.leaves(target=kp.TokenCategory.NOTE_REST))

    def test_hierarchy_tree(self):
        with open('resource_dir/hierarchy/tree.txt', 'r') as f:
            expected_tree = f.read()

        real_output = kp.TokenCategoryHierarchyMapper.tree()

        self.assertEqual(expected_tree, real_output)

    def test_hierarchy_valid_categories_CORE(self):
        self._is_valid_category(
            include={kp.TokenCategory.CORE},
            exclude=set(),
            expected_categories={
                kp.TokenCategory.CORE,
                kp.TokenCategory.NOTE_REST,
                kp.TokenCategory.NOTE,
                kp.TokenCategory.REST,
                kp.TokenCategory.DURATION,
                kp.TokenCategory.CHORD,
                kp.TokenCategory.EMPTY,
                kp.TokenCategory.DECORATION,
                kp.TokenCategory.PITCH
            }
        )

    def test_hierarchy_valid_categories_SIGNATURES(self):
        self._is_valid_category(
            include={kp.TokenCategory.SIGNATURES},
            exclude=set(),
            expected_categories={
                kp.TokenCategory.SIGNATURES,
                kp.TokenCategory.CLEF,
                kp.TokenCategory.TIME_SIGNATURE,
                kp.TokenCategory.METER_SYMBOL,
                kp.TokenCategory.KEY_SIGNATURE
            }
        )

    def test_hierarchy_valid_categories_NOTE_REST(self):
        self._is_valid_category(
            include={kp.TokenCategory.NOTE_REST},
            exclude=set(),
            expected_categories={
                kp.TokenCategory.NOTE_REST,
                kp.TokenCategory.NOTE,
                kp.TokenCategory.REST,
                kp.TokenCategory.DURATION,
                kp.TokenCategory.PITCH,
                kp.TokenCategory.DECORATION
            }
        )

class PitchRestTestCase(unittest.TestCase):
    def test_PitchRest_creation_generic(self):
        pitch_rest = kp.PitchRest('c')
        self.assertEqual(pitch_rest.pitch, 'c')
        self.assertEqual(pitch_rest.octave, 4)
        self.assertEqual(pitch_rest.is_rest(), False)

    def test_PitchRest_creation_pitch(self):
        pitch_rest = kp.PitchRest('c')
        self.assertEqual(pitch_rest.pitch, 'c')
        pitch_rest = kp.PitchRest('ccc')
        self.assertEqual(pitch_rest.pitch, 'c')
        pitch_rest = kp.PitchRest('C')
        self.assertEqual(pitch_rest.pitch, 'c')
        pitch_rest = kp.PitchRest('CCCCC')
        self.assertEqual(pitch_rest.pitch, 'c')

    def test_PitchRest_creation_octave(self):
        pitch_rest = kp.PitchRest('c')
        self.assertEqual(pitch_rest.octave, 4)
        pitch_rest = kp.PitchRest('ccc')
        self.assertEqual(pitch_rest.octave, 6)
        pitch_rest = kp.PitchRest('ccccc')
        self.assertEqual(pitch_rest.octave, 8)
        pitch_rest = kp.PitchRest('C')
        self.assertEqual(pitch_rest.octave, 3)
        pitch_rest = kp.PitchRest('CCC')
        self.assertEqual(pitch_rest.octave, 1)
        pitch_rest = kp.PitchRest('CCCCC')
        self.assertEqual(pitch_rest.octave, -1)

    def test_PitchRest_creation_rest(self):
        pitch_rest = kp.PitchRest('r')
        self.assertEqual(pitch_rest.pitch, 'r')
        self.assertEqual(pitch_rest.octave, None)
        self.assertEqual(pitch_rest.is_rest(), True)

    def test_PitchRest_eq(self):
        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('c')
        self.assertTrue(pitch_rest_a == pitch_rest_b)

        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('ccc')
        self.assertFalse(pitch_rest_a == pitch_rest_b)

        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('r')
        self.assertFalse(pitch_rest_a == pitch_rest_b)

        pitch_rest_a = kp.PitchRest('r')
        pitch_rest_b = kp.PitchRest('r')
        self.assertTrue(pitch_rest_a == pitch_rest_b)

    def test_PitchRest_ne(self):
        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('d')
        self.assertTrue(pitch_rest_a != pitch_rest_b)

    def test_PitchRest_gt(self):
        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('c')
        self.assertFalse(pitch_rest_a > pitch_rest_b)

        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('ccc')
        self.assertFalse(pitch_rest_a > pitch_rest_b)

        pitch_rest_a = kp.PitchRest('C')
        pitch_rest_b = kp.PitchRest('C')
        self.assertFalse(pitch_rest_a > pitch_rest_b)

        pitch_rest_a = kp.PitchRest('C')
        pitch_rest_b = kp.PitchRest('CCC')
        self.assertTrue(pitch_rest_a > pitch_rest_b)

        pitch_rest_a = kp.PitchRest('CCC')
        pitch_rest_b = kp.PitchRest('C')
        self.assertFalse(pitch_rest_a > pitch_rest_b)

        pitch_rest_a = kp.PitchRest('r')
        pitch_rest_b = kp.PitchRest('r')
        with self.assertRaises(ValueError):
            pitch_rest_a > pitch_rest_b

    def test_PitchRest_lt(self):
        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('c')
        self.assertFalse(pitch_rest_a < pitch_rest_b)

        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('ccc')
        self.assertTrue(pitch_rest_a < pitch_rest_b)

        pitch_rest_a = kp.PitchRest('C')
        pitch_rest_b = kp.PitchRest('C')
        self.assertFalse(pitch_rest_a < pitch_rest_b)

        pitch_rest_a = kp.PitchRest('C')
        pitch_rest_b = kp.PitchRest('CCC')
        self.assertFalse(pitch_rest_a < pitch_rest_b)

        pitch_rest_a = kp.PitchRest('CCC')
        pitch_rest_b = kp.PitchRest('C')
        self.assertTrue(pitch_rest_a < pitch_rest_b)

        pitch_rest_a = kp.PitchRest('r')
        pitch_rest_b = kp.PitchRest('r')
        with self.assertRaises(ValueError):
            pitch_rest_a < pitch_rest_b

    def test_PitchRest_ge(self):
        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('c')
        self.assertTrue(pitch_rest_a >= pitch_rest_b)

        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('ccc')
        self.assertFalse(pitch_rest_a >= pitch_rest_b)

        pitch_rest_a = kp.PitchRest('C')
        pitch_rest_b = kp.PitchRest('C')
        self.assertTrue(pitch_rest_a >= pitch_rest_b)

        pitch_rest_a = kp.PitchRest('C')
        pitch_rest_b = kp.PitchRest('CCC')
        self.assertTrue(pitch_rest_a >= pitch_rest_b)

        pitch_rest_a = kp.PitchRest('CCC')
        pitch_rest_b = kp.PitchRest('C')
        self.assertFalse(pitch_rest_a >= pitch_rest_b)

        pitch_rest_a = kp.PitchRest('r')
        pitch_rest_b = kp.PitchRest('r')
        with self.assertRaises(ValueError):
            pitch_rest_a >= pitch_rest_b

        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('r')
        with self.assertRaises(ValueError):
            pitch_rest_a >= pitch_rest_b

    def test_PitchRest_le(self):
        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('c')
        self.assertTrue(pitch_rest_a <= pitch_rest_b)

        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('ccc')
        self.assertTrue(pitch_rest_a <= pitch_rest_b)

        pitch_rest_a = kp.PitchRest('C')
        pitch_rest_b = kp.PitchRest('C')
        self.assertTrue(pitch_rest_a <= pitch_rest_b)

        pitch_rest_a = kp.PitchRest('C')
        pitch_rest_b = kp.PitchRest('CCC')
        self.assertFalse(pitch_rest_a <= pitch_rest_b)

        pitch_rest_a = kp.PitchRest('CCC')
        pitch_rest_b = kp.PitchRest('C')
        self.assertTrue(pitch_rest_a <= pitch_rest_b)

        pitch_rest_a = kp.PitchRest('r')
        pitch_rest_b = kp.PitchRest('r')
        with self.assertRaises(ValueError):
            pitch_rest_a <= pitch_rest_b

        pitch_rest_a = kp.PitchRest('c')
        pitch_rest_b = kp.PitchRest('r')
        with self.assertRaises(ValueError):
            pitch_rest_a <= pitch_rest_b


class DurationTestCase(unittest.TestCase):
    def test_Duration_creation_generic(self):
        duration = kp.DurationClassical(2)
        self.assertEqual(duration.duration, 2)

        duration = kp.DurationClassical(16)
        self.assertEqual(duration.duration, 16)

        duration = kp.DurationClassical(1)
        self.assertEqual(duration.duration, 1)

        with self.assertRaises(ValueError):
            duration = kp.DurationClassical(0)

        with self.assertRaises(ValueError):
            duration = kp.DurationClassical('abcde')

    def test_Duration_eq(self):
        duration_a = kp.DurationClassical(2)
        duration_b = kp.DurationClassical(2)
        self.assertTrue(duration_a == duration_b)

        duration_a = kp.DurationClassical(2)
        duration_b = kp.DurationClassical(16)
        self.assertFalse(duration_a == duration_b)

    def test_Duration_ne(self):
        duration_a = kp.DurationClassical(2)
        duration_b = kp.DurationClassical(2)
        self.assertFalse(duration_a != duration_b)

        duration_a = kp.DurationClassical(2)
        duration_b = kp.DurationClassical(16)
        self.assertTrue(duration_a != duration_b)

    def test_Duration_gt(self):
        duration_a = kp.DurationClassical(2)
        duration_b = kp.DurationClassical(2)
        self.assertFalse(duration_a > duration_b)

        duration_a = kp.DurationClassical(2)
        duration_b = kp.DurationClassical(16)
        self.assertFalse(duration_a > duration_b)

        duration_a = kp.DurationClassical(16)
        duration_b = kp.DurationClassical(2)
        self.assertTrue(duration_a > duration_b)

    def test_Duration_lt(self):
        duration_a = kp.DurationClassical(2)
        duration_b = kp.DurationClassical(2)
        self.assertFalse(duration_a < duration_b)

        duration_a = kp.DurationClassical(2)
        duration_b = kp.DurationClassical(16)
        self.assertTrue(duration_a < duration_b)

        duration_a = kp.DurationClassical(16)
        duration_b = kp.DurationClassical(2)
        self.assertFalse(duration_a < duration_b)

    def test_Duration_ge(self):
        duration_a = kp.DurationClassical(2)
        duration_b = kp.DurationClassical(2)
        self.assertTrue(duration_a >= duration_b)

        duration_a = kp.DurationClassical(2)
        duration_b = kp.DurationClassical(16)
        self.assertFalse(duration_a >= duration_b)

        duration_a = kp.DurationClassical(16)
        duration_b = kp.DurationClassical(2)
        self.assertTrue(duration_a >= duration_b)

    def test_Duration_le(self):
        duration_a = kp.DurationClassical(2)
        duration_b = kp.DurationClassical(2)
        self.assertTrue(duration_a <= duration_b)

        duration_a = kp.DurationClassical(2)
        duration_b = kp.DurationClassical(16)
        self.assertTrue(duration_a <= duration_b)

        duration_a = kp.DurationClassical(16)
        duration_b = kp.DurationClassical(2)
        self.assertFalse(duration_a <= duration_b)

    def test_Duration_modify_duration(self):
        duration = kp.DurationClassical(2)
        new_duration = duration.modify(4)
        self.assertEqual(new_duration.duration, 8)

        duration = kp.DurationClassical(16)
        new_duration = duration.modify(2)
        self.assertEqual(new_duration.duration, 32)

        duration = kp.DurationClassical(2)
        new_duration = duration.modify(1)
        self.assertEqual(new_duration.duration, 2)

        duration = kp.DurationClassical(2)
        with self.assertRaises(ValueError):
            new_duration = duration.modify(0)

        duration = kp.DurationClassical(2)
        with self.assertRaises(ValueError):
            new_duration = duration.modify(-1)

        duration = kp.DurationClassical(2)
        with self.assertRaises(ValueError):
            new_duration = duration.modify(1.5)


class DurationMensuralTestCase(unittest.TestCase):
    def test_DurationMensural_creation_generic(self):
        pass
