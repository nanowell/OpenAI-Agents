# Input
# You will answer T testcases (1≤T≤10). Each testcase consists of 2 lines. The first line is two integers d(2≤d≤60) and k(1≤k≤500). The following line consists of d integers, which describes the dimensions of the d-dimensional lattice (D[i]≤109).

# Testcase 2 satisfies, d=k=5,(1≤D[i]≤5).

# Output
# The one integer for the ith testcase, ans[i], which is the maximum spanning tree of the lattice grid inputted. Since this number may be very large, please find it modulus 109+7.

# Example
# Input
# 3
# 2 2
# 2 2
# 3 2
# 2 2 2
# 4 20
# 6 9 96 66
# Output
# 5
# 18
# 742488253
# Note
# For the first testcase, you could draw edges between: (1,1) and (2,2) with weight |1−2|2+|1−2|2, (1,2) and (2,1) with weight |1−2|2+|2−1|2 , (1,1) and (2,1) with weight |1−2|2+|1−1|2 or 2+2+1 summing up to 5.

# For the second testcase, edges are between (1,1,1)→(2,2,2); (1,1,1)→(2,2,1), (1,1,1)→(2,1,2), (1,1,1)→(1,2,2), (1,2,1)→(2,1,2), (2,1,1)→(1,2,2), (1,1,2)→(2,2,1) with a total sum of 4∗(12+12+12) + 3∗(12+12+02).

# Due to the difficulty of drawing a 6×9×96×66 4-dimension lattice grid on a 2d screen, an explanation is omitted.

def get_distance(p1, p2):
    return sum([abs(p1[i] - p2[i]) for i in range(len(p1))])


def get_max_spanning_tree(d, k, D):
    nodes = [(i, j) for i in range(d) for j in range(D[i])]
    edges = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            edges.append((nodes[i], nodes[j], get_distance(nodes[i], nodes[j])))

    edges.sort(key=lambda x: x[2])

    visited = set()
    total_weight = 0

    while len(visited) < d:
        edge = None
        for e in edges:
            if e[0] not in visited and e[1] not in visited:
                edge = e
                break

        if edge is None:
            return -1

        visited.add(edge[0])
        visited.add(edge[1])

        total_weight += edge[2] % (10 ** 9 + 7)

    return total_weight


if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        d, k = [int(x) for x in input().split()]
        D = [int(x) for x in input().split()]

        print(get_max_spanning_tree(d, k, D))