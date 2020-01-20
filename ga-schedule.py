
# coding: utf-8

# In[23]:


get_ipython().magic('matplotlib nbagg')
import random

#from scoop import futures
import pandas as pd

from deap import base
from deap import creator
from deap import tools
from deap import cma

import matplotlib.pyplot as plt
import matplotlib.animation as animation

#creator.create("FitnessPeopleCount", base.Fitness, weights=(0.4, 0.5, 0.1))
creator.create("FitnessPeopleCount", base.Fitness, weights=(-0.3,-0.6,-0.1))#-10.0,-100.0,-1.0))#, -1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessPeopleCount)

toolbox = base.Toolbox()



toolbox.register("map", map)



toolbox.register("attr_bool", random.randint, 0, 1)

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 140)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)





# 従業員を表すクラス

class Employee(object):

  def __init__(self, no, name, wills):

    self.no = no

    self.name = name



    self.wills = wills



  def is_applicated(self, box_name):

    return (box_name in self.wills)



# シフトを表すクラス

# 内部的には  14日 * 10人 = 140次元のタプルで構成される

class Shift(object):

  # コマの定義

  SHIFT_BOXES = [
    '2020/2/1',
    '2020/2/2',
    '2020/2/3',
    '2020/2/4',
    '2020/2/5',
    '2020/2/6',
    '2020/2/7',
    '2020/2/8',
    '2020/2/9',
    '2020/2/10',
    '2020/2/11',
    '2020/2/12',
    '2020/2/13',
    '2020/2/14'
    ]



  # 各コマの想定人数

  NEED_PEOPLE = [
    #7,7,7,7,7,8,8,7,7,7,7,7,8,8
    4,    4,    3,    3,    5,    6,      6,
    4,    4,    3,    3,    5,    6,      6  
  ]



  def __init__(self, list):

    if list == None:

      self.make_sample()

    else:

      self.list = list

    self.employees = []



  # ランダムなデータを生成

  def make_sample(self):

    sample_list = []
    
    for num in range(140):

      sample_list.append(random.randint(0, 1))

    self.list = tuple(sample_list)



  # タプルを1ユーザ単位に分割

  def slice(self):

    sliced = []

    start = 0

    for num in range(10):

      sliced.append(self.list[start:(start + 14)])

      start = start + 14

    return tuple(sliced)



  # ユーザ別にアサインコマ名を出力する

  def print_inspect(self):

    user_no = 0

    for line in self.slice():

      print("ユーザ "+str(user_no))

      print(line)

      user_no = user_no + 1



      index = 0

      for e in line:

        if e == 1:

          print (self.SHIFT_BOXES[index])

        index = index + 1



  # CSV形式でアサイン結果の出力をする

  def print_csv(self):

    for line in self.slice():

      print(','.join(map(str, line)))



  # TSV形式でアサイン結果の出力をする

#  def print_tsv(self):

#    for line in self.slice():

#      print("\t".join(map(str, line)))



  # ユーザ番号を指定してコマ名を取得する

  def get_boxes_by_user(self, user_no):

    line = self.slice()[user_no]

    return self.line_to_box(line)



  # 1ユーザ分のタプルからコマ名を取得する

  def line_to_box(self, line):

    result = []

    index = 0

    for e in line:

      if e == 1:

        result.append(self.SHIFT_BOXES[index])

      index = index + 1

    return result    



  # コマ番号を指定してアサインされているユーザ番号リストを取得する

  def get_user_nos_by_box_index(self, box_index):

    user_nos = []

    index = 0

    for line in self.slice():

      if line[box_index] == 1:

        user_nos.append(index)

      index += 1

    return user_nos



  # コマ名を指定してアサインされているユーザ番号リストを取得する

  def get_user_nos_by_box_name(self, box_name):

    box_index = self.SHIFT_BOXES.index(box_name)

    return self.get_user_nos_by_box_index(box_index)



  # 想定人数と実際の人数の差分を取得する

  def abs_people_between_need_and_actual(self):

    result = []

    index = 0

    for need in self.NEED_PEOPLE:

      actual = len(self.get_user_nos_by_box_index(index))

      result.append(abs(need - actual))

      index += 1

    return result



  # 応募していないコマにアサインされている件数を取得する

  def not_applicated_assign(self):

    count = 0

    for box_name in self.SHIFT_BOXES:

      user_nos = self.get_user_nos_by_box_name(box_name)

      for user_no in user_nos:

        e = self.employees[user_no]

        if not e.is_applicated(box_name):

          count += 1

    return count




  # 週休2日　2日は出勤

  def few_or_lot(self):

    r = 0 
    result = []
    for user_no in range(10):

      #e = self.employees[user_no]

      ratio = len(self.get_boxes_by_user(user_no))
      #print("b",e,ratio)
      if ratio <=3 or ratio >=11 :

        r += 1 
      result.append(r)

    """for user_no in range(10):

      boxes = self.get_boxes_by_user(user_no)

      wdays = []

      for box in boxes:

        wdays.append(box)

      for wday_name in self.SHIFT_BOXES:

        if wdays.count(wday_name) >=11 or wdays.count(wday_name) <=3 :

          result.append(wday_name)
    """
    return result
    



