import curses
import threading
import time
from unittest.mock import Mock, patch

import pytest

from cursers import App, Screen, Thread, ThreadedApp

@pytest.fixture()
def mock_stdscr():
    with patch("cursers.curses.initscr") as mock_initscr:
        mock_stdscr = Mock()
        mock_initscr.return_value = mock_stdscr
        yield mock_stdscr

class TestScreen:
    def test_init(self, mock_stdscr):
        screen = Screen()

        assert screen._stdscr == mock_stdscr
        mock_stdscr.nodelay.assert_called_once_with(True)
        mock_stdscr.keypad.assert_not_called()

    def test_init_with_keypad(self, mock_stdscr):
        screen = Screen(keypad=True)

        assert screen._stdscr == mock_stdscr
        mock_stdscr.keypad.assert_called_once_with(True)

    def test_get_key(self, mock_stdscr):
        mock_stdscr.getch.return_value = 65
        screen = Screen()

        assert screen.get_key() == 65

    def test_refresh(self, mock_stdscr):
        screen = Screen()
        screen.refresh()

        mock_stdscr.refresh.assert_called_once()

    class TestDrawText:
        def test_normal(self, mock_stdscr):
            screen = Screen()
            screen.draw_text(5, 10, "Hello")

            mock_stdscr.addstr.assert_called_once_with(5, 10, "Hello", curses.A_NORMAL)

        def test_bold(self, mock_stdscr):
            screen = Screen()
            screen.draw_text(5, 10, "Hello", bold=True)

            mock_stdscr.addstr.assert_called_once_with(5, 10, "Hello", curses.A_BOLD)

        def test_underline(self, mock_stdscr):
            screen = Screen()
            screen.draw_text(5, 10, "Hello", underline=True)

            mock_stdscr.addstr.assert_called_once_with(5, 10, "Hello", curses.A_UNDERLINE)

        def test_bold_underline(self, mock_stdscr):
            screen = Screen()
            screen.draw_text(5, 10, "Hello", bold=True, underline=True)

            mock_stdscr.addstr.assert_called_once_with(5, 10, "Hello", curses.A_BOLD | curses.A_UNDERLINE)
