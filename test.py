import copy

if __name__ == '__main__':
    i = 0
    child1 = [[1, 2],[ 3, 4]]
    child2 = [[5, 6],[ 7, 8]]
    child3 = [[9, 10],[ 11, 12]]
    child4 = [[13, 14],[ 15, 16]]
    children = [child1, child2, child3, child4]
    result = []
    len_i = len(children[1][0])
    child1 = copy.deepcopy(children[1])
    child2 = copy.deepcopy(children[2])
    child3 = copy.deepcopy(children[0])
    child4 = copy.deepcopy(children[3])
    while i < len(child1):
        result.append(child1[i])
        result[i].extend(child2[i])
        i += 1
    l = 0
    while l < len(child1):
        result.append(child3[l])
        result[l + i].extend(child4[l])
        l += 1
    print(result)