from typing import Iterator
import time,math


def readLines(path: str) -> Iterator[str]:
    with open(path, 'r') as f:
        for line in f.read().split('\n'):
            yield line

def dfs(id,tree,top_list):
    for item in tree[id]:
        top_list[item].append(tree[id][item][0])
        dfs(tree[id][item][0],tree,top_list)

#判断是不是链
def judge(tree):
    for item in tree:
        cnt = 0
        for x in item:
            cnt += 1
            if cnt >= 2:
                return False
    return True


def create_FP_tree(lst,s:int,pre,ans):
    if pre != []:
        ans.append(pre)
    length = 0
    support = {}
    for item in lst:
        for x in item:
            if x in support.keys():
                support[x] += 1
            else:
                support[x] = 1
    for item in lst:
        for i in range(len(item)-1,-1,-1):
            if support[item[i]] < s:
                item.pop(i)
            else:
                length += 1
    if length == 0:
        return
    for item in lst:
        item.sort(key=lambda x:-support[x])
    top_list = []
    for item in support:
        if support[item] >= s:
            top_list.append(item)
    top_list.sort(key=lambda x:support[x])
    top_arr = {}
    for item in top_list:
        top_arr[item] = []

    tree = [{} for _ in range(length)]
    fa = [-1 for _ in range(length)]
    b = [0 for _ in range(length)]#节点代表的值
    cnt = 1
    # 构造FP-tree
    for item in lst:
        id = 0
        for x in item:
            if x in tree[id]:
                tree[id][x][1] += 1
                id = tree[id][x][0]
            else:
                tree[id][x] = [cnt,1]
                b[cnt] = x
                fa[cnt] = id
                id = cnt
                cnt += 1
                top_arr[x].append(id)
    if judge(tree):
        for i in range(1,2**top_list.__len__()):
            temp1 = []
            id,j = 0,i
            while j:
                if j & 1:
                    temp1.append(top_list[id])
                j = j >> 1
                id += 1
            ans.append(temp1 + pre)
        return

    for item in top_list:
        new_list = []
        for p in top_arr[item]:
            temp = []
            cnt = tree[fa[p]][item][1]
            p = fa[p]
            while p:
                temp.append(b[p])
                p = fa[p]
            for _ in range(cnt):
                new_list.append(temp)

        create_FP_tree(new_list,s,pre+[item],ans)




def main():
    s = float(input())
    start = time.time()
    reader = readLines('retail.dat')
    lst = []
    for line in reader:
        lst.append(list(map(lambda x: int(x), line.strip().split())))
    print(len(lst))
    sum = len(lst)

    ans = []

    s = math.ceil(s*sum)
    create_FP_tree(lst,s,[],ans)
    ans.sort(key=lambda x:x.__len__())
    vis = {}
    for item in ans:
        if len(item) in vis.keys():
            vis[len(item)] += 1
        else:
            vis[len(item)] = 1
        item.sort()
        print(item)
    print(len(ans))
    print(vis)
    end = time.time()
    print('The time is {id}s'.format(id=end - start))

if __name__ == '__main__':
    main()