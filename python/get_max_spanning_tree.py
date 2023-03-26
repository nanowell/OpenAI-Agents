MOD = 10**9 + 7

# function to calculate distance between two points in the lattice grid
def distance(p1, p2):
    return sum((abs(p1[i] - p2[i])**2 for i in range(len(p1))))

# function to find maximum spanning tree
def max_spanning_tree(points):
    n = len(points)
    dist = [[distance(points[i], points[j]) for j in range(n)] for i in range(n)]
    parent = [-1] * n
    key = [float('-inf')] * n
    visited = [False] * n
    key[0] = 0

    for _ in range(n):
        max_key = float('-inf')
        max_idx = -1
        for i in range(n):
            if not visited[i] and key[i] > max_key:
                max_key = key[i]
                max_idx = i
        visited[max_idx] = True

        for j in range(n):
            if not visited[j] and dist[max_idx][j] > key[j]:
                parent[j] = max_idx
                key[j] = dist[max_idx][j]

    return sum(dist[i][parent[i]] for i in range(1, n)) % MOD

# main function to process input and output results
def main():
    t = int(input())
    for _ in range(t):
        d, k = map(int, input().split())
        points = []
        for _ in range(k):
            coords = list(map(int, input().split()))
            coords += [0] * (d - k)
            points.append(coords)
        for _ in range(k, d):
            coords = [0] * d
            coords[_] = 1
            points.append(coords)
        ans = max_spanning_tree(points)
        print(ans)

if __name__ == '__main__':
    main()
