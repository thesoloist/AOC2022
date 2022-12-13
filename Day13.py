import re

def parse_line(l):
    arr = []
    my_l = l
    while len(my_l):
        if(my_l[0]=='['):
            item, my_l = parse_line(my_l[1:])
            arr.append(item)
        elif(my_l[0]==']'):
            my_l = my_l[1:]
            return (arr, my_l)
        elif(my_l[0]==','):
            my_l = my_l[1:]
            continue            
        else:
            result = re.match(r'^(\d+)', my_l)
            if result:
                arr.append(int(result.group(1)))
                my_l = my_l[result.span()[1]:]
                
    return (arr, my_l)

def parse_input(fn):
    arr_input = []
    with open(fn) as f:        
        lines = [x.rstrip() for x in f.readlines()]
        for l in lines:
            if l:
                line, left = parse_line(l[1:-1])
                arr_input.append(line)
    return arr_input            

def compare_list(left, right):
    for i in range(min(len(left), len(right))):
        li = left[i]
        ri = right[i]
        if(type(li)==int and type(ri)==int):
            if(li < ri):
                return True
            elif(li > ri):
                return False
        elif(type(li) is list and type(ri) is list):
            result = compare_list(li, ri)
            if(result != None):
                return result
        else:
            if type(li)==int:
                lis = [li]
            else:
                lis = li
            if type(ri)==int:
                ris = [ri]
            else:
                ris = ri
            result = compare_list(lis,ris)
            if(result != None):
                return result
    # if at this point still can't decide, then if left is shorter
    if(len(left) == len(right)):
        return None
    else:
        return (len(left) < len(right))   

def part1(input_arr):    
    idx = 1
    idx_sum = 0
    while len(input_arr):
        left = input_arr[0]
        right = input_arr[1]
        input_arr = input_arr[2:]
        print("Comparing {} against {} -> ".format(left, right), end='')
        result = compare_list(left, right)
        print(result)
        if(result == True):
            print("Pair {} shows right order".format(idx))
            idx_sum += idx        
        idx += 1                
    print("Sum of valid pair indexes = ", idx_sum)

def get_first_item(lst):    
    if len(lst)==0:
        return '-1'
    else:       
        if type(lst[0])==list:
            return get_first_item(lst[0])
        else:
            return str(lst[0])    

def part2(input_arr):
    first_dict = {}
    for i in input_arr:
        first = get_first_item(i)
        print("getting first item from {} -> {}".format(i, first))
        if first in first_dict.keys():
            first_dict[first].append(i)
        else:
            first_dict[first] = [i]
        print(first_dict[first])
    fd_keys = [int(x) for x in first_dict.keys()]
    fd_keys.sort()
    print(fd_keys)
    idx = 1
    tgt = [2,6]
    idx_prd = 1
    for k in fd_keys:
        if k in tgt:
            idx_prd *= idx        
        idx += len(first_dict[str(k)])
        print("After fd key {}, idx now at {}, idx_prd at {}".format(k, idx, idx_prd))
    #print("index 2/6 = {}/{}".format(div2_idx, div6_idx))
    return idx_prd

arr = parse_input("day13_input.txt")
#[print(a) for a in arr]
#part1(arr)
div_arr = arr + [[[2]]] + [[[6]]]
[print(a) for a in div_arr]
result = part2(div_arr)
print("div index product = ", result)

