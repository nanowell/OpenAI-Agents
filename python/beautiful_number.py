def beautiful_number(n, k):
    count = 0
    for i in range(n, 10 ** 100):
        if len(set(str(i))) <= k:
            return i
    return -1


if __name__ == '__main__':
    t = int(input())
    for i in range(t):
        n, k = [int(i) for i in input().split()][0:2]
        print(beautiful_number(n, k))
