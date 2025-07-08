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

from .app import App, ThreadedApp
from .thread import Thread

__all__ = ["App", "Thread", "ThreadedApp"]
