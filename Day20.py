with open("day20_sample.txt") as f:
    ls = f.readlines()
    input = list(map(int, ls))    
    uniq_input = list(set(input))
    if len(input)==len(uniq_input):
        print("input is unique")
    else:
        print("input is not unique: input size {} uniq size {}".format(len(input), len(uniq_input)))
    print("max/min of list =", max(input), min(input))
# print(input)

def barrel_rshift(input, amt):  
    rs_amt = amt % len(input)
    if rs_amt == 0:
        return input.copy()
    rs_amt = rs_amt if rs_amt > 0 else len(input)+rs_amt
    new_l = input[-rs_amt:]
    new_r = input[0:len(input)-rs_amt]
    output = new_l + new_r    
    return output



pt2 = True
if(pt2):
    input = [i * 811589153 for i in input]

state = input.copy()
print(input)
state = barrel_rshift(state, 3)
print(state)
state = barrel_rshift(state, -3)
print(state)
state = barrel_rshift(state, len(state)-1)
print(state)
state = barrel_rshift(state, -(len(state)-1))
print(state)
state = barrel_rshift(state, len(state))
print(state)
state = barrel_rshift(state, -(len(state)))
print(state)
state = barrel_rshift(state, len(state)+1)
print(state)
state = barrel_rshift(state, -(len(state)+1))
print(state)

rounds = 10 if pt2 else 1
for round in range(rounds):
    print("Start mixing round ", round+1)
    for mv in range(len(input)):
        my_tgt_idx = state.index(input[mv])        
        # print("current state {}: moving value {}, currently at state[{}], moving {} places to the right".format(state, input[mv], my_tgt_idx, input[mv]))
        if(input[mv] == 0):
            continue
        state = barrel_rshift(state, -my_tgt_idx)
        # print("  state shifted to ", state)

        # Need to consider the magnitude: if value is larger than input size, shrink until it's within
        my_mag_check = (input[mv] % (len(state)-1))

        # my_mag  = (input[mv] % (len(state)-1))
        my_mag = input[mv]
        while(abs(my_mag) >= len(state)-1):
            if my_mag > 0:
                my_mag -= len(state)-1
            else:
                my_mag += len(state)-1

        print("  shifiting state[0] by ", my_mag, " from ", input[mv], ", check = ", my_mag_check)
        if(my_mag > 0):
            state = state[1:1+my_mag] + [input[mv]] + state[my_mag+1:]
        else:
            state = state[1:(len(state)+my_mag)] + [input[mv]] + state[len(state)+my_mag:]
        # print("  state moved   to ", state)
        #roll my target to [0] if positive, 
    state = barrel_rshift(state, len(state) - state.index(0))
    print("state after round {} and 0-shift: {}".format(round+1, state))
# print("state after 0-shift: {}".format(state))
print("1000th / 2000th / 3000th value = {} {} {}, sum={}".format(state[1000%len(state)], state[2000%len(state)], state[3000%len(state)],
                                                                 state[1000%len(state)]+state[2000%len(state)]+state[3000%len(state)]))