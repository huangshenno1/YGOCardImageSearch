import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class Window:
    def __init__(self, font_file):
        self.img_window_name = 'Image'
        cv2.namedWindow(self.img_window_name)
        cv2.resizeWindow(self.img_window_name, 200, 200)

        self.text_window_name = 'Text'
        cv2.namedWindow(self.text_window_name)
        cv2.resizeWindow(self.text_window_name, 200, 200)

        self.font_file = font_file

    def show_image(self, img):
        if type(img) != np.ndarray:
            img = np.array(img)
        cv2.imshow(self.img_window_name, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    def show_text(self, text, text_size=16, text_color=(0, 0, 0)):
        text = self.auto_break_line(text)
        img = Image.fromarray(np.full((500, 280), 255, np.int8)).convert('RGB')
        draw = ImageDraw.Draw(img)
        font_style = ImageFont.truetype(self.font_file, text_size, encoding='gbk')
        draw.text((10, 10), text, font=font_style, fill=text_color, direction=None)
        img = np.array(img)
        cv2.imshow(self.text_window_name, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    def auto_break_line(self, text, line_char_limit=16):
        new_text = ''
        char_count = 0
        for c in text:
            if c == '\n':
                char_count = 0
                if not new_text.endswith(c):
                    new_text += c
            else:
                char_count += 1
                new_text += c
            if char_count >= line_char_limit:
                new_text += '\n'
                char_count = 0
        return new_text

    def wait(self, milliseconds=500):
        if cv2.waitKey(milliseconds) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit()