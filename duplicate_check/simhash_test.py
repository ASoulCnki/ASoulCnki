from duplicate_check import check, init_simhash_database, replies_dict


def test():
    init_simhash_database()
    text = """
我真的想A-SOUL想得要发疯了。我躺在床上会想A-SOUL，我洗澡会想A-SOUL，我出门会想A-SOUL，我走路会想A-SOUL，我坐车会想A-SOUL，我工作会想A-SOUL，我玩手机会想A-SOUL，我盯着路边的A-SOUL看,我盯着马路对面的A-SOUL立牌看,我盯着地铁里的A-SOUL看，我盯着网上的A-SOUL看，我盯着朋友圈别人合照里的A-SOUL看，我每时每刻眼睛都直直地盯着A-SOUL看，像一台雷达一样扫视经过我身边的每一个A-SOUL成员，我真的觉得自己像中邪了一样，我对A-SOUL的念想似乎都是病态的了，我好孤独啊!真的好孤独啊!乐华那么多成员为什么没有一个是属于我的。你知道吗?每到深夜，我的舌头滚烫滚烫，我发病了我要疯狂舔A-SOUL，我要狠狠舔A-SOUL，我的钱包受不了了。???",
    """
    text2 = """
    我真的想嘉然想得要发疯了。我躺在床上会想嘉然，我洗澡会想嘉然，我出门会想嘉然，我走路会想嘉然，我坐车会想嘉然，我工作会想嘉然，我玩手机会想嘉然，我盯着路边的嘉然看,我盯着马路对面的嘉然立牌看,我盯着地铁里的嘉然看，我盯着网上的嘉然看，我盯着朋友圈别人合照里的嘉然看，我每时每刻眼睛都直直地盯着嘉然看，像一台雷达一样扫视经过我身边的每一个嘉然成员，我真的觉得自己像中邪了一样，我对嘉然的念想似乎都是病态的了，我好孤独啊!真的好孤独啊!乐华那么多成员为什么没有一个是属于我的。你知道吗?每到深夜，我的舌头滚烫滚烫，我发病了我要疯狂舔嘉然，我要狠狠舔嘉然，我的钱包受不了了。???",
        """

    text3 = """
    我真的想贝拉想得要发疯了。我躺在床上会想贝拉，我洗澡会想贝拉，我出门会想贝拉，我走路会想贝拉，我坐车会想贝拉，我工作会想贝拉，我玩手机会想贝拉，我盯着路边的贝拉看,我盯着马路对面的贝拉立牌看,我盯着地铁里的贝拉看，我盯着网上的贝拉看，我盯着朋友圈别人合照里的贝拉看，我每时每刻眼睛都直直地盯着贝拉看，像一台雷达一样扫视经过我身边的每一个贝拉成员，我真的觉得自己像中邪了一样，我对贝拉的念想似乎都是病态的了，我好孤独啊!真的好孤独啊!乐华那么多成员为什么没有一个是属于我的。你知道吗?每到深夜，我的舌头滚烫滚烫，我发病了我要疯狂舔贝拉，我要狠狠舔贝拉，我的钱包受不了了。???",
        """
    check_and_print_result(text)
    check_and_print_result(text2)
    check_and_print_result(text3)


def check_and_print_result(text):
    print("checking text: {}".format(text))
    result = check(text, 5)
    for r in result:
        print("content: {} han: {} similarity: {}".format(replies_dict[str(r[0])]["content"], r[1][1], r[1][2]))
    print("result number: {}\n".format(len(result)))


if __name__ == "__main__":
    test()
