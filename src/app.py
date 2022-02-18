import os
import sys
from src.db.cdb import CardDatabase
from src.cv.pic_index import PicIndex
from src.cv.utils import image_sim, load_img_and_resize
from src.ui.screen_capturer import ScreenCapturer
from src.ui.window import Window


class App:
    THUMBNAIL_SIZE = (32, 47)
    CARD_SHOW_SIZE = (250, 365)
    SC_SIM_THRESHOLD = 0.99
    PIC_SIM_THRESHOLD = 0.8

    def __init__(self):
        ygo_window_name = 'masterduel'

        cdb_path = os.path.join('res', 'cards.cdb')
        cache_file = os.path.join('res', 'pic_feats.cache')
        pic_dir = os.path.join('res', 'picture', 'card')
        font_file = os.path.join('res', 'font', 'msyh.ttc')

        self.cdb = CardDatabase(cdb_path)
        self.pi = PicIndex(cache_file, pic_dir)
        self.sc = ScreenCapturer(ygo_window_name)
        self.window = Window(font_file)

    def mainloop(self):
        last_thumbnail = None
        while True:
            self.window.wait(milliseconds=500)
            img = self.sc.capture()
            thumbnail = img.copy()
            thumbnail.thumbnail(App.THUMBNAIL_SIZE)
            thumbnail.convert('L')
            if last_thumbnail:
                sim = image_sim(thumbnail, last_thumbnail)
                if sim > App.SC_SIM_THRESHOLD:
                    continue
            cid, score = self.pi.query_img(img)
            if score > App.PIC_SIM_THRESHOLD:
                card = self.cdb.query_by_cid(cid)
                text = card.get_text()
                print('\n\n', file=sys.stderr)
                print(score, text, file=sys.stderr)
                card_img_path = os.path.join('res', 'picture', 'card', cid+'.jpg')
                card_img = load_img_and_resize(card_img_path, App.CARD_SHOW_SIZE)
                self.window.show_image(card_img)
                self.window.show_text(text)
            last_thumbnail = thumbnail


if __name__ == '__main__':
    app = App()
    app.mainloop()
