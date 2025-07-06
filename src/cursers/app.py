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

    def draw_text(self, y: int, x: int, text: str, *, bold: bool = False) -> None:
        attr = curses.A_BOLD if bold else curses.A_NORMAL
        self.stdscr.addstr(y, x, text, attr)


__all__ = ["App"]
