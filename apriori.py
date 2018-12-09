from typing import Iterator
import time


def readLines(path: str) -> Iterator[str]:
    with open(path, 'r') as f:
        for line in f.read().split('\n'):
            yield line

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
    vis = [0 for _ in range(20000)]
    for item in lst:
        for x in item:
            vis[x] += 1
    c1 = []
    temp_vis = [0 for _ in range(20000)]
    for id in range(vis.__len__()):
        if vis[id] / sum >= s:
            c1.append([id])
            ans.append([id])
            temp_vis[id] = 1
    temp_lst = []
    for item in lst:
        temp_item = [x for x in item if temp_vis[x]]
        if temp_item.__len__():
            temp_lst.append(temp_item)
    lst = temp_lst
    tree = [{}]#动态维护字典树
    fa = [-1]#子节点的父亲
    cnt = 1#节点总个数
    tree_k = [] #记录第k层节点的下标
    tree_value = [-1] #节点代表的值
    tree_k.append(0)#一开始只有第0层的一个点
    #将1频繁项集加入字典树中
    for item in c1:
        tree[0][item[0]] = cnt
        fa.append(0)
        tree_value.append(item[0])
        tree.append({})
        cnt += 1
    while 1:
        #根据第k-1层的点剪枝生成k候选项集
        temp_k = []#记录第k层的id
        pre_cnt = cnt
        for id in tree_k:
            if tree[id].__len__() == 1:#删除这条支路
                tree[id] = {}
                p = id
                while p and tree[p].__len__() == 0:
                    del tree[fa[p]][tree_value[p]]
                    p = fa[p]
                continue
            #生成候选项集
            temp = list(tree[id].keys())
            temp.sort()
            for i in range(0,temp.__len__()):
                for j in range(i+1,temp.__len__()):
                    id1 = tree[id][temp[i]]
                    tree[id1][temp[j]] = (cnt,1)
                    temp_k.append(cnt)
                    tree_value.append(temp[j])
                    tree.append({})
                    fa.append(id1)
                    cnt += 1
            del tree[id][temp[-1]] #删除最后一个元素
        # 遍历数据库
        temp_support = {}#记录候选项被支持了几次
        print(cnt-pre_cnt + 5)
        temp_support = [0 for _ in range(cnt-pre_cnt + 5)]
        for item in lst:
            pre_arr = [0]
            last_arr = []
            for x in item:
                last_arr = last_arr + pre_arr
                pre_arr = []
                for y in last_arr:
                    if tree[y].get(x,0):
                        p = tree[y][x]
                        if isinstance(p, tuple):
                            temp_support[p[0]-pre_cnt]+=1
                        else:
                            pre_arr.append(p)
        #查找频繁项并准备记录下一层的tree_k
        temp_tree_k = set()
        for item in temp_k:
            tree[fa[item]][tree_value[item]] = item
            if temp_support[item-pre_cnt] / sum >= s:#该项是频繁项
                temp = []
                p = item
                while p:
                    temp.append(tree_value[p])
                    p=fa[p]
                temp.sort()
                ans.append(temp)
                temp_tree_k.add(fa[item])
            else:
                # 删除这条支路
                p = item
                while p and tree[p].__len__() == 0:
                    del tree[fa[p]][tree_value[p]]
                    p = fa[p]
        tree_k = list(temp_tree_k)
        if tree[0].keys().__len__() == 0:
            break


    vis = {}
    for item in ans:
        if len(item) in vis:
            vis[len(item)]+= 1
        else:
            vis[len(item)] = 1
        print(item)
    print(len(ans))
    print(vis)
    end = time.time()
    print('The time is {id}s'.format(id=end - start))


if __name__ == '__main__':
    main()
