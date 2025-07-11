import cursers


class MoveControlApp(cursers.App):
    def __init__(self) -> None:
        super().__init__(keypad=True)
        self.y = 0
        self.x = 0

    def on_enter(self, screen: cursers.Screen) -> None:
        screen.draw_text(0, 7, "Movement Control", bold=True, underline=True)

        screen.draw_text(3, 2, f"X coordinate: {self.x:12}")
        screen.draw_text(4, 2, f"Y coordinate: {self.y:12}")

        screen.draw_text(7, 2, "Keyboard Controls:", bold=True)
        screen.draw_text(8, 4, "W/S - Move up/down")
        screen.draw_text(9, 4, "A/D - Move left/right")
        screen.draw_text(10, 4, "ESC - Exit app", bold=True)

    def on_update(self, screen: cursers.Screen) -> None:
        key = screen.get_key()
        match chr(key) if key != -1 else None:
            case "\x1b":  # ESC
                self.exit()
                return
            case "w" | "W":
                self.y -= 1
            case "s" | "S":
                self.y += 1
            case "a" | "A":
                self.x -= 1
            case "d" | "D":
                self.x += 1

        screen.draw_text(3, 16, f"{self.x:12}")
        screen.draw_text(4, 16, f"{self.y:12}")


if __name__ == "__main__":
    with MoveControlApp() as app:
        while app.is_running():
            app.update()
