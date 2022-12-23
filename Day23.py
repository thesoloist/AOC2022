rounds_tgt = 100000

def niceprint(map_arr):
    for idx, r in enumerate(map_arr):
        print("row {:2d}: ".format(idx), end='')
        for cidx, c in enumerate(r):
            print(c,end='')
            if cidx%10 == 9:
                print(' ',end='')
        print()

def check_around(elf_loc, map_arr):
    clear_around = True    
    for y in [-1,0,1]:
        if clear_around == False:
            break
        for x in [-1,-0,1]:
            if x==0 and y==0:
                continue
            if map_arr[elf_loc[1]+y][elf_loc[0]+x] == "#":
                clear_around = False
                break    
    return clear_around

def expand_grove(grove: list, elves: list):
    print("Expanding grove...")
    grove.insert(0, ['.' for i in range(len(grove[0]))])
    grove.append(['.' for i in range(len(grove[0]))])
    for i in range(len(grove)):
        grove[i] = ['.'] + grove[i] + ['.']
    # now update elves
    for eidx in range(len(elves)):
        elves[eidx] = (elves[eidx][0]+1, elves[eidx][1]+1)

grove_map = []
elf_arr = []
with open("day23_input.txt") as f:
    lines = f.readlines()
    # pre-build extra spaces around input so I don't have to worry about expansion...
    # add number of rounds to edges so even if an elf go straight it won't go OB
    # cheated that for pt1, still have to do proper expansion for pt2...
    for yidx, l in enumerate(lines):                
        line = l.rstrip()
        grove_map.append([])
        for xidx, c in enumerate(line):
            grove_map[-1].append(c)
            if(c=='#'):
                elf_arr.append((xidx, yidx))        
    
# niceprint(grove_map)

#now get moving
direction_pref = 0 # 0=North first, 1=South, 2=West, 3=East

rnd = 0
while True:
    print("Starting round {}...".format(rnd+1))
    # prelude: Expand grove if any of the elf is on the edge
    elf_xs = [e[0] for e in elf_arr]
    elf_ys = [e[1] for e in elf_arr]    
    # niceprint(grove_map)
    # print(elf_arr)
    if min(elf_xs) == 0 or max(elf_xs)==len(grove_map[0])-1 or min(elf_ys)==0 or max(elf_ys)==len(grove_map)-1:
        expand_grove(grove_map, elf_arr)
    # print("After potential expansion:")
    # niceprint(grove_map)
    # print(elf_arr)
    # first half: get proposals    
    elf_proposals = [] # hold the elf's proposed destination
    for eidx, elf in enumerate(elf_arr):
        #if elf doesn't have anyone around, don't move and move on to next elf
        if check_around(elf, grove_map):
            elf_proposals.append(None)
            continue

        #calculate proposed moves
        elf_moves = [None, None, None, None]        
        # Calculate N-S-W-E, then shift and pick the first valid
        if((grove_map[elf[1]-1][elf[0]-1], grove_map[elf[1]-1][elf[0]], grove_map[elf[1]-1][elf[0]+1]) == ('.','.','.')): #North
            elf_moves[0] = (elf[0], elf[1]-1)
        if((grove_map[elf[1]+1][elf[0]-1], grove_map[elf[1]+1][elf[0]], grove_map[elf[1]+1][elf[0]+1]) == ('.','.','.')): #South
            elf_moves[1] = (elf[0], elf[1]+1)
        if((grove_map[elf[1]-1][elf[0]-1], grove_map[elf[1]][elf[0]-1], grove_map[elf[1]+1][elf[0]-1]) == ('.','.','.')): #West
            elf_moves[2] = (elf[0]-1, elf[1])
        if((grove_map[elf[1]-1][elf[0]+1], grove_map[elf[1]][elf[0]+1], grove_map[elf[1]+1][elf[0]+1]) == ('.','.','.')): #East
            elf_moves[3] = (elf[0]+1, elf[1])
        #Now pick the first true with direction_shift in mind
        # print("moves N/S/W/E for elf {} at {}: {}".format(eidx, elf, elf_moves))
        stuck = True
        for i in range(len(elf_moves)):
            if elf_moves[(direction_pref + i)%len(elf_moves)] != None:
                # print("Picking move to {} for elf {} at {}".format(elf_moves[(direction_pref + i)%len(elf_moves)], eidx, elf))
                elf_proposals.append(elf_moves[(direction_pref + i)%len(elf_moves)])
                stuck = False
                break # pick the first and done
        # if we're stuck, add None into proposal
        if stuck:
            elf_proposals.append(None)

    # print("Proposals from elf: ", elf_proposals)
    # second half: check proposals and move
    for idx, e in enumerate(elf_proposals):
        if e == None:
            # print("elf {} has nowhere to go, stay".format(idx))
            continue
        if elf_proposals.count(elf_proposals[idx]) == 1:
            # print("elf {} is the only one trying to go {}, granted".format(idx, e))
            # elf on the move: update map, then update elf_arr
            grove_map[elf_arr[idx][1]][elf_arr[idx][0]] = '.'
            grove_map[e[1]][e[0]] = '#'
            elf_arr[idx] = e
        else:
            # print("elf {} is NOT the only one trying to go {}, stay...".format(idx, e))
            continue

    # finally: update direction_shift
    direction_pref += 1
    if(direction_pref == 4):
        direction_pref = 0 # I could leave it increasing as I'm using mods, but for debug sanity keep it within [0-3]
    
    # niceprint(grove_map)
    print("Finished moving for round ", rnd+1)
    #do possible expansion again before checking spread_out
    elf_xs = [e[0] for e in elf_arr]
    elf_ys = [e[1] for e in elf_arr]    
    # niceprint(grove_map)
    # print(elf_arr)
    if min(elf_xs) == 0 or max(elf_xs)==len(grove_map[0])-1 or min(elf_ys)==0 or max(elf_ys)==len(grove_map)-1:
        expand_grove(grove_map, elf_arr)
    # if all elves are spread out, break out. Else continue
    spread_out = True
    for e in elf_arr:
        if not check_around(e, grove_map):
            spread_out = False
            break        
    if spread_out:
        print("All elves spread out after {} rounds, break...".format(rnd+1))
        break
    elif rnd+1 == rounds_tgt:
        break
    rnd += 1

#Now calculate the minimum rectangle: get min/max elf_x/y
elf_xs = [e[0] for e in elf_arr]
elf_ys = [e[1] for e in elf_arr]

rect_area = (max(elf_xs) - min(elf_xs) + 1) * (max(elf_ys) - min(elf_ys) + 1)
print("Rect area = ", rect_area, ", elf count = ", len(elf_arr), ", empty tiles = ", rect_area - len(elf_arr))