import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from faker import Faker

pd.set_option('display.max_rows',None)

def sum_consume():
    sum_c=0
    for i in people:
        sum_c=sum_c+i.consume_i
    return sum_c

def sum_income():
    sum_i=0
    for i in people:
        sum_i=sum_i+i.income
    return sum_i

def game1(data, roundi):
    # for i in range(1,society.people+1):


    if len(data[data[roundi - 1] ==0]) > 0:
    # 当数据包含财富值为0的玩家时
        round_i = pd.DataFrame({'pre_round':data[roundi-1],'lost':0})
        con = round_i['pre_round'] > 0
        round_i['lost'][con] = 1               # 设定每轮分配财富之前的情况 → 该轮财富值为0的不需要拿钱给别人
        round_players_i = round_i[con]         # 筛选出参与游戏的玩家：财富值>0
        choice_i = pd.Series(np.random.choice(person_n,len(round_players_i)))
        gain_i = pd.DataFrame({'gain':choice_i.value_counts()})     # 这一轮中每个人随机指定给“谁”1元钱，并汇总这一轮每个人的盈利情况
        round_i = round_i.join(gain_i)
        round_i.fillna(0,inplace = True)
        return round_i['pre_round'] -  round_i['lost'] + round_i['gain']
        # 合并数据，得到这一轮财富分配的结果
    else:
    # 当数据不包含财富值为0的玩家时
        round_i = pd.DataFrame({'pre_round':data[roundi-1],'lost':1}) # 设定每轮分配财富之前的情况
        choice_i = pd.Series(np.random.choice(person_n,100))
        gain_i = pd.DataFrame({'gain':choice_i.value_counts()})       # 这一轮中每个人随机指定给“谁”1元钱，并汇总这一轮每个人的盈利情况
        round_i = round_i.join(gain_i)
        round_i.fillna(0,inplace = True)
        return round_i['pre_round'] -  round_i['lost'] + round_i['gain']
        # 合并数据，得到这一轮财富分配的结果

class society_basics:
    people_no=0
    maxSalary=0
    nowsalary=0
    totalCap=0
    totalInd=0
    working_force=0
    working_force_on_post=0
    k4=0

    def __init__(self,k4,people):
        self.k4=k4
        self.people_no=people
        # self.maxSalary=k4*sum_consume()

    def __supplyDemand__(self):
        self.maxSalary = self.k4 * sum_consume()

    def __unemploymentRate__(self):
        return (self.working_force - self.working_force_on_post)/self.working_force


class person_basics:
    initMoney=0
    industrial=0
    capability=0
    initConsume=0
    delta_consume=0
    income=0
    money_i=0
    consume_i=0
    lowestmoney=0
    highermoney=0
    day_to_retire=0
    job=False
    name=''
    def __init__(self,k1,k2,k3,name):
        self.initMoney=np.random.randint(low=0,high=501)*100
        self.industrial=np.random.randint(low=1,high=11)
        self.capability=np.random.randint(low=1,high=11)
        self.income = k1 * self.industrial * self.capability
        self.initConsume=np.random.randint(low=min(int(k1*30.25*0.1),int(k1*self.industrial*self.capability*0.5)),high=int(k1*self.industrial*self.capability*1.5))
        self.consume_i=self.initConsume
        self.delta_consume=np.random.randint(low=int(k1*30.25*0.1),high=int(k1*30.25*0.2))
        self.lowestmoney=self.industrial**2*k3
        self.highermoney=self.industrial**2*k2
        if self.income<self.initConsume:
            self.initConsume=self.initConsume-(int((self.initConsume-self.income)/self.delta_consume)+1)*self.delta_consume#cut consume to increase money to get
        self.day_to_retire=int((self.highermoney-self.initMoney)/(self.income-self.initConsume+1))
        self.name=name

    def list_all_member(self):
        for name, value in vars(self).items():
            print('%s=%s' % (name, value))

person_n = [x for x in range(1,101)]
fortune = pd.DataFrame([100 for i in range(100)], index = person_n)
fortune.index.name = 'id'
# 设定初始参数：游戏玩家100人，起始资金100元




if(__name__=="__main__"):
    #initialization
    society = society_basics(k4=1,people=100)
    #names
    fake = Faker()#random name
    ss = set()
    str = ''
    while len(ss) < society.people_no:
        str = fake.name()
        ss.add(str)

    namelist=list(ss)

    for j in range(500):
        print(j)
        people=[]
        for i in range(0,society.people_no):
            person=person_basics(k1=20,k2=6000,k3=1000,name=namelist[i])
            people.append(person)
            # print(i)
            # people[i].list_all_member()


        person_n = [x for x in range(1, 101)]
        fortune = pd.DataFrame({'money':[people[i-1].initMoney for i in range(1,society.people_no+1)]}, index=person_n)
        fortune.index.name = 'id'



        #day0
        print('sum_consume=%d'%(sum_consume()))
        print('sum_income=%d'%sum_income())

        society = society_basics(k4=1, people=100)
        society.__supplyDemand__()
        people.sort(key=lambda pb:person_basics.income)
        for i in people:
            if i.day_to_retire>0:
                society.working_force=society.working_force+1
                if society.nowsalary+i.income<=society.maxSalary:
                    i.job=True
                    society.working_force_on_post=society.working_force_on_post+1
                    society.nowsalary=society.nowsalary+i.income
                    society.totalCap=society.totalCap+i.capability
                    society.totalInd=society.totalInd+i.industrial

        print('劳动人口=%d'%(society.working_force))
        print('在岗劳动人口=%d'%(society.working_force_on_post))
        print('unemployment rate: {:.2%}'.format(society.__unemploymentRate__()))
        print(society.nowsalary)
        print(society.totalInd)
        print(society.totalCap)

#initialization reasonable


    # print(fortune)
    # for round in range(1, 201):
    #     fortune[round] = game1(fortune, round)












