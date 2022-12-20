import re

ingr_lut = {'ore':0, 'clay':1, 'obsidian':2, 'geode':3}

blueprints = []

with open("day19_sample.txt") as f:
    lines = f.readlines()
    for l in lines:
        l = l.rstrip()
        blueprints.append({}) #empty dict
        results = re.findall(r'Each (\w+) robot costs (.+?)\.', l)
        if results:            
            for r in results:            
                blueprints[-1][ingr_lut[r[0]]] = [0,0,0,0]
                ingrs = r[1].split(' and ')
                for i in ingrs:
                    cnt, typ = re.findall(r'(\d+) (\w+)', i)[0]
                    blueprints[-1][ingr_lut[r[0]]][ingr_lut[typ]] = int(cnt)
        #print(blueprints[-1])

def can_build(worker, inv, bp_dict):
    cost = bp_dict[worker]
    cb = True
    for i in range(len(inv)):
        if cost[i] > inv[i]:
            cb = False
            break
    return cb

runtime = 24

for bp in blueprints:

    max_cost = [0,0,0,0]
    for item_idx in bp.keys():
        for idx, ing in enumerate(bp[item_idx]):
            if ing > max_cost[idx]:
                max_cost[idx] = ing

    print("Trying blueprint {}".format(bp))
    progress_state = []
    #(minute, inventory, workers)
    progress_state.append((1, [0,0,0,0], [1,0,0,0]))
    while len(progress_state):
        (cur_min, cur_inv, cur_workers) = progress_state.pop(0)
        
        print("Processing state: cur_min={}, cur_inv={}, cur_workers={}".format(cur_min, cur_inv, cur_workers))
        if(cur_min == runtime):
            print("Time UP: geode cnt = {}".format(cur_inv[ingr_lut['geode']]))
            continue


        #see if we can produce a robot
        for i in range(len(cur_workers)):
            if cur_workers[i] >= max_cost[i]:
                continue # don't make more robot-X than max-cost of X needed by any robot
            has_enough = True
            for r in range(len(cur_inv)):
                if cur_inv[r] < bp[i][r]:
                    has_enough = False
                    break
            if has_enough:
                new_workers = cur_workers.copy()
                pd_inv = cur_inv.copy()
                for r in range(len(cur_inv)):
                    pd_inv[r] -= bp[i][r]
                    pd_inv[r] += cur_workers[r]
                new_workers[i] += 1
                print("building robot ", i)
                progress_state.append((cur_min+1, pd_inv, new_workers))
        # also we can just wait
        new_inv = cur_inv.copy()        
        new_workers = cur_workers.copy()
        for r in range(len(cur_inv)):
            new_inv[r] += cur_workers[r]        
        print("Not building robot")
        progress_state.append((cur_min+1, new_inv, new_workers))
    
