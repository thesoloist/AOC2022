class PriorityQueue:    
    def __init__(self) -> None:
        self.queue = []
        pass
    def enqueue(self, pri, item):
        for idx, it in enumerate(self.queue):
            if pri > it[0]:
                #1st tier priority: distance to end
                self.queue.insert(idx, (pri, item))
                return        
            elif pri == it[0]:
                if(item[0] < it[1][0]):
                    #2nd tier priority: lower minute if same distance
                    self.queue.insert(idx, (pri, item))
                    return                     
        self.queue.append((pri, item))
    def dequeue(self):
        it = self.queue.pop(0)
        return it[1]    
    def get_len(self):
        return len(self.queue)
        
def get_dist(cur, base):
    return abs(cur[0]-base[0]) + abs(cur[1] - base[1])
blz_tup = [] # entry = (dir,x,y) tuple for blz location
start = (None, None)
valley_size = (None, None)
with open("day24_input.txt") as f:
    lines = f.readlines()
    # pre-build extra spaces around input so I don't have to worry about expansion...
    # add number of rounds to edges so even if an elf go straight it won't go OB
    # cheated that for pt1, still have to do proper expansion for pt2...    
    for yidx, l in enumerate(lines):        
        line = l.rstrip()        
        valley_size = (len(line), len(lines))
        for xidx, c in enumerate(line):
            if(yidx == 0 and c=='.'):
                start = (xidx, yidx)
            elif(yidx == len(lines)-1 and c=='.'):
                end = (xidx, yidx)
            if(c != '.' and c != '#'):
                # got blizzard
                blz_tup.append((c, xidx, yidx))

