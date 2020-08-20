def test(s1, s2):
    b, c, t = 0, 0, 0
    i = len(s2) - 1
    res = 0
    while i >= 0:
        if s2[i] == s1[2]:
            c += 1
        elif s2[i] == s1[1]:
            b += 1
            t += c
        elif s2[i] == s1[0]:
            res += t
            t = 0
        i -= 1
    return res


test('abc', 'abcabcabc')