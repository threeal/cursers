import curses
import time
from typing import Self


class App:
    def __init__(self, *, fps: int = 30) -> None:
        self._fps = fps
        self._is_running = False

    def __enter__(self) -> Self:
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(True)  # noqa: FBT003
        curses.curs_set(0)
        curses.noecho()

        self.on_enter()
        self._is_running = True

        return self

    def __exit__(self, *args: object) -> None:
        self._is_running = False
        self.on_exit()
        curses.endwin()

    def is_running(self) -> bool:
        return self._is_running

    def update(self) -> None:
        if self._is_running:
            key = self.stdscr.getch()
            self.on_update(key)
            self.stdscr.refresh()
            time.sleep(1 / self._fps)

    def exit(self) -> None:
        self._is_running = False

    def on_enter(self) -> None:
        pass

    def on_update(self, key: int) -> None:
        pass

    def on_exit(self) -> None:
        pass

    def draw_text(self, y: int, x: int, text: str, *, bold: bool = False) -> None:
        attr = curses.A_BOLD if bold else curses.A_NORMAL
        self.stdscr.addstr(y, x, text, attr)


__all__ = ["App"]
