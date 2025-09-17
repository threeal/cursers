import curses
import threading
import time
from unittest.mock import Mock, patch

import pytest

from cursers import App, Screen, Thread, ThreadedApp


class TestApp:

    def test_init_defaults(self):
        app = App()

        assert app._fps == 30
        assert app._keypad is False
        assert app._is_exit_requested is False
        assert app._screen is None

    def test_init_custom_values(self):
        app = App(fps=60, keypad=True)

        assert app._fps == 60
        assert app._keypad is True
        assert app._is_exit_requested is False
        assert app._screen is None

    @patch("cursers.curses")
    @patch("cursers.Screen")
    def test_enter_context(self, mock_screen_class, mock_curses):
        mock_screen = Mock()
        mock_screen_class.return_value = mock_screen

        app = App(fps=60, keypad=True)

        with patch.object(app, 'on_enter') as mock_on_enter:
            result = app.__enter__()

            mock_screen_class.assert_called_once_with(keypad=True)
            mock_curses.curs_set.assert_called_once_with(0)
            mock_curses.noecho.assert_called_once()
            mock_on_enter.assert_called_once_with(mock_screen)
            assert result is app
            assert app._screen == mock_screen
            assert app._App__is_exit_requested is False

    @patch("cursers.curses")
    @patch("cursers.Screen")
    def test_exit_context(self, mock_screen_class, mock_curses):
        mock_screen = Mock()
        mock_screen_class.return_value = mock_screen

        app = App()
        app.__enter__()

        with patch.object(app, 'on_exit') as mock_on_exit:
            app.__exit__(None, None, None)

            mock_on_exit.assert_called_once_with(mock_screen)
            mock_curses.endwin.assert_called_once()

    def test_request_exit(self):
        app = App()
        app._App__is_exit_requested = False

        app.request_exit()

        assert app._App__is_exit_requested is True

    def test_is_exit_requested(self):
        app = App()
        app._App__is_exit_requested = False

        assert app.is_exit_requested() is False

        app._App__is_exit_requested = True
        assert app.is_exit_requested() is True

    @patch("cursers.time.sleep")
    def test_update(self, mock_sleep):
        app = App(fps=60)
        mock_screen = Mock()
        app._screen = mock_screen

        with patch.object(app, 'on_update') as mock_on_update:
            app.update()

            mock_on_update.assert_called_once_with(mock_screen)
            mock_screen.refresh.assert_called_once()
            mock_sleep.assert_called_once_with(1/60)

    def test_on_enter_default(self):
        app = App()
        mock_screen = Mock()

        # Should not raise any exception
        app.on_enter(mock_screen)

    def test_on_update_default(self):
        app = App()
        mock_screen = Mock()

        # Should not raise any exception
        app.on_update(mock_screen)

    def test_on_exit_default(self):
        app = App()
        mock_screen = Mock()

        # Should not raise any exception
        app.on_exit(mock_screen)
