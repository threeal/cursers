"""Threading utilities for the cursers library."""

import threading
from typing import Self


class Thread:
    """Basic threading context manager for custom threading needs.

    Provides a context manager interface for creating and managing threads.
    Override the run() method to define the thread's behavior.
    """

    def __init__(self) -> None:
        """Initialize the thread manager.

        Creates a new thread manager instance with no active thread.
        """
        self._thread = None

    def __enter__(self) -> Self:
        """Enter the context and start the thread.

        Returns:
            The thread instance.

        """
        self._thread = threading.Thread(target=self.run)
        self._thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        """Exit the context and join the thread.

        Args:
            *args: Exception information (unused).

        """
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def run(self) -> None:
        """Execute the target method for the thread.

        Override this method in subclasses to define the thread's behavior.
        This method is called automatically when the thread starts.
        """


__all__ = ["Thread"]
