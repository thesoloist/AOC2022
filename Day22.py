map_arr = []
move_arr = []

# should be 6 entries: each entry is ((tl_x, tl_y),(br_x, br_y))
box_faces = []
box_face_tl = []
box_face_grid = [] #either a 3x4 or a 4x3 entry
# face transitions: key = (src_face, dst_face), value = new_dir
face_transitions = {}
import re

def get_tile(loc):
    return map_arr[loc[1]][loc[0]]
def update_loc(cur_loc, mv):
    return tuple(map(lambda i, j: i + j, cur_loc, mv))

def wrap_around(cur_loc, dir):
    #returns wrapped around location
    #check reverse
    chk_dir = (-dir[0], -dir[1])
    my_loc = cur_loc
    while True:
        nxt_loc = update_loc(my_loc, chk_dir)        
        #boundary check
        if(nxt_loc[0]) < 0:
            nxt_loc = (max_mapw-1, nxt_loc[1])
        elif nxt_loc[0] == max_mapw:
            nxt_loc = (0, nxt_loc[1])
        elif nxt_loc[1] < 0:
            nxt_loc = (nxt_loc[0], len(map_arr)-1)
        elif nxt_loc[1] == len(map_arr):
            nxt_loc = (nxt_loc[0], 0)
        
        if(get_tile(my_loc) == '.' and get_tile(nxt_loc)==' '):
            # print("Wrapping around done, new location {}".format(my_loc))
            return my_loc
        elif(get_tile(my_loc) == '#' and get_tile(nxt_loc)==' '):
            # print("Wrapping around into a wall, return None")
            return None
        else:
            my_loc = nxt_loc

def turn(cur_dir, turn_lr):    
    if(turn_lr == "R"): # turn right        
        if(cur_dir == (1,0)):
            return (0, 1)
        elif cur_dir == (0,1):
            return (-1, 0)
        elif cur_dir == (-1,0):
            return (0, -1)
        elif cur_dir == (0, -1):
            return (1, 0)
    elif(turn_lr == "L"): # turn left
        if(cur_dir == (1,0)):
            return (0, -1)
        elif cur_dir == (0, -1):
            return (-1, 0)
        elif cur_dir == (-1, 0):
            return (0, 1)
        elif cur_dir == (0, 1):
            return (1, 0)
    else:
        #for some reason it's not turning left or right
        return cur_dir

def get_facing(cur_dir):
    if cur_dir == (1,0):
        return "RIGHT"
    elif cur_dir == (0, 1):
        return "DOWN"
    elif cur_dir == (-1, 0):
        return "LEFT"
    elif cur_dir == (0, -1):
        return "UP"

def get_facing_value(cur_dir):
    if cur_dir == (1,0):
        return 0
    elif cur_dir == (0, 1):
        return 1
    elif cur_dir == (-1, 0):
        return 2
    elif cur_dir == (0, -1):
        return 3

def calculate_moves(start_loc, dir, steps, folded): #returns updated location
    cur_loc = start_loc    
    for i in range(steps):
        nxt_loc = update_loc(cur_loc, dir)
        # check if we're wrapping
        if(nxt_loc[0]==len(map_arr[cur_loc[1]]) or nxt_loc[1]==len(map_arr) or nxt_loc[0]==-1 or nxt_loc[1]==-1): #we're at map edge, wrap
            # print("at map edge {}, try wrapping around...".format(cur_loc))
            wrap_loc = wrap_around(cur_loc, dir)
            if wrap_loc: 
                cur_loc = wrap_loc
            else:
                # we wrap into a wall, so keep cur_loc and we're done
                # print("Wrapping will be into a wall, we're done")
                return cur_loc
        elif(map_arr[nxt_loc[1]][nxt_loc[0]] == ' '): #cliff! wrap around
            # print("at cliff edge {}, try wrapping around...".format(cur_loc))
            wrap_loc = wrap_around(cur_loc, dir)
            if wrap_loc: 
                cur_loc = wrap_loc
            else:
                # we wrap into a wall, so keep cur_loc and we're done
                # print("Wrapping will be into a wall, we're done")
                return cur_loc
        elif(map_arr[nxt_loc[1]][nxt_loc[0]] == '#'): #into the wall, we're done, return cur_loc
            # print("Hitting a wall at {}, return...".format(cur_loc))
            return cur_loc
        elif(map_arr[nxt_loc[1]][nxt_loc[0]] == '.'): # free to move further
            # print("next step {} is free, keep going...".format(nxt_loc))
            cur_loc = nxt_loc
            continue
        else:
            print("SHOULD NEVER BE HERE")
    return cur_loc

