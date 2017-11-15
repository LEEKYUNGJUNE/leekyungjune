#!/usr/bin/python
# -*- coding: utf-8 -*-


def get_tree_result(sentences, original_token=False):
    final_list = list()
    word_list = list()
    depen_list = list()
    for sent in sentences:

        if original_token:
            for word in sent["word"]:
                word_list.append(unicode(word["text"]))
        sent_list = list()
        for morp in sent["morp_eval"]:
            tokens = morp["result"].replace("+", "\t").replace("\t/SW", "+/SW").split("\t")
            item_list = list()
            for token in tokens:
                item = token.split("/")
                if len(item) > 2:
                    item = ["/"] + [item[-1]]
                t = "/".join([item[0], item[1].lower()])
                if type(t) == unicode:
                    item_list.append(t)
                else:
                    item_list.append(unicode(t, "utf-8"))
            sent_list.append(item_list)
        for depen in sent["dependency"]:
            depen_list.append(depen)
        final_list.append(sent_list)
        q = sent["text"]
    if original_token:
        return final_list, word_list, depen_list
    else:
        return q, final_list, depen_list


def map_original_idx(morph, original):
    flatten_morph = list()
    for s in morph:
        flatten_morph += s
    map_dic = dict()
    m_idx = 0
    o_idx = 0
    for m, o in zip(flatten_morph, original):
        max_o_idx = o_idx + len(o)
        if len(m) == 1:
            map_dic[m_idx] = (o_idx, o_idx + len(o))
            m_idx += 1
            o_idx += len(o) + 1
        else:
            pass_list = list()  # splitted morph ex. 나서+었
            start_from = 0
            fail = False  # beforehand
            for each_m in m:
                splitted_m = each_m.rsplit("/", 1)[0]
                location = o.find(splitted_m, start_from)
                if location >= 0:
                    if fail:
                        o_idx += location
                        fail = False
                    map_dic[m_idx] = (o_idx, o_idx + len(splitted_m))
                    o_idx += len(splitted_m)
                    start_from = location
                else:
                    pass_list.append((m_idx, m, start_from + o_idx, o))
                    fail = True
                m_idx += 1
            pass_list_tmp = pass_list
            if len(pass_list) > 0:  # if there is a splitted morphs
                for pass_item in pass_list:
                    # m_idx, m, start_position
                    backward_until = 1
                    while m_idx > (pass_item[0] + backward_until):
                        try:
                            # 만약 그 다음 것도 찾지 못하면 하나 더 뒤로 감
                            map_dic[pass_item[0]] = (pass_item[2], map_dic[pass_item[0] + backward_until][0])
                            pass_list_tmp.remove(pass_item)
                            break
                        except KeyError:
                            backward_until += 1
            if len(pass_list_tmp) > 0:
                for pass_item in pass_list_tmp:
                    map_dic[pass_item[0]] = (pass_item[2], max_o_idx)
            o_idx = max_o_idx
            o_idx += 1  # space
    # for </s> tag
    map_dic[m_idx] = (o_idx - 1, o_idx - 1)
    return map_dic
