import curses
from typing import Self


class App:
    def __enter__(self) -> Self:
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(True)  # noqa: FBT003
        curses.curs_set(0)
        curses.noecho()
        return self

    def __exit__(self, *args: object) -> None:
        curses.endwin()


__all__ = ["App"]
