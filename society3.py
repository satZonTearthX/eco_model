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
    for i in people:
        #people keeps to their posts
        if i.job==1:
            i.money_i=i.money_i+i.income-i.consume_i
        #people with enough money choose to retire for some time
            if i.money_i>=i.highermoney:
                i.job=0
                society.totalCap=society.totalCap-i.capability
                society.totalInd=society.totalInd-i.industrial
                society.__type__()
                society.working_force=society.working_force-1
                society.working_force_on_post=society.working_force_on_post-1
        else:
        #people retires temporarily at home
            i.money_i = i.money_i - i.consume_i
        #have to back to work due to lack of money
            if i.money_i <=i.lowestmoney:
                i.job=-1
                society.working_force=society.working_force+1#back to work add to the working force

    #deal with unemployment issue
    while (society.working_force>society.working_force_on_post):
        #find who is qualified to compete for a post
        if society.type==0:
            res=people
        else:
            res=[one for one in people if society.type == one.type and one.job == -1]
        res.sort(key=lambda pb: person_basics.income,reverse=True)
        for job_hunter in res:
            job_hunter.queue_for_a_job()

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
    type=0

    def __init__(self,k4,people):
        self.k4=k4
        self.people_no=people
        # self.maxSalary=k4*sum_consume()

    def __supplyDemand__(self):
        self.maxSalary = self.k4 * sum_consume()

    def __unemploymentRate__(self):
        return (self.working_force - self.working_force_on_post)/self.working_force

    def __type__(self):
        self.type=(self.totalInd-self.totalCap)/abs(self.totalInd-self.totalCap)
        return (self.totalInd-self.totalCap)/abs(self.totalInd-self.totalCap)

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
    day_to_job=0
    job=0
    name=''
    type=0#more on ind or cap
    def __init__(self,k1,k2,k3,name):
        self.initMoney=np.random.randint(low=0,high=501)*100
        self.industrial=np.random.randint(low=1,high=11)
        self.capability=np.random.randint(low=1,high=11)
        self.income = k1 * self.industrial * self.capability
        self.initConsume=np.random.randint(low=min(int(k1*30.25*0.1),int(k1*self.industrial*self.capability*0.5)),high=int(k1*self.industrial*self.capability*0.67))
        self.consume_i=self.initConsume
        self.delta_consume=np.random.randint(low=int(k1*30.25*0.1),high=int(k1*30.25*0.2))
        self.lowestmoney=self.capability*self.industrial**2*k3
        self.highermoney=self.capability*self.industrial**2*k2
        if self.income<self.initConsume:
            self.initConsume=self.initConsume-(int((self.initConsume-self.income)/self.delta_consume)+1)*self.delta_consume#cut consume to increase money to get
        self.day_to_retire=int((self.highermoney-self.initMoney)/(self.income-self.initConsume+1))
        self.name=name
        self.day_to_job=int(((self.highermoney-self.lowestmoney)/(self.initConsume)))

    def list_all_member(self):
        for name, value in vars(self).items():
            print('%s=%s' % (name, value))

    def __type__(self):
        self.type=(self.totalInd-self.totalCap)/abs(self.totalInd-self.totalCap)
        return (self.totalInd-self.totalCap)/abs(self.totalInd-self.totalCap)

    def queue_for_a_job(self):
        if society.maxSalary>=society.nowsalary+self.income:
            self.job=1
            self.consume_i=self.initConsume #recover to normal consuming standards
            society.working_force_on_post+1
            society.totalCap=society.totalCap+self.capability
            society.totalInd=society.totalCap+self.industrial
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

    people=[]
    aver_day=0
    day_to=[]
    for i in range(0,society.people_no):
        person=person_basics(k1=20,k2=600,k3=300,name=namelist[i])
        people.append(person)
        print(i)
        people[i].list_all_member()
        if person.day_to_retire>0:
            day_to.append(person.day_to_retire)
            aver_day=aver_day+person.day_to_retire
    print(aver_day/society.people_no)
    print(day_to)

    # person_n = [x for x in range(1, 101)]
    # fortune = pd.DataFrame({'money':[people[i-1].initMoney for i in range(1,society.people_no+1)]}, index=person_n)
    # fortune.index.name = 'id'



    #day0
    print('sum_consume=%d'%sum_consume())
    print('sum_income=%d'%sum_income())

    society = society_basics(k4=2, people=100)
    society.__supplyDemand__()
    people.sort(key=lambda pb:person_basics.income,reverse=True)
    for i in people:
        if i.day_to_retire>0:
            society.working_force=society.working_force+1
            if society.nowsalary+i.income<=society.maxSalary:
                i.job=1
                society.working_force_on_post=society.working_force_on_post+1
                society.nowsalary=society.nowsalary+i.income
                society.totalCap=society.totalCap+i.capability
                society.totalInd=society.totalInd+i.industrial
            else:
                i.job=-1 #who is hunting for a job

    print('劳动人口=%d'%(society.working_force))
    print('在岗劳动人口=%d'%(society.working_force_on_post))
    print('unemployment rate: {:.2%}'.format(society.__unemploymentRate__()))
    print(society.nowsalary)
    print(society.totalInd)
    print(society.totalCap)

#initialization reasonable


    # print(fortune)
    for round in range(1, 201):
       game1(people, round)












