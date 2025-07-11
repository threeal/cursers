"""Test suite for the cursers package."""

import curses
import threading
import time
from unittest.mock import Mock, patch

import pytest

from cursers import App, Screen, Thread, ThreadedApp


class TestThread:

    def test_init(self):
        thread = Thread()

        assert thread._thread is None

    def test_enter_context(self):
        thread = Thread()

        with patch("cursers.threading.Thread") as mock_thread_class:
            mock_thread_instance = Mock()
            mock_thread_class.return_value = mock_thread_instance

            result = thread.__enter__()

            mock_thread_class.assert_called_once_with(target=thread.run)
            mock_thread_instance.start.assert_called_once()
            assert result is thread
            assert thread._thread == mock_thread_instance

    def test_exit_context_with_thread(self):
        thread = Thread()
        mock_thread_instance = Mock()
        thread._thread = mock_thread_instance

        thread.__exit__(None, None, None)

        mock_thread_instance.join.assert_called_once()
        assert thread._thread is None

    def test_exit_context_without_thread(self):
        thread = Thread()
        thread._thread = None

        # Should not raise any exception
        thread.__exit__(None, None, None)

        assert thread._thread is None

    def test_run_default(self):
        thread = Thread()

        # Should not raise any exception
        thread.run()
