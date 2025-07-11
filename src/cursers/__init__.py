"""Cursers: A minimal threaded wrapper for Python curses.

A minimal threaded wrapper for Python curses that simplifies terminal user interface
development with built-in threading support and lifecycle management.

Features:
    - Simple context manager for curses applications
    - Built-in update loop with configurable FPS
    - Lifecycle hooks for application logic
    - Threaded version for running updates in separate thread
    - Text drawing utilities with styling support
"""

import curses
import threading
import time
from typing import Self


class Screen:
    """Low-level screen management for curses applications.

    Provides a wrapper around curses screen operations including initialization,
    input handling, and display management.
    """

    def __init__(self, *, init: bool = True, keypad: bool = False) -> None:
        """Initialize the screen.

        Args:
            init: Whether to initialize the screen immediately (default: True).
            keypad: Whether to enable arrow keys and function keys (default: False).

        """
        self._stdscr = None
        self._keypad = keypad

        if init:
            self.init()

    def __del__(self) -> None:
        self.cleanup()

    def __enter__(self) -> Self:
        self.init()
        return self

    def __exit__(self, *args: object) -> None:
        self.cleanup()

    def init(self) -> None:
        if self._stdscr is None:
            self._stdscr = curses.initscr()
            self._stdscr.nodelay(True)  # noqa: FBT003

            if self._keypad:
                self._stdscr.keypad(True)  # noqa: FBT003

    def cleanup(self) -> None:
        if self._stdscr is not None:
            self._stdscr = None

    def get_key(self) -> int:
        """Get the next key from the input buffer.

        Returns:
            The key code, or -1 if no key is available.

        """
        return self._stdscr.getch()

    def refresh(self) -> None:
        """Refresh the screen to display pending changes."""
        self._stdscr.refresh()

    def draw_text(
        self, y: int, x: int, text: str, *, bold: bool = False, underline: bool = False
    ) -> None:
        """Draw text at the specified position.

        Args:
            y: Row position.
            x: Column position.
            text: Text to draw.
            bold: Whether to draw in bold style (default: False).
            underline: Whether to draw in underline style (default: False).

        """
        attr = curses.A_NORMAL
        if bold:
            attr |= curses.A_BOLD
        if underline:
            attr |= curses.A_UNDERLINE

        self._stdscr.addstr(y, x, text, attr)


class App:
    """The main application class that provides a context manager for curses apps.

    The App class handles curses initialization and cleanup, provides an update loop
    with configurable FPS, and offers lifecycle hooks for application logic.
    """

    def __init__(self, *, fps: int = 30, keypad: bool = False) -> None:
        """Initialize the application.

        Args:
            fps: Target frames per second (default: 30).
            keypad: Whether to enable arrow keys (default: False).

        """
        self._screen = None
        self._fps = fps
        self._keypad = keypad
        self._is_exit_requested = False

    def __enter__(self) -> Self:
        """Enter the application context and initialize curses.

        Returns:
            The application instance.

        """
        if self._screen is None:
            self._screen = Screen(keypad=self._keypad)
            curses.curs_set(0)
            curses.noecho()

            self._is_exit_requested = False
            self.on_enter(self._screen)

        return self

    def __exit__(self, *args: object) -> None:
        """Exit the application context and cleanup curses.

        Args:
            *args: Exception information (unused).

        """
        if self._screen is not None:
            self.on_exit(self._screen)
            self._screen.cleanup()
            curses.endwin()

    def request_exit(self) -> None:
        """Request the application to exit.

        Sets the exit flag to True, which will cause the application
        to exit on the next update cycle.
        """
        self._is_exit_requested = True

    def is_exit_requested(self) -> bool:
        """Check if an exit has been requested.

        Returns:
            True if exit has been requested, False otherwise.

        """
        return self._is_exit_requested

    def update(self) -> None:
        """Update the application state and handle input.

        Call this method in your main loop to update the application state
        and handle keyboard input.
        """
        self.on_update(self._screen)
        self._screen.refresh()
        time.sleep(1 / self._fps)

    def on_enter(self, screen: Screen) -> None:
        """Handle entering the application context.

        Override this method in your subclass to perform initialization
        tasks when the application starts.

        Args:
            screen: The Screen instance for drawing and input handling.

        """

    def on_update(self, screen: Screen) -> None:
        """Handle frame updates.

        Override this method in your subclass to handle keyboard input
        and update your application state.

        Args:
            screen: The Screen instance for drawing and input handling.

        """

    def on_exit(self, screen: Screen) -> None:
        """Handle exiting the application context.

        Override this method in your subclass to perform cleanup
        tasks when the application exits.

        Args:
            screen: The Screen instance for drawing and input handling.

        """


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


class ThreadedApp(App, Thread):
    """Extends App to run the update loop in a separate thread.

    This class combines the functionality of App and Thread to provide
    a threaded application that runs the update loop automatically in
    the background.
    """

    def __init__(self, *, fps: int = 30, keypad: bool = False) -> None:
        """Initialize the threaded application.

        Args:
            fps: Target frames per second (default: 30).
            keypad: Whether to enable arrow keys (default: False).

        """
        App.__init__(self, fps=fps, keypad=keypad)
        Thread.__init__(self)

    def __enter__(self) -> Self:
        """Enter the application context and start the thread.

        Returns:
            The threaded application instance.

        """
        App.__enter__(self)
        Thread.__enter__(self)
        return self

    def __exit__(self, *args: object) -> None:
        """Exit the application context and join the thread.

        Args:
            *args: Exception information (unused).

        """
        Thread.__exit__(self)
        App.__exit__(self)

    def run(self) -> None:
        """Run the update loop in the thread.

        This method is called automatically when the thread starts.
        It continuously calls update() while the application is running.
        """
        while not self.is_exit_requested():
            self.update()


__all__ = ["App", "Screen", "Thread", "ThreadedApp"]
