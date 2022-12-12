import re

class Monkey:
    def __init__(self) -> None:
        self.id = 0
        self.items = []
        self.op = ""
        self.test_div = 0
        self.tgt_true = 0
        self.tgt_false = 0
        self.processed = 0
    
    def throw_one(self, worried):
        item = self.items.pop(0)
        self.processed += 1
        # print("before play: item value = {}".format(item))
        if self.op[0] == "+":
            item += int(self.op[1:])
        elif self.op[0] == "*":
            item *= int(self.op[1:])
        elif self.op[0] == "^":
            for i in range(int(self.op[1:]) - 1):
                item *= item
        # print("After play: item value = {}".format(item))
        if not worried:
            item = int(item / 3)        
        # print("Before check: item value = {}, test_div = {}".format(item, self.test_div), end="")
        if((item % self.test_div) == 0):
            # print(" - Test passed, Throwing to Monkey {}".format(self.tgt_true))
            return (item, self.tgt_true)
        else:
            # print(" - Test failed, Throwing to Monkey {}".format(self.tgt_false))
            return (item, self.tgt_false)
        #returns tuple (updated item factor, target)

Monkeys = []
with open("day11_input.txt") as f:
    lines = f.readlines()
    m_id = 0    
    for l in lines:
        if not l:
            m_id += 1
        else:
            result = re.match(r'^Monkey (\d):', l)
            if result:
                # print("New Monkey")
                Monkeys.append(Monkey())                
                Monkeys[-1].id = result.group(1)
                continue                                    
            result = re.match(r'^  Starting items', l)
            if result:
                items = re.findall(r'\d+', l)
                Monkeys[-1].items = [int(x) for x in items]
                # print("Monkey #{} got items {}".format(Monkeys[-1].id, Monkeys[-1].items))
                continue
            result = re.match(r"^  Operation: new = old (.) (\w+)", l)
            if result:
                if result.group(1) == "*" and result.group(2) == "old":
                    Monkeys[-1].op = "^2"
                else:
                    Monkeys[-1].op = "{}{}".format(result.group(1), result.group(2))
                # print("Monkey #{} got OPcode {}".format(Monkeys[-1].id, Monkeys[-1].op))
                continue
            result = re.match(r"^  Test: divisible by (\d+)", l)
            if result:
                Monkeys[-1].test_div = int(result.group(1))
                # print("Monkey #{} got test_div {}".format(Monkeys[-1].id, Monkeys[-1].test_div))
                continue
            result = re.match(r'^    If true: throw to monkey (\d+)', l)
            if result:                
                Monkeys[-1].tgt_true = int(result.group(1))
                continue
            result = re.match(r'^    If false: throw to monkey (\d+)', l)
            if result:                
                Monkeys[-1].tgt_false = int(result.group(1))
                continue
            # print("Monkey #{} got throw true/false = {}/{}".format(Monkeys[-1].id, Monkeys[-1].tgt_true, Monkeys[-1].tgt_false))

max_common = 1
for m in Monkeys:
    max_common *= m.test_div
print("Maximum common = {}".format(max_common))
rnd = 0
rnd_cnt = 10000
worried = True
while True:    
    for m in Monkeys:
        for i in range(len(m.items)):
            (new_i, tgt) = m.throw_one(worried)            
            #if worried and target is doing multiply, just pass on the mod part to new monkey
            if worried:
                new_i = new_i % max_common
            # print("Monkey {} throws a item worth {} to Monkey {}".format(m.id, new_i, tgt))
            Monkeys[tgt].items.append(new_i)
    rnd += 1
    # print("Finished round #{}".format(rnd))    
    if (rnd==1 or rnd==20 or rnd%1000==0):
        for m in Monkeys:
            print("Rnd {} - Monkey {} processed {} items, now list = {}".format(rnd, m.id, m.processed, m.items))
    if rnd == rnd_cnt:
        #Count monkey business        
        biz = []
        for m in Monkeys:
            print("Monkey {} processed {} items".format(m.id, m.processed))
            biz.append(m.processed)
        biz.sort()
        print(biz)
        print("product of Top 2 biz = {}".format(biz[-1]*biz[-2]))
        break

                


