import curses
import time

from cursers import App

KEY_ESC = 27

if __name__ == "__main__":
    with App() as app:
        y = 0
        x = 0

        title = "Movement Control"
        app.stdscr.addstr(0, (29 - len(title)) // 2, title, curses.A_BOLD)

        app.stdscr.addstr(3, 2, f"X coordinate: {x:12}")
        app.stdscr.addstr(4, 2, f"Y coordinate: {y:12}")

        app.stdscr.addstr(7, 2, "Keyboard Controls:", curses.A_BOLD)
        app.stdscr.addstr(8, 4, "W/S - Move up/down")
        app.stdscr.addstr(9, 4, "A/D - Move left/right")
        app.stdscr.addstr(10, 4, "ESC - Exit app", curses.A_BOLD)

        while True:
            key = app.stdscr.getch()
            if key == KEY_ESC:
                break
            elif key == ord("w"):
                y -= 1
            elif key == ord("s"):
                y += 1
            elif key == ord("a"):
                x -= 1
            elif key == ord("d"):
                x += 1

            app.stdscr.addstr(3, 16, f"{x:12}")
            app.stdscr.addstr(4, 16, f"{y:12}")

            time.sleep(1 / 30)
