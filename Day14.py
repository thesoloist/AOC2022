cave_map = {} # key=depth, value=list of columns at the depth

cleared_cave_map_arr = []
lo_col, hi_col = 9999999999,0
with open("day14_input.txt") as f:
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

print("cols = {} - {}, max depth = {}".format(lo_col, hi_col, max(cave_map.keys())))

for x in range(max(cave_map.keys())+1):
    cleared_cave_map_arr.append([])
    for y in range(lo_col, hi_col+1):
        if x in cave_map.keys():
            if y in cave_map[x]:
                cleared_cave_map_arr[-1].append("#")
            else:
                cleared_cave_map_arr[-1].append(".")
        else:
            cleared_cave_map_arr[-1].append(".")

drop_point = (500-lo_col, 0)

def print_map(m):
    for l in m:
        print(l)
    print("\n")

def drop(pt, state_map):
    my_state = []    
    sand_x, sand_y = pt[0], pt[1]
    if(state_map[sand_y][sand_x] == 'o'):
        print("Gummed up, return...")
        return None
    for l in state_map:
        my_state.append([])
        my_state[-1] = [c for c in l]
    if(sand_y+1 >= len(my_state)): #gonna fall out bottom
        return None
    elif my_state[sand_y+1][sand_x] == '.': # down-middle
        my_state = drop((sand_x, sand_y+1), my_state)
    else:
        if(sand_x==0): #gonna fall out left
            return None
        elif(my_state[sand_y+1][sand_x-1] == '.'): # can fall left
            my_state = drop((sand_x-1, sand_y+1), my_state)
        elif (sand_x == (len(my_state[sand_y+1])-1)): #gonna fall out right
            return None
        elif (my_state[sand_y+1][sand_x+1] == '.'):
            my_state = drop((sand_x+1, sand_y+1), my_state)
        else:            
            my_state[sand_y][sand_x] = 'o'
    return my_state

def part1(drop_point):
    rnd_cnt = 0
    updated_map = []
    for l in cleared_cave_map_arr:
        updated_map.append([])
        updated_map[-1] = [c for c in l]  
        
    while True:      
        cur_state = drop(drop_point, updated_map)
        if(cur_state == None):           
            print("Stablized, rnd_cnt = ",rnd_cnt)
            #print_map(updated_map)
            break            
        else:
            for l in range(len(updated_map)):
                for c in range(len(updated_map[l])):
                    updated_map[l][c] = cur_state[l][c] 
            #print_map(updated_map)
            rnd_cnt +=1
            if(rnd_cnt % 100 == 0):
                print("Done round ",rnd_cnt)
                #print_map(updated_map)
   
def part2(drop_point, floor_expand):    
    updated_map = []
    for l in cleared_cave_map_arr:
        updated_map.append([])
        updated_map[-1] = [c for c in l]
    if floor_expand>0:
        # for l in range(len(updated_map)):
        #     updated_map[l] = ['.' for i in range(floor_expand+1)] + updated_map[l] + ['.' for i in range(floor_expand+1)]
        for i in range(floor_expand):
            if i+1==floor_expand:
                updated_map.append(['#' for c in range(len(updated_map[-1]))])
            else:
                updated_map.append(['.' for c in range(len(updated_map[-1]))])

    # process updated_map:        
    total_dots = len(updated_map) - 1
    for i in range(len(updated_map) - 1):
        total_dots += 2*i
    print("Total possible dots = ", total_dots)
    # remove existing rocks
    for idy, l in enumerate(updated_map[:-floor_expand+1]):
        for idx, c in enumerate(l):
            if c=='#':
                #print("Found rock")
                total_dots -= 1
            elif(0<idy and 0<idx<len(l)-1):
                # remove points with a l-c-r ceiling
                if updated_map[idy-1][idx-1] == '#' and updated_map[idy-1][idx]=='#' and updated_map[idy-1][idx+1] =='#':
                    #print("Found point with full ceiling")
                    total_dots -=1
                    #since it's not possible, might as well consider it as rock. should be in time for next row
                    updated_map[idy][idx] = "#"
    print("After rock/ceiling, total possible dots = ", total_dots)
#part1(drop_point)
expand = 2
part2(drop_point, expand)