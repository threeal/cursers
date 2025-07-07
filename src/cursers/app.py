"""Core application classes for the cursers library."""

import curses
import time
from typing import Self

from .thread import Thread


class App:
    """Context manager that provides curses application framework.

    The App class handles curses initialization and cleanup,
    provides an update loop with configurable FPS, and offers
    lifecycle hooks for application logic.
    """

    def __init__(self, *, fps: int = 30) -> None:
        """Initialize the application.

        Args:
            fps: Target frames per second for the update loop.

        """
        self._stdscr = None
        self._fps = fps
        self._is_running = False

    def __enter__(self) -> Self:
        """Enter the application context and initialize curses."""
        self._stdscr = curses.initscr()
        self._stdscr.nodelay(True)  # noqa: FBT003
        curses.curs_set(0)
        curses.noecho()

        self.on_enter()
        self._is_running = True

        return self

    def __exit__(self, *args: object) -> None:
        """Exit the application context and cleanup curses."""
        self._is_running = False
        self.on_exit()
        curses.endwin()

    def is_running(self) -> bool:
        """Check if the application is currently running."""
        return self._is_running

    def update(self) -> None:
        """Update the application state and handle input."""
        if self._is_running:
            key = self._stdscr.getch()
            self.on_update(key)
            self._stdscr.refresh()
            time.sleep(1 / self._fps)

    def exit(self) -> None:
        """Signal the application to exit."""
        self._is_running = False

    def on_enter(self) -> None:
        """Handle application entry into the context."""

    def on_update(self, key: int) -> None:
        """Handle frame updates with the current key input.

        Args:
            key: Key code from getch(), or -1 if no key pressed.

        """

    def on_exit(self) -> None:
        """Handle application exit from the context."""

    def draw_text(
        self, y: int, x: int, text: str, *, bold: bool = False, underline: bool = False
    ) -> None:
        """Draw text to the screen at the specified position.

        Args:
            y: Row position.
            x: Column position.
            text: Text to draw.
            bold: Whether to draw in bold style.
            underline: Whether to draw in underline style.

        """
        attr = curses.A_NORMAL
        if bold:
            attr |= curses.A_BOLD
        if underline:
            attr |= curses.A_UNDERLINE

        self._stdscr.addstr(y, x, text, attr)


class ThreadedApp(App, Thread):
    """Threaded version of App that runs the update loop in a separate thread."""

    def __init__(self, *, fps: int = 30) -> None:
        """Initialize the threaded application.

        Args:
            fps: Target frames per second for the update loop.

        """
        App.__init__(self, fps=fps)
        Thread.__init__(self)

    def __enter__(self) -> Self:
        """Enter the application context and start the thread."""
        App.__enter__(self)
        Thread.__enter__(self)
        return self

    def __exit__(self, *args: object) -> None:
        """Exit the application context and join the thread."""
        App.__exit__(self)
        Thread.__exit__(self)

    def run(self) -> None:
        """Run the update loop in the thread."""
        while self.is_running():
            self.update()


__all__ = ["App", "ThreadedApp"]
