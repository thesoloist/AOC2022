min_x, max_x = 99999999,0
min_y, max_y = 99999999,0
min_z, max_z = 99999999,0

cube_dict = {} # key=xyz tuple, value = 6-entry array for x+ x- y+ y- z+ z-
with open("day18_input.txt") as f:
    while True:
        l = f.readline().rstrip()
        if not l:
            break
        cube = tuple(map(int, l.split(',')))
        cube_dict[cube] = [1 for x in range(6)]
        max_x = cube[0] if cube[0] > max_x else max_x
        max_y = cube[1] if cube[1] > max_y else max_y
        max_z = cube[2] if cube[2] > max_z else max_z
        min_x = cube[0] if cube[0] < min_x else min_x
        min_y = cube[1] if cube[1] < min_y else min_y
        min_z = cube[2] if cube[2] < min_z else min_z

print("range X Y Z = {}-{} {}-{} {}-{}".format(min_x, max_x, min_y, max_y, min_z, max_z))
# print(cube_dict)

# pt 1
for c in cube_dict.keys():
    if sum(cube_dict[c]) == 0:
        continue
    adj_cubes = [(c[0]+1, c[1], c[2]),(c[0]-1, c[1], c[2]),
                (c[0], c[1]+1, c[2]),(c[0], c[1]-1, c[2]),
                (c[0], c[1], c[2]+1),(c[0], c[1], c[2]-1)]
    opp_idx = [1,0,3,2,5,4]
    for idx, a in enumerate(adj_cubes):
        if a in cube_dict.keys():
            cube_dict[c][idx] = 0
            cube_dict[a][opp_idx[idx]] = 0

sum_faces = 0
for c in cube_dict.keys():
    sum_faces += sum(cube_dict[c])

print(sum_faces)

# pt 2
# build space with cubes in, and fill from all space on surface(min-max XYZ).
# then check if there's any unfilled space. exclude any face touching the unfilled space

space = [] # idx1 = Z
for z in range(max_z  + 1):
    space.append([])
    for y in range(max_y + 1): #idx2=Y
        space[-1].append([])
        for x in range(max_x + 1): #idx3=X
            space[-1][-1].append(".") # air
for c in cube_dict.keys():
    space[c[2]][c[1]][c[0]] = "L"

# build up array for spaces on face.
face_dict = {}
for z in range(min_z, max_z + 1):
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            acc_arr = [1,1,1,1,1,1]
            if x == max_x:
                acc_arr[0] = 0
            if x == min_x:
                acc_arr[1] = 0   
            if y == max_y:
                acc_arr[2] = 0
            if y == min_y:
                acc_arr[3] = 0   
            if z == max_z:
                acc_arr[4] = 0
            if z == min_z:
                acc_arr[5] = 0            
            if (x, y, z) not in cube_dict.keys() and (0 in acc_arr):
                face_dict[(x, y, z)] = acc_arr

print("there are {} spaces on surface".format(len(face_dict.keys())))

fillable_arr = list(face_dict.keys())
#print(fillable_arr)
# start filling
while len(fillable_arr):
    cur_space = fillable_arr.pop(0)
    space[cur_space[2]][cur_space[1]][cur_space[0]] = "W"
    cand_space = [(cur_space[0]+1, cur_space[1], cur_space[2]),(cur_space[0]-1, cur_space[1], cur_space[2]),
                  (cur_space[0], cur_space[1]+1, cur_space[2]),(cur_space[0], cur_space[1]-1, cur_space[2]),
                  (cur_space[0], cur_space[1], cur_space[2]+1),(cur_space[0], cur_space[1], cur_space[2]-1)]
    for cand in cand_space:
        if (min_x <= cand[0] <= max_x) and (min_y <= cand[1] <= max_y) and (min_z <= cand[2] <= max_z):
            if cand not in cube_dict.keys():            
                if space[cand[2]][cand[1]][cand[0]] == ".":
                    if cand not in fillable_arr:
                        fillable_arr.append(cand)


#Filling is done. now find pockets
interior_face_cnt = 0
for z in range(min_z, max_z + 1):    
    for y in range(min_y, max_y + 1): #idx2=Y        
        for x in range(min_x, max_x + 1): #idx3=X
            if space[z][y][x] == ".":
                print("Found space X,Y,Z = {},{},{} UNFILLED".format(x,y,z))
                # add up lava surface next to this pocket
                cand_space = [(x+1, y,   z  ), (x-1, y,   z  ),
                              (x,   y+1, z  ), (x,   y-1, z  ),
                              (x,   y,   z+1), (x,   y,   z-1)]
                for c in cand_space:
                    if c in cube_dict.keys():
                        interior_face_cnt += 1

print("Got {} interior faces -> leads to {} exterior faces".format(interior_face_cnt, sum_faces - interior_face_cnt))

          

    


