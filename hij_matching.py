import os, sys
import operator
import random 
import numpy
import math
import copy
from operator import mul

class Person():
    
    def __init__(self, pid):

        self.pid = pid
        ''' information of this person '''
        self.sleep_time = 0
        self.getup_time = 0
        self.smoke_flag = 0
        self.rm_smoke_flag = 0
        self.clean_flag = 0

        ''' importances of each item '''
        self.imp_sleep = 0.0
        self.imp_getup = 0.0
        self.imp_smoke = 0.0
        self.imp_clean = 0.0

        ''' score list of other Person '''
        self.score_dic = {}
        self.mutual_score_dic = {}
        self.score_sum = 0.0

    def set_sleep_time(self, n):
        self.sleep_time = n
    def set_getup_time(self, n):
        self.getup_time = n
    def set_smoke_flag(self, n):
        self.smoke_flag = n
    def set_rm_smoke_flag(self, n):
        self.rm_smoke_flag = n
    def set_clean_flag(self, n):
        self.clean_flag = n

    def set_imp_sleep(self, n):
        self.imp_sleep = n
    def set_imp_getup(self, n):
        self.imp_getup = n
    def set_imp_smoke(self, n):
        self.imp_smoke = n
    def set_imp_clean(self, n):
        self.imp_clean = n

    def score_dic_update(self, n, score):
        self.score_dic[n] = score

    def mutual_score_dic_update(self, n, score):
        self.mutual_score_dic[n] = score


def insert_person_information(p, sleep_time, getup_time, smoke_flag, rm_smoke_flag, clean_flag, 
				imp_sleep, imp_getup, imp_smoke, imp_clean):
    p.set_getup_time(getup_time)
    p.set_sleep_time(sleep_time)
    p.set_smoke_flag(smoke_flag)
    p.set_rm_smoke_flag(rm_smoke_flag)
    p.set_clean_flag(clean_flag)

    imp_sum = imp_sleep + imp_getup + imp_smoke + imp_clean
#    p.set_imp_getup(float(imp_getup) / imp_sum)
#    p.set_imp_sleep(float(imp_sleep) / imp_sum)
#    p.set_imp_smoke(float(imp_smoke) / imp_sum)
#    p.set_imp_clean(float(imp_clean) / imp_sum)
    p.set_imp_getup(round(imp_getup / imp_sum, 2))
    p.set_imp_sleep(round(imp_sleep / imp_sum, 2))
    p.set_imp_smoke(round(imp_smoke / imp_sum, 2))
    p.set_imp_clean(round(imp_clean / imp_sum, 2))


def score_update_all(person_dic, mutual_func):
    #score_sum_dic = {}
    person_num = len(person_dic)

    for i in range(1, person_num + 1):
        p1 = person_dic[i]
        for j in range(i+1, person_num + 1):
            p2 = person_dic[j]
            score_ij = score_compute(p1, p2)
            score_ji = score_compute(p2, p1)
            
            p1.score_dic_update(j, score_ij)
            p2.score_dic_update(i, score_ji)

            mutual_score = mutual_func(score_ij, score_ji)

            p1.mutual_score_dic_update(j, mutual_score)
            p2.mutual_score_dic_update(i, mutual_score)

    return
    #return sorted(score_sum_dic.items(), key=operator.itemgetter(1), reverse=True)

def mutual_score_compute(p1, p2, mutual_func):
    m_score_1 = score_compute(p1, p2)
    m_score_2 = score_compute(p2, p1)
    return mutual_func(m_score_1, m_score_2)

def score_compute(p1, p2):
    m_score = (score_getup(p1, p2) * p1.imp_getup) + \
                (score_sleep(p1, p2) * p1.imp_sleep) + \
                (score_smoke(p1, p2) * p1.imp_smoke) + \
                (score_clean(p1, p2) * p1.imp_clean)

    # normalize to 0~1
    m_score /= 100.0

    if m_score > 1.0:   #precision
        m_score = 1.0
#    if m_score > 100.0:
#        m_score = 100.0

    return m_score

def score_getup(p1, p2):
    score_matrix = [100, 50, 30, 30, 10]
    score = 0

    if (p1.getup_time == -1):
        if (p2.getup_time == -1):
            score = 30
        else:
            score = 10
    elif (p2.getup_time == -1):
        score = 0
    else:
        diff = abs(p1.getup_time - p2.getup_time)
        if diff >= len(score_matrix):
            diff = len(score_matrix) - 1
        score = score_matrix[diff]

    return score

def score_sleep(p1, p2):
    score_matrix = [100, 50, 30, 30, 10]
    score = 0

    if (p1.sleep_time == -1):
        if (p2.sleep_time == -1):
            score = 30
        else:
            score = 10
    elif (p2.sleep_time == -1):
        score = 0
    else:
        diff = abs(p1.sleep_time - p2.sleep_time)
        if diff >= len(score_matrix):
            diff = len(score_matrix) - 1
        score = score_matrix[diff]

    return score

def score_smoke(p1, p2):
    score = 0
    if(p1.rm_smoke_flag == 2):
        score = 100
    elif(p1.rm_smoke_flag == p2.smoke_flag):
        score = 100
    else:
        score = 0
    return score

def score_clean(p1, p2):
    score = 0
    if(p1.clean_flag == p2.clean_flag):
        score = 100
    elif(abs(p1.clean_flag - p2.clean_flag) == 1):
        score = 50
    else:
        score = 0
    return score

def total_score(person_dic, pid, total_func):
    return total_func(person_dic[pid].mutual_score_dic.values())

