import re

glbl_hx = 0
glbl_hy = 0
glbl_tx = 0
glbl_ty = 0

def move_h(dir, amt, head_t, tail_t):
    print("Moving head to {} for {}".format(dir, amt))
    my_hx = head_t[0]
    my_hy = head_t[1]
    my_tx = tail_t[0]
    my_ty = tail_t[1]
    for a in range(amt):
        if(dir=="R"):
            my_hx += 1
        elif(dir=="L"):
            my_hx -= 1
        elif(dir=="U"):
             my_hy += 1
        elif(dir=="D"):
            my_hy -= 1
        # now move T based on new H
        
        my_tx, my_ty = move_mark_t(my_hx, my_hy, my_tx, my_ty)
        print("After move: head x/y = {}/{}, tail x/y={}/{}".format(my_hx, my_hy, my_tx, my_ty)) 
    return (my_hx, my_hy), (my_tx, my_ty)

def move_mark_t(hx, hy, tx, ty):
    print("Moving tail x/y={}/{} towards head x/y {}/{}".format(tx,ty,hx,hy))
    #check if need to move at all
    if((abs(hx-tx) <= 1) and (abs(hy-ty) <= 1)):
        print("No need to move")
        return tx, ty
    else:
        if((hx != tx) and (hy != ty)):            
            print("Need to move diagonally to catch up!")
            if(hx>tx):
                tx += 1
            else:
                tx -= 1
            if(hy > ty):
                ty += 1
            else:
                ty -= 1
        elif(abs(hx-tx) == 2): # move horiz
            print("Need to move horiz to catch up!")
            if(hx>tx):
                tx += 1
            else:
                tx -= 1
        elif(abs(hy-ty) == 2): #move vert
            print("Need to move vert to catch up!")
            if(hy > ty):
                ty += 1
            else:
                ty -= 1
        print("new tail at x/y {}/{}".format(tx,ty))
        # log new position
        if((tx,ty) not in t_trail):
            t_trail.append((tx,ty))
        return tx, ty    

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
    (glbl_hx, glbl_hy), (glbl_tx, glbl_ty) = move_h(m[0], m[1], (glbl_hx, glbl_hy), (glbl_tx, glbl_ty))
    print("After line: head x/y = {}/{}, tail x/y={}/{}".format(glbl_hx, glbl_hy, glbl_tx, glbl_ty))
    print("Tail went through {} points".format(len(t_trail)))