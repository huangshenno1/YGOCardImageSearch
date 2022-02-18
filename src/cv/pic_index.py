import os
import sys
import numpy as np
import pickle
from tqdm import tqdm

from .pic_feat import PicFeat


class PicIndex:
    def __init__(self, feats_cache_file=None, card_pic_dir=None):
        assert (feats_cache_file is not None) or (card_pic_dir is not None)
        self.pic_feat = PicFeat()
        self.init_index(feats_cache_file, card_pic_dir)

    def init_index(self, feats_cache_file=None, card_pic_dir=None):
        if feats_cache_file is not None:
            if os.path.exists(feats_cache_file):
                with open(feats_cache_file, 'rb') as f:
                    self.cids, self.feats = pickle.load(f)
                return
            else:
                print('[WARNING] feats cache file not exist:', feats_cache_file, file=sys.stderr)
        self.cids, pic_paths = self.load_pictures(card_pic_dir)
        self.feats = self.gen_feats(pic_paths)
        with open(feats_cache_file, 'wb') as f:
            pickle.dump([self.cids, self.feats], f)

    def load_pictures(self, card_pic_dir):
        cids = []
        pic_paths = []
        for pic_file in os.listdir(card_pic_dir):
            cid = os.path.splitext(pic_file)[0]
            pic_path = os.path.join(card_pic_dir, pic_file)
            cids.append(cid)
            pic_paths.append(pic_path)
        return cids, pic_paths

    def gen_feats(self, pic_paths):
        feats = []
        for pic_path in tqdm(pic_paths):
            feat = self.pic_feat.process_file(pic_path)
            feats.append(feat)
        feats = np.array(feats)
        return feats

    def query_img_file(self, img_path):
        feat = self.pic_feat.process_file(img_path)
        return self.query_feat(feat)

    def query_img(self, img):
        feat = self.pic_feat.process(img)
        return self.query_feat(feat)

    def query_feat(self, feat):
        scores = np.dot(feat, self.feats.T)
        ranked_id = np.argsort(scores)[::-1][0]
        ranked_score = scores[ranked_id]
        ranked_cid = self.cids[ranked_id]
        return ranked_cid, ranked_score
