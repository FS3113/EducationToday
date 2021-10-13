def find_possible_list(path_dict):
    candidate_num = sum([len(path_dict[i]) for i in path_dict.keys()])
    common_structure = []
    a = 0
    while True:
        count = {}
        for i in path_dict.keys():
            for j in path_dict[i]:
                if a >= len(j) or j[: len(common_structure)] != common_structure:
                    continue
                if j[a] not in count.keys():
                    count[j[a]] = 0
                count[j[a]] += 1
        t = []
        for i in count.keys():
            t.append([i, count[i]])
        t = sorted(t, key=lambda x: x[1], reverse=True)
        # print(t)
        try:
            if t[0][1] > 0.1 * candidate_num:
                common_structure.append(t[0][0])
            else:
                break
        except:
            return
        a += 1
    t = {}
    for i in path_dict.keys():
        t[i] = path_dict[i].copy()
    for i in t.keys():
        j = 0
        while j < len(t[i]):
            if t[i][j][:len(common_structure)] == common_structure:
                del t[i][j]
            else:
                j += 1
    result = [common_structure]
    a = find_possible_list(t)
    if a:
        result.extend(a)
    return result


def find_info_in_grandchildren(subtree_dict_pre, subtree_path_pre, raw_html):
    subtree_path = {}
    for i in subtree_path_pre.keys():
        t = subtree_path_pre[i]
        if isinstance(t, str) and t != 'None':
            if t.count('<') > 2:
                subtree_path[i] = t[t.index('>') + 1:]
            else:
                return 0, []
        else:
            if isinstance(t, str):
                subtree_path[i] = t
            else:
                subtree_path[i] = t.copy()
    a = ''
    for i in subtree_path.keys():
        if isinstance(subtree_path[i], str) and subtree_path[i] != 'None':
            t = subtree_path[i][:subtree_path[i].index('>')]
            if ' ' in t:
                t = t[:t.index(' ')]
            if a == '':
                a = t
            if t != a:
                return 0, []

    subtree_dict = {}
    for i in subtree_dict_pre.keys():
        subtree_dict_key = []
        if len(subtree_dict_pre[i]) < 3:
            continue
        for j in subtree_dict_pre[i][1]:
            subtree_dict_key.append(j[4])
        for j in subtree_dict_key:
            l = []
            for k in subtree_dict_pre[i][1:]:
                lt = []
                for kk in k:
                    t = kk[-1][kk[-1].index('-') + 1:]
                    if t[:t.index('-')] != str(j):
                        continue
                    t1 = kk[1][kk[1].index('>') + 1:]
                    t11 = t1[:t1.index('>')]
                    t11 = t11.replace('@', '') + t1[t1.index('>'):]
                    lt.append([kk[0], t11, kk[2], kk[3], kk[4], t])
                if len(lt) == 0:
                    break
                l.append(lt.copy())
            subtree_dict[j] = l
    # for i in subtree_dict.keys():
    #     print(subtree_dict[i])

    path_to_result = {}
    for i in subtree_dict.keys():
        path_to_result[i] = {}
        for j in subtree_dict[i]:
            for k in j:
                path_to_result[i][k[1]] = [k[2], k[3]]
    # print(subtree_path)

    result = []
    total_miss, total_num, total_match = 0, 1, 0
    for i in path_to_result.keys():
        d = {}
        missing = 0
        for j in subtree_path.keys():
            p = subtree_path[j]
            if isinstance(p, str):
                if p not in path_to_result[i].keys():
                    p = p[:p.rfind('<')]
                    if p in path_to_result[i].keys() and path_to_result[i][p][1] - path_to_result[i][p][0] > 2:
                        p = subtree_path[j]
                if p not in path_to_result[i].keys():
                    p = p[:p.rfind('<')]
                    if p in path_to_result[i].keys() and path_to_result[i][p][1] - path_to_result[i][p][0] > 2:
                        p = subtree_path[j]
                if p in path_to_result[i].keys():
                    a = ''
                    for k in range(path_to_result[i][p][0], path_to_result[i][p][1]):
                        if raw_html[k][0] != '<':
                            a += raw_html[k] + ' '
                    a = a.replace('\n', ' ')
                    if ' ' in a:
                        a = a[:-1]
                    # print(j + ': ' + a)
                    d[j] = a
                    total_match += 1
                else:
                    # print(j + ': missing')
                    d[j] = 'Missing'
                    missing += 1
            else:
                try:
                    parent = ''
                    if p[0] == 'start' or p[0] == 'end':
                        parent = p[-1]
                    else:
                        parent = p[0][:p[0].rfind('<')]
                    siblings = []
                    for kk in subtree_dict[i][parent.count('<')]:
                        if kk[1][:len(parent)] == parent:
                            siblings.append(kk.copy())
                    position = -1
                    if p[0] == 'start':
                        position = p[1]
                    elif p[0] == 'end':
                        position = len(siblings) - 1 + p[1]
                    else:
                        for k in range(len(siblings)):
                            if siblings[k][1] == p[0]:
                                position = k + p[1]
                    if 0 <= position < len(siblings):
                        a = ''
                        for k in range(siblings[position][2], siblings[position][3]):
                            if raw_html[k][0] != '<':
                                a += raw_html[k] + ' '
                        a = a.replace('\n', ' ')
                        if ' ' in a:
                            a = a[:-1]
                        # print(j + ': ' + a)
                        d[j] = a
                        total_match += 1
                    else:
                        # print(j + ': missing')
                        d[j] = 'Missing'
                        missing += 1
                except:
                    # print(j + ': missing')
                    d[j] = 'Missing'
                    missing += 1

        cell_range = [0, 0]
        for j in path_to_result[i].keys():
            if j.count('<') == 1:
                cell_range = path_to_result[i][j].copy()
        expected_name = ''
        for j in range(cell_range[0], cell_range[1]):
            if raw_html[j][0] != '<' and len(raw_html[j]) > 2:
                if 1 < len(raw_html[j].split()) < 4:
                    expected_name = raw_html[j]
                    break
                elif len(raw_html[j].split()) == 1:
                    expected_name = raw_html[j] + ' '
                    for k in range(j + 1, cell_range[1]):
                        if raw_html[k][0] != '<' and len(raw_html[k]) > 2:
                            if len(raw_html[k].split()) < 2:
                                expected_name += raw_html[k]
                            else:
                                expected_name = ''
                            break
                    break
        if expected_name != '' and 'Name' in d.keys() and d['Name'] != 'Missing':
            d['Name'] = expected_name

        # print(d)
        if missing < 4:
            result.append(d.copy())
        total_miss += missing
        total_num += 5
    # print(subtree_path)
    # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    return total_match, result

