#!/usr/bin/env python3

import itertools
import json

# Creates an image-mapping.json file from a message dump file

msgs_file = 'messages.txt'
delimiter = '<delimiter>'

def main():
    with open(msgs_file, "r") as f:
        msgs = f.read()
        msg_list = msgs.split(delimiter)
    mapping = build_msg_index(msg_list)
    with open('image-mapping.json', 'w') as f:
        json.dump(mapping, f)

def build_msg_index(msg_list):
    label_mapping = translation_dict()
    msg_index = {}

    def find_matches(msg_i, words, key, labels):
        for w in words:
            for l in labels:
                if w.startswith(l):
                    if key not in msg_index:
                        msg_index[key] = []
                    msg_index[key].append(msg_i)
                    return

    for msg_i, msg in enumerate(msg_list):
        if msg_i % 1000 == 0:
            print(f'Indexing message #{msg_i} out of {len(msg_list)}')
        for key, labels in label_mapping.items():
            find_matches(msg_i, msg.split(' '), key, labels)

    return msg_index

def translation_dict():
    with open('label-dict.json', 'r') as f:
        label_dict = json.load(f)
    return {k: expand_label(v.lower()) for k, v in label_dict.items()}

phrase_substitutions = {
    'экран окна': ['жалюз'],
    'французский хлеб': ['батон', 'булк'],
    'бабушка смит': ['яблок', 'яблоч'],
    'фотокопировальное устройство': ['копирк', 'печат'],
    'карманный компьютер': ['смартфон', 'телефон'],
    'портативный компьютер': ['ноут', 'комп'],
    'СиДи плэйер': ['плеер', 'музык'],
    'блуждающий огонек': ['halloween', 'хэллоуин', 'тыкв']
}

word_substitutions = {
    'веб-сайт': ['веб', 'сайт'],
    'телевидение': ['теле'],
    'фуфайка': ['кофт', 'джемп'],
    'клубника': ['клубник'],
    'гранатовый': ['гранат'],
    'пластина': ['тарелк', 'блюд', 'еда', 'кушат'],
    'чизбургер': ['бургер', 'макд'],
    'школьный': ['школ'],
    'тедди': ['плюш', 'мишк'],
    'петух': ['петух', 'петуш'],
    'hammerhead': ['акул', 'рыб'],
    'конвертируемый': ['кабриолет', 'машин', 'авто', 'дорога'],
    'электрогитара': ['гитара', 'рок', 'метал'],
    'hoopskirt': ['плать'],
    'overskirt': ['плать'],
    'ipod': ['яблоко', 'ipod', 'apple', 'джобс'],
    'почтовый': ['почт'],
    'легче': ['зажигалка'],
    'футеровка': ['корабл'],
    'объектива': ['фото', 'объектив', 'зеркалк'],
    'jinrikisha': ['карет'],
    'люка': ['люк', 'водопровод', 'канализ'],
    'комикс': ['аниме', 'манга'],
}

def expand_label(label):
    if ' ' in label:
        if label in phrase_substitutions:
            return phrase_substitutions[label]
        return list(itertools.chain.from_iterable(
            expand_label(l) for l in label.split(' ')
            if l != 'на' and l != 'для' and l != 'от' and l != 'с' and l != 'в'
        ))

    if label in word_substitutions:
        return word_substitutions[label]

    if n.endswith('ы'):
        return [n[:-1]]
    if n.endswith('ок'):
        return [n[:-2]]
    if n.endswith('нский') or n.endswith('нская'):
        return [n[:-5]]
    if n.endswith('ский') or n.endswith('ская') or n.endswith('ское') or n.endswith('ские'):
        return [n[:-4]]
    if n.endswith('ный') or n.endswith('ная') or n.endswith('ное') or n.endswith('ные'):
        return [n[:-3]]
    if n.endswith('ая'):
        return [n[:-2]]

    return [n]

main()
