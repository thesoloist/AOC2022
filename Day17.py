import re
shapes = [  [list("..@@@@.")],

            [list("...@..."), 
             list("..@@@.."),
             list("...@...")],

            [list("....@.."), 
             list("....@.."),
             list("..@@@..")],

            [list("..@...."), 
             list("..@...."),
             list("..@...."),
             list("..@....")],

            [list("..@@..."), 
             list("..@@...")] ]

wind = []
wind_cnt = 0
wind_mod_array = []
height_array = []
with open("day17_input.txt")as f:
    wind = list(f.readline().rstrip())

def get_wind():
    global wind_cnt
    global wind #use the global version
    w = wind[0]
    wind = wind[1:] + list(wind[0])
    wind_cnt += 1
    return w

def print_chamber(cha):
    for l in cha:
        for c in l:
            print(c, end="")
        print()    

def fall_chamber(chamber):
    new_chamber = chamber.copy()
    for y in range(len(new_chamber)-1, 0, -1):
        for x in range(len(new_chamber[y])):
            if new_chamber[y][x] == '.' and new_chamber[y-1][x] == '@':
                #swap
                new_chamber[y][x], new_chamber[y-1][x] = new_chamber[y-1][x], new_chamber[y][x]    
    return new_chamber

def move_chamber(chamber, wind, debug=False):
    # move portion of the rock within chamber if possible. chamber height in this function must the height of rock being moved
    ret_chamber = []
    check_str = "#@" if wind=="<" else "@#"
    pat_re = r'\.(\@+)' if wind=='<' else r'(\@+)\.'
    repl_re = r'\1.' if wind=='<' else r'.\1'
    can_move = True
    if debug:
        print("Moving chamber towards {}, chamber now looks like:".format(wind))
        print_chamber(chamber)
    for l in chamber:
        if(check_str in "".join(l)):
            can_move = False
            break
        elif(l[0] == "@" and wind=="<"):
            can_move = False
            break
        elif(l[-1]== "@" and wind==">"):
            can_move = False
            break
    if can_move:
        for l in chamber:
            l_str = "".join(l)
            l_str = re.sub(pat_re, repl_re, l_str)
            ret_chamber.append(list(l_str))
        if debug:
            None
            print("Moved successfully, new chamber looks like:")
            # print_chamber(ret_chamber)
        return ret_chamber
    else:
        # print("Can't move, return original")
        return chamber

def check_stable(chamber):
    # chamber is rock height+1. so chamber[-1] doesn't contain @, only '.'/'-'/'#' 
    # if we have a "#" or "-" below a "@" that's a stable sign
    # print("Checking stable for chamber section shown:")
    # print_chamber(chamber)
    new_chamber = None
    stable = False
    for y in range(len(chamber)-1, 0, -1):
        for x in range(len(chamber[-1])):
            chk_str = chamber[y-1][x] + chamber[y][x]
            if chk_str in ["@#","@-"]:
                # print("chamber xy={}/{} is hindering, stablized".format(x,y))                
                stable = True
                break
        if stable:
            break
    # now that we're stablized, change all @ to #
    if stable:
        new_chamber = []
        for l in chamber:
            l_str = "".join(l)
            l_str = l_str.replace("@", "#")
            new_chamber.append(list(l_str))

    return new_chamber

def find_wind_pattern(wind_mod_array):
    #print("Trying to find a pattern in: ",wind_mod_array)
    for l in range(len(wind_mod_array)):
        patlen = int((len(wind_mod_array)-l) / 2)
        if(patlen == 0):
            continue
        if(wind_mod_array[l:l+patlen] == wind_mod_array[l+patlen:l+patlen*2]):
            print("Found pattern! lead len = {}, patt len = {}".format(l, patlen))
            return l, patlen
            
    return None, None

chamber = [['-' for x in range(7)]]
#print(wind, chamber)

# rocks_needed = 2022
rocks_needed = 1000000000000
rock_cnt = 0

while True:
    # add rock. given the 3 free row of movement, just shift the rock 4 times(3 row + initial fall) before adding to chamber at top
    moved_rock = shapes[rock_cnt%5].copy()
    
    for i in range(4): #
        moved_rock = move_chamber(moved_rock, get_wind())
    chamber = moved_rock + chamber
    # print("Chamber at start of rock {} after initial free rows:".format(rock_cnt))
    # print_chamber(chamber)
    rock_level = 0 # from top
    rock_height = len(shapes[rock_cnt%5])
    while True:
        # check if stable 
        new_chamber = check_stable(chamber[rock_level:rock_level + rock_height + 1])
        if new_chamber:
            chamber[rock_level:rock_level + rock_height + 1] = new_chamber.copy()
            break
        else:
            # print("Free falling continues...")                        
            # rock fall
            chamber[rock_level:rock_level + rock_height + 1] = fall_chamber(chamber[rock_level:rock_level + rock_height + 1])
            rock_level += 1
            # rock shift
            chamber[rock_level:rock_level + rock_height] = move_chamber(chamber[rock_level:rock_level + rock_height], get_wind())
           
    # print("Chamber stablized after {} fall/shifts".format(rock_level))
    # shave the top empty rows    
    while True:
        if "".join(chamber[0]) == '.......':
            chamber = chamber[1:]
        else:
            break
            
    rock_cnt += 1
    # print("Chamber at end of rock {} is {} + {} tall:".format(rock_cnt, shaved_height, len(chamber)-1))
    # print_chamber(chamber)
    #print("At end of rock {}, wind_cnt = {}, mod wind length({}) = {}, height = {}".format(rock_cnt, wind_cnt, len(wind), wind_cnt % len(wind), len(chamber)-1))
    wind_mod_array.append(wind_cnt % len(wind))    
    height_array.append(len(chamber)-1)
    lead_cnt, patt_len = find_wind_pattern(wind_mod_array)
    if patt_len:
        print("Found a pattern! initial cnt = {}, pattern length = {}".format(lead_cnt, patt_len))
        # for i in range(len(wind_mod_array)):
        #     print("cnt: {} -> wm: {} - height {}".format(i, wind_mod_array[i], height_array[i]))
        print("Init part adds {} to height".format(height_array[lead_cnt-1]))
        print("each pattern loop adds {} to height".format(height_array[-1] - height_array[-1-patt_len]))
        loops = int((rocks_needed-lead_cnt) / patt_len)
        leftover = (rocks_needed-lead_cnt) % patt_len
        print("for {} rocks, lead-loopcnt-leftover = {}-{}-{}".format(rocks_needed, lead_cnt, loops, leftover))
        total_height = height_array[lead_cnt-1] + loops * (height_array[-1] - height_array[-1-patt_len])
        for i in range(leftover):
            total_height += height_array[lead_cnt + i] - height_array[lead_cnt + i-1]
        print("therefore, for {} rocks, total height = {}".format(rocks_needed, total_height))
        break
    
    #print("Chamber at end of rock {} is {} + {} tall:".format(rock_cnt, shaved_height, len(chamber)-1))
    if rock_cnt == rocks_needed:
        break

print("FINAL: Chamber at end of rock {} is {} tall".format(rock_cnt, len(chamber)-1))