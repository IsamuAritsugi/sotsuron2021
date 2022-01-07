# coding: utf-8
import random
import csv
from operator import attrgetter
import time
import datetime

t1 = time.time()
ima_time = datetime.datetime.now()

#-----以下の内容を手打ちで変更する-----

fixed_worldstep = 50  # シミュレーションの実行回数
fixed_timestep = 1000  # 1回のシミュレーションでの試行年数

# 昇進方法
protype = "B-"  # 最も有能を昇進
# protype = "R-"  # ランダムで昇進
# protype = "W-"  # 最も無能を昇進

# 能力が受け継がれるか
hypotype = "CS-" # 昇進後も能力が受け継がれる
# hypotype = "PP-" # 能力が受け継がれない

# 身分境界線の設定方法の名称。CSVファイルタイトルに記載される。
classtype = "1_123-456"
#"0_123456" "1_123-456" "2_12345-6-1" "3_1234-5-7-6" "4_1-3-6-11-21-41"
#"p_1-23456" "q_12-3456" "r-123-456" "s-1234-56" "t-12345-6" "u-1-2-5-10-20-0"

# 身分境界線の上下どちらかの組織の構成人数。
num_companyA = [1, 5, 11, 0, 0, 0]
# [1, 5, 11, 21, 41, 81] [1, 5, 11, 0, 0, 0] [1, 5, 11, 21, 41, 1] [1, 5, 11, 21, 7, 0] [1, 3, 6, 11, 21, 41]
# [1, 0, 0, 0, 0, 0] [1, 5, 0, 0, 0, 0] [1, 5, 11, 0, 0, 0] [1, 5, 11, 21, 0, 0] [1, 5, 11, 21, 41, 0] [1,2,5,10,20,0]

# 出力するSCVファイルの名称。
str_ima_time = classtype+"-"+hypotype+protype+"fws"+str(fixed_worldstep)+"-"+"fts"+str(fixed_timestep)+ima_time.strftime(
    "-%m-%d-%H-%M-")
listname = str_ima_time+"-lasts_ex_list"+".csv"
# 例：1_123-456-CS-B-fws50-fts1000-01-07-15-14--lasts_ex_list.csv

#-----以上の内容を手打ちで変更する-----

ex_list_all = []  # 出力するリストを定義
num_companyB = []

#各階の部屋の数
number_of_Tier1, number_of_Tier2, number_of_Tier3, number_of_Tier4, number_of_Tier5, number_of_Tier6 = 1, 5, 11, 21, 41, 81
number_of_Tiers = [number_of_Tier1, number_of_Tier2, number_of_Tier3,
                   number_of_Tier4, number_of_Tier5, number_of_Tier6]

for i in range(len(number_of_Tiers)):
    num_companyB.append(number_of_Tiers[i]-num_companyA[i])
num_companys = [num_companyA, num_companyB]


class Agent:
    def __init__(self, number, age, competence, newemployee, stay):
        self.number = number     #
        self.age = age  # 平均27　標準偏差5
        self.competence = competence  # 平均7　標準偏差2
        self.newemployee = newemployee  # 新入社員かどうか　新入社員なら無能でも残留。
        self.stay = stay  # 残れるかどうか


def setAge():
    randomAge = random.gauss(27, 5)
    return randomAge

def setCompetenceto10not0():
    randomCompetence = 100
    while(randomCompetence < 0 or 10 < randomCompetence):
        randomCompetence = random.gauss(7, 2)

    return randomCompetence


def addTimestep(n):
    n = n+1
    return n


def rECal(list):
    roomEfficency = 0.0
    for a in list:
        roomEfficency += a.competence

    return roomEfficency


def getEpercentage(a, b):
    return a/b*100


def addAgentage(n):
    n = n+1
    return n


def isroomstayok(list):
    b = True
    for a in list:
        if a.stay == True:
            continue
        else:
            b = False
    return b


