import re

def get_mdist(sen, bea):
    return (abs(sen[0]-bea[0]) + abs(sen[1]-bea[1]))
sensor_dict = {} # key=sensor location, value = closet beacon location

with open("day15_input.txt") as f:
    while True:
        l = f.readline().rstrip()
        if not l:
            break
        result = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): .+ at x=(-?\d+), y=(-?\d+)',l)
        if result:
            sen_loc = (int(result.group(1)), int(result.group(2)))
            bea_loc = (int(result.group(3)), int(result.group(4)))
            sensor_dict[sen_loc] = bea_loc

print("Number of sensors = ", len(sensor_dict))
print(sensor_dict)

def build_ranges(row, incl_beacon):
    ranges = []
    for s in sensor_dict.keys():
        if abs(row - s[1]) < get_mdist(s, sensor_dict[s]):            
            half_width = (get_mdist(s, sensor_dict[s]) - abs(row - s[1]))
            lb = s[0] - half_width
            rb = s[0] + half_width
            if(not incl_beacon):
                if(sensor_dict[s] == (lb, row)):
                    lb += 1
                if(sensor_dict[s] == (rb, row)):
                    rb -= 1            
            # print("Sensor {} (dist {}) touched row {}, adding range {}".format(\
            #     s, get_mdist(s, sensor_dict[s]), row, (lb, rb)))
            ranges.append((lb,rb))
    return ranges

def get_impossible_loc_cnt(row):
    cnt = 0
    ranges = build_ranges(row, False)
    
    
    lb = ranges[0][0]
    rb = ranges[0][1]
    for r in ranges[1:]:
        if r[0] < lb: 
            lb = r[0]
        if r[1] > rb:
            rb = r[1]
        
    for pt in range(lb, rb+1):        
        for r in ranges:
            if(r[0]<=pt<=r[1]):
                cnt += 1
                break        
    return cnt

def scan_for_possible_loc(row, bound):
    x = 0
    ranges = build_ranges(row, True) # include beacon location in coverage
    #print("Checking row ", row, " for possible loc")
    while x<=bound:
        my_x = x
        for r in ranges:
            if(r[0]<=my_x<=r[1]):
                # print("x={} in range of a sensor{}, move out...".format(x, r))
                my_x = r[1]+1
                break
        if my_x != x:
            # print("updating x to ", my_x)
            x = my_x
        else:
            #found possible location
            print("Possible loc at {}/{}".format(x, row))
            return (x, row)
    return None
    
check_row = 2000000
bound = 4000000

#part 1
row_cnt = get_impossible_loc_cnt(check_row)
print("Impossible positions for row {} = {}".format(check_row, row_cnt))

#part 2
for r in range(bound+1):
    if(r % 10000 == 0):
        print("Checking row {} for missing beacon".format(r))
    result = scan_for_possible_loc(r, bound)
    if result:
        print("Frequency = ", result[0] * 4000000 + result[1])
        break
