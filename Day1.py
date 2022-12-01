def Day1_1():
    with open("Day1_input.txt") as f:    
        max_cal = 0
        cur_cal = 0
        lines = f.readlines()
        for line in lines:        
            # print(line)
            if line == "\n":
                if(cur_cal >= max_cal):
                    max_cal = cur_cal                                    
                cur_cal = 0
            else:
                cur_cal = cur_cal + int(line)
                # print("Cur cal now = ", cur_cal)
    # print("Max cal = ", max_cal)

def Day1_2():
    with open("Day1_input.txt") as f:
        elf_cals = []
        cur_cal = 0
        lines = f.readlines()
        for line in lines:        
            # print(line)
            if line == "\n":
                if(len(elf_cals) < 3):
                    elf_cals.append(cur_cal)
                    elf_cals.sort()
                else:
                    if(cur_cal >= elf_cals[0]):
                        elf_cals.append(cur_cal)
                        elf_cals.pop(0)
                        elf_cals.sort()
                print(elf_cals)
                cur_cal = 0
            else:
                cur_cal = cur_cal + int(line)
        print("Top 3 elves total calories = ", sum(elf_cals))
Day1_2()
        
        
