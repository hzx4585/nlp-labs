'''
1	From	3
2	the	    3
3	AP	    4
4	comes   0
5	this	6
6	story	4
7	:	    4
'''

tree = []
trees = []
with open('litenmensnällare.txt') as f:
    for line in f:
        #print(line)
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
    heads = [head for head,idx,word in tree]
    A = [[0 if i == j else -1000 for i in range(n)] for j in range(n)]

    for child in range(1, n + 1):
        tmp_child = child
        cnt = 1
        while True:
            parent = tree[tmp_child-1][0]
            if parent == 0:
                break
            A[child-1][parent-1] = cnt
            cnt += 1
            tmp_child = parent

    for i, c in enumerate(A):
        for x in c:
            if x == -1:
                print('.', end=" ")
            else:
                print(x, end=" ")
        print()

    T1 = [[0 for i in range(n)] for j in range(n)]
    T2 = [[0 for i in range(n)] for j in range(n)]
    T3 = [[0 for i in range(n)] for j in range(n)]
    T4 = [[0 for i in range(n)] for j in range(n)]

    for k in range(2, n):
        for i in range(k - 2, -1, -1):
            for j in range(i + 1, k - 1):
                # combining two triangles
                #if A[i][k-1] == -1:
                #    T3[i][k] = T3[i][k]
                #else:

                T3[i][k] = max(T3[i][k], T2[i][j] + T1[j][k] + A[i][k-1])

                #if A[k-1][i] == -1:
                #     T4[i][k] = T4[i][k]
                #else:
                T4[i][k] = max(T4[i][k], T2[i][j] + T1[j][k] + A[k-1][i])


                # box + triangle
                T2[i][k] = max(T2[i][k], T3[i][j] + T2[j][k])
                 # triangle + box
                T1[i][k] = max(T1[i][k], T1[i][j] + T3[j][k])


    for i, te in enumerate(T1):
        print(tree[i][2][:3], '\t' , te)

    print()
    print()
    for i, te in enumerate(T2):
        print(tree[i][2][:3], '\t' , te)

    print()
    print()
    for i, te in enumerate(T3):
        print(tree[i][2][:3], '\t' , te)

    print()
    print()
    for i, te in enumerate(T4):
        print(tree[i][2][:3], '\t' , te)
    print()
    print()
    print()
    print(T2[0][-1])









    print(" HEJ :) ")
    break

    #break
