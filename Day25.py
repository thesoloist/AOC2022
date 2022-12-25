pen2dec_dict = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
dec2pen_dict = {0: '0', 1: '1', 2: '2', -1: '-', -2: '='}

def pen2dec(pen_str):
    dec_val = 0
    rev_pen = pen_str[::-1]
    for idx, c in enumerate(rev_pen):
        dec_val += 5**idx * pen2dec_dict[c]
    return dec_val

def dec2pen(dec_int):
    mid_dec = abs(dec_int)
    mid_pen_str = "" # each digit is 0-4
    pen_str = ""
    
    while mid_dec != 0:
        mid_pen_str = str(mid_dec%5) + mid_pen_str
        mid_dec = int(mid_dec / 5)
    print("  dec_int = {} -> mid_pen_str = {}".format(dec_int, mid_pen_str))
    
    # now parse each digit. if 3/4, carry 1 up, THEN add carry if needed
    carry_up = False        
    for d in mid_pen_str[::-1]:
        my_carry = False
        my_val = 0
        if d=='3':
            my_carry = True
            my_val = -2
            if carry_up == True:
                my_val += 1
        elif d=='4':
            my_carry = True
            my_val = -1
            if carry_up == True:
                my_val += 1
        elif d=='2':
            if carry_up == True:
                my_carry = True
                my_val = -2
            else:
                my_carry = False
                my_val = 2
        else:
            my_carry = False
            my_val = int(d)
            if carry_up == True:
                my_val += 1
        pen_str = dec2pen_dict[my_val] + pen_str
        carry_up = my_carry
    if carry_up:
        pen_str = '1' + pen_str
    return pen_str

with open("day25_input.txt") as f:
    pen_arr = f.readlines()
    pen_arr = [s.rstrip() for s in pen_arr]

sum_snafu = 0
for p in pen_arr:
    p_dec = pen2dec(p)
    print("SNAFU {} -> decimal {}".format(p, p_dec))    
    print("decimal {} -> SNAFU {}".format(p_dec, dec2pen(p_dec)))
    sum_snafu += p_dec

print("sum_snafu in dec = {}, in SNAFU = {}".format(sum_snafu, dec2pen(sum_snafu)))



