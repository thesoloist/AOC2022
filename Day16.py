import re,copy

class Valve:
    def __init__(self, name) -> None:
        self.n = name
        self.r = 0 #flowrate
        self.v = False # True = Open
        self.t = []        

def print_map(valve_map):
    cls_cnt = 0
    for v in valve_map:
        print("Valve {} is {}, flows {}, tunnels to {}".format(v.n, "OPEN" if v.v else "CLOSED", v.r, v.t))
        if v.v:
            cls_cnt += 1
    print("Total valve cnt = {}, Closed valve cnt = {}".format(len(valve_map), cls_cnt))

def copy_map(src_map):
    return copy.deepcopy(src_map)

def get_closed_valves(valve_map):
    cv = []
    for v in valve_map:
        cv.append(v.n) if v.v==False else None
    return cv

def get_valve(name, valve_map):
    items = [ x for x in valve_map if x.n==name ]
    return items[0] #assuming unique valves

def get_tunnels(vn, valve_map):
    return get_valve(vn, valve_map).t

def get_map_drain(v_map):
    s = 0
    for v in v_map:
        s += v.total_drain
    return s

valve_map = []

with open("day16_input.txt") as f:
    while True:
        l = f.readline().rstrip()
        if not l:
            break
        res = re.match(r'Valve (\w+) .+ rate=(\d+).+valves? (.+)', l)
        if res:
            valve_map.append(Valve( res.group(1)))
            valve_map[-1] = Valve(res.group(1))            
            valve_map[-1].r = int(res.group(2))
            if(valve_map[-1].r == 0):
                valve_map[-1].v = True # flow-less valve should be considered open - to save some checking maybe?
            ts = res.group(3).split(' ')
            for t in ts:
                valve_map[-1].t.append(t.rstrip(','))
            # parse tunnels
            
print_map(valve_map)

def djikstra(valve_map, src_val):    
    val_names = [x.n for x in valve_map]
    shortest_path = {}
    prev_nodes = {}
    max_val = 99999999999999
    for v in val_names:
        shortest_path[v] = max_val
        shortest_path[src_val] = 0
    while val_names:
        cmin_v = None
        for v in val_names:
            if cmin_v == None:
                cmin_v = v
            elif(shortest_path[v] < shortest_path[cmin_v]):
                cmin_v = v
        neighbors = get_tunnels(cmin_v, valve_map)
        for n in neighbors:
            tval = shortest_path[cmin_v]+1
            if tval<shortest_path[n]:
                shortest_path[n] = tval
                prev_nodes[n] = cmin_v
        val_names.remove(cmin_v)
    return(prev_nodes, shortest_path)

def get_path(v_map, src, dst):
    prev_nodes, shortest_path = djikstra(v_map, src)
    path = []
    node = dst
    while node != src:
            path.append(node)
            node = prev_nodes[node]
    # print("Path from {} to {} backwards: {}, len = {}".format(src, dst, path, len(path)))
    path.append(src)
    return path

def build_djikstra_map(valve_map):
    for v in valve_map:        
        djikstra_map[v.n] = {}
        prev, distances = djikstra(valve_map, v.n)
        for d in valve_map:
            djikstra_map[v.n][d.n] = distances[d.n]
    

cur_val = "AA"
time_limit = 30

djikstra_map = {} #key = src, value = dict(key=dst, val=dist)
possible_routes = []