def jyuutou(roomlist, numroomlist, i, ptype, htype):
    #そのルームに人を充当する。埋めたときに、能力値を再判定する。
    this_i = i
    while(len(roomlist[this_i]) != numroomlist[this_i]):
        if i != 5:  # その一つ下のリストがあるかどうかの判定 iは0-5
            if(len(roomlist[i+1]) != 0):  # 一つ下に人がいるとき

                if ptype == "W-":
                    #-WORST
                    #昇進の基準
                    roomlist[i+1].sort(key=attrgetter("competence"))
                    #その人の能力を再判定
                    if htype == "CS-":
                        somecomp = roomlist[i+1][-1].competence
                        roomlist[i +
                                 1][-1].competence += random.uniform(-1.0, 1.0)
                        # 能力が10を超えないように再判定する。
                        while(roomlist[i+1][-1].competence > 10):
                            roomlist[i+1][-1].competence = somecomp + \
                                random.uniform(-1.0, 1.0)
                    else:
                        roomlist[i+1][0].competence = setCompetenceto10not0()
                    #昇進した人を昇進先のルームに充当。
                    roomlist[this_i].append(roomlist[i+1][0])
                    del roomlist[i+1][0]

                elif ptype == "B-":
                    #-BEST
                    #昇進の基準
                    roomlist[i+1].sort(key=attrgetter("competence"))
                    #その人の能力を再判定

                    if htype == "CS-":
                        somecomp = roomlist[i+1][-1].competence
                        roomlist[i +
                                 1][-1].competence += random.uniform(-1.0, 1.0)
                        # 能力が10を超えないように再判定する。
                        while(roomlist[i+1][-1].competence > 10):
                            roomlist[i+1][-1].competence = somecomp + \
                                random.uniform(-1.0, 1.0)
                    else:
                        roomlist[i+1][-1].competence = setCompetenceto10not0()
                    #昇進した人を昇進先のルームに充当。
                    roomlist[this_i].append(roomlist[i+1][-1])
                    del roomlist[i+1][-1]

                elif ptype == "R-":
                    #-RANDOM
                    #昇進の基準
                    roomlist[i+1].sort(key=attrgetter("competence"))
                    #その人の能力を再判定
                    random.shuffle(roomlist[i+1])
                    #その人の能力を再判定
                    if htype == "CS-":
                        somecomp = roomlist[i+1][-1].competence
                        roomlist[i +
                                 1][-1].competence += random.uniform(-1.0, 1.0)
                        # 能力が10を超えないように再判定する。
                        while(roomlist[i+1][-1].competence > 10):
                            roomlist[i+1][-1].competence = somecomp + \
                                random.uniform(-1.0, 1.0)
                    else:
                        roomlist[i+1][0].competence = setCompetenceto10not0()
                    #昇進した人を昇進先のルームに充当。
                    roomlist[this_i].append(roomlist[i+1][0])
                    del roomlist[i+1][0]

            else:
                i = i+1
                #print("i:",i)
        else:
            numnum = agent_Name_Num+1
            agents.append(Agent(numnum, setAge(),
                                setCompetenceto10not0(), True, True))
            roomlist[this_i].append(agents[-1])


def addavelist(alllist, lastlist):
    for i in range(len(alllist[0])-1):
        e_ts = 0
        ave_e_ts = 0
        for g in range(len(alllist)-1):
            e_ts += alllist[g+1][i+1]
            ave_e_ts = e_ts/(len(alllist)-1)
        lastlist.append(ave_e_ts)

    alllist.append(lastlist)


#出力するリストの最初の行を定義
ex_list_01 = []
ex_list_01.append("w-t")
for i in range(fixed_timestep+1):
    ex_list_01.append(i)
    i = i+1

ex_list_all.append(ex_list_01)

#最後に出力するものを定義
lasts_ex_list = []
lasts_ex_list.append(ex_list_01)

#roomごとの効率を出力するリストの最初の行を定義
roomX_list_01 = []
roomX_list_01.append("w-t")
for i in range(fixed_timestep+1):
    roomX_list_01.append(i)

room1_list_all, room2_list_all, room3_list_all, room4_list_all, room5_list_all, room6_list_all = [], [], [], [], [], []
room1to6_list_all = [room1_list_all, room2_list_all,
                     room3_list_all, room4_list_all, room5_list_all, room6_list_all]
for i in room1to6_list_all:
    i.append(roomX_list_01)


#部屋を作成
room1_A, room2_A, room3_A, room4_A, room5_A, room6_A = [], [], [], [], [], []
room1_B, room2_B, room3_B, room4_B, room5_B, room6_B = [], [], [], [], [], []

#会社を作成
company_A = [room1_A, room2_A, room3_A, room4_A, room5_A, room6_A]
company_B = [room1_B, room2_B, room3_B, room4_B, room5_B, room6_B]
companys = [company_A, company_B]

timestep = 0
ws = 0
agents = []
agent_Name_Num = 0

#各部屋の効率
rbilityL = [1.0, 0.9, 0.8, 0.6, 0.4, 0.2]

#全体の効率計算
MaxE = 0
xi = 0
for kazu in number_of_Tiers:
    MaxE = MaxE + 10*kazu*rbilityL[xi]
    xi = xi+1

print("fws:", fixed_worldstep)
print("fts:", fixed_timestep)
print("MaxE:", MaxE)


