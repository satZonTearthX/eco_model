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

def ave_consume():
    return sum_consume()/society.people_no

def median_consume():
    consume_list=[]
    for i in people:
        consume_list.append(i.consume_i)
    return np.median(consume_list)

def lowest_society_consume():
    return int(int(max(ave_consume()*0.5,sum_money()/10000)))

def sum_income():
    sum_i=0
    for i in people:
        sum_i=sum_i+i.income
    return sum_i

def sum_money():
    sum=0
    for i in people:
        sum=sum+i.money_i
    return (sum)


def game1(round):
    print('Day%d'%round)
    for i in people:
        #people keeps to their posts
        if i.money_i>0:
            if i.job==1:
                i.money_i=i.money_i+i.income-i.consume_i

            #people with enough money choose to retire for some time
                if i.money_i>=i.highermoney:
                    i.job=0
                    society.nowSalary= society.nowSalary - i.income
                    society.totalCap=society.totalCap-i.capability
                    society.totalInd=society.totalInd-i.industrial
                    society.__type__()
                    society.working_force=society.working_force-1
                    society.working_force_on_post=society.working_force_on_post-1

                    print('%d号%s居民决定辞职，由于觉得钱够用了'%(i.id,i.name))
            elif i.job ==0:
            #people retires temporarily at home
                i.money_i = i.money_i - i.consume_i
                if i.money_i<=0:
                    i.money_i=0
                    i.consume_i=0
                    i.job=-2
                    society.people_no=society.people_no-1
                    print('%d号%s居民揭不开锅，饥饿中死去' % (i.id, i.name))

            #have to back to work due to lack of money
                if i.money_i <=i.lowestmoney :
                    i.job=-1
                    society.working_force=society.working_force+1#back to work add to the working force
                    print('%d号%s居民决定找工作，由于觉得手头有点紧' % (i.id, i.name))

            elif i.job ==-1:
                i.money_i=i.money_i-i.consume_i
                if i.money_i<=0:
                    i.money_i=0
                    i.consume_i=0
                    i.job=-2
                    society.people_no=society.people_no-1
                    society.working_force=society.working_force-1
                    print('%d号%s居民揭不开锅，饥饿中死去' % (i.id, i.name))

    #deal with unemployment issue


    while (society.working_force>society.working_force_on_post):
        past_wf = society.working_force_on_post
        ori_queue_for_jobs = [one for one in people if one.job == -1]
        #find who is qualified to compete for a post
        print(society.type)

        if society.type==0:
            res=[one for one in people if one.job == -1]
        else:
            res=[one for one in people if society.type != one.type and one.job == -1]
            res_2=[one for one in people if society.type == one.type and one.job == -1]

        res_2.sort(reverse=True)
        if len(res)==0:
            res=res_2
        print('求职者数量=', len(res))
        res.sort(reverse=True)
        count = 0
        while count<len(res):

            jobhunter=res[count]
            if jobhunter.queue_for_a_job() == False:
                count=count+1
            else:
                break
        if past_wf==society.working_force_on_post:#people who cannot find a job will have to lower their living standards
            for unemployment_one in ori_queue_for_jobs:
                print('%d号%s居民决定降低日常开销，由于缺钱又找不到工作' % (unemployment_one.id, unemployment_one.name))
                if unemployment_one.consume_i-unemployment_one.delta_consume>=int(max(ave_consume()*0.5,sum_money()/10000)):
                    unemployment_one.consume_i=unemployment_one.consume_i-unemployment_one.delta_consume
                    society.__supplyDemand__()#check supply-demand relation from time to time
                else:
                    print('其消费水平已降至社会最低水平')
                    print('其余额为',unemployment_one.money_i)
                    unemployment_one.consume_i=int(max(ave_consume()*0.5,sum_money()/10000))
                    society.__supplyDemand__()
                    print('其消费为',unemployment_one.consume_i)
            break

    print('社会情况综述：')
    print('社会总人口',society.people_no)
    print('劳动人口=%d'%(society.working_force))
    print('在岗劳动人口=%d'%(society.working_force_on_post))
    print('失业率: {:.2%}'.format(society.__unemploymentRate__()))
    print('社会总消费=%d' % sum_consume())
    print('社会总需求=%d' % society.maxSalary)
    print('社会总产值=%d' % society.nowSalary)
    print('社会勤奋劳动力总和=%d'%society.totalInd)
    print('社会能力劳动力总和=%d'%society.totalCap)
    print('社会总财富=%d'%sum_money())
    print(type(society.type))


