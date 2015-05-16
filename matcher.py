from random import *

class Matcher():
    def __init__(self, person_dic):
        self.person_dic = person_dic
        self.num_person = len(person_dic)
        if self.num_person % 2 != 0:
            raise "number is not a multiple of 2"
        self.person_list = self.sort_V(person_dic.items())
        self.tot_score = 0
        self.max_score = 0
        self.result = []
        self.final_result = []
        self.snapshots = []

    def get_roommates(self):
        top5_indices = [randint(0, self.num_person) for _ in xrange(10)]
       
        print '========= before iteration ========='
        print self.person_dic
        print self.person_list

        # main part
        iterate_more = True

        while iterate_more:
            self.iterate(self.num_person / 2)
            if self.tot_score > self.max_score:
                self.final_result = self.result
            iterate_more = self.restore_snapshot()

        self.print_result()

    def iterate(self, num):
        for i in range(self.num_person / 2):
            if i in top5_indices:
                self.take_snapshot()
                self.match(self.person_list[0])
                #TODO
                pass
            else:
                self.match(self.person_list[0])

            print '==== iteration %d ====' % i
            print self.person_dic
            print self.person_list

    # person: (idx, score_dic)
    def match(self, person):
        pid = person[0]
        score_dic = self.person_dic[pid]
        roommate_id = max(score_dic, key=score_dic.get)
        self.tot_score += score_dic[roommate_id]
        self.result.append((pid, roommate_id))
        self.delete_person(pid)
        self.delete_person(roommate_id)

    def update_result(self, candidate):
        if self.

    def delete_person(self, pid):
        self.person_dic.pop(pid, None)
        
        # reconstruct person_list
        self.person_list = self.person_dic.items()
        for p in self.person_list:
            p[1].pop(pid, None)

        self.person_list = self.sort_V(self.person_list)

    def take_snapshot(self):
        pass

    # sort in descending order of V
    def sort_V(self, l):
        key_f = lambda (k, p): sum(p.values())
        return sorted(l, key = key_f, reverse=True)

    def print_result(self):
        print self.person_list
        print self.result


def get_roommates(person_dic):
    m = Matcher(person_dic)
    m.get_roommates()

if __name__ == '__main__':
    match({0:1,1:2,2:3})
