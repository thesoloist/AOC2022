import re
class file:    
    def __init__(self, size, name) -> None:
        self.name = name
        self.size = size

    def get_size(self):
        return self.size

class dir:
    def __init__(self, name) -> None:
        self.name = name        
        self.subdirs = {}
        self.files = {}

    def add_subdir(self, path_array, name):
        if(path_array == []):
            print("dir name: {} - Adding subdir {}".format(self.name, name))
            self.subdirs[name] = dir(name)
        else:
            tgt_dir = path_array[0]
            if tgt_dir not in self.subdirs.keys():
                self.subdirs[tgt_dir] = dir(tgt_dir)
            new_path_array = path_array.copy() # deep copy
            new_path_array.pop(0)
            print("Calling subdir add_subdir with patharray {}".format("/".join(new_path_array)))
            self.subdirs[tgt_dir].add_subdir(new_path_array,name)        

    def add_file(self, path_array, name, size):
        # if path_array is empty, file is in own directory.
        if(path_array == []):
            print("dir name: {} - Adding file {} with size {}".format(self.name, name, size))
            self.files[name] = int(size)
        else:
            tgt_dir = path_array[0]
            if tgt_dir not in self.subdirs.keys():
                self.subdirs[tgt_dir] = dir(tgt_dir)
            new_path_array = path_array.copy() # deep copy
            new_path_array.pop(0)
            print("Calling subdir add_file with patharray {}".format("/".join(new_path_array)))
            self.subdirs[tgt_dir].add_file(new_path_array,name,size)
    def build_dir_size_dict(self,path,out_dict):
        dir_size = 0
        for f in self.files.keys():
            dir_size += self.files[f]
        my_name = path + self.name + "/"
        if(not self.subdirs.keys()):            
            out_dict[my_name] = dir_size
        else:            
            for d in self.subdirs.keys():                        
                self.subdirs[d].build_dir_size_dict(self.name+"/", out_dict)
                dir_size += out_dict[self.name+"/"+d+"/"]
            out_dict[my_name] = dir_size
        
            

cur_path = []

dir_struct = dir("")

dir_size_dict = {}
with open("day7_input.txt") as f:
    while True:
        line = f.readline().rstrip()
        if not line:
            break
        m = re.match(r'^\$ cd (.+)', line)
        if m:
            print("moving to dir {}".format(m.group(1)))
            if(m.group(1) == "/"):
                cur_path = []
            elif(m.group(1) == ".."):                
                cur_path.pop()
            else:
                cur_path.append(m.group(1))
            print("After move, cur_path = {}".format("/".join(cur_path)))
            continue
        m = re.match(r'^\$ ls', line)
        m = re.match(r'^dir (.+)', line)
        if m:
            print("Found subdir {}".format(m.group(1)))
            dir_struct.add_subdir(cur_path,m.group(1))
            continue
        m = re.match(r'^(\d+) (.+)', line)
        if m:
            print("Found file {} with size {}".format(m.group(2), m.group(1)))
            dir_struct.add_file(cur_path, m.group(2), m.group(1))
            continue
    dir_struct.build_dir_size_dict("",dir_size_dict)

total_le100k_size = 0
for d in dir_size_dict.keys():
    print("Size of dir {} is {}".format(d, dir_size_dict[d]))
    if(dir_size_dict[d] <= 100000):
        total_le100k_size += dir_size_dict[d]
print("Total size for dirs less than 100k = {}".format(total_le100k_size))

fs_size = 70000000
fs_used = dir_size_dict["/"]
fs_needed = 30000000 - (fs_size - fs_used)
print("Need to delete {} worth of files".format(fs_needed))
smallest_dir_needed_name = ""
for d in dir_size_dict.keys():
    if dir_size_dict[d] >= fs_needed:
        if(smallest_dir_needed_name==""):
            smallest_dir_needed_name = d
        elif(dir_size_dict[d] <= dir_size_dict[smallest_dir_needed_name]):
            smallest_dir_needed_name = d

print("Smallest dir needed name ={} size = {}".format(smallest_dir_needed_name, dir_size_dict[smallest_dir_needed_name]))
