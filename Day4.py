import re

def find_encompass(areas):
    if((areas[3] == areas[1]) and (areas[2] == areas[0])):
        print(" - identical sections")
        return 1                        
    if((areas[3] >= areas[1]) and (areas[2] <= areas[0])):
        print(" - Section 2 encompasses section 1")
        return 1
    if((areas[3] <= areas[1]) and (areas[2] >= areas[0])):
        print(" - Section 1 encompasses section 2")
        return 1
    return 0

def find_overlap(areas):
    if(areas[2] > areas[1]):
        print(" - Section 2 overshoots section 1")
        return 0
    if(areas[3] < areas[0]):
        print(" - Section 1 overshoots section 2")
        return 0
    return 1

with open("day4_input.txt") as f:
    encompass = 0
    overlap = 0
    lines = f.readlines()
    for idx, line in enumerate(lines):    
        re_2pairs = re.compile('(\d+)-(\d+),(\d+)-(\d+)')            
        areas =[eval(i) for i in re_2pairs.match(line).groups()]
        print("line {} - {}".format(idx, areas),end='')
        # size1 = int(areas[1]) - int(areas[0])
        # size2 = int(areas[3]) - int(areas[2])

        # if(size1 == size2) :
        #     continue
        # if((size1 < size2) and int(areas[0])>=):
        # encompass += find_encompass(areas)
        overlap += find_overlap(areas)
        print("")
    print("encompass pairs = ", encompass)
    print("overlap pairs = ", overlap)