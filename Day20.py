input_dict = {} # key = value, value=[idx in input array] 
input_tuple = [] #entry is (input value, occurance)
with open("day20_input.txt") as f:
    ls = f.readlines()
    input = list(map(int, ls))    
    uniq_input = list(set(input))
    if len(input)==len(uniq_input):
        print("input is unique")
    else:
        print("input is not unique: input size {} uniq size {}".format(len(input), len(uniq_input)))
        # for i in input:
        #     if input.count(i) > 1:
        #         print("Got {} more than once".format(i))
    # print("max/min of list =", max(input), min(input))

    for idx, i in enumerate(input):
        if(i not in input_dict.keys()):
            input_dict[i] = [idx]
        else:
            input_dict[i].append(idx)
        input_tuple.append((i, len(input_dict[i])-1))

# print(input)
#print(input_tuple)

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
    input_tuple = [(a * 811589153, b) for a,b in input_tuple]

state = input_tuple.copy()

rounds = 10 if pt2 else 1
for round in range(rounds):
    print("Start mixing round ", round+1)
    for mv in range(len(input_tuple)):
        my_tgt_idx = state.index(input_tuple[mv])
        # print("current state {}: moving value {}, currently at state[{}], moving {} places to the right".format(state, input[mv], my_tgt_idx, input[mv]))
        if(input_tuple[mv][0] == 0):
            continue
        state = barrel_rshift(state, -my_tgt_idx)
        # print("  state shifted to ", state)

        # Need to consider the magnitude: if value is larger than input size, shrink until it's within       
        my_mag_check = (input_tuple[mv][0] % (len(state)-1)) if input_tuple[mv][0] > 0 else (input_tuple[mv][0] % (len(state)-1)) - (len(state)-1)

        my_mag = (input_tuple[mv][0] % (len(state)-1)) if input_tuple[mv][0] > 0 else (input_tuple[mv][0] % (len(state)-1)) - (len(state)-1)

        if((input_tuple[mv][0] % (len(state)-1)) == 0):
            print("WARNING: input {} is intg multiple of (len(state)-1), leading to my_mag = {}".format(input[mv], my_mag))
        # my_mag = input[mv]
        # while(abs(my_mag) >= len(state)-1):
        #     if my_mag > 0:
        #         my_mag -= len(state)-1
        #     else:
        #         my_mag += len(state)-1

        # print("  shifiting state[0] by ", my_mag, " from ", input[mv], ", check = ", my_mag_check)
        if(my_mag > 0):
            state = state[1:1+my_mag] + [input_tuple[mv]] + state[my_mag+1:]
        else:
            state = state[1:(len(state)+my_mag)] + [input_tuple[mv]] + state[len(state)+my_mag:]
        # print("  state moved   to ", state)
    # shift (0,0) to first of state. Assuming input has only one entry of 0
    state = barrel_rshift(state, len(state) - state.index((0,0)))
    #print("state after round {} and 0-shift: {}".format(round+1, state))
# print("state after 0-shift: {}".format(state))
print("1000th / 2000th / 3000th value = {} {} {}, sum={}".format(state[1000%len(state)], state[2000%len(state)], state[3000%len(state)],
                                                                 state[1000%len(state)][0]+state[2000%len(state)][0]+state[3000%len(state)][0]))