family = []
def find_children(op, first, node):
    print("=============")
    print(node)
    dictionary = globals()[node[0]]
    key = tuple([node[1], node[2]])

    print("dictionary", node[0])
    print("key", key)
    if key in dictionary:
        print("dict Value", dictionary[key])
        print("going deeper :>")
        left = dictionary[key][0]
        right = dictionary[key][1]

        a = find_children(node[0], 'first', left)
        b = find_children(node[0], 'second', right)

        if op in ['t2', 't4']:
            family.append([a,b])
        else:
            family.append([b,a])

    else:
        print("plain Value", key)

        # two elements
        if node[2] - node[1] >= 2:
            first = sentence[node[1]]
            second = sentence[node[2]-1]
            print("FIRST", first)
            print("SECOND", second)
            if node[0] == 't2':
                print(second, '------>', first)
                family.append([second, first])
                return second

            elif node[0] == 't1':
                print(second, '------>', first)
                family.append([first, second])
                return first

            else:
                print("t3 or t4, not in dictionary :(")
        # one element :)
        else:
            first = sentence[node[1]]
            second = sentence[node[2]]

            if node[0] == 't2':
                print(first, '------>', second)
                family.append([first, second])
                return second
            elif node[0] == 't1':
                print(second, '------>', first)
                family.append([second, first])
                return first
            else:
                print("t3 or t4, not in dictionary :(")

def follow_child(parent, child):
    #t3 0, 2         t2 2 4
    family.append((parent, child))
    min_length = 2
    for gren in [parent, child]:
        print("====================")
        print(gren)
        if gren[2] - gren[1] <= min_length and gren[0] in ['t1', 't2']:
            if gren[0] == 't1':
                print("", sentence[gren[2]-1], "---->", sentence[gren[1]])
            elif gren[0] == 't2':
                print("", sentence[gren[1]], "---->", sentence[gren[2]-1])

        else:

            if gren[2] - gren[1] == 2:
                if gren[0] == 't3':
                    print("", sentence[gren[2]-1], "---->", sentence[gren[1]])
                else:
                    print("", sentence[gren[1]], "---->", sentence[gren[2]-1])
            else:
                dict_1 = globals()[gren[0]]

                print("jag pekar på det under")
                if gren[0] == 't3':
                    follow_child( dict_1[tuple(gren[1:])][0], dict_1[tuple(gren[1:])][1])
                else:
                    follow_child( dict_1[tuple(gren[1:])][1], dict_1[tuple(gren[1:])][0])

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
            for j in range(i + 1, k - 1 + 1):
                print(i, k)
                if T3[i][k] < T2[i][j] + T1[j][k] + A[i][k-1]:
                    t3[(i,k)] = [["t2", i, j], ["t1", j, k]]
                T3[i][k] = max(T3[i][k], T2[i][j] + T1[j][k] + A[i][k-1])

                if T4[i][k] < T2[i][j] + T1[j][k] + A[k-1][i]:
                    t4[(i,k)] = [["t2", i, j], ["t1", j, k]]
                T4[i][k] = max(T4[i][k], T2[i][j] + T1[j][k] + A[k-1][i])

            for j in range(i+2,k-1 + 1):
                # box + triangle
                if T2[i][k] < T3[i][j] + T2[j][k]:
                    t2[(i,k)] = [["t3", i, j], ["t2", j, k]]
                T2[i][k] = max(T2[i][k], T3[i][j] + T2[j][k])
            for j in range(i+1,k-2 + 1):
                 # triangle + box
                if T1[i][k] < T1[i][j] + T3[j][k]:
                    t1[(i,k)] = [["t1", i, j], ["t3", j, k]]
                T1[i][k] = max(T1[i][k], T1[i][j] + T3[j][k])
            print("best values: i, k", i, k)
            print(T1[i][k])
            print(T2[i][k])
            print(T3[i][k])
            print(T4[i][k])


            print("t1",t1)
            print("t2",t2)
            print("t3",t3)
            print("t4",t4)

            # input()

    print(len(T2[0]))
    print("opt cost, t2[0][-1]",T2[0][-1])

    start = T2[0][-1]
    value = t2[(0, len(T2[0])-1)]
    #print("", sentence[gren[2]-1], "---->", sentence[gren[1]])
    print("start:", value)

    #follow_child('t2', value[0], value[1])
    a = find_children('t2', 'first', value[0])
    b = find_children('t2', 'second', value[1])

    family.append([a,b])

    break

    #break
print(family)
