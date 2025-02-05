import random

class Request:
    seq = None
    id = None
    src = None
    dst = None
    start = None
    
def get_request(seed, request_name_extend,cur_time,delayed_requests):
    prefer_ratio=0
    random.seed(seed)
    num_request = len(request_name_extend)
    origin_region = ['zurich', 'milan', 'madrid', 'oregon', 'mumbai']
    prop = [0.2, 0.2, 0.2, 0.2, 0.2]
    label_counts = [int(num_request*prop[0]), int(num_request*prop[1]), int(num_request*prop[2]), \
        int(num_request*prop[3]), num_request-int(num_request*prop[0])-int(num_request*prop[1])-int(num_request*prop[2])-int(num_request*prop[3])]
    assert sum(label_counts) == num_request
    src_list = []
    for label, count in zip(origin_region, label_counts):
        src_list.extend([label] * count)
    while len(src_list) < num_request:
        src_list.append("zurich")
    random.shuffle(src_list)
    num_prefer = int(num_request* prefer_ratio*0.01)
    preferred_regions = random.choices(origin_region, k=num_prefer)
    
    requests = []
    count_num=0
    for single_name in request_name_extend:
        request_i = Request()
        request_i.id = single_name
        request_i.seq = str(count_num)+'_'+str(single_name)+'_'+str(cur_time)
        request_i.src = src_list.pop()
        request_i.start = cur_time
        if preferred_regions:
            request_i.dst = preferred_regions.pop()
        requests.append(request_i)
        count_num+=1
    
    if num_prefer>0:
        next_req = requests[num_prefer:]
        next_req.extend(delayed_requests)
        return next_req, requests[0:num_prefer]
    else:
        requests.extend(delayed_requests)
        return requests, []
