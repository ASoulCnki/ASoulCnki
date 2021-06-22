# 初始化，将论文的名称/片段/Simhash保存到数据库
import time
import prepare_data
from simhashalgo import SimhashAlgo, get_simhash_part, hamming_distance

indices = []

kv_store = {
    "part_1": {},
    "part_2": {},
    "part_3": {},
    "part_4": {},
}


def get_or_create_list(source, key):
    if key not in source:
        source[key] = []
    return source[key]


def get_simhash_list(part, simhash_part):
    if part == 1:
        return get_or_create_list(kv_store["part_1"], str(simhash_part))
    elif part == 2:
        return get_or_create_list(kv_store["part_2"], str(simhash_part))
    elif part == 3:
        return get_or_create_list(kv_store["part_3"], str(simhash_part))
    elif part == 4:
        return get_or_create_list(kv_store["part_4"], str(simhash_part))


def build_simhash_index(s_hash, rpid):
    simhash_part_one = get_simhash_part(s_hash, 1)
    simhash_part_two = get_simhash_part(s_hash, 2)
    simhash_part_three = get_simhash_part(s_hash, 3)
    simhash_part_four = get_simhash_part(s_hash, 4)

    get_simhash_list(1, simhash_part_one).append((s_hash, rpid))
    get_simhash_list(2, simhash_part_two).append((s_hash, rpid))
    get_simhash_list(3, simhash_part_three).append((s_hash, rpid))
    get_simhash_list(4, simhash_part_four).append((s_hash, rpid))


replies_dict = {}


def init_simhash_database():
    print("init() starting …")
    replies = prepare_data.get_reply_data("data/select_from_reply_where_length_content.json")
    clock_0 = time.time()
    counter = 0
    for reply in replies:
        counter += 1
        if counter % 10 == 0:
            print(counter)
        rpid = reply["rpid"]
        replies_dict[str(rpid)] = reply
        s_hash = SimhashAlgo(reply['content'], 64)
        if s_hash == 0:
            continue
        build_simhash_index(s_hash.hash, rpid)

    clock_1 = time.time()
    print("【init time】【", clock_1 - clock_0, '】')
    print("init() executed!")


def check(text, n):
    text_simhash = SimhashAlgo(text)

    # the four part can be executed using multi-thread
    simhash_part_one = get_simhash_part(text_simhash.hash, 1)
    simhash_part_two = get_simhash_part(text_simhash.hash, 2)
    simhash_part_three = get_simhash_part(text_simhash.hash, 3)
    simhash_part_four = get_simhash_part(text_simhash.hash, 4)

    check_set = get_simhash_list(1, simhash_part_one) + \
                get_simhash_list(2, simhash_part_two) + \
                get_simhash_list(3, simhash_part_three) + \
                get_simhash_list(4, simhash_part_four)

    result = {}

    for t in check_set:
        s_hash = t[0]
        rpid = t[1]
        h_distance = hamming_distance(s_hash, text_simhash.hash, 64)
        if h_distance <= 3:
            result[str(rpid)] = (rpid, (1 - h_distance / 64), text_simhash.similarity(s_hash))
    sorted_list = sorted(result.items(), key=lambda item: item[1], reverse=True)
    return sorted_list[:n]
