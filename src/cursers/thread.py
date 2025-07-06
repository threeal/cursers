import threading
from typing import Self


class Thread:
    def __init__(self) -> None:
        self._thread = None

    def __enter__(self) -> Self:
        self._thread = threading.Thread(target=self.run)
        self._thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def run(self) -> None:
        pass


__all__ = ["Thread"]
