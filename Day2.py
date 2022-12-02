def rps(line):
    score = 0
    match = line.split()    
    score += my_shape_dict[match[1]]
    print("line = ", line, ", shape score = ", score, ', ', end='')
    match_val = my_shape_dict[match[1]] - elf_shape_dict[match[0]]
    if(match_val == -2 or match_val == 1):
        score += 6
    elif(match_val == 0):
        score += 3
    print("total score = ", score)
    return score

def rps2(line):
    score = 0  
    match = line.split()
    score += (my_shape_dict[match[1]] - 1) * 3
    print("line = ", line, ", match score = ", score, ', ', end='')
    shape = elf_shape_dict[match[0]]
    if(match[1]=="X"):
        shape -= 1
        if(shape==0):
            shape = 3        
    elif(match[1]=="Z"):
        shape += 1
        if(shape==4):
            shape = 1
    score += shape
    print("total score = ", score)
    return score

elf_shape_dict = {"A":1, "B":2, "C":3}
my_shape_dict = {"X":1, "Y":2, "Z":3}

match_score = 0
match_score_2 = 0
with open("day2_input.txt") as f:    
    while True:
        line = f.readline().rstrip()
        if line:
            # match_score += rps(line)
            match_score_2 += rps2(line)
        else:
            break
    print("Total score = ", match_score, " / ", match_score_2)
