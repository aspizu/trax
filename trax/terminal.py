import sys
import termios
from shutil import get_terminal_size

# fmt: off
reset  = "\033[0m"
bold   = "\033[1m"
italic = "\033[3m"
ulined = "\033[4m"

black  = "\033[30m"
red    = "\033[31m"
green  = "\033[32m"
yellow = "\033[33m"
blue   = "\033[34m"
pink   = "\033[35m"
cyan   = "\033[36m"
white  = "\033[37m"

bgblack  = "\033[40m"
bgred    = "\033[41m"
bggreen  = "\033[42m"
bgyellow = "\033[43m"
bgblue   = "\033[44m"
bgpink   = "\033[45m"
bgcyan   = "\033[46m"
bgwhite  = "\033[47m"

brblack  = "\033[90m"
brred    = "\033[91m"
brgreen  = "\033[92m"
bryellow = "\033[93m"
brblue   = "\033[94m"
brpink   = "\033[95m"
brcyan   = "\033[96m"
brwhite  = "\033[97m"

brbgblack  = "\033[100m"
brbgred    = "\033[101m"
brbggreen  = "\033[102m"
brbgyellow = "\033[103m"
brbgblue   = "\033[104m"
brbgpink   = "\033[105m"
brbgcyan   = "\033[106m"
brbgwhite  = "\033[107m"
# fmt: on

width, height = get_terminal_size()


def f():
    sys.stdout.flush()


def w(s: str):
    sys.stdout.write(s)


def wf(s: str):
    w(s)
    f()


def m(x: int, y: int):
    w(f"\u001b[{y+1};{x+1}H")


def h():
    m(0, 0)


def c():
    w("\u001b[2J\u001b[3J")


def chf():
    c()
    h()
    f()


def init():
    """References:
    https://www.man7.org/linux/man-pages/man3/termios.3.html
    https://man7.org/linux/man-pages/man1/stty.1.html
    https://github.com/python/cpython/blob/3.10/Lib/tty.py"""
    IFLAG = 0
    LFLAG = 3
    CC = 6
    mode = termios.tcgetattr(sys.stdin)
    mode[LFLAG] = mode[LFLAG] & ~(termios.ECHO | termios.ICANON)
    mode[IFLAG] = mode[IFLAG] & ~(termios.IXON | termios.IXOFF)
    mode[CC][termios.VMIN] = 1
    mode[CC][termios.VTIME] = 0
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, mode)


def read():
    n = sys.stdin.read(1)
    if ord(n) == 17:
        return "CTRL+Q"
    if ord(n) == 127:
        return "BACKSPACE"
    if ord(n) == 19:
        return "CTRL+S"
    if ord(n) == 27:
        n = sys.stdin.read(1)
        if ord(n) == 91:
            n = sys.stdin.read(1)
            if ord(n) == 72:
                return "HOME"
            if ord(n) == 70:
                return "END"
            if ord(n) == 65:
                return "UP"
            if ord(n) == 66:
                return "DOWN"
            if ord(n) == 68:
                return "LEFT"
            if ord(n) == 67:
                return "RIGHT"

    wf(repr(ord(n)) + ";")
    return n


__all__ = ["init", "width", "height", "f", "w", "wf", "m", "h", "c", "chf", "read"]
