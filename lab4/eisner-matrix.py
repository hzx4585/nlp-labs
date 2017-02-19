import numpy as np
import sys

INF = 1000

def set_scores(tree, heads):

    A = {}
    for i in range(len(tree)):
        for j in range(len(tree)):
            if i == j:
                A[(i, j)] = 0
            else:
                A[(i, j)] = INF    

    sentence = [word for head,idx,word in tree]

    for child in range(1, n + 1):
        tmp_child = child
        cnt = 0
        while True:
            parent = tree[tmp_child-1][0]
            if parent == 0:
                break
            A[(child-1, parent-1)] = cnt
            cnt += 1
            tmp_child = parent

    print("===printing A===")
    for i in range(len(tree)):
        for j in range(len(tree)):
            score = A[(i,j)]
            if(score == INF):
                print('.', end=" ")
            else:
                print(score, end=" ")

        print()
    return A

def eisner(scores, sentence, backtrack):
    print("eisner")

    n = len(sentence)

    comp_rh = np.empty((n, n), dtype=np.int)  # C[i][j][←][0] T4
    comp_lh = np.empty((n, n), dtype=np.int)  # C[i][j][→][0] T3
    incomp_rh = np.empty((n, n), dtype=np.int)  # C[i][j][←][1] T1
    incomp_lh = np.empty((n, n), dtype=np.int)  # C[i][j][→][1] T2

    bp_comp_rh = backtrack[0]
    bp_comp_lh = backtrack[1]
    bp_incomp_rh = backtrack[2]
    bp_incomp_lh = backtrack[3]

    for i in range(0, n):
        comp_rh[i][i] = 0
        comp_lh[i][i] = 0
        incomp_rh[i][i] = 0
        incomp_lh[i][i] = 0

    for m in range(1, n):
        for i in range(0, n):
            j = i + m
            if j >= n:
                break

            # C[i][j][←][1] : right head, incomplete
            max = -INF
            bp = -1
            print(i,j,tree[j], "->", tree[i], scores[(j,i)])
            ex = scores[(j, i)]
            print(ex)
            for k in range(i, j):
                score = comp_lh[i][k] + comp_rh[k + 1][j] + ex
                if score > max:
                    max = score
                    bp = k
            incomp_rh[i][j] = max
            bp_incomp_rh[i][j] = bp

            # C[i][j][→][1] : left head, incomplete
            max = -INF
            bp = -1
            print(i,j,tree[j], "<-", tree[i], scores[(i,j)])
            ex = scores[(i, j)]
            for k in range(i, j):
                score = comp_lh[i][k] + comp_rh[k + 1][j] + ex
                if score > max:
                    max = score
                    bp = k
            incomp_lh[i][j] = max
            bp_incomp_lh[i][j] = bp
            #input()

            # C[i][j][←][0] : right head, complete
            max = -INF
            bp = -1
            for k in range(i, j):
                score = comp_rh[i][k] + incomp_rh[k][j]
                if score > max:
                    max = score
                    bp = k
            comp_rh[i][j] = max
            bp_comp_rh[i][j] = bp

            # C[i][j][→][0] : left head, complete
            max = -INF
            bp = -1
            for k in range(i + 1, j + 1):
                score = incomp_lh[i][k] + comp_lh[k][j]
                if score > max:
                    max = score
                    bp = k
            comp_lh[i][j] = max
            bp_comp_lh[i][j] = bp

    heads = [-1] * n

    return heads

def _backtrack(i, j, lh, c, backtrack, heads):
    """
        lh: right head = 0, left head = 1
        c: complete = 0, incomplete = 1
    """

    bp_comp_rh = backtrack[0]
    bp_comp_lh = backtrack[1]
    bp_incomp_rh = backtrack[2]
    bp_incomp_lh = backtrack[3]

    if i == j:
        return
    elif lh == 1 and c == 0:  # comp_lh
        k = bp_comp_lh[i][j]
        heads[k] = i
        heads[j] = k
        _backtrack(i, k, 1, 1, backtrack, heads)
        _backtrack(k, j, 1, 0, backtrack, heads)
    if lh == 0 and c == 0:  # comp_rh
        k = bp_comp_rh[i][j]
        heads[k] = j
        heads[i] = k
        _backtrack(i, k, 0, 0, backtrack, heads)
        _backtrack(k, j, 0, 1, backtrack, heads)
    elif lh == 1 and c == 1:  # incomp_lh
        k = bp_incomp_lh[i][j]
        heads[j] = i
        _backtrack(i, k, 1, 0, backtrack, heads)
        _backtrack(k + 1, j, 0, 0, backtrack, heads)
    elif lh == 0 and c == 1:  # incomp_rh
        k = bp_incomp_rh[i][j]
        heads[i] = j
        _backtrack(i, k, 1, 0, backtrack, heads)
        _backtrack(k + 1, j, 0, 0, backtrack, heads)


tree = []
trees = []
with open('litenmensnällare.txt') as f:
    for line in f:
        line = line.strip().split()
        if line:
            if line[0] == '#':
                continue
            idx = int(line[0])
            word = line[1]
            head = int(line[6])
            tree.append((head,idx,word))
        else:
            trees.append(tree[:])
            tree = []
    trees.append(tree[:])

for tree in trees:
    n = len(tree)

    old_heads = [head for head,idx,word in tree]

    A = set_scores(tree, old_heads)

    backtrack = (np.empty((n, n), dtype=np.int), np.empty((n, n), dtype=np.int), np.empty((n, n), dtype=np.int), np.empty((n, n), dtype=np.int)) 
    heads_new = eisner(A, tree, backtrack)

    print("eisner is done")
    print(heads_new)
    print(backtrack[0])
    print(backtrack[1])
    print(backtrack[2])
    print(backtrack[3])

    print("best score? ", backtrack[-1][0][-1])
    print("best score? ", backtrack[-2][0][-1])

    _backtrack(0, (n - 1), 1, 0, backtrack, heads_new)

    print("finished")
    print("old heads", old_heads)
    print("new heads", heads_new)
    