with open("day22_sample.txt") as f:    
    lines = f.readlines()
    for l in lines:
        l = l.rstrip('\n')
        if l == '':
            continue
        if l.find('R') == -1:
            map_arr.append([])
            for c in l:
                map_arr[-1].append(c)
        else:
            moves = re.findall(r'(\d+)(\w?)', l)
            for m in moves:
                move_arr.append((int(m[0]), m[1]))
    print(move_arr[-1])
    max_mapw = 0
    for l in map_arr:
        if len(l) > max_mapw:
            max_mapw = len(l)
    for idx, l in enumerate(map_arr):
        if len(l) < max_mapw:
            map_arr[idx] = l + [' ' for i in range(max_mapw - len(l))]

    #analyze for faces/edges
    # max_mapw may have 3/4x width for a face. find that out. if it's divisible by 3 then it has 3x width
    face_size = 0
    if (max_mapw % 3 == 0):        
        face_size = int(max_mapw/3)
        #the map is 3w x 4h, so figure out how to fold vertically into a loop
        box_face_grid = [[None for x in range(3)] for y in range(4)]
    else:
        face_size = int(max_mapw/4)
        box_face_grid = [[None for x in range(4)] for y in range(3)]
            
    for y in range(0, len(map_arr), face_size):
        for x in range(0, max_mapw, face_size):
            if map_arr[y][x] != ' ':
                box_face_tl.append((x,y))
                box_faces.append(((x,y), (x+face_size-1, y+face_size-1)))
                box_face_grid[int(y/face_size)][int(x/face_size)] = 1
    face_proc_q = [(box_faces[0],'top')]
    box_face_names = [None, None, None, None, None, None]
    while len(face_proc_q):
        face, facename = face_proc_q.pop(0)
        faceidx = box_faces.index(face)
        box_face_names[faceidx] = facename
        print("checking faces adjacent to {} aka {}".format(face, facename))
        if((face[0][0] + face_size, face[0][1]) in box_face_tl): # adjacent to right
            # name new face based on current face


    print(box_faces)    
    
    # build face-transition table    
    for sdx, src_face in enumerate(box_faces):
        for ddx, dst_face in enumerate(box_faces[sdx+1:]):
            face_distance = (int((dst_face[0][0] - src_face[0][0])/face_size), int((dst_face[0][1] - src_face[0][1]) / face_size))
            print("Face distance between src {} and dst{} is {}".format(src_face, dst_face, face_distance))
            if src_face[0][0] == dst_face[0][0] or src_face[0][1] == dst_face[0][1]: #inline, keep same direction
                face_transitions[sdx+1, sdx+ddx+2] = None #keep the same direction            
                face_transitions[sdx+ddx+2, sdx+1] = None #keep the same direction
            elif(face_distance == (1,1)): # dst is bot-right, forward=down,reverse=left
                face_transitions[sdx+1, sdx+ddx+2] = (0,1)
                face_transitions[sdx+ddx+2, sdx+1] = (-1,0)
            elif(face_distance == (1,-1)): # dst is top-right, forward=up,reverse=left
                face_transitions[sdx+1, sdx+ddx+2] = (0,-1)
                face_transitions[sdx+ddx+2, sdx+1] = (-1,0)
            elif(face_distance == (-1,1)): # dst is bot-left, forward=down,reverse=right
                face_transitions[sdx+1, sdx+ddx+2] = (0,1)
                face_transitions[sdx+ddx+2, sdx+1] = (1,0)
            elif(face_distance == (-1,-1)): # dst is top-left, forward=up,reverse=right
                face_transitions[sdx+1, sdx+ddx+2] = (0,-1)
                face_transitions[sdx+ddx+2, sdx+1] = (1,0)
            elif face_distance == (-2,1):
                face_transitions[sdx+1, sdx+ddx+2] = (0,1)
                face_transitions[sdx+ddx+2, sdx+1] = (1,0)
            elif face_distance == (1,2):
                face_transitions[sdx+1, sdx+ddx+2] = (0,1)
                face_transitions[sdx+ddx+2, sdx+1] = (-1,0)
            elif face_distance == 5:
                None
            else: 
                print("THIS SHOULD NEVER HAPPEN")

    print(face_distance)
#print(map_arr)
#print(move_arr)


my_loc = (map_arr[0].index('.'), 0)
my_dir = (1, 0)

folded = True
for move in move_arr:
    # print("Attempting to move {} steps {} from location {}".format(move[0], get_facing(my_dir), my_loc))
    # update my location
    my_loc = calculate_moves(my_loc, my_dir, move[0], folded)        
    # update my direction
    my_dir = turn(my_dir, move[1])
    # print("after move {}, we're now at {}, facing {}".format(move, my_loc, get_facing(my_dir)))

print("After moves, location {}, facing {}".format(my_loc, get_facing(my_dir)))
print("final password = ", (1000*(my_loc[1]+1) + 4*(my_loc[0]+1) + get_facing_value(my_dir)))