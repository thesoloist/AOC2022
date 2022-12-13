def get_height_val(pt, h_map):
    height = h_map[pt[1]][pt[0]]
    if height == "S":
        return ord('a')
    elif height == "E":
        return ord('z')
    else:
        return ord(height)
        
def bfs(start_pt,end_pt,h_map):
    frontier = []
    frontier.append(start_pt)
    came_from = {}
    came_from[start_pt] = None
    dirs = [(0,-1), (0,1), (-1,0), (1, 0)] # up/down/left/right
    while len(frontier):
        current = frontier.pop(0)
        #print("Testing frontier {}".format(current))
        if current == end_pt:
            # print path length
            path_len = 0
            prev = current
            while prev != start_pt:
                path_len += 1
                prev = came_from[prev]
            print("Found path, took {} steps".format(path_len))
            return path_len
        neighbor = []
        for d in dirs:
            candidate = (current[0]+d[0], current[1]+d[1])            
            # if inbound and can move
            if((0 <= candidate[0] < len(h_map[0])) and (0<=candidate[1]<(len(h_map)))):
                val_diff = get_height_val(candidate, h_map) - get_height_val(current, h_map)
                if val_diff<=1:                    
                    neighbor.append(candidate)
        for next in neighbor:
            if next not in came_from:
                #print("Putting next {} into frontier".format(next))
                frontier.append(next)
                came_from[next] = current
            else:
                #print("next {} is already checked, not putting to frontier".format(next))
                None
        None
    #print("Can't find path!")
    return -1

h_map = []
with open("day12_input.txt") as f:
    ls = f.readlines()
    for l in ls:
        h_map.append([x for x in list(l.rstrip())])

print(h_map)
start_pt = ()
end_pt = ()
a_pts = []
for idy, l in enumerate(h_map):
    for idx, c in enumerate(l):
        if c=="S":
          start_pt = (idx, idy)
          a_pts.append(start_pt)
        elif c=="E":
            end_pt = (idx, idy)
        elif c=='a':
            a_pts.append((idx, idy))
            None
print(start_pt, end_pt)

min_length = 999999999
for pt in a_pts:
    length = bfs(pt, end_pt, h_map)
    if(-1 < length < min_length):
        min_length = length
print("Shorted a_pt to end takes {} steps".format(min_length))
        
#move(start_pt, 0, seen_map)

