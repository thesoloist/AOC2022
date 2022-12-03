def item_priority(item):
    if(ord(item) < 96): #capital
        return (26 + ord(item) - 64)
    else:
        return (ord(item) - 96)

def part1(line):
    items = list(line)
    dict = {}           
    line_score = 0
    for idx, x in enumerate(items):
        if(idx < (len(line)/2)): # first compartment
            if(x not in dict.keys()):
                dict[x] = 1
        else: # second compartment
            if(x in dict.keys()):
                # Found double. Assuming any further double is the same kind?
                # print("found double = {}".format(x))
                line_score += item_priority(x)
                break
    #print("line score = ", line_score)
    return line_score

def part2(line, dict):
    updated_dict = {}
    items = list(line)
    if(len(dict.keys()) == 0):
        for idx, x in enumerate(items):
            if(x not in dict.keys()):
                updated_dict[x] = 1
    else:
        for idx, x in enumerate(items):
            if(x in dict.keys()):
                updated_dict[x] = 1
    return updated_dict
    

total_priority = 0
total_badge_priority = 0
with open("day3_input.txt") as f:
    line_idx = 0
    badge_dict = {}
    while True:
        line = f.readline().rstrip()
        if line:
            line_score = part1(line)
            total_priority += line_score            
            badge_dict = part2(line, badge_dict)
            line_idx += 1
            if(line_idx == 3):
                # badge_dict should contain only item shared by all 3
                line_idx = 0
                # print(badge_dict.keys())

                total_badge_priority += item_priority(list(badge_dict.keys())[0])
                badge_dict = {}
        else:
            break
    print("total priority (common/badge) = {} / {}".format(total_priority, total_badge_priority))