
def seen_val(self, grid, x, y, side):
    # 0=north 1=west 2=south 3=east
    self.seen = True

    return self.seen
grid = []
with open("day8_input.txt") as f:
    while True:
        line = f.readline().rstrip()
        if not line:
            break
        else:
            grid.append([int(x) for x in list(line)])
    #print(grid)

# now we have a grid
height = len(grid)
width = len(grid[0])
for l in grid:
    if(width < len(l)):
        width = len(l)
print("Forest size: width = {} height = {}".format(width, height))

visible_cnt = 0
max_scenic_score = 0

part1 = False

for y in range(height):
    max_west = grid[y][0]
    max_east = grid[y][-1]    
    for x in range(width):        
        #see if this point can see out
        scenic_score = 0
        if(x==0 or y==0):
            visible_cnt += 1
            continue
        elif(x==width-1 or y==height-1):
            visible_cnt += 1
            continue
        else:
            scenic_score = 1
            distance = 0
            #check west            
            seen = True
            loop_range = []
            if(part1):
                loop_range = range(x)
            else:
                loop_range = range(x-1,0,-1)
            for dx in loop_range:
                distance += 1
                #print("West - Comparing x/y = {}/{} against {}/{}".format(x,y,dx,y))
                if(grid[y][x] <= grid[y][dx]):
                    seen = False                    
                    break
            if seen:
                visible_cnt +=1
                distance = x
                if(part1): continue
            scenic_score = scenic_score * distance
            #print("West - scenic score so far for x/y={}/{} is {} (dist {})".format(x,y,scenic_score,distance))
            distance = 0            
            #check east
            seen = True
            loop_range = range(x+1, width)            
            for dx in loop_range:
                distance += 1
                #print("East - Comparing x/y = {}/{} against {}/{}".format(x,y,dx,y))
                if(grid[y][x]<= grid[y][dx]):                    
                    seen = False
                    break                
            if seen:
                visible_cnt += 1
                distance = width - x - 1
                if(part1): continue
            scenic_score = scenic_score * distance
            #print("East - scenic score so far for x/y={}/{} is {} (dist {})".format(x,y,scenic_score,distance))
            distance = 0                        
            #check north
            seen = True
            if(part1):
                loop_range = range(y)
            else:
                loop_range = range(y-1,0,-1)
            for dy in loop_range:
                distance += 1
                #print("North - Comparing x/y = {}/{} against {}/{}".format(x,y,dx,y))
                if(grid[y][x]<= grid[dy][x]):
                    seen = False
                    break
            if seen:
                visible_cnt += 1
                distance = y
                if(part1): continue
            scenic_score = scenic_score * distance
            #print("North - scenic score so far for x/y={}/{} is {} (dist {})".format(x,y,scenic_score,distance))
            distance = 0            
            #check south
            seen = True            
            for dy in range(y+1, height):
                distance += 1
                #print("South - Comparing x/y = {}/{} against {}/{}".format(x,y,dx,y))
                if(grid[y][x]<= grid[dy][x]):
                    seen = False
                    break
            if seen:
                visible_cnt += 1
                distance = height - y - 1
                if(part1): continue            
            scenic_score = scenic_score * distance
            #print("South - scenic score so far for x/y={}/{} is {} (dist {})".format(x,y,scenic_score,distance))            
            if(scenic_score > max_scenic_score):
                max_scenic_score = scenic_score
                print("Location x/y = {}/{} has higher score = {}".format(x,y,max_scenic_score))

#print(visible_cnt)




