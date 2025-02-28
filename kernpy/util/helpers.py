import warnings
import functools


def deprecated(reason: str):
    """
    Decorator to mark a function or class as deprecated.
    
    Args:
        reason (str): The reason why the function/class is deprecated.
    
    Example:
        @deprecated("Use new_function instead.")
        def old_function():
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"'{func.__name__}' is deprecated: {reason}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def deprecated_argument(arg_name: str, reason: str):
    """
    Decorator to mark a specific argument as deprecated.
    
    Args:
        arg_name (str): The deprecated argument name.
        reason (str): The reason why the argument is deprecated.
    
    Example:
        @deprecated_argument("old_param", "Use 'new_param' instead.")
        def my_function(new_param, old_param=None):
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if arg_name in kwargs:
                warnings.warn(
                    f"Argument '{arg_name}' in '{func.__name__}' is deprecated: {reason}",
                    category=DeprecationWarning,
                    stacklevel=2,
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

