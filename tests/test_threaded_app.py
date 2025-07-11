"""Test suite for the cursers package."""

import curses
import threading
import time
from unittest.mock import Mock, patch

import pytest

from cursers import App, Screen, Thread, ThreadedApp


class TestThreadedApp:
    """Test the ThreadedApp class."""

    def test_init_defaults(self):
        """Test ThreadedApp initialization with default values."""
        app = ThreadedApp()

        assert app._fps == 30
        assert app._keypad is False
        assert app._is_exit_requested is False
        assert app._screen is None
        assert app._thread is None

    def test_init_custom_values(self):
        """Test ThreadedApp initialization with custom values."""
        app = ThreadedApp(fps=60, keypad=True)

        assert app._fps == 60
        assert app._keypad is True
        assert app._is_exit_requested is False
        assert app._screen is None
        assert app._thread is None

    @patch("cursers.curses")
    @patch("cursers.Screen")
    @patch("cursers.threading.Thread")
    def test_enter_context(self, mock_thread_class, mock_screen_class, mock_curses):
        """Test entering the threaded application context."""
        mock_screen = Mock()
        mock_screen_class.return_value = mock_screen
        mock_thread_instance = Mock()
        mock_thread_class.return_value = mock_thread_instance

        app = ThreadedApp(fps=60, keypad=True)

        with patch.object(app, 'on_enter') as mock_on_enter:
            result = app.__enter__()

            # Check App.__enter__ was called
            mock_screen_class.assert_called_once_with(keypad=True)
            mock_curses.curs_set.assert_called_once_with(0)
            mock_curses.noecho.assert_called_once()
            mock_on_enter.assert_called_once_with(mock_screen)

            # Check Thread.__enter__ was called
            mock_thread_class.assert_called_once_with(target=app.run)
            mock_thread_instance.start.assert_called_once()

            assert result is app
            assert app._screen == mock_screen
            assert app._thread == mock_thread_instance

    @patch("cursers.curses")
    @patch("cursers.Screen")
    @patch("cursers.threading.Thread")
    def test_exit_context(self, mock_thread_class, mock_screen_class, mock_curses):
        """Test exiting the threaded application context."""
        mock_screen = Mock()
        mock_screen_class.return_value = mock_screen
        mock_thread_instance = Mock()
        mock_thread_class.return_value = mock_thread_instance

        app = ThreadedApp()
        app.__enter__()

        with patch.object(app, 'on_exit') as mock_on_exit:
            app.__exit__(None, None, None)

            # Check App.__exit__ was called
            mock_on_exit.assert_called_once_with(mock_screen)
            mock_curses.endwin.assert_called_once()

            # Check Thread.__exit__ was called
            mock_thread_instance.join.assert_called_once()
            assert app._thread is None

    @patch("cursers.time.sleep")
    def test_run_loop(self, mock_sleep):
        """Test the run method loop."""
        app = ThreadedApp()
        mock_screen = Mock()
        app._screen = mock_screen

        # Mock is_exit_requested to return False twice, then True
        app._App__is_exit_requested = False
        call_count = 0

        def mock_is_exit_requested():
            nonlocal call_count
            call_count += 1
            return call_count > 2

        with patch.object(app, 'is_exit_requested', side_effect=mock_is_exit_requested):
            with patch.object(app, 'on_update') as mock_on_update:
                app.run()

                # Should call on_update twice before exiting
                assert mock_on_update.call_count == 2
                assert mock_screen.refresh.call_count == 2
                assert mock_sleep.call_count == 2

    def test_run_exit_immediately(self):
        """Test the run method when exit is requested immediately."""
        app = ThreadedApp()
        app._App__is_exit_requested = True

        with patch.object(app, 'update') as mock_update:
            app.run()

            # Should not call update when exit is requested
            mock_update.assert_not_called()
