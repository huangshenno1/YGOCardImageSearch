

class Card:
    def __init__(self, cid, name, desc):
        self.cid = cid
        self.name = name
        self.desc = desc

    def get_text(self):
        text = (self.name + '\n======\n' + self.desc).replace('\r', '')
        return text
