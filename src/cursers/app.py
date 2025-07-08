"""Core application classes for the cursers library."""

import curses
import time
from typing import Self

from .thread import Thread


class App:
    """The main application class that provides a context manager for curses apps.

    The App class handles curses initialization and cleanup, provides an update loop
    with configurable FPS, and offers lifecycle hooks for application logic.
    """

    def __init__(self, *, fps: int = 30) -> None:
        """Initialize the application.

        Args:
            fps: Target frames per second (default: 30).

        """
        self._stdscr = None
        self._fps = fps
        self._is_running = False

    def __enter__(self) -> Self:
        """Enter the application context and initialize curses.

        Returns:
            The application instance.

        """
        self._stdscr = curses.initscr()
        self._stdscr.nodelay(True)  # noqa: FBT003
        curses.curs_set(0)
        curses.noecho()

        self.on_enter()
        self._is_running = True

        return self

    def __exit__(self, *args: object) -> None:
        """Exit the application context and cleanup curses.

        Args:
            *args: Exception information (unused).

        """
        self._is_running = False
        self.on_exit()
        curses.endwin()

    def is_running(self) -> bool:
        """Check if the application is currently running.

        Returns:
            True if the application is running, False otherwise.

        """
        return self._is_running

    def update(self) -> None:
        """Update the application state and handle input.

        Call this method in your main loop to update the application state
        and handle keyboard input.
        """
        if self._is_running:
            key = self._stdscr.getch()
            self.on_update(key)
            self._stdscr.refresh()
            time.sleep(1 / self._fps)

    def exit(self) -> None:
        """Signal the application to exit.

        Sets the running state to False, which will cause the application
        to exit on the next update cycle.
        """
        self._is_running = False

    def on_enter(self) -> None:
        """Handle entering the application context.

        Override this method in your subclass to perform initialization
        tasks when the application starts.
        """

    def on_update(self, key: int) -> None:
        """Handle frame updates with key input.

        Override this method in your subclass to handle keyboard input
        and update your application state.

        Args:
            key: Key code from getch(), or -1 if no key pressed.

        """

    def on_exit(self) -> None:
        """Handle exiting the application context.

        Override this method in your subclass to perform cleanup
        tasks when the application exits.
        """

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


class ThreadedApp(App, Thread):
    """Extends App to run the update loop in a separate thread.

    This class combines the functionality of App and Thread to provide
    a threaded application that runs the update loop automatically in
    the background.
    """

    def __init__(self, *, fps: int = 30) -> None:
        """Initialize the threaded application.

        Args:
            fps: Target frames per second (default: 30).

        """
        App.__init__(self, fps=fps)
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
        App.__exit__(self)
        Thread.__exit__(self)

    def run(self) -> None:
        """Run the update loop in the thread.

        This method is called automatically when the thread starts.
        It continuously calls update() while the application is running.
        """
        while self.is_running():
            self.update()


__all__ = ["App", "ThreadedApp"]
