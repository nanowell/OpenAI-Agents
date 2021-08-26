# P=N⋅P

# when 0≤P≤X and 0≤N≤Y where X and Y are given as input.

# Input
# One line with two integers, X and Y. (1≤X,Y≤1000). Note that despite X and Y being greater than 0, N and P in the equation can be greater than or equal to 0.

# Output
# A single integer denoting the number of pairs (N,P) such that P=N⋅P and (0≤N≤X) and (0≤P≤Y).

# Example
# input
# 2 2
# output
# 5

def main():
    x, y = map(int, input().split())
    count = 0
    for n in range(x+1):
        for p in range(y+1):
            if n*p == p*n:
                count += 1
    print(count)

if __name__ == "__main__":
    main()