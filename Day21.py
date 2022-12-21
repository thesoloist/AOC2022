import re
class Monkey:
    def __init__(self, name) -> None:        
        self.name = name
        self.op = None
        self.v1 = None
        self.v2 = None
    
    def set_op(self, opstr):
        res = re.match(r'^(-?\d+)$', opstr)
        if res:
            self.op = None
            self.v1 = int(res.group(1))
        else:
            res = re.match(r'(\w{4}) (.) (\w{4})', opstr)
            if res:
                self.op = res.group(2)
                self.v1 = res.group(1)
                self.v2 = res.group(3)

    def solve(self):
        #print("Solving monkey {}'s problem".format(self.name))
        if self.op == None:
            return self.v1
        else:            
            val1 = monkeys_dict[self.v1].solve()
            val2 = monkeys_dict[self.v2].solve()            
            if(self.op == "+"):
                result = val1 + val2
            elif(self.op == "-"):
                result = val1 - val2
            elif(self.op == "*"):
                result = val1 * val2
            elif(self.op == "/"):
                result = int(val1 / val2)

            # update self so we don't have to calculate again
            self.op = None
            self.v1 = result
            return result

    def has_human_input(self):
        if self.name == "humn":
            return True
        elif self.op == None:
            return False
        else:
            return monkeys_dict[self.v1].has_human_input() or monkeys_dict[self.v2].has_human_input()
    
    def solve_non_human_part(self):
        for v in self.v1, self.v2:
            if(v == "humn"):
                continue
            elif(monkeys_dict[v].has_human_input() == False):
                monkeys_dict[v].solve()
            else:
                monkeys_dict[v].solve_non_human_part()
    
    def check_for_one_operand(self):
        if self.op==None:
            return True
        else:
            return monkeys_dict[self.v1].check_for_one_operand() or monkeys_dict[self.v2].check_for_one_operand()

    def reverse_op(self, exp_val, known_op, known_is_op1):
        if self.op == "+":
            return exp_val - known_op
        elif self.op == "-":
            if(known_is_op1):
                return known_op - exp_val
            else:
                return exp_val + known_op
        elif self.op == "*":
            return int(exp_val / known_op)
        elif self.op == "/":
            if(known_is_op1):
                return int(known_op / exp_val)
            else:
                return exp_val * known_op

    def reverse_solve_for_human(self, exp_val, steps):
        # print("we're {} deep trying to find human".format(steps))
        if monkeys_dict[self.v1].name == "humn":
            hmval = self.reverse_op(exp_val, monkeys_dict[self.v2].v1, False)
            print("Human value (op1) should be ", hmval)
            return hmval
        elif monkeys_dict[self.v2].name == "humn":
            hmval = self.reverse_op(exp_val, monkeys_dict[self.v1].v1, True)
            print("Human value (op2) should be ", hmval)
            return hmval
        else:
            #check which of my 2 ops is unknown
            if monkeys_dict[self.v1].op == None:
                return monkeys_dict[self.v2].reverse_solve_for_human(self.reverse_op(exp_val, monkeys_dict[self.v1].v1, True), steps+1)
            elif monkeys_dict[self.v2].op == None:
                return monkeys_dict[self.v1].reverse_solve_for_human(self.reverse_op(exp_val, monkeys_dict[self.v2].v1, False), steps+1)
            


monkeys_dict = {}
with open("day21_input.txt") as f:
    while True:
        l = f.readline().rstrip()
        if not l:
            break
        result = re.match(r'(\w{4}): (.+)', l)
        if result:
            name, op = list(result.groups())
            monkeys_dict[name] = Monkey(name)
            monkeys_dict[name].set_op(op)
            if(name == "humn"):
                print("we got a human")
            elif(monkeys_dict[name].v1=="humn"):
                print("we need a human for op1")
            elif(monkeys_dict[name].v2=="humn"):
                print("we need a human for op2")

print("We have ", len(monkeys_dict.keys()), " Monkeys")
#pt1 is one call
#print("pt1 Root answer is ", monkeys_dict["root"].solve())

#pt2 though...
monkeys_dict["root"].solve_non_human_part()
# at this point, for each monkey, there should be only up to 1 arm that's unsolved
if(monkeys_dict["root"].check_for_one_operand()):
    print("Root is properly primed")

if monkeys_dict[monkeys_dict["root"].v1].op == None:
    hmval = monkeys_dict[monkeys_dict["root"].v2].reverse_solve_for_human(monkeys_dict[monkeys_dict["root"].v1].v1, 0)
else:
    hmval = monkeys_dict[monkeys_dict["root"].v1].reverse_solve_for_human(monkeys_dict[monkeys_dict["root"].v2].v1, 0)

print("Need human to shout", hmval)


