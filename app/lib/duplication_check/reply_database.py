import json
import pickle
from typing import Optional, Any
from readerwriterlock import rwlock

from app.lib.duplication_check.hash import hash
from app.lib.duplication_check.reply_model import Reply


class ReplyDatabase:

    def __init__(self):
        self.reply_dict = {}
        self.hash_dict = {}
        self.min_time = (1 << 32) - 1
        self.max_time = 0
        self.max_rpid = 0
        self.lock = rwlock.RWLockFair()

    def __getstate__(self):
        """Return state values to be pickled."""
        return self.reply_dict, self.hash_dict, self.min_time, self.max_time, self.max_rpid

    def __setstate__(self, state):
        """Restore state from the unpickled state values."""
        self.reply_dict, self.hash_dict, self.min_time, self.max_time, self.max_rpid = state
        self.lock = rwlock.RWLockFair()

    @staticmethod
    def load_from_json(file_path):
        with open(file_path, 'r', encoding="utf-8") as load_f:
            json_data = json.load(load_f)
            db = ReplyDatabase()
            for reply in json_data:
                r = Reply()
                r.rpid = reply["rpid"]
                r.content = reply["content"]
                r.ctime = reply["ctime"]
                r.like_num = reply["like_num"]
                r.oid = reply["oid"]
                r.type_id = reply["type_id"]
                r.m_name = reply["m_name"]
                r.mid = reply["mid"]
                r.dynamic_id = reply["dynamic_id"]
                db.add_reply_data(r)
            return db

    @staticmethod
    def load_from_image(path) -> Optional[Any]:
        try:
            with open(path, "rb") as f:
                db = pickle.load(f)
            return db
        except Exception:
            return ReplyDatabase()

    def dump_to_image(self, path):
        with self.lock.gen_rlock():
            with open(path, "wb") as f:
                pickle.dump(self, f)

    def reset(self):
        with self.lock.gen_wlock():
            self.reply_dict = {}
            self.hash_dict = {}
            self.min_time = (1 << 32) - 1
            self.max_time = 0

    def add_reply_data(self, r):

        if r.rpid in self.reply_dict:
            return

        self.reply_dict[r.rpid] = r

        if r.ctime > self.max_time:
            self.max_time = r.ctime

        if r.ctime < self.min_time:
            self.min_time = r.ctime

        if r.rpid > self.max_rpid:
            self.max_rpid = r.rpid

        text_hash_list = hash(r.content)
        for text_hash in text_hash_list:
            if text_hash not in self.hash_dict:
                self.hash_dict[text_hash] = []
            self.hash_dict[text_hash].append(r.rpid)

    def get_reply(self, rpid) -> Optional[Reply]:
        with self.lock.gen_rlock():
            if rpid in self.reply_dict:
                return self.reply_dict[rpid]
            else:
                return None

    def search_hash(self, text_hash) -> Optional[Any]:
        with self.lock.gen_rlock():
            if text_hash in self.hash_dict:
                return self.hash_dict[text_hash]
            else:
                return None
