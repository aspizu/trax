import subprocess
from pathlib import Path

import terminal as T


class Cursor:
    def __init__(self, buffer: "Buffer") -> None:
        self.x = 0
        self.y = 0
        self.buffer = buffer

    def right(self) -> None:
        if (self.x + 1) <= len(self.buffer.buffer[self.y]):
            self.x += 1
        self.clip()

    def left(self) -> None:
        if 0 <= (self.x - 1):
            self.x -= 1
        self.clip()

    def up(self) -> None:
        if 0 <= (self.y - 1):
            self.y -= 1
        self.clip()
        self.scroll()

    def down(self) -> None:
        if (self.y + 1) < len(self.buffer.buffer):
            self.y += 1
        self.clip()
        self.scroll()

    def clip(self) -> None:
        if self.x > len(self.buffer.buffer[self.y]):
            self.x = len(self.buffer.buffer[self.y])
        if self.y >= len(self.buffer.buffer):
            self.y = len(self.buffer.buffer) - 1

    def scroll(self) -> None:
        if self.y >= self.buffer.scroll + self.buffer.height:
            self.buffer.scroll += 1
        elif self.y < self.buffer.scroll:
            self.buffer.scroll -= 1


class Buffer:
    def __init__(self, file: Path) -> None:
        self.height: int = T.height - 2
        self.file = file
        self.buffer: list[list[str]] = [[]]
        self.scroll: int = 0
        self.cursor = Cursor(self)
        self.open()

        T.init()
        while True:
            self.draw()
            key = T.read()
            if key == "CTRL+Q":
                T.chf()
                break
            if key == "CTRL+S":
                self.save()
            elif key == "RIGHT":
                self.cursor.right()
            elif key == "LEFT":
                self.cursor.left()
            elif key == "UP":
                self.cursor.up()
            elif key == "DOWN":
                self.cursor.down()
            elif key == "BACKSPACE":
                self.delete()
            elif key.isprintable() or key == "\n":
                self.insert(key)

    def open(self) -> None:
        self.buffer = [list(line) for line in self.file.read_text().split("\n")][:-1]

    def save(self) -> None:
        with self.file.open("w") as file:
            file.write("\n".join("".join(line) for line in self.buffer))
            file.write("\n")
        if self.file.suffix == ".py":
            process = subprocess.run(["black", self.file.as_posix()])
            if process.returncode == 0:
                self.open()

    def draw(self) -> None:
        T.chf()
        for i in range(self.scroll, min(len(self.buffer), self.scroll + self.height)):
            T.w(f"{T.brblack}{i+1: 4} {T.reset}")
            T.w("".join(self.buffer[i]))
            T.w("\n")
        T.w(f"{T.brblue}{self.file}{T.reset}")
        T.m(5 + self.cursor.x, self.cursor.y - self.scroll)
        T.f()

    def insert(self, char: str) -> None:
        if char == "\n":
            self.buffer.insert(self.cursor.y + 1, [])
            self.buffer[self.cursor.y + 1].extend(
                self.buffer[self.cursor.y][self.cursor.x :]
            )
            self.buffer[self.cursor.y] = self.buffer[self.cursor.y][: self.cursor.x]
            self.cursor.down()
            self.cursor.x = 0
            return
        self.buffer[self.cursor.y].insert(self.cursor.x, char)
        self.cursor.right()

    def delete(self) -> None:
        if self.cursor.x == 0:
            if self.cursor.y > 0:
                x = len(self.buffer[self.cursor.y - 1])
                self.buffer[self.cursor.y - 1].extend(self.buffer[self.cursor.y])
                self.buffer.pop(self.cursor.y)
                self.cursor.up()
                self.cursor.x = x
            return
        self.buffer[self.cursor.y].pop(self.cursor.x - 1)
        self.cursor.left()
