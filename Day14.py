cave_map = {} # key=depth, value=list of columns at the depth

cleared_cave_map_arr = []
lo_col, hi_col = 9999999999,0
with open("day14_sample.txt") as f:
    for l in f.readlines():
        nodes = l.rstrip().split(' -> ')
        start_node = nodes[0].split(',')
        cur_x, cur_y = int(start_node[0]), int(start_node[1])
        if(cur_x > hi_col):
            hi_col = cur_x
        if(cur_x < lo_col):
            lo_col = cur_x
        if cur_y in cave_map.keys():
            cave_map[cur_y].append(cur_x)
        else:
            cave_map[cur_y] = [cur_x]
        for node in nodes[1:]:
            cn = node.split(',')
            nx, ny = int(cn[0]), int(cn[1])
            if(nx < lo_col):
                lo_col = nx
            if(nx > hi_col):
                hi_col = nx
            # print("Rock goes from {}/{} to {}/{}".format(cur_x, cur_y, nx, ny))
            # assuming nodes are all unique
            if(cur_x == nx):
                lo_v, hi_v = cur_y, ny
                if(lo_v > hi_v):
                    lo_v, hi_v = hi_v, lo_v
                for y in range(lo_v, hi_v+1):
                    if y in cave_map.keys():
                        cave_map[y].append(cur_x)
                    else:
                        cave_map[y] = [cur_x]
            elif(cur_y == ny):
                lo_v, hi_v = cur_x, nx
                if(lo_v > hi_v):
                    lo_v, hi_v = hi_v, lo_v
                for x in range(lo_v, hi_v+1):
                    if cur_y in cave_map.keys():
                        cave_map[cur_y].append(x)
                    else:
                        cave_map[cur_y] = [x]
            cur_x, cur_y = nx, ny
for k in cave_map.keys():
    cave_map[k] = list(set(cave_map[k]))
print(cave_map)

print("cols = {} - {}, max depth = {}".format(lo_col, hi_col, max(cave_map.keys())))

for x in range(max(cave_map.keys())+1):
    cleared_cave_map_arr.append([])
    for y in range(lo_col, hi_col+1):
        if x in cave_map.keys():
            if y in cave_map[x]:
                cleared_cave_map_arr[-1].append("o")
            else:
                cleared_cave_map_arr[-1].append(".")
        else:
            cleared_cave_map_arr[-1].append(".")

for a in cleared_cave_map_arr:
    print(a)