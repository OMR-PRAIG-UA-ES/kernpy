class StoreCache:
    """
    A simple cache that stores the result of a callback function
    """
    def __init__(self):
        """
        Constructor
        """
        self.memory = {}

    def request(self, callback, request):
        """
        Request a value from the cache. If the value is not in the cache, it will be calculated by the callback function
        Args:
            callback (function): The callback function that will be called to calculate the value
            request (any): The request that will be passed to the callback function

        Returns (any): The value that was requested

        Examples:
            >>> def add_five(x):
            ...     return x + 5
            >>> store_cache = StoreCache()
            >>> store_cache.request(callback, 5)  # Call the callback function
            10
            >>> store_cache.request(callback, 5)  # Return the value from the cache, without calling the callback function
            10
        """
        if request in self.memory:
            return self.memory[request]
        else:
            result = callback(request)
            self.memory[request] = result
            return result