def build_possible_routes(time_limit, v_map, cur_val, route):    
    # try going for each and see what can we do until time runs out
    print("Looking for best next move with time left = {}, cur_val = {}, path = {}".format(time_limit, cur_val, route))
    if not get_closed_valves(v_map):
        print("No more closed valves! path = {}".format(route))
        possible_routes.append(route) if route not in possible_routes else None
    else:
        for cv in get_closed_valves(v_map):        
            time_cost = djikstra_map[cur_val][cv] + 1 #add one for opening
            print("Shortest path cost to {} from {} = {}".format(cv, cur_val, time_cost))
            pushed = False
            if(time_cost > time_limit):
                print("not enough time(need {} against {}) to open {} from {}".format(time_cost, time_limit, cv, cur_val))
                if not pushed:                    
                    if route not in possible_routes:
                        print("Pusing route ", route) 
                        possible_routes.append(route) 
                        pushed = True
            else:            
                #print("Opened valve {}, Trying further...".format(cv))
                new_map = copy_map(v_map)
                get_valve(cv, new_map).v = True
                if(time_limit - time_cost > 2): # need at least 1m to move and 1m to open
                    build_possible_routes((time_limit - time_cost), new_map, cv, str.format("{}{}-", route, cv))
                else: #don't bother trying, push here                    
                    nr = str.format("{}{}-", route, cv)
                    if nr not in possible_routes:
                        print("Pusing last step here:", nr)
                        possible_routes.append(nr) 
                        pushed = True
                        

 
        
       
    
        
                    
#approach: find out all the valve paths we can hit within 30m, and calculate each path
build_djikstra_map(valve_map)
build_possible_routes(time_limit, valve_map, cur_val, "")
print("Possible routes cnt = ", len(possible_routes))
max_drain = 0
for r in possible_routes:
    # print("Pricing route {}".format(r))
    valves = r.rstrip('-').split('-')
    time_left = time_limit
    drain_val = 0
    start_val = "AA"
    for idx, v in enumerate(valves):
        end_val = v
        time_taken = djikstra_map[start_val][end_val] + 1 #add one for opening
        time_left -= time_taken
        drain_val += (time_left) * get_valve(v, valve_map).r        
        start_val = v
    if(drain_val > max_drain):        
        max_drain = drain_val
        print("Max drain path = {} for val {}".format(r, drain_val))


    

# Follow this approach:
# if no closed valves: we're done. return accumulation value
# else: for each closed valve, find shortest path of cur->valve. calculate oppo cost = (path_length + 1 for opening it)*(sum(flow of all other closed valve))
#       go for the lowest oppo cost valve and open it
# total_drain = 0
# while time_left > 0:
#     # build shortest paths with djikstra
#     prev_nodes, shortest_path = djikstra(valve_map, cur_val)
#     lowest_opp_cost = 9999999999999999999
#     lowest_node = ""
#     lowest_opp_length = 0
#     lowest_next_node = ""
#     lowest_node_gain = 0
#     for cls_val in get_closed_valves(valve_map):
#         p = get_path(prev_nodes, shortest_path, cur_val, cls_val)                
#         sum_flow = 0
#         for o in get_closed_valves(valve_map):
#             sum_flow += get_valve(o, valve_map).r
#             print("    adding flow of {} = {} as opp cost".format(o, get_valve(o, valve_map).r))
#         opp_cost = sum_flow * (len(p)+1)
#         opp_gain = (time_left - (len(p)+1))*get_valve(cls_val, valve_map).r
#         print("  Opening {} from {} takes {} min, has opp cost {}, can gain {} - net {}".format(cls_val, cur_val, len(p)+1, opp_cost, opp_gain, opp_gain - opp_cost))
#         if (opp_cost < lowest_opp_cost) or ((opp_cost == lowest_opp_cost) and (opp_gain > lowest_node_gain)):
#             lowest_node = cls_val
#             lowest_opp_cost = opp_cost
#             lowest_opp_length = len(p)+1
#             lowest_next_node = p[-1] if len(p) else cls_val
#             lowest_node_gain = opp_gain        
            
#     if(lowest_node == cur_val):
#         print("Opening node {} seems to be optimal".format(lowest_node))
#     else:
#         print("Going to node {} seems to be optimal, cost {} minutes to travel+open, next step {}".format(lowest_node, lowest_opp_length, lowest_next_node))
#     # Only move 1 step towards that?
#     time_left -= 1
#     # if optimal path is ourselves, open ourself, and add total drain up
#     if lowest_node == cur_val:
#         get_valve(cur_val, valve_map).v = True
#         total_drain += get_valve(lowest_node, valve_map).r * time_left
#         cur_val = lowest_node
#     else:
#         cur_val = lowest_next_node