def smp_matching(person_dic_arg, total_func=sum, order_func=max):
    score_sum = 0
    person_dic = copy.deepcopy(person_dic_arg)
    result_dic = {}

    while person_dic:
        n = order_func(person_dic, key=lambda pid: total_score(person_dic, pid, total_func))
        target_n = max(person_dic[n].mutual_score_dic, key=lambda k: person_dic[n].mutual_score_dic[k])
#        print "%d %d" % (n, target_n)
        result_dic[n] = target_n
        result_dic[target_n] = n

        for p in person_dic:
            if n in person_dic[p].mutual_score_dic.keys():
                del person_dic[p].mutual_score_dic[n]
            if target_n in person_dic[p].mutual_score_dic.keys():
                del person_dic[p].mutual_score_dic[target_n]

        del person_dic[n]
        del person_dic[target_n]

    return result_dic

def random_matching(person_dic):
    result_dic = {}
    choice_list = []
    for n in person_dic:
        choice_list.append(n)

    while(choice_list):
        n = random.choice(choice_list)
        choice_list.remove(n)
        target_n = random.choice(choice_list)
        result_dic[target_n] = n
        result_dic[n] = target_n
        choice_list.remove(target_n)

    return result_dic


def random_matching_sleep(person_dic, pre_list, post_list):
    result_dic = {}
    pre_choice = copy.deepcopy(pre_list)
    post_choice = copy.deepcopy(post_list)

    while(len(pre_choice) >= 2):
        n = random.choice(pre_choice)
        pre_choice.remove(n)
        target_n = random.choice(pre_choice)
        result_dic[target_n] = n
        result_dic[n] = target_n
        pre_choice.remove(target_n)

    while(len(post_choice) >= 2):
        n = random.choice(post_choice)
        post_choice.remove(n)
        target_n = random.choice(post_choice)
        result_dic[target_n] = n
        result_dic[n] = target_n
        post_choice.remove(target_n)

    if len(pre_choice) >= 1 and len(post_choice) >= 1:
        result_dic[pre_choice[0]] = post_choice[0]
        result_dic[post_choice[0]] = pre_choice[0]

    return result_dic

def insert_data(path):
    person_dic = {}

    buf = []
    with open(path, 'r') as f:
        buf = f.readlines()

    for line in buf[1:]:    #remove title line
        data = line.rstrip().split(',')
        person_dic[int(data[0])] = Person(int(data[0]))
        insert_person_information(person_dic[int(data[0])], int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), float(data[6]), float(data[7]), float(data[8]), float(data[9]))

    return person_dic

def main(filename, op1=0, op2=0, op3=0):
    if op1==0:
        mutual_func = lambda x, y: math.sqrt(x * y)
    else:
        mutual_func = lambda x, y: (x + y) / 2.0
    if op2==0:
        order_func = max
    else:
        order_func = min
    if op3==0:
        total_func = sum
    else:
        total_func = lambda l: reduce(mul, l, 1.0)


    if op3>0:
        print total_func([1,2,3,4,5])

    ''' Step0. get data from csv '''
    person_dic = insert_data(filename)

    ''' Step1. score computating '''
    score_update_all(person_dic, mutual_func)

    ''' Step2. Matching '''
    ''' SMP '''
    result_dic = smp_matching(person_dic, total_func, order_func)

    result_score = {}
    for r in result_dic:
        result_score[r] = score_compute(person_dic[r], person_dic[result_dic[r]])
    print_result(result_score.values(), 100.0)

    outfiledir = "results/"
    outfilename = "result_%s_%d%d%d.csv" % (filename[:filename.index('.')], op1, op2, op3)
    with open(outfiledir + outfilename, "w") as f:
        for r in result_dic:
            f.write("%d,\t%d,\t" % (r, result_dic[r]))
            f.write("%f,\t%f\n" % (100.0 * result_score[r], 100.0 * result_score[result_dic[r]]))

    ''' Random '''
    rand_avg_list = []
    num_rand = 1000
    for i in range(num_rand):
        random_dic = random_matching(person_dic)
        random_sum = 0.0
        for r in random_dic:
            random_sum += score_compute(person_dic[r], person_dic[random_dic[r]])
        rand_avg = random_sum / len(person_dic)
        rand_avg_list.append(rand_avg)

    print "random experiment: %d times" % num_rand
    print_result(rand_avg_list, 100.0)

    ''' Random - sleep time'''
    pre_list = []
    post_list = []
    for n, p in person_dic.items():
        if p.sleep_time in (1,2,3,4,5):
            pre_list.append(n)
        else:
            post_list.append(n)

    rand_avg_list_s = []
    num_rand_s = 1000
    for i in range(num_rand_s):
        random_dic_s = random_matching_sleep(person_dic, pre_list, post_list)
        random_sum_s = 0.0
        for r in random_dic_s:
            random_sum_s += score_compute(person_dic[r], person_dic[random_dic_s[r]])
        rand_avg_s = random_sum_s / len(person_dic)
        rand_avg_list_s.append(rand_avg_s)

    print "(SLEEP)random experiment: %d times" % num_rand_s
    print_result(rand_avg_list_s, 100.0)

def print_result(arr, m):
    score_avg = numpy.mean(arr)
    score_std = numpy.std(arr)
    score_max = max(arr)
    score_min = min(arr)
    print "avg: %f" % (score_avg * m)
    print "std: %f" % (score_std * m)
    print "max: %f" % (score_max * m)
    print "min: %f" % (score_min * m)
    print ""


if __name__ == '__main__':
    filename = "male.csv"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    if len(sys.argv) >= 5:
        main(filename, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    else:
        main(filename)

