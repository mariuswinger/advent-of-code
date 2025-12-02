import numpy as np


def rolling_window(a: np.ndarray, size: int) -> np.ndarray:
    """Return a rolling window view into a numpy array."""
    shape = a.shape[:-1] + (a.shape[-1] - size + 1, size)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)