for fws in range(fixed_worldstep):

    #各シミュレーションで最初に行う処理。
    timestep = 0
    agents.clear()
    agent_Name_Num = 0

    for cs in companys:
        for rs in cs:
            rs.clear()

    room1_A, room2_A, room3_A, room4_A, room5_A, room6_A = [], [], [], [], [], []
    room1_B, room2_B, room3_B, room4_B, room5_B, room6_B = [], [], [], [], [], []

    company_A.clear()
    company_A = [room1_A, room2_A, room3_A, room4_A, room5_A, room6_A]
    company_B.clear()
    company_B = [room1_B, room2_B, room3_B, room4_B, room5_B, room6_B]
    companys = [company_A, company_B]

    #部屋に、何かをとりあえず充当する
    yi = 0
    zi = 0
    for nc in num_companys:
        yi = 0
        for num in nc:
            for i in range(num):
                companys[zi][yi].append(i)
            yi += 1
        zi += 1

    for cp in companys:
        for rs in cp:
            for i in range(len(rs)):
                agents.append(Agent(agent_Name_Num, setAge(),
                              setCompetenceto10not0(), True, True))
                agent_Name_Num += 1

    #部屋に社員を充当
    n = 0
    for cp in companys:
        for rs in cp:
            for i in range(len(rs)):
                rs[i] = agents[n]
                n += 1

    RealE = 0
    for cp in companys:
        for i in range(len(cp)):
            RealE += rECal(cp[i])*rbilityL[i]

    print("----------")
    print("worldstep:", ws+1)
    print("E(%):", getEpercentage(RealE, MaxE))
    print("初期状態準備完了")

    #timestep0の時の状態
    ex_list_XX = []
    ex_list_XX.clear()
    ex_list_XX.append(ws+1)
    ex_list_XX.append(getEpercentage(RealE, MaxE))

    #timestep0の時の状態をリストに記録
    room1_list_XX, room2_list_XX, room3_list_XX, room4_list_XX, room5_list_XX, room6_list_XX = [], [], [], [], [], []
    room1to6_list_XX = [room1_list_XX, room2_list_XX,
                        room3_list_XX, room4_list_XX, room5_list_XX, room6_list_XX]
    for i in room1to6_list_XX:
        i.clear()
        i.append(ws+1)

    MaxRoom1to6E = []
    for i in number_of_Tiers:
        MaxRoom1to6E.append(10*i)

    RealRoom1to6E = []
    for i in range(len(room1to6_list_XX)):
        e = 0
        for cp in companys:
            e += rECal(cp[i])
        RealRoom1to6E.append(e)

    for i in range(len(room1to6_list_XX)):
        room1to6_list_XX[i].append(getEpercentage(
            RealRoom1to6E[i], MaxRoom1to6E[i]))

    for fts in range(fixed_timestep):  # 繰り返し文

        #年次が変わった時の処理
        #timestepを１足す
        timestep = addTimestep(timestep)

        #社員の年齢を1足す
        for a in agents:
            a.age = addAgentage(a.age)

        #新入社員ではなくする
        for a in agents:
            a.newemployee = False

        #全員に対して残留判定。
        for cp in companys:
            for rs in cp:
                for a in rs:
                    if a.newemployee == False:
                        if a.age >= 60 or a.competence < 4.0:
                            a.stay = False

        #この時点で退職すべき人は、全員退職させる。
        for cp in companys:
            for rs in cp:
                for a in rs:
                    if a.stay == False:
                        rs.remove(a)

        #このあと、昇進する人は昇進して、能力値の再判定が行われる。再判定後の能力が無能でも、退職しない。
        #全員が充当され、かつその全員が残留OKになるまで繰り返す

        for cp in range(len(companys)):  # cp ->0 1
            for g in range(len(companys[cp])):  # g -> 0 1 2 3 4 5
                jyuutou(companys[cp], num_companys[cp], g, protype, hypotype)

        RealE = 0
        for cp in companys:
            for i in range(len(cp)):
                RealE += rECal(cp[i])*rbilityL[i]

        print("E(%):", getEpercentage(RealE, MaxE))

        # listに出力
        ex_list_XX.append(getEpercentage(RealE, MaxE))

        RealRoom1to6E.clear()
        for i in range(len(room1to6_list_XX)):
            e = 0
            for cp in companys:
                e += rECal(cp[i])
            RealRoom1to6E.append(e)

        for i in range(len(room1to6_list_XX)):
            room1to6_list_XX[i].append(getEpercentage(
                RealRoom1to6E[i], MaxRoom1to6E[i]))

    ex_list_all.append(ex_list_XX)

    for i in range(len(room1to6_list_all)):
       room1to6_list_all[i].append(room1to6_list_XX[i])

    ws += 1

#出力する最終行に平均を記載
ex_list_last = []
ex_list_last.append(hypotype+protype+classtype)

room1_list_last, room2_list_last, room3_list_last, room4_list_last, room5_list_last, room6_list_last = [], [], [], [], [], []
room1to6_list_last = [room1_list_last, room2_list_last,
                      room3_list_last, room4_list_last, room5_list_last, room6_list_last]

x = 1
for i in room1to6_list_last:
    i.append(hypotype+protype+classtype+"-room"+str(x))
    x += 1

addavelist(ex_list_all, ex_list_last)

for i in range(len(room1to6_list_all)):
    addavelist(room1to6_list_all[i], room1to6_list_last[i])

for i in room1to6_list_last:
    lasts_ex_list.append(i)

lasts_ex_list.append(ex_list_all[-1])




with open(listname, "w", newline="", encoding="utf-16") as f:  # csvファイルを書き込みモードで開く
    writer = csv.writer(f, dialect="excel-tab")
    writer.writerows(lasts_ex_list)

print("----------")
print("timestep:", timestep)
t2 = time.time()
print("経過時間", t2-t1)
print("処理を終了します")
