from PIL import ImageGrab
import win32gui
import time


class ScreenCapturer:
    WINDOW_SIZE_OFFSETS_MAPPNIG = {
        (1616, 939): (44, 204, -1436, -533)
    }

    def __init__(self, window_title):
        self.hwnd = self.get_window(window_title)

    def get_window(self, window_title):
        hwnd = win32gui.FindWindow(None, window_title)
        return hwnd

    def adjust_offsets(self, rect):
        weight, height = rect[2]-rect[0], rect[3]-rect[1]
        while (weight, height) not in ScreenCapturer.WINDOW_SIZE_OFFSETS_MAPPNIG:
            time.sleep(1)
        # assert (weight, height) in ScreenCapturer.WINDOW_SIZE_OFFSETS_MAPPNIG, f'不支持的窗口大小！{weight}x{height}'
        return (rect[i]+ScreenCapturer.WINDOW_SIZE_OFFSETS_MAPPNIG[(weight, height)][i] for i in range(4))

    def capture(self):
        rect = win32gui.GetWindowRect(self.hwnd)
        rect = self.adjust_offsets(rect)
        img = ImageGrab.grab(bbox=rect)
        return img
