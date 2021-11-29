import sys
import numpy as np
import math
import random
 
def check_input(N, nearest_connect, farthest_connect):
    if(nearest_connect <= 0 or farthest_connect <= 0 or N <= 0):
        print('error: nearest_connect should bigger than 0')
        exit()
    elif(nearest_connect > farthest_connect):
        print('error: nearest_connect should not bigger than farthest_connect')
        exit()
    elif(farthest_connect > N/2):
        print('error: farthest_connect should not exceed half of total node')
        exit()
    else:
        return

def create_array(N, nearest_connect, farthest_connect):
    array = np.zeros((N,N))
    for i in range (N):
        for j in range(nearest_connect, farthest_connect+1):
            if(i+j>N-1):
                array[i][i+j-N]=1
            else:
                array[i][i+j] = 1
    for i in range (N):
        for j in range(nearest_connect, farthest_connect+1):
            if(i-j<0):
                array[i][i-j+N]=1
            else:
                array[i][i-j] = 1
    return array

def decision(probability):
    return random.random() < probability

def find_min_one_idx(low_idx,high_idx,f):
    min_one_idx = -1
    for j in range(low_idx,high_idx+1):
        if(f[j]):
            min_one_idx = j
            break
    return min_one_idx

def find_max_one_idx(low_idx,high_idx,f):
    max_one_idx = -1
    for j in range(high_idx,low_idx-1,-1):
        if(f[j]):
            max_one_idx = j
            break
    return max_one_idx

def is_any_one(low_idx,high_idx,f):
    is_any_one_var = 0
    for k in range(low_idx,high_idx+1):
        if(k >= N):
            k = k - N
        if(f[k]):
            is_any_one_var = 1
            break
    return is_any_one_var

if __name__ == '__main__':
    N = int(sys.argv[1])
    nearest_connect = int(sys.argv[2]) #0 < lower < upper <= N/2
    farthest_connect = int(sys.argv[3])
    prob = float(sys.argv[4])

    check_input(N, nearest_connect, farthest_connect)
    a = create_array(N, nearest_connect, farthest_connect)

    f = np.zeros(N)

    for i in range(N):
        f[i] = decision(prob)
    print(f)
    if(farthest_connect != nearest_connect):
        chunk_size = farthest_connect - nearest_connect
        is_collision_in_chunk_arr = np.zeros(math.ceil(N/chunk_size))
        
        for i in range(math.ceil(N/chunk_size)):
            min_idx_in_chunk = chunk_size * i
            max_idx_in_chunk = min(chunk_size * (i+1) - 1,N-1)
            min_one_idx_in_chunk = find_min_one_idx(min_idx_in_chunk,max_idx_in_chunk,f)
            max_one_idx_in_chunk = find_max_one_idx(min_idx_in_chunk,max_idx_in_chunk,f)

            if(min_one_idx_in_chunk==-1):
                continue

            connect_low_idx = min_one_idx_in_chunk + nearest_connect
            connect_high_idx = max_one_idx_in_chunk + farthest_connect

            is_collision_in_chunk_arr[i] = is_any_one(connect_low_idx,connect_high_idx,f)

        is_collision_var = is_any_one(0,len(is_collision_in_chunk_arr)-1,is_collision_in_chunk_arr)
    else:
        is_collision_in_chunk_arr = np.zeros(N)
        for i in range(N):
            connect_low_idx = i + nearest_connect
            connect_high_idx = i + farthest_connect
            if(f[i]):
                is_collision_in_chunk_arr[i] = is_any_one(connect_low_idx, connect_high_idx,f)

        is_collision_var = is_any_one(0,len(is_collision_in_chunk_arr)-1,is_collision_in_chunk_arr)
    print(is_collision_var)