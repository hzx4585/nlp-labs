import sys

INF = sys.maxsize

tree = []
trees = []

filename = sys.argv[1]
with open(filename) as f:
    for line in f:
        line = line.strip().split()
        if line:
            if line[0] == '#':
                continue
            idx = int(line[0])
            word = line[1]
            head = int(line[6])
            tree.append(line)
        else:
            trees.append(tree[:])
            tree = []

    trees.append(tree[:])

for tree_idx, tree in enumerate(trees):
    n = len(tree)
    heads = [int(line[6]) for line in tree]
    A = [[-INF for i in range(n+1)] for j in range(n+1)]

    for child in tree:
        idx = int(child[0])
        parent = int(child[6])
        cnt = 0
        while parent > 0:
            A[parent][idx] = cnt
            parent = heads[parent-1]
            cnt -= 1
        A[0][idx] = cnt

    T1 = [[-INF for i in range(n+1)] for j in range(n+1)]
    T2 = [[-INF for i in range(n+1)] for j in range(n+1)]
    T3 = [[-INF for i in range(n+1)] for j in range(n+1)]
    T4 = [[-INF for i in range(n+1)] for j in range(n+1)]

    for i in range(len(T1)):
        T1[i][i] = 0
        T2[i][i] = 0
        T3[i][i] = 0
        T4[i][i] = 0

    t1 = {}
    t2 = {}
    t3 = {}
    t4 = {}

    for m in range(1, n + 1):
        for s in range(n + 1):
            t = s+m
            if t > n:
                break;

            best_q = -1
            for q in range(s,t):
                tmp = T2[s][q] + T1[q+1][t] + A[s][t]
                if tmp > T3[s][t]:
                    T3[s][t] = tmp
                    best_q = q
            if best_q != -1:
                t3[(s,t)] = t2.get((s, best_q), []) + t1.get((best_q + 1,t), []) + [(s,t)]

            best_q = -1
            for q in range(s,t):
                tmp = T2[s][q] + T1[q+1][t] + A[t][s]
                if tmp > T4[s][t]:
                    T4[s][t] = tmp
                    best_q = q
            if best_q != -1:
                t4[(s,t)] = t2.get((s, best_q), []) + t1.get((best_q + 1, t), []) + [(t,s)]

            best_q = -1
            for q in range(s,t):
                tmp = T2[s][q] + T3[q][t]
                if tmp > T2[s][t]:
                    T2[s][t] = tmp
                    best_q = q
            if best_q != -1:
                t2[(s,t)] = t2.get((s, best_q), []) + t3.get((best_q,t), [])

            best_q = -1
            for q in range(s,t):
                q2 = q + 1
                tmp = T4[s][q2] + T1[q2][t]
                if tmp > T1[s][t]:
                    T1[s][t] = tmp
                    best_q = q2
            if best_q != -1:
                t1[(s,t)] = t4.get((s, best_q), []) + t1.get((best_q,t), [])

    # The total cost for lifting
    #print("Cost:", -T2[0][n])

    # Update with new heads
    for head, idx in t2[(0, n)]:
        trees[tree_idx][idx-1][6] = str(head)

# Save projective trees
with open(filename + '_projective', 'w') as f:
    for t in trees:
        for hej in t:
            f.write("\t".join(hej) + '\n')
        f.write('\n')
