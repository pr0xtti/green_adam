def comparison(ver_a: str, ver_b: str) -> int:
    if not ver_a and ver_b:
        return -1
    if ver_a and not ver_b:
        return 1
    if not ver_a and not ver_b:
        return 0

    a = [int(item) for item in ver_a.split('.')]
    b = [int(item) for item in ver_b.split('.')]
    min_len = min(len(a), len(b))
    for i in range(min_len):  # len(a) == len(b) included
        if a[i] > b[i]:
            return 1
        elif a[i] < b[i]:
            return -1
    max_len = max(len(a), len(b))
    for i in range(min_len, max_len):
        if len(a) > min_len:
            if a[i] > 0:
                return 1
        else:
            if b[i] > 0:
                return -1
    return 0


assert comparison('2.1', '2.0') == 1
assert comparison('', '') == 0
assert comparison('0', '0') == 0
assert comparison('1', '2') == -1
assert comparison('2', '1') == 1
assert comparison('2.0', '2.1') == -1
assert comparison('2.0.0', '2') == 0
assert comparison('2.0.0.1', '2') == 1
assert comparison('2.0.0', '2.0.0.5') == -1
assert comparison('1', '1.0.0.5') == -1

print("OK")

