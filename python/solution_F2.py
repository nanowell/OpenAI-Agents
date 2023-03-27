# Codex managed to slove the hard problem on Codeforces

T = int(input())
for _ in range(T):
    N, K = map(int, input().split())
    x = N
    while True:
        if len(set(str(x))) <= K:
            print(x)
            break
        x += 1
