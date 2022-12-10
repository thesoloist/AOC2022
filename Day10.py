import re
with open("day10_input.txt") as f:
    lines = f.readlines()

cycle_cnt = 1
reg_val = 1
next_check_cycle = 20
total_sig_strength = 0

crt_screen = [["." for j in range(40)] for i in range(6)]

def draw(cycle_cnt, reg_val):
    crt_row = int((cycle_cnt-1)/40)
    crt_loc = (cycle_cnt-1)%40
    if(abs(reg_val - crt_loc) <= 1):
        crt_screen[crt_row][crt_loc] = "#"
    else:
        crt_screen[crt_row][crt_loc] = "."
    print("Drawing {} at row {} loc {}".format(crt_screen[crt_row][crt_loc], crt_row, crt_loc))

for line in lines:
    result = re.match(r'(\w{4})', line)
    if result:
        op = result.group(1)
        arg = 0
        if op == "addx":
            result = re.match(r'\w{4} (-?\d+)', line)
            arg = int(result.group(1))
        #print("Got OP = {}, arg = {}".format(op, arg))
        if op == "noop":
            draw(cycle_cnt, reg_val)            
            cycle_cnt += 1            
        elif op == "addx":
            if cycle_cnt+1 == next_check_cycle:                
                total_sig_strength += reg_val * next_check_cycle
                next_check_cycle += 40
                print("Crossing boundary mid-cycle, use current reg val {} - updated sig = {}".format(reg_val, total_sig_strength))
            draw(cycle_cnt, reg_val)
            draw(cycle_cnt+1, reg_val)
            reg_val += arg            
            cycle_cnt += 2
        print("updated reg_val = {}, now at beginning of cycle {}".format(reg_val, cycle_cnt))
        if cycle_cnt == next_check_cycle:            
            total_sig_strength += reg_val * next_check_cycle
            next_check_cycle += 40
            print("at check cycle {}, regval {} - updated sig = {}".format(cycle_cnt, reg_val, total_sig_strength))
print("Total sig strength = {}".format(total_sig_strength))
for row in crt_screen:
    print("".join(row))
            
        
