import unittest
from unittest.mock import Mock, MagicMock

import kernpy as kp

class TestStoreCache(unittest.TestCase):
    def test_request_calculates_value(self):
        """Test that the callback is called on the first request."""
        callback = Mock(return_value=10)
        cache = kp.util.store_cache.StoreCache()

        # First request: callback should be called.
        result = cache.request(callback, 5)
        self.assertEqual(result, 10)
        callback.assert_called_once_with(5)

    def test_request_uses_cache(self):
        """Test that subsequent requests use the cached value and do not call the callback again."""
        callback = Mock(return_value=10)
        cache = kp.util.store_cache.StoreCache()

        # First call to store the value in cache.
        first_result = cache.request(callback, 5)
        self.assertEqual(first_result, 10)
        callback.assert_called_once_with(5)

        # Reset the mock call history.
        callback.reset_mock()

        # Second call should retrieve value from cache.
        second_result = cache.request(callback, 5)
        self.assertEqual(second_result, 10)
        callback.assert_not_called()  # The callback should not have been called again.

    def test_hierarchy_nodes(self):
        expected_nodes = {kp.TokenCategory.PITCH, kp.TokenCategory.ALTERATION, kp.TokenCategory.DECORATION}

        # 1. Assert that the direct call returns the expected nodes.
        nodes_result = kp.TokenCategoryHierarchyMapper.nodes(kp.TokenCategory.NOTE)
        self.assertEqual(nodes_result, expected_nodes)

        # 2. Create an instance of the cache and request the nodes value via the cache.
        cache = kp.util.store_cache.StoreCache()
        response1 = cache.request(kp.TokenCategoryHierarchyMapper.nodes, kp.TokenCategory.NOTE)
        self.assertEqual(response1, expected_nodes)

        # 3. Request again to confirm that the cached value is used (the result remains the same).
        response2 = cache.request(kp.TokenCategoryHierarchyMapper.nodes, kp.TokenCategory.NOTE)
        self.assertEqual(response2, expected_nodes)

        # 4. Assert that the callback was only invoked once,
        # you can wrap the nodes method with a MagicMock. For example:
        original_nodes = kp.TokenCategoryHierarchyMapper.nodes
        kp.TokenCategoryHierarchyMapper.nodes = MagicMock(wraps=original_nodes)

        # Call through the cache
        cache = kp.util.store_cache.StoreCache()
        cache.request(kp.TokenCategoryHierarchyMapper.nodes, kp.TokenCategory.NOTE)
        cache.request(kp.TokenCategoryHierarchyMapper.nodes, kp.TokenCategory.NOTE)

        # Assert that the original method was only called once.
        kp.TokenCategoryHierarchyMapper.nodes.assert_called_once_with(kp.TokenCategory.NOTE)

        # Restore the original nodes method.
        kp.TokenCategoryHierarchyMapper.nodes = original_nodes


if __name__ == '__main__':
    unittest.main()
