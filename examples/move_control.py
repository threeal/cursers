import cursers

KEY_ESC = 27


class MoveControlApp(cursers.App):
    def __init__(self) -> None:
        super().__init__()
        self.y = 0
        self.x = 0

    def on_enter(self) -> None:
        title = "Movement Control"
        self.draw_text(0, (29 - len(title)) // 2, title, bold=True)

        self.draw_text(3, 2, f"X coordinate: {self.x:12}")
        self.draw_text(4, 2, f"Y coordinate: {self.y:12}")

        self.draw_text(7, 2, "Keyboard Controls:", bold=True)
        self.draw_text(8, 4, "W/S - Move up/down")
        self.draw_text(9, 4, "A/D - Move left/right")
        self.draw_text(10, 4, "ESC - Exit app", bold=True)

    def on_update(self) -> None:
        key = self.stdscr.getch()
        if key == KEY_ESC:
            self.exit()
            return
        if key == ord("w"):
            self.y -= 1
        elif key == ord("s"):
            self.y += 1
        elif key == ord("a"):
            self.x -= 1
        elif key == ord("d"):
            self.x += 1

        self.draw_text(3, 16, f"{self.x:12}")
        self.draw_text(4, 16, f"{self.y:12}")


if __name__ == "__main__":
    with MoveControlApp() as app:
        while app.is_running():
            app.update()
