import jieba
import jieba.analyse


def hamming_distance(hash_a, hash_b, hashbits=128):
    x = (hash_a ^ hash_b) & ((1 << hashbits) - 1)
    tot = 0
    while x:
        tot += 1
        x &= x - 1
    return tot


class SimhashAlgo:
    def __init__(self, tokens='', hashbits=128):
        self.hashbits = hashbits
        self.hash = self.simhash(tokens)

    def __str__(self):
        return str(self.hash)

    def __float__(self):
        return float(self.hash)

    def simhash(self, tokens):
        # Returns a Charikar simhash with appropriate bitlength
        v = [0] * self.hashbits
        keyWord = jieba.analyse.extract_tags(
            tokens, topK=20, withWeight=True, allowPOS=())  # 根据 TD-IDF 提取关键词，并按照权重排序
        if len(keyWord) < 6:  # 少于5个词放弃这个句子
            return 0
        for feature, weight in keyWord:  # 对关键词进行 hash
            weight = int(weight * 20)
            feature = self._string_hash(feature)
            for i in range(self.hashbits):
                bitmask = 1 << i
                # print(t,bitmask, t & bitmask)
                if int(feature) & bitmask:
                    v[i] += weight  # 查看当前bit位是否为1，是的话则将该位+1
                else:
                    v[i] += -weight  # 否则得话，该位减1

        fingerprint = 0
        for i in range(self.hashbits):
            if v[i] >= 0:
                fingerprint += 1 << i
        # 整个文档的fingerprint为最终各个位大于等于0的位的和
        return fingerprint

    def _string_hash(self, v):
        # A variable-length version of Python's builtin hash
        if v == "":
            return 0
        else:
            x = ord(v[0]) << 7
            m = 1000003
            mask = 2 ** self.hashbits - 1
            for c in v:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(v)
            if x == -1:
                x = -2
            return x

    def hamming_distance(self, other_hash):
        x = (self.hash ^ other_hash.hash) & ((1 << self.hashbits) - 1)
        tot = 0
        while x:
            tot += 1
            x &= x - 1
        return tot

    def similarity(self, other_hash):
        a = float(self.hash)
        b = float(other_hash)
        if a > b:
            return b / a
        return a / b


PART_BITS = 16
PART_MAX = -1 ^ (-1 << PART_BITS)

PART_ONE_MASK = PART_MAX
PART_TWO_MASK = PART_MAX << (PART_BITS * 1)
PART_THREE_MASK = PART_MAX << (PART_BITS * 2)


def get_simhash_part(hash_val, part):
    if part < 1 or part > 4:
        raise ValueError("wrong input")
    if part == 1:
        return hash_val & PART_ONE_MASK
    elif part == 2:
        return (hash_val & PART_TWO_MASK) >> (PART_BITS * 1)
    elif part == 3:
        return (hash_val & PART_THREE_MASK) >> (PART_BITS * 2)
    elif part == 4:
        return hash_val >> (PART_BITS * 3)


if __name__ == '__main__':
    s_hash = (2 << 64) - 10000

    print('%x' % s_hash)
    print('%x' % get_simhash_part(s_hash, 4))
    print('%x' % get_simhash_part(s_hash, 3))
    print('%x' % get_simhash_part(s_hash, 2))
    print('%x' % get_simhash_part(s_hash, 1))

    pass