# 従業員定義




e0 = Employee(0, "a", [1, 1, 1, 1, 1, 0, 0,1,0,1,1,1,1,0])



e1 = Employee(1, "b", [1, 1, 0, 0, 0, 1, 1,1, 1, 0, 1, 0, 1, 1])



e2 = Employee(2, "c", [1, 0, 0, 0, 0, 0, 1,1, 1, 0, 0, 0, 0, 1])


# 
e3 = Employee(3, "d", [0, 0, 0, 0, 1, 1, 1,0, 0, 0, 1, 0, 1, 1])


#
e4 = Employee(4, "e", [0, 1, 1, 0, 1, 1, 0,0, 1, 1, 0, 1, 1, 1])


#
e5 = Employee(5, "f", [1, 0, 1, 1, 1, 1, 0,1, 1, 1, 0, 1, 0, 0])



e6 = Employee(6, "g", [0, 0, 0, 0, 0, 1, 0,1, 0, 0, 0, 0, 1,0 ])



e7 = Employee(7, "h", [0, 1, 1, 1, 1, 1, 1,0, 0, 1, 1, 1, 1, 1])



e8 = Employee(8, "i", [1, 0, 1, 0, 1, 0, 0,1, 0, 1, 1, 1, 1, 0])



e9 = Employee(9, "j", [1, 1, 1, 0, 1, 0, 0,1, 1, 1, 0, 1, 0, 0])




employees = [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9]



def evalShift(individual):

  s = Shift(individual)

  s.employees = employees



  # 想定人数とアサイン人数の差

  people_count_sub_sum = sum(s.abs_people_between_need_and_actual())/14.0 #/140.0 

  # 応募していない時間帯へのアサイン数

  not_applicated_count = s.not_applicated_assign()/140.0 #/140.0 

  #f=0.2*people_count_sub_sum + not_applicated_count 
  # 週休2または出勤2以下従業員数

  few_or_lot_user = sum(s.few_or_lot())/10 #/ 10.0



  return (people_count_sub_sum, not_applicated_count,few_or_lot_user) #, three_box_per_day)
  


toolbox.register("evaluate", evalShift)

# 交叉関数を定義(二点交叉)

toolbox.register("mate", tools.cxTwoPoint)



# 変異関数を定義(ビット反転、変異隔離が5%ということ?)

toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)



# 選択関数を定義(トーナメント選択、tournsizeはトーナメントの数？)

toolbox.register("select", tools.selTournament, tournsize=3)




