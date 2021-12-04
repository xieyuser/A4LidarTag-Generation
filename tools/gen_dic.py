#! /usr/bin/env python
import numpy as np
import random
import click
import json

def random01():
    return random.choice([0, 0, 1])

def mat2num(pattern):
    np_num1 = np.hstack([pattern[0], pattern[1]])
    np_num2 = np.hstack([pattern[2], pattern[3]])

    binary_num1 = ''.join(list(map(str, np_num1.tolist())))
    binary_num2 = ''.join(list(map(str, np_num2.tolist())))
    num1 = int(binary_num1, 2)
    num2 = int(binary_num2, 2)
    return [num1, num2], binary_num1 + binary_num2

def generater(decode_cell_count):
    re = np.zeros(16, dtype=np.int)
    re[0]=re[3]=re[12]=re[15]=1
    pos_1 = random.sample([1,2,4,5,6,7,8,9,10,11,13,14], decode_cell_count)
    re[np.array(pos_1)] = 1
    return re

def ham_dis(c, binary):
    return sum(el1 != el2 for el1, el2 in zip(c, binary))

def cal_ham_dis(c, binary, d):
    return ham_dis(c, binary) < d

def judge_dis(existd_code, binary, d):
    for c in existd_code:
        if cal_ham_dis(c, binary, d):
            return False
    return True

def sche(d, i):
    return d - i//100


@click.command()
@click.option('--num', default=20)
@click.option('--decode-pixel-count', default=3)
@click.option('--dic-path', default='config/dict.json')
@click.option('--dic-decode-save-path', default='config/redict.json')
def main(num, decode_pixel_count, dic_path, dic_decode_save_path):
    dic = {}
    min_hamming_dis_first = 100
    all_binary_code = []
    count = 0
    i = 0
    while True:
        min_hamming_dis = sche(min_hamming_dis_first, i)
        i += 1
        print(min_hamming_dis)
        assert min_hamming_dis > 0, 'no enough ids'
        if count >= num:
            break
        lis = []
        code = generater(decode_pixel_count)
        code = np.array(code).reshape(4, 4)
        nums, binary_1 = mat2num(code)
        if not judge_dis(all_binary_code, binary_1, min_hamming_dis):
            continue
        lis.append([nums, binary_1])

        code = np.rot90(code)
        nums, binary_2 = mat2num(code)
        if not judge_dis(all_binary_code, binary_2, min_hamming_dis):
            continue
        lis.append([nums, binary_2])

        code = np.rot90(code)
        nums, binary_3 = mat2num(code)
        if not judge_dis(all_binary_code, binary_3, min_hamming_dis):
            continue
        lis.append([nums, binary_3])

        code = np.rot90(code)
        nums, binary_4 = mat2num(code)
        if not judge_dis(all_binary_code, binary_4, min_hamming_dis):
            continue
        all_binary_code += [binary_1, binary_2, binary_3, binary_4]
        lis.append([nums, binary_4])
        print(lis)
        dic.update({
            count:lis,
        })
        count += 1

    with open(dic_path, 'w') as f:
        json.dump(dic, f)

    dic_decode = {}
    for k,v in dic.items():
        for i, c in enumerate(v):
            dic_decode.update({
                "#".join(list(map(str, c[0])) + [str(i)] + [c[1]]) : str(k)
            })

    with open(dic_decode_save_path, 'w') as f:
        json.dump(dic_decode, f)


if __name__ == '__main__':
    main()


