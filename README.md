# Cursers

A minimal threaded wrapper for [Python curses](https://docs.python.org/3/howto/curses.html) that simplifies terminal user interface development with built-in threading support and lifecycle management.

## Features

- Simple context manager for curses applications
- Built-in update loop with configurable FPS
- Lifecycle hooks for application logic
- Threaded version for running updates in separate thread
- Text drawing utilities with styling support

## Installation

```bash
pip install cursers
```

## Quick Start

### Basic App

```python
import cursers


class MyApp(cursers.App):
    # Called when entering the application context
    def on_enter(self):
        self.draw_text(0, 0, "Hello, World!", bold=True)

    # Called each frame with the current key input
    def on_update(self, key):
        if key == 27:  # ESC key
            self.exit()


# Run the application
with MyApp() as app:
    while app.is_running():
        app.update()
```

### Threaded App

```python
import cursers
import time


class MyThreadedApp(cursers.ThreadedApp):
    def on_enter(self):
        self.draw_text(0, 0, "Running in background thread!")

    def on_update(self, key):
        if key == 27:  # ESC key
            self.exit()


# Run in background thread
with MyThreadedApp() as app:
    while app.is_running():
        time.sleep(0.1)  # Do other work
```

## API Reference

### App Class

The main application class that provides a context manager for curses applications.

#### Constructor

```python
App(fps=30)
```

- `fps`: Target frames per second (default: 30)

#### Methods

- `is_running()`: Returns `True` if the application is running
- `update()`: Updates the application state and handles input (call in main loop)
- `exit()`: Signals the application to exit
- `draw_text(y, x, text, bold=False, underline=False)`: Draw text at position

#### Lifecycle Hooks

Override these methods in your subclass:

- `on_enter()`: Called when entering the context
- `on_update(key)`: Called every frame with key input (-1 if no key pressed)
- `on_exit()`: Called when exiting the context

### ThreadedApp Class

Extends `App` to run the update loop in a separate thread.

```python
class MyThreadedApp(cursers.ThreadedApp):
    def on_update(self, key):
        # Handle input and drawing
        pass


with MyThreadedApp() as app:
    # Update loop runs automatically in background thread
    while app.is_running():
        # Main thread is free for other tasks
        time.sleep(0.1)
```

### Thread Class

Basic threading context manager for custom threading needs.

```python
class MyThread(cursers.Thread):
    def run(self):
        # Your thread code here
        pass


with MyThread() as thread:
    # Thread runs automatically
    pass
```

## Examples

Check out the [`examples/`](./examples/) directory for complete working examples:

- [`examples/move_control.py`](./examples/move_control.py) - Basic movement control with keyboard input
- [`examples/move_control_gravity.py`](./examples/move_control_gravity.py) - Threaded application with gravity simulation

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/threeal/cursers.git
cd cursers

# Install development dependencies
uv sync

# Install Git hooks
uv run lefthook install
```

### Code Quality

```bash
# Format code
dprint fmt

# Run linter
uv run ruff check --fix
```

## License

This project is licensed under the terms of the [MIT License](./LICENSE).

Copyright © 2025 [Alfi Maulana](https://github.com/threeal)