if __name__ == '__main__':
    
    f1_fit = [] 
    f2_fit = []
    f3_fit = []
    ims =[]
    ims2 =[]
    ims3=[]
    fig,ax = plt.subplots()
    #Shift=pd.read_csv("tab-shift.csv")

    # 初期集団を生成する

    pop = toolbox.population(n=30)

    CXPB, MUTPB, NGEN = 0.6, 0.4, 100 # 交差確率、突然変異確率、進化計算のループ回数



    print("進化開始")



    # 初期集団の個体を評価する

    fitnesses = list(map(toolbox.evaluate, pop))

    for ind, fit in zip(pop, fitnesses):  # zipは複数変数の同時ループ

        # 適合性をセットする

        ind.fitness.values = fit


    print("  "+str(len(pop))+" の個体を評価")



     # 進化計算開始

    for g in range(NGEN):

        print("-- "+str(g)+" 世代 --" )



        # 選択

        # 次世代の個体群を選択

        offspring = toolbox.select(pop, len(pop))

        # 個体群のクローンを生成

        offspring = list(map(toolbox.clone, offspring))



        # 選択した個体群に交差と突然変異を適応する



        # 交叉

        # 偶数番目と奇数番目の個体を取り出して交差

        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            if random.random() < CXPB:

                toolbox.mate(child1, child2)

                # 交叉された個体の適合度を削除する

                del child1.fitness.values

                del child2.fitness.values



        # 変異

        for mutant in offspring:

            if random.random() < MUTPB:

                toolbox.mutate(mutant)

                del mutant.fitness.values



        # 適合度が計算されていない個体を集めて適合度を計算

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

        fitnesses = map(toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitnesses):

            ind.fitness.values = fit


        print("  "+str(len(invalid_ind))+" の個体を評価")



        # 次世代群をoffspringにする

        pop[:] = offspring


        #ts = [ind.fitness.values for ind in pop]
        #print("len",len(ts),type(ts),"ts:",ts)
        # すべての個体の適合度を配列にする

        index = 1
        #print(pop[1].fitness.values)

        for v in ind.fitness.values:

          fits = [v for ind in pop]



          length = len(pop)

          mean = sum(fits) / length

          sum2 = sum(x*x for x in fits)

          std = abs(sum2 / length - mean**2)**0.5



          print("* パラメータ"+str(index)) 

          print("  Min %s" % min(fits))

          print("  Max %s" % max(fits))

          print("  Avg %s" % mean)

          print("  Std %s" % std)
          

          index += 1
        
        t_ind = tools.selBest(pop, 1)[0]
        print("最大適応度：",t_ind.fitness.values)
        SS = Shift(t_ind)
        print("シフト")
        SS.print_csv()
#        if max(fits)>=1.0 :
 #           print("aaaaaa")
  #          break
        f1_fit.append(t_ind.fitness.values[0])
        f2_fit.append(t_ind.fitness.values[1])
        f3_fit.append(t_ind.fitness.values[2])
        im = ax.plot(f1_fit,'r-o')
        ims.append(im)
        im2 = ax.plot(f2_fit,'b-o')
        ims2.append(im2)
        im3 = ax.plot(f3_fit,'g-o')
        ims3.append(im3)


    print("-- 進化終了 --")



    best_ind = tools.selBest(pop, 1)[0]

    print("最も優れていた個体: %s, %s" % (best_ind, best_ind.fitness.values))

    s = Shift(best_ind)

    s.print_csv()
    """t=range(0,len(f1_fit))
    ax.plot(t,f1_fit,label="1")
    ax.plot(t,f2_fit,label="2")
    ax.plot(t,f3_fit,label="3")
    plt.legend()
    plt.show()
    """
    ani = animation.ArtistAnimation(fig, ims,blit = True)
    ani2 = animation.ArtistAnimation(fig, ims2,blit = True)
    ani3 = animation.ArtistAnimation(fig, ims3,blit = True)
    plt.show()
     
    best=best_ind
    BEST=[best[i:i+14] for i in range(0,len(best),14)]
    SCEDULE=pd.DataFrame(BEST,columns=s.SHIFT_BOXES)
    SCEDULE    
    #s.print_tsv()
#SCEDULE
num=SCEDULE.sum()
num.name="合計"
SCEDULE=SCEDULE.append(num)
d=SCEDULE.sum(axis=1)
SCEDULE=SCEDULE.assign(勤務日数=d)
need=s.NEED_PEOPLE
need.append("-")
SCEDULE.loc['必要']=need
#need.name="必要人数"
#SCEDULE=SCEDULE.append(need)
SCEDULE

