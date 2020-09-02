import json

the_file = open("data.json")
file_data = json.load(the_file)
g_trie = file_data['trie']
sentences = file_data['sentences']


def replace_score(query, index, offset):
    reduced_score_dict = {0: 5, 1: 4, 2: 3, 3: 2}
    reduced_score = reduced_score_dict[index+offset] if index+offset in reduced_score_dict.keys() else 1
    return (index + len(query))*2 - reduced_score


def delete_or_add_score(query, index, offset):
    reduced_score_dict = {0: 10, 1: 8, 2: 6, 3: 4}
    reduced_score = reduced_score_dict[index+offset] if index+offset in reduced_score_dict.keys() else 2
    return (index + len(query))*2 - reduced_score


def get_ids_with_offset(ids_dict):
    return {k: ids_dict[k]['offset'] for k in ids_dict.keys()}


def by_sub(query, trie):
    tmp_trie = trie
    for letter in query:
        if letter in tmp_trie.keys():
            tmp_trie = tmp_trie[letter]
        else:
            return {}
    return get_ids_with_offset(tmp_trie['sentences_ids'])


def merge_by_score(replace_results,delete_results,add_results):
    res = replace_results
    for key, value in delete_results.items():
        if key not in res:
            res[key] = value
        elif res[key] < delete_results[key]:
            res[key] = delete_results[key]
    for key, value in add_results.items():
        if key not in res:
            res[key] = value
        elif res[key] < add_results[key]:
            res[key] = add_results[key]
    return res


def get_delete_or_add_score(results, query, index):
    if results == {}:
        return {}
    results_score = {}
    for result in results.keys():
        results_score[result] = delete_or_add_score(query, index, results[result])
    return results_score


def get_replece_score(replace_results,query, index):
    if replace_results == {}:
        return {}
    replace_results_score = {}
    for result in replace_results.keys():
        replace_results_score[result] = replace_score(query, index, replace_results[result])
    return replace_results_score


def by_replace(query, trie, key,index):
    return get_replece_score(by_sub(query, trie[key]),query, index)


def by_delete(query, trie,key,index):
        return get_delete_or_add_score(by_sub(query[1:], trie[key]),query, index)


def by_add(query, trie,index):
    if len(query) == 1:
        return {}
    return get_delete_or_add_score(by_sub(query[1:], trie),query, index)


def by_change(query):
    tmp_trie = g_trie
    replace_results = {}
    delete_results = {}
    add_results = {}

    for index, letter in enumerate(query):
        for key in tmp_trie.keys():
            if key != "sentences_ids":
                replace_results.update(by_replace(query[index:], tmp_trie, key ,index))
                delete_results.update(by_delete(query[index:], tmp_trie, key ,index))
                add_results.update(by_add(query[index:], tmp_trie ,index))
        if letter not in tmp_trie:
            break
        tmp_trie = tmp_trie[letter]
    return merge_by_score(replace_results,delete_results,add_results)


def find_5_best_sentences(suitable_sentences):
    return [k for k, v in sorted(suitable_sentences.items(), reverse=True, key=lambda item: item[1])][:5]


def find_best_subs(suitable_sentences):
    return [k for k, v in sorted(suitable_sentences.items(), key=lambda item: item[1])][:5]


def find_sentences(query):
    score = len(query) * 2
    suitable_id_score = {}
    suitable_sentences = find_5_best_sentences(by_sub(query, g_trie))
    if len(suitable_sentences) >= 5:
        suitable_sentences = suitable_sentences[:5]
    else:
        for id in suitable_sentences:
            suitable_id_score [id] = score
        suitable_with_change = by_change(query)
        best_5_sentences = [sen for sen in find_5_best_sentences(suitable_with_change) if sen not in suitable_sentences]
        suitable_sentences = (suitable_sentences + best_5_sentences)[:5]
    for id in suitable_sentences:
        print(sentences[str(id)]['sentence'],"  file:", sentences[str(id)]['source'])
