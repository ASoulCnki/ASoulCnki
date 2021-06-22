import json


def get_reply_data(file_path):
    with open(file_path, 'r') as load_f:
        load_dict = json.load(load_f)
        # result = []
        # for reply_dict in load_dict:
        #     result.append(reply_dict["content"])
        return load_dict


if __name__ == '__main__':
    replies = get_reply_data("data/select_from_reply_where_length_content_10000.json")
    for reply in replies:
        print(reply)
