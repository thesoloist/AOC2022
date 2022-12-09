import re

knot_cnt = 10
knot_x = [0 for i in range(knot_cnt)]
knot_y = [0 for i in range(knot_cnt)]

def chain_move_h(dir, amt, x_arr, y_arr):
    chain_len = len(x_arr)
    print("Moving chain head to {} for {}, chain length {}".format(dir, amt, chain_len))
    for a in range(amt):
        if(dir=="R"):
            x_arr[0] += 1
        elif(dir=="L"):
            x_arr[0] -= 1
        elif(dir=="U"):
            y_arr[0] += 1
        elif(dir=="D"):
            y_arr[0] -= 1
        for i in range(len(x_arr) - 1):
            chain_move_t(i, x_arr, y_arr)
        print("After move, last knot is at x/y={}/{}".format(x_arr[-1], y_arr[-1]))
        if((knot_x[-1], knot_y[-1]) not in t_trail):
            t_trail.append((knot_x[-1], knot_y[-1]))

def chain_move_t(iter, x_arr, y_arr):
    print("Moving knot {}".format(iter+1))
    if((abs(x_arr[iter+1] - x_arr[iter])<=1) and (abs(y_arr[iter+1] - y_arr[iter])<=1)):
        print("No need to move")
        return        
    else:
        if((x_arr[iter] != x_arr[iter+1]) and (y_arr[iter] != y_arr[iter+1])):            
            print("Need to move diagonally to catch up!")
            if(x_arr[iter]>x_arr[iter+1]):
                x_arr[iter+1] += 1
            else:
                x_arr[iter+1] -= 1
            if(y_arr[iter] > y_arr[iter+1]):
                y_arr[iter+1] += 1
            else:
                y_arr[iter+1] -= 1
        elif(abs(x_arr[iter]-x_arr[iter+1]) == 2): # move horiz
            print("Need to move horiz to catch up!")
            if(x_arr[iter]>x_arr[iter+1]):
                x_arr[iter+1] += 1
            else:
                x_arr[iter+1] -= 1
        elif(abs(y_arr[iter]-y_arr[iter+1]) == 2): #move vert
            print("Need to move vert to catch up!")
            if(y_arr[iter] > y_arr[iter+1]):
                y_arr[iter+1] += 1
            else:
                y_arr[iter+1] -= 1
        print("new knot {} at x/y {}/{}".format(iter+1,x_arr[iter+1],y_arr[iter+1]))

moves = []
with open("day9_input.txt") as f:
    while True:
        line = f.readline().rstrip()
        if not line: 
            break
        find = re.match(r'(\w) (\d+)', line)
        moves.append((find.group(1), int(find.group(2))))

print(moves)

t_trail = [(0,0)]
for m in moves:    
    chain_move_h(m[0], m[1], knot_x, knot_y)
    print("After line: head x/y = {}/{}, tail x/y={}/{}".format(knot_x[0], knot_y[0], knot_x[-1], knot_y[-1]))    
print("Tail went through {} points".format(len(t_trail)))