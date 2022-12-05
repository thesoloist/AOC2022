import re

stacks = []
def set_stack_line(line:str):    
    # print("stack line(len {})={}".format(len(line),line))
    # read 4 chars and match then
    for i in range(0, len(line), 4):
        item = re.search(r'\[(.)\]',line[i:i+4])
        if(len(stacks) <= i/4):
                stacks.append([])
        if(item) :
            #print("Item for stack {} = {}".format(i/4, item.group(1)))            
            stacks[int(i/4)].insert(0,(item.group(1)))
        else:
            #print("No item for stack {}".format(i/4))
            None
            # not match, moving on
    print(stacks)
    return    
def move_line(line):
    match = re.search('move (\d+) from (\d+) to (\d+)', line).groups()
    amt = match[0]
    src = match[1]
    dst = match[2]
    #print("Moving {} from {} to {}".format(amt, src, dst))
    for i in range(int(amt)):
        item = stacks[int(src)-1].pop()
        stacks[int(dst)-1].append(item)
    #print("After moving, stacks look like:")
    #print(stacks)

def move_line_part2(line):
    match = re.search('move (\d+) from (\d+) to (\d+)', line).groups()
    amt = match[0]
    src = match[1]
    dst = match[2]
    # print("Moving {} from {} to {}".format(amt, src, dst))
    items = stacks[int(src)-1][-int(amt):]
    stacks[int(dst)-1] += items
    del stacks[int(src)-1][-int(amt):]
    # print(items)
    # print("After moving, stacks look like:")
    # print(stacks)

with open("day5_input.txt") as f:
    while True:
        line = f.readline()
        if not line:
            break
        if(re.match(r'\[.\]', line)):
            set_stack_line(line)
        elif(re.match(r'move', line)):
            #move_line(line)
            move_line_part2(line)
    for s in stacks:
        print(s[-1], end="")