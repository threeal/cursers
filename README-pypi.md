# Cursers

A minimal threaded wrapper for [Python curses](https://docs.python.org/3/howto/curses.html) that simplifies terminal user interface development with built-in threading support and lifecycle management.

## Features

- Simple context manager for curses applications
- Built-in update loop with configurable FPS
- Lifecycle hooks for application logic
- Threaded version for running updates in separate thread
- Text drawing utilities with styling support

## Quick Start

### Basic App

```python
import cursers


class MyApp(cursers.App):
    # Called when entering the application context
    def on_enter(self, screen):
        screen.draw_text(0, 0, "Hello, World!", bold=True)

    # Called each frame with screen object for input/drawing
    def on_update(self, screen):
        key = screen.get_key()
        if key == 27:  # ESC key
            self.request_exit()


# Run the application
with MyApp() as app:
    while not app.is_exit_requested():
        app.update()
```

### Threaded App

```python
import cursers
import time


class MyThreadedApp(cursers.ThreadedApp):
    def on_enter(self, screen):
        screen.draw_text(0, 0, "Running in background thread!")

    def on_update(self, screen):
        key = screen.get_key()
        if key == 27:  # ESC key
            self.request_exit()


# Run in background thread
with MyThreadedApp() as app:
    while not app.is_exit_requested():
        time.sleep(0.1)  # Do other work
```

## API Reference

For complete API documentation, visit the [project documentation](https://threeal.github.io/cursers/).

### App Class

The main application class that provides a context manager for curses applications.

#### Constructor

```python
App(fps=30, keypad=False)
```

- `fps`: Target frames per second (default: 30)
- `keypad`: Whether to enable arrow keys and function keys (default: False)

#### Methods

- `request_exit()`: Requests the application to exit
- `is_exit_requested()`: Returns `True` if exit has been requested
- `update()`: Updates the application state and handles input (call in main loop)

#### Lifecycle Hooks

Override these methods in your subclass:

- `on_enter(screen)`: Called when entering the context
- `on_update(screen)`: Called every frame
- `on_exit(screen)`: Called when exiting the context

### ThreadedApp Class

Extends `App` to run the update loop in a separate thread.

```python
class MyThreadedApp(cursers.ThreadedApp):
    def on_update(self, screen):
        # Handle input and drawing
        key = screen.get_key()
        pass


with MyThreadedApp() as app:
    # Update loop runs automatically in background thread
    while not app.is_exit_requested():
        # Main thread is free for other tasks
        time.sleep(0.1)
```

### Screen Class

Low-level screen management for curses applications. Provides direct access to curses screen operations.

#### Methods

- `get_key()`: Returns the next key code from input buffer (-1 if no key available)
- `refresh()`: Refreshes the screen to display pending changes
- `draw_text(y, x, text, bold=False, underline=False)`: Draw styled text at position

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
