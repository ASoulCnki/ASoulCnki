import os


class Cookie:
    @staticmethod
    def list_to_dict(res: list) -> dict:
        res_dict = dict()
        for i in res:
            res_dict[i['name']] = i['value']
        return res_dict

    @staticmethod
    def dict_to_str(res: dict) -> str:
        res_str = ''
        for i, j in res.items():
            res_str += '{}={}; '.format(i, j)
        return res_str[:-2]

    @staticmethod
    def str_to_dict(res: str) -> dict:
        res_dict = dict()
        for i in res.split('; '):
            k, v = i.split('=', 1)
            res_dict[k] = v
        return res_dict

    @classmethod
    def list_to_str(cls, res: list) -> str:
        tmp = cls.list_to_dict(res)
        return cls.dict_to_str(tmp)

    @staticmethod
    def save_to_disk(cookies: str, filename: str):
        with open(filename, "w") as f:
            f.write(cookies)

    @staticmethod
    def load_from_disk(filename: str):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return f.read()
        raise Exception('文件不存在')


if __name__ == '__main__':
    cookies_dict = {
        'a': 'b',
        'c': 'd'
    }
    cookies_str = Cookie.dict_to_str(cookies_dict)
    cookies_dict_tmp = Cookie.str_to_dict(cookies_str)
    assert cookies_dict == cookies_dict_tmp
    print(1)
