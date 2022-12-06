with open("day6_input.txt") as f:
    char_processed = 0    
    line = f.readline()
    #line = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
    
    pkt_len = 14 # 4 for start_of_pkt, 14 for start_of_msg

    while True:
        chars = line[char_processed : char_processed+pkt_len]
        # print(chars)        
        if(len(set(list(chars))) == pkt_len):
            print("Found unique marker detected after {} chars".format(char_processed + pkt_len))
            break
        char_processed += 1        
        # if(char_processed == 50):
            # break
