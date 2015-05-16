import os, sys
import matcher

class Person():
    
    def __init__(self, pid):

        self.pid = pid
        ''' information of this person '''
        self.getup_time = 0
        self.sleep_time = 0
        self.smoke_flag = 0
        self.clean_flag = 0

        ''' importances of each item '''
        self.imp_getup = 0.0
        self.imp_sleep = 0.0
        self.imp_smoke = 0.0
        self.imp_clean = 0.0

        ''' score list of other Person '''
        self.score_dic = {}

    def set_getup_time(self, n):
        self.getup_time = n
    def set_sleep_time(self, n):
        self.sleep_time = n
    def set_smoke_flag(self, n):
        self.smoke_flag = n
    def set_clean_flag(self, n):
        self.clean_flag = n

    def set_imp_getup(self, n):
        self.imp_getup = n
    def set_imp_sleep(self, n):
        self.imp_sleep = n
    def set_imp_smoke(self, n):
        self.imp_smoke = n
    def set_imp_clean(self, n):
        self.imp_clean = n

    def score_dic_update(self, n, score):
        self.score_dic[n] = score

def insert_person_information(p, getup_time, sleep_time, smoke_flag, clean_flag, 
				imp_getup, imp_sleep, imp_smoke, imp_clean):
    p.set_getup_time(getup_time)
    p.set_sleep_time(sleep_time)
    p.set_smoke_flag(smoke_flag)
    p.set_clean_flag(clean_flag)
    p.set_imp_getup(imp_getup)
    p.set_imp_sleep(imp_sleep)
    p.set_imp_smoke(imp_smoke)
    p.set_imp_clean(imp_clean)


def score_compute_all(person_dic, person_num):
    
    for i in range(0, person_num):
        for j in range(i+1, person_num):
            score = score_compute(person_dic[i], person_dic[j])
            person_dic[i].score_dic_update(j, score)
            person_dic[j].score_dic_update(i, score)

def score_compute(p1, p2):

    m_score_1 = (score_getup(p1, p2) * p1.imp_getup) + (score_sleep(p1, p2) * p1.imp_sleep) + (score_smoke(p1, p2) * p1.imp_smoke) + (score_clean(p1, p2) * p1.imp_clean)
    m_score_2 = (score_getup(p2, p1) * p2.imp_getup) + (score_sleep(p2, p1) * p2.imp_sleep) + (score_smoke(p2, p1) * p2.imp_smoke) + (score_clean(p2, p1) * p2.imp_smoke)

    m_score = m_score_1 * m_score_2

    return m_score

def score_getup(p1, p2):
    
    score = 0

    if (p1.getup_time == 10):
        if (p2.getup_time == 10):
            score = 30
        else:
            score = 10
    else:
        if (p2.getup_time == 10):
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

    if (p1.getup_time == 10):
        if (p2.getup_time == 10):
            score = 30
        else:
            score = 10
    else:
        if (p2.getup_time == 10):
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
    if(p1.smoke_flag == p2.smoke_flag):
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

def smp_matching():
    pass


def main():
    
    ''' Step1. Score Computation '''

    person_dic= {}
    person_num = 6
    
    for i in range(0,person_num):
        person_dic[i] = Person(i)
    
    ''' TO DO : should be inserted automatically from xls '''
    insert_person_information(person_dic[0], 2,3,0,1, 0.3, 0.3, 0.2, 0.2)
    insert_person_information(person_dic[1], 1,2,0,3, 0.2, 0.2, 0.5, 0.1)
    insert_person_information(person_dic[2], 3,3,0,2, 0.2, 0.2, 0.5, 0.1)
    insert_person_information(person_dic[3], 1,2,1,3, 0.1, 0.1, 0.1, 0.7)
    insert_person_information(person_dic[4], 2,1,1,1, 0.1, 0.1, 0.7, 0.1)
    insert_person_information(person_dic[5], 3,4,0,2, 0.2, 0.2, 0.5, 0.1)

    score_compute_all(person_dic, 6)
    
    score_dic = {}

    for n in person_dic:
        print n
        print(person_dic[n].score_dic)
        score_dic[n] = person_dic[n].score_dic

    '''
    0
    {1: 3500.0, 2: 5700.0, 3: 300.0, 4: 7200.0, 5: 5700.0}
    1
    {0: 3500.0, 2: 5829.0, 3: 1500.0, 4: 200.0, 5: 5829.0}
    2
    {0: 5700.0, 1: 5829.0, 3: 187.0, 4: 1125.0, 5: 14000.0}
    3
    {0: 300.0, 1: 1500.0, 2: 187.0, 4: 1600.0, 5: 1517.0}
    4
    {0: 7200.0, 1: 200.0, 2: 1125.0, 3: 1600.0, 5: 675.0}
    5
    {0: 5700.0, 1: 5829.0, 2: 14000.0, 3: 1517.0, 4: 675.0}
    '''

    ''' Step2. SMP Matching '''
    matcher.get_roommates(score_dic)

if __name__ == '__main__':
    main()

