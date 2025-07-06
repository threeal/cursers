import time

from cursers import App

KEY_ESC = 27

if __name__ == "__main__":
    with App() as app:
        y = 0
        x = 0

        title = "Movement Control"
        app.draw_text(0, (29 - len(title)) // 2, title, bold=True)

        app.draw_text(3, 2, f"X coordinate: {x:12}")
        app.draw_text(4, 2, f"Y coordinate: {y:12}")

        app.draw_text(7, 2, "Keyboard Controls:", bold=True)
        app.draw_text(8, 4, "W/S - Move up/down")
        app.draw_text(9, 4, "A/D - Move left/right")
        app.draw_text(10, 4, "ESC - Exit app", bold=True)

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

            app.draw_text(3, 16, f"{x:12}")
            app.draw_text(4, 16, f"{y:12}")

            time.sleep(1 / 30)
