"""Threading utilities for the cursers library."""

import threading
from typing import Self


class Thread:
    """Context manager that provides threading functionality."""

    def __init__(self) -> None:
        """Initialize the thread manager."""
        self._thread = None

    def __enter__(self) -> Self:
        """Enter the context and start the thread."""
        self._thread = threading.Thread(target=self.run)
        self._thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        """Exit the context and join the thread."""
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def run(self) -> None:
        """Execute the target method for the thread. Override in subclasses."""


__all__ = ["Thread"]
