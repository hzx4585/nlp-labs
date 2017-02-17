'''
1	From	3
2	the	    3
3	AP	    4
4	comes   0
5	this	6
6	story	4
7	:	    4
'''


def follow_child(left, right):
    print(left)
    print(right)
    #t3 0, 2         t2 2 4
    input()
    if left[2] - left[1] == 1:
        print(left[1], left[2], sentence[left[1]:left[2]])
        return
    else:
#        dict_1 = locals()[left[0]]
#        dict_2 = locals()[right[0]]

        dict_1 = globals()[left[0]]
        dict_2 = globals()[right[0]]

        print(left[0])
        print(right[0])
        new_left = (left[1], left[2])
        new_right = (right[1], right[2])
        return follow_child(dict_1[new_left], dict_2[new_right])




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



    sentence = [word for head,idx,word in tree]

    for child in range(1, n + 1):
        tmp_child = child
        cnt = 0
        while True:
            parent = tree[tmp_child-1][0]
            if parent == 0:
                break
            # A[parent-1][child-1] = -cnt
            # A[parent-1][child-1] = cnt
            # A[child-1][parent-1] = -cnt
            A[child-1][parent-1] = cnt
            cnt += 1
            tmp_child = parent

    for i, c in enumerate(A):
        for x in c:
            if x == -1000:
                print('.', end="  ")
            else:
                print(x, end=" ")
        print()
    print()
    T1 = [[0 for i in range(n+1)] for j in range(n+1)]
    T2 = [[0 for i in range(n+1)] for j in range(n+1)]
    T3 = [[0 for i in range(n+1)] for j in range(n+1)]
    T4 = [[0 for i in range(n+1)] for j in range(n+1)]

    t1 = {}
    t2 = {}
    t3 = {}
    t4 = {}

    for k in range(2, n+1):
        for i in range(k - 2, -1, -1):
            # print(k,i,tree[k][2],tree[i][2])
            for j in range(i + 1, k - 1 + 1):
                print(i, k)
                if T3[i][k] < T2[i][j] + T1[j][k] + A[i][k-1]:
                    t3[(i,k)] = [["t2", i, j], ["t1", j, k]]
                #else:
                #    t3[(i,j)] = [["T3", i, j]]
                T3[i][k] = max(T3[i][k], T2[i][j] + T1[j][k] + A[i][k-1])

                if T4[i][k] < T2[i][j] + T1[j][k] + A[k-1][i]:
                    t4[(i,k)] = [["t2", i, j], ["t1", j, k]]
                T4[i][k] = max(T4[i][k], T2[i][j] + T1[j][k] + A[k-1][i])

            for j in range(i+2,k-1 + 1):
                # box + triangle
                if T2[i][k] < T3[i][j] + T2[j][k]:
                    t2[(i,k)] = [["t3", i, j], ["t2", j, k]]
                T2[i][k] = max(T2[i][k], T3[i][j] + T2[j][k])

                #print("T2:", i, k, T2[i][k])
            for j in range(i+1,k-2 + 1):
                 # triangle + box
                if T1[i][k] < T1[i][j] + T3[j][k]:
                    t1[(i,k)] = [["t1", i, j], ["t3", j, k]]
                T1[i][k] = max(T1[i][k], T1[i][j] + T3[j][k])
#                print("T1:", i, k, T1[i][k])
            print("best values: i, k", i, k)
            # print(tree[i][2], tree[k][2])
            print(T1[i][k])
            print(T2[i][k])
            print(T3[i][k])
            print(T4[i][k])


            print("t1",t1)
            print("t2",t2)
            print("t3",t3)
            print("t4",t4)

            input()

    print(len(T2[0]))
    print("opt cost, t2[0][-1]",T2[0][-1])

    start = T2[0][-1]
    value = t2[(0, len(T2[0])-1)]
    print("start:", value)

    follow_child(value[0], value[1])




    print(T1)
    print(T2)
    print(T3)
    print(T4)
    print(" HEJ :) ")
    break

    #break
