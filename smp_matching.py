import os, sys
import operator
import random 

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


def insert_person_information(p, sleep_time, getup_time, smoke_flag, rm_smoke_flag, clean_flag, 
				imp_sleep, imp_getup, imp_smoke, imp_clean):
    p.set_getup_time(getup_time)
    p.set_sleep_time(sleep_time)
    p.set_smoke_flag(smoke_flag)
    p.set_rm_smoke_flag(rm_smoke_flag)
    p.set_clean_flag(clean_flag)

    imp_sum = imp_sleep + imp_getup + imp_smoke + imp_clean
    p.set_imp_getup(round(imp_getup / imp_sum,2))
    p.set_imp_sleep(round(imp_sleep / imp_sum,2))
    p.set_imp_smoke(round(imp_smoke / imp_sum,2))
    p.set_imp_clean(round(imp_clean / imp_sum,2))


def score_compute_all(person_dic, person_num):
    
    score_sum_dic = {}

    for i in range(1, person_num):
        for j in range(i+1, person_num):
            score = score_compute(person_dic[i], person_dic[j])
            person_dic[i].score_dic_update(j, score)
            person_dic[j].score_dic_update(i, score)

    for i in range(1, person_num):
        for value in person_dic[i].score_dic.values():
            person_dic[i].score_sum += value;
        score_sum_dic[i] = person_dic[i].score_sum

    # sort score_sum_dic
    return sorted(score_sum_dic.items(), key=operator.itemgetter(1), reverse=True)

def score_compute(p1, p2):

    m_score_1 = (score_getup(p1, p2) * p1.imp_getup) + (score_sleep(p1, p2) * p1.imp_sleep) + (score_smoke(p1, p2) * p1.imp_smoke) + (score_clean(p1, p2) * p1.imp_clean)
    m_score_2 = (score_getup(p2, p1) * p2.imp_getup) + (score_sleep(p2, p1) * p2.imp_sleep) + (score_smoke(p2, p1) * p2.imp_smoke) + (score_clean(p2, p1) * p2.imp_smoke)

    m_score = m_score_1 * m_score_2

    return m_score

def score_getup(p1, p2):
    
    score = 0

    if (p1.getup_time == -1):
        if (p2.getup_time == -1):
            score = 30
        else:
            score = 10
    else:
        if (p2.getup_time == -1):
            score = 0
        elif (p1.getup_time == p2.getup_time):
            score = 100
        elif (abs(p1.getup_time - p2.getup_time) == 1):
            score = 50
        elif (abs(p1.getup_time - p2.getup_time) in (2,3)):
            score = 30
        else:
            score = 10

    return score

def score_sleep(p1, p2):
    
    score = 0

    if (p1.getup_time == -1):
        if (p2.getup_time == -1):
            score = 30
        else:
            score = 10
    else:
        if (p2.getup_time == -1):
            score = 0
        elif (p1.getup_time == p2.getup_time):
            score = 100
        elif (abs(p1.getup_time - p2.getup_time) == 1):
            score = 50
        elif (abs(p1.getup_time - p2.getup_time) in (2,3)):
            score = 30
        else:
            score = 10

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

def smp_matching(person_dic, score_sum_list):
    
    score_sum = 0
    result_dic = {}
    
    for item in score_sum_list:
        n = item[0]

        if n not in result_dic.values():
            target_n = max(person_dic[n].score_dic.iterkeys(), key=lambda k: person_dic[n].score_dic[k])
            result_dic[n] = target_n
            score_sum = score_sum + person_dic[n].score_dic[target_n]

            for p in person_dic:
                if n in person_dic[p].score_dic.keys():
                    del person_dic[p].score_dic[n]
                if target_n in person_dic[p].score_dic.keys():
                    del person_dic[p].score_dic[target_n]

    return score_sum, result_dic


def random_matching(person_dic):

    score_sum = 0
    result_dic = {}
    choice_list = []
    for n in person_dic:
        choice_list.append(n)

    while(choice_list):
        n = random.choice(choice_list)
        choice_list.remove(n)
        target_n = random.choice(choice_list)
        score_sum = score_sum + person_dic[n].score_dic[target_n]
        result_dic[n] = target_n
        choice_list.remove(target_n)

    return score_sum, result_dic

def insert_data(path):

    person_dic = {}

    f = open(path)

    i = 0
    for line in f:
        if i>0:
            data = line.rstrip().split(',')
            person_dic[int(data[0])] = Person(int(data[0]))
            insert_person_information(person_dic[int(data[0])], int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), float(data[6]), float(data[7]), float(data[8]), float(data[9]))
        i = i + 1

    return person_dic

def main():
 
    score_sum_list = []
    ''' Step0. get data from csv '''
    person_dic = insert_data("male.csv")

    ''' Step1. score computating '''
    score_sum_list = score_compute_all(person_dic, len(person_dic)+1)

    ''' Step2. SMP Matching '''

    rd_sum, rd_dic = random_matching(person_dic)
    print "random sum : %d\n" % rd_sum

    score_sum, result_dic = smp_matching(person_dic, score_sum_list)
    print result_dic
    print "sum : %d\n" % score_sum
if __name__ == '__main__':
    main()