class society_basics:
    people_no=0
    maxSalary=0
    nowSalary=0
    totalCap=0
    totalInd=0
    working_force=0
    working_force_on_post=0
    unemploymentRate=0
    k4=0
    type=0

    def __init__(self,k4,people):
        self.k4=k4
        self.people_no=people
        # self.maxSalary=k4*sum_consume()

    def __supplyDemand__(self):
        self.maxSalary = int(self.k4 * sum_consume())
        return self.maxSalary

    def __unemploymentRate__(self):
        self.unemploymentRate=(self.working_force - self.working_force_on_post)/self.working_force
        return self.unemploymentRate

    def __type__(self):
        if self.totalCap==self.totalInd:
            return 0
        else:
            self.type=int((self.totalInd-self.totalCap)/abs(self.totalInd-self.totalCap))
        return (self.type)

class person_basics:
    id=0
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
    def __init__(self,k1,k2,k3,name,id):
        self.id=id
        self.initMoney=np.random.randint(low=0,high=501)*10
        self.industrial=np.random.randint(low=1,high=11)
        self.capability=np.random.randint(low=1,high=11)
        self.income = k1 * self.industrial * self.capability
        self.initConsume=np.random.randint(low=int(k1*self.industrial*self.capability*0.5),high=int(k1*self.industrial*self.capability*0.67))
        self.consume_i=self.initConsume
        self.delta_consume=np.random.randint(low=int(k1*30.25*0.1),high=int(k1*30.25*0.2))
        self.lowestmoney=self.capability*self.industrial**2*k3
        self.highermoney=self.capability*self.industrial**2*k2
        if self.income<self.initConsume:
            self.initConsume=self.initConsume-(int((self.initConsume-self.income)/self.delta_consume)+1)*self.delta_consume#cut consume to increase money to get
        self.day_to_retire=int((self.highermoney-self.initMoney)/(self.income-self.initConsume+1))
        self.name=name
        self.day_to_job=int(((self.highermoney-self.lowestmoney)/(self.initConsume)))
        self.money_i=self.initMoney
        self.__type__()

    def list_all_member(self):
        for name, value in vars(self).items():
            print('%s=%s' % (name, value))
        print('job=%d'% self.job)
        print('money_i=%d'%self.money_i)
        print('type=',self.type)

    def __type__(self):
        if self.capability==self.industrial:
            return 0
        else:
            self.type=int((self.industrial-self.capability)/abs(self.industrial-self.capability))
        return (self.type)

    def queue_for_a_job(self):
        print(society.maxSalary)
        print(society.nowSalary)
        print(self.income)
        if society.maxSalary>=society.nowSalary+self.income:
            self.job=1
            self.consume_i=self.initConsume
            society.__supplyDemand__()
            #recover to normal consuming standards
            society.working_force_on_post=society.working_force_on_post+1
            society.nowSalary= society.nowSalary + self.income

            society.totalCap=society.totalCap+self.capability
            society.totalInd=society.totalCap+self.industrial
            society.__type__()
            print('%d号%s居民找到了一份工作，生活恢复了以往的水平' % (self.id, self.name))
            return True
        else:
            return False

    def __lt__(self, other):  # override <操作符
        if self.income < other.income:
            return True
        return False

        #modify the type if necessary
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
        person=person_basics(k1=20,k2=600,k3=300,name=namelist[i],id=i+1)
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

    society = society_basics(k4=1, people=100)
    society.__supplyDemand__()
    people.sort(reverse=True)
    for k in people:
        print(k.income)
        print(k.id)
        print(k.job)
    for i in people:
        if i.day_to_retire>0:
            society.working_force=society.working_force+1
            if society.nowSalary+i.income<=society.maxSalary:
                i.job=1
                society.working_force_on_post=society.working_force_on_post+1
                society.nowSalary= society.nowSalary + i.income
                society.totalCap=society.totalCap+i.capability
                society.totalInd=society.totalInd+i.industrial
                society.__type__()
            else:
                i.job=-1 #who is hunting for a job

    print('劳动人口=%d'%(society.working_force))
    print('在岗劳动人口=%d'%(society.working_force_on_post))
    print('失业率: {:.2%}'.format(society.__unemploymentRate__()))
    print('社会总消费=%d' % sum_consume())
    print('社会总需求=%d' % society.maxSalary)
    print('社会总产值=%d' % society.nowSalary)
    print('社会勤奋劳动力总和=%d'%society.totalInd)
    print('社会能力劳动力总和=%d'%society.totalCap)

#initialization reasonable


    # print(fortune)
    for round in range(1, 51):
       game1(round)