print(len(blz_tup))
#beginning
state_pq = PriorityQueue() # priority is distance from start: farther is higher pri
death_moves = [] #each entry is (minute, cur_loc). that combo can't move, and will be blown away for staying
solved_moves = [] #each entry is (minute, cur_loc). that combo can't move, and will be blown away for staying
min_minute = 999999999 #better be out before this...
course_dist = abs(end[0]-start[0]) + abs(end[1] - start[1])
state_pq.enqueue(0, (0, start, blz_tup))
blz_dict = {} #key=minute, value = list of blz locations at that minute
blz_loc_dict = {} #key=minute
blz_dict[0] = blz_tup
while state_pq.get_len() > 0:
    cur_min, cur_loc, cur_blz = state_pq.dequeue()    
    # print("Solving min {} - loc {}".format(cur_min, cur_loc))
    if(cur_min > min_minute):
        # print("Already slower than another solution, give up...")
        continue
    elif(get_dist(cur_loc, end) > (min_minute-cur_min)):
        # print("too far from exit even without blz, give up...")
        continue
    elif((cur_min, cur_loc) in death_moves):
        # print("this min/loc combo is a known death trap, give up...")
        continue
    elif((cur_min, cur_loc) in solved_moves):
        # print("this min/loc combo have been solved, move on...")
        continue
    new_blz = []
    blz_locs = {} #key = loc, value = # of blzs
    if cur_min+1 in blz_dict.keys():
        new_blz = blz_dict[cur_min+1]
        blz_locs = blz_loc_dict[cur_min+1]
    else:
        for b in cur_blz:
            new_x = b[1]
            new_y = b[2]
            if b[0] == '>':
                new_x += 1
                if(new_x == valley_size[0]-1):
                    new_x = 1            
            elif b[0] == '<':
                new_x -=1
                if(new_x == 0):
                    new_x = valley_size[0]-2            
            elif b[0] == '^':
                new_y -= 1
                if(new_y == 0):
                    new_y = valley_size[1]-2            
            elif b[0] == 'v':
                new_y += 1
                if(new_y == valley_size[1]-1):
                    new_y = 1            
            new_blz.append((b[0], new_x, new_y))
            if((new_x,new_y) in blz_locs.keys()):
                blz_locs[(new_x,new_y)] += 1
            else:
                blz_locs[(new_x,new_y)] = 1
        blz_dict[cur_min+1] = new_blz
        blz_loc_dict[cur_min+1] = blz_locs
    
    #now see if we can move to a place
    next_x, next_y = cur_loc
    avail_move = [True, True, True, True, True] #s/u/d/l/r
    #we could wait it out if blz doesn't come to us. would a blz blow into start position?
    if((next_x, next_y) in blz_locs.keys()):
        # print("Staying would run into blz - not staying")
        avail_move[0] = False
    else:
        if (cur_min+1, (next_x, next_y)) in death_moves:
            avail_move[0] = False #don't think we'll get here, but just for uniformity
        else:
            state_pq.enqueue(get_dist((next_x, next_y), start) ,(cur_min+1, (next_x, next_y), new_blz))

    #or we could move up(if we aren't at start)
    next_x, next_y = cur_loc[0], cur_loc[1]-1
    if(cur_loc[1] == 0):
        #start can't move up
        avail_move[1] = False
        None
    else:
        if(next_y == 0 and next_x == start[0]):
            #back to beginning
            if (cur_min+1, (next_x, next_y)) not in death_moves:
                state_pq.enqueue(get_dist((next_x, next_y), start) ,(cur_min+1, (next_x, next_y), new_blz))            
        elif next_y<=0:
            # print("moving up would run into north wall")
            avail_move[1] = False
            None    
            # Do nothing. can't go to row 0 except back to start
        else:
            # see if the place is occupied
            if((next_x, next_y) in blz_locs.keys()):
                # print("Moving up to {} would run into blz - not going there".format((next_x, next_y)))
                avail_move[1] = False
                None            
            else:
                if (cur_min+1, (next_x, next_y)) in death_moves:
                    avail_move[1] = False
                else:
                    state_pq.enqueue(get_dist((next_x, next_y), start) ,(cur_min+1, (next_x, next_y), new_blz))                
    #down
    next_x, next_y = cur_loc[0], cur_loc[1]+1
    if((next_x, next_y) == end):
        print("Got to exit! we're done after ", cur_min+1, " minutes")
        if(cur_min+1 < min_minute):
            print("New record! {} minutes".format(cur_min+1))
            min_minute = cur_min+1
            continue
    elif next_y == valley_size[1]-1:
        # print("moving down would run into south wall")
        avail_move[2] = False
        None
    else:
        if((next_x, next_y) in blz_locs.keys()):
            # print("Moving down to {} would run into blz - not going there".format((next_x, next_y)))
            avail_move[2] = False
            None            
        else:
            if (cur_min+1, (next_x, next_y)) in death_moves:
                avail_move[2] = False
            else:
                state_pq.enqueue(get_dist((next_x, next_y), start) ,(cur_min+1, (next_x, next_y), new_blz))            
    #left
    next_x, next_y = cur_loc[0]-1, cur_loc[1]
    if cur_loc==start: # start can't move left
        avail_move[3] = False
        None 
    else:
        if next_x == 0:
            # print("moving left would run into west wall")
            avail_move[3] = False
            None
        else:
            if((next_x, next_y) in blz_locs.keys()):
                # print("Moving left to {} would run into blz - not going there".format((next_x, next_y)))
                avail_move[3] = False
                None            
            else:
                if (cur_min+1, (next_x, next_y)) in death_moves:
                    avail_move[3] = False
                else:
                    state_pq.enqueue(get_dist((next_x, next_y), start) ,(cur_min+1, (next_x, next_y), new_blz))                
    #right
    next_x, next_y = cur_loc[0]+1, cur_loc[1]
    if cur_loc == start:
        avail_move[4] = False
        None # start can't move right
    else:
        if next_x == valley_size[0]-1:
            # print("moving right would run into east wall")
            avail_move[4] = False
            None
        else:
            if((next_x, next_y) in blz_locs.keys()):
                # print("Moving right to {} would run into blz - not going there".format((next_x, next_y)))
                avail_move[4] = False
                None            
            else:
                if (cur_min+1, (next_x, next_y)) in death_moves:
                    avail_move[4] = False
                else:
                    state_pq.enqueue(get_dist((next_x, next_y), start) ,(cur_min+1, (next_x, next_y), new_blz))                
    # now check if we are about to be blown away
    # print("Possible move: s/u/d/l/r = ", avail_move)
    if(avail_move.count(True) == 0):
        # print("We're dead - log the minute and location for future generations...")
        death_moves.append((cur_min, cur_loc))
    solved_moves.append((cur_min, cur_loc))
    

print("fewest minutes used = ", min_minute)

