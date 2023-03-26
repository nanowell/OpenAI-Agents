from ctypes import *

# C struct definitions

class MOUSEINPUT(Structure):
    _fields_ = (("dx",          c_long),
                ("dy",          c_long),
                ("mouseData",   c_ulong),
                ("dwFlags",     c_ulong),
                ("time",        c_ulong),
                ("dwExtraInfo", POINTER(c_ulong)))

class KEYBDINPUT(Structure):
    _fields_ = (("wVk",         c_ushort),
                ("wScan",       c_ushort),
                ("dwFlags",     c_ulong),
                ("time",        c_ulong),
                ("dwExtraInfo", POINTER(c_ulong)))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(Structure):
    _fields_ = (("uMsg",    c_ulong),
                ("wParamL", c_ushort),
                ("wParamH", c_ushort))

class INPUT(Structure):
    class _INPUT(Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   c_ulong),
                ("_input", _INPUT))

LPINPUT = POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise WinError(get_last_error())
    return args

user32 = WinDLL('user32', use_last_error=True)
user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (c_uint, # nInputs
                             LPINPUT,       # pInputs
                             c_int)  # cbSize

# Functions

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0


def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, byref(x), sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, byref(x), sizeof(x))

def GetScreenPosition(hWnd):
    hWndDC = user32.GetWindowDC(hWnd)
    mPos = POINT(0, 0)
    user32.GetCursorPos(byref(mPos))
    user32.ScreenToClient(hWnd, byref(mPos))
    return (mPos.x, mPos.y)

def ClickPosition(hWnd, x, y):
    lParam = (y << 16) | x
    user32.PostMessageW(hWnd, WM_LBUTTONDOWN, MK_LBUTTON, lParam)
    user32.PostMessageW(hWnd, WM_LBUTTONUP, MK_LBUTTON, lParam)

def ClickButton(hWnd, button):
    btnPos = button.GetPosition()
    ClickPosition(hWnd, btnPos[0], btnPos[1])
    
