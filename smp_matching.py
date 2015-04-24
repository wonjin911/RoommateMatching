import os, sys


class Person():

    ''' person unique id '''
    pid = 0

    ''' information of this person '''
    getup_time = 0
    sleep_time = 0
    smoke_flag = 0
    clean_flag = 0

    ''' importances of each item '''
    imp_getup = 0
    imp_sleep = 0
    imp_smoke = 0
    imp_clean = 0

    ''' score list of other Person '''
    score_dic = {}

    def __init__(self, pid):
        self.pid = pid     

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

def insert_person_information(p, getup_time, sleep_time, smoke_flag, clean_flag, 
				imp_getup, imp_sleep, imp_smoke, imp_clean):
    p.set_getup_time = getup_time
    p.set_sleep_time = sleep_time
    p.set_smoke_flag = smoke_flag
    p.set_clean_flag = clean_flag
    p.set_imp_getup = imp_getup
    p.set_imp_sleep = imp_sleep
    p.set_imp_smoke = imp_smoke
    p.set_imp_clean = imp_clean


def score_computate(path):
    pass

def smp_matching():
    pass


def main():
    
    ''' Step1. Score Computation '''

    # example (-1 for self core)
    person_dic= {}
    person_num = 6

    for i in range(0,person_num):
        person_dic[i] = Person(i)

    person_dic[0].score_dic = {1:10, 2:50, 3:70, 4:20, 5:60}
    person_dic[1].score_dic = {0:50, 2:80, 3:60, 4:30, 5:70}
    person_dic[2].score_dic = {0:40, 1:80, 2:50, 4:60, 5:30}
    person_dic[3].score_dic = {0:80 ,1:40, 2:60, 4:20, 5:70}
    person_dic[4].score_dic = {0:60, 1:50, 2:80, 3:90, 5:20}
    person_dic[5].score_dic = {0:90, 1:30, 2:20, 3:70, 4:60}
    
    for i in range(0,person_num):
        print(person_dic[i].score_dic)

    ''' Step2. SMP Matching '''
    


if __name__ == '__main__':
    main()

