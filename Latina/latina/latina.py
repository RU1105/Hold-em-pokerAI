import csv
import sklearn
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets
import numpy as np
import os
import matplotlib.pyplot as plt
import math
import threading
import random

class latina (): 
    def __init__(self): 
        self.model = []
        self.round_value = []
        self.train_model = []
    def board_card(self,index,action_index,player1_hand,player2_hand,player1,player2):  #顯示public_card(公共牌)，index為一列資料
        if(action_index == int(float(player2[index]['Flop0']))) :                       #檢查是否為FLOP的位置
            player1_hand[0] = (int(float(player1[index]['Flop0'])))                     #把FLOP第1張放入[0]的位置
            player2_hand[0] = (int(float(player1[index]['Flop0'])))                     #把FLOP第1張放入[0]的位置
            player1_hand[1] = (int(float(player1[index]['Flop1'])))
            player2_hand[1] = (int(float(player1[index]['Flop1'])))
            player1_hand[2] = (int(float(player1[index]['Flop2'])))
            player2_hand[2] = (int(float(player1[index]['Flop2'])))
        if(action_index ==  int(float(player2[index]['Flop1']))) :                      #public_card(Turn)
            player1_hand[3] = (int(float(player1[index]['Turn'])))
            player2_hand[3] = (int(float(player1[index]['Turn'])))
        if(action_index == int(float(player2[index]['Flop2']))) :                       #public_card(River)
            player1_hand[4] = (int(float(player1[index]['River'])))
            player2_hand[4] = (int(float(player1[index]['River'])))
        
        return player1_hand,player2_hand

    def is_next_move_end (self,player,action_index):    #show、蓋牌、無動作(便是下一步為結束)
        if int(float(player['Action'+str(action_index)])) == 6 or int(float(player['Action'+str(action_index)])) == 7 or int(float(player['Action'+str(action_index)])) == -1 or int(float(player['Action'+str(action_index)])) == -2: 
            return True
        else :
            return False

    def open_csv(self,dirPath,file_name,player1,player2):
        print("reading file from [ " +dirPath + "\\" +file_name + " ] ......")
        path = (os.path.abspath('.'))
        #with open( path + r'\data\onemerge.csv', newline='') as csvfile:
        with open(dirPath + "\\" +file_name, newline='',encoding='utf-8') as csvfile: # 開啟 CSV 檔案至csvfile
            # 讀取 CSV 檔內容，將每一列轉成一個 dictionary
            rows = csv.DictReader(csvfile) #csv.DictReader可以資料查找 d = {key1: value1, key2: value2}
            
            row_divide = 0
            # 以迴圈輸出指定欄位
            for row in rows:
                if row_divide %2 == 0 :
                    player1.append(row)
                else :
                    player2.append(row)
                row_divide += 1
        print("finish [ " +dirPath + "\\" +file_name + " ] reading")

    def csv_files(self,dirPath,player1,player2):
        temp = (os.listdir(dirPath)) #os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。
        for i in range(len(temp)-1):
            token_temp = temp[i].split(".")
            if(token_temp[1]=="csv"):
                self.open_csv(dirPath,temp[i],player1,player2)

    def set(self):
        player1 = []
        player2 = []
        self.csv_files(r"D:\pork1\dataset\EXCEL\.csv",player1,player2)
        print("total data : " + str(len(player1)))
        print("start training")
        x = []
        y = []
        
        for index in range(len(player1)) : #index是參數0 ~ 133332
            player1_hand = [-1,-1,-1,-1,-1] 
            player2_hand = [-1,-1,-1,-1,-1]
            player1_show = True
            player2_show = True
            flop_index = int(float(player2[index]['Flop0']))  #前三張公共牌
            turn_index = int(float(player2[index]['Flop1']))  #第四張公共牌
            river_index = int(float(player2[index]['Flop2'])) #第五張公共牌
            count = 3
            move_first = 0
            big_blind = 1
            small_blind_amount = 0
            if int(float(player1[index]['Hands0'])) != -1 :
                player1_hand.append(int(float(player1[index]['Hands0'])))  #append方法是將元素加在串列最後面
                player1_hand.append(int(float(player1[index]['Hands1'])))
                player1_hand.append(self.set_hands_level(int(float(player1[index]['Hands0'])),int(float(player1[index]['Hands1']))))
                player1_hand.append(float(player1[index]['Chips']))
                player1_hand.append(float(player2[index]['Chips']))
            else :
                player1_show = False
                
            if int(float(player2[index]['Hands0'])) != -1 :
                player2_hand.append(int(float(player2[index]['Hands0'])))
                player2_hand.append(int(float(player2[index]['Hands1'])))
                player2_hand.append(self.set_hands_level(int(float(player2[index]['Hands0'])),int(float(player2[index]['Hands1']))))
                player2_hand.append(float(player2[index]['Chips']))
                player2_hand.append(float(player1[index]['Chips']))
            else :
                player2_show = False
                
            if int(float(player1[index]['Action0'])) == 0 : #下小盲注
                self.list_set(player1_hand,player2_hand,player1[index],0,small_blind_amount,1)
                self.list_set(player1_hand,player2_hand,player2[index],0,small_blind_amount,0)
                if player1_show :
                    x.append(self.check_strength(player1_hand[0:7])+player1_hand[:]+[-1]*(14-len(player1_hand)))
                    y.append(player1[index]['Action'+str(1)])
            else :
                self.list_set(player1_hand,player2_hand,player2[index],0,small_blind_amount,0)
                self.list_set(player1_hand,player2_hand,player1[index],0,small_blind_amount,1)
                move_first = 1  #???
                big_blind = 0
                if player2_show :
                    x.append(self.check_strength(player1_hand[0:7])+player2_hand[:]+[-1]*(14-len(player2_hand)))
                    y.append(player2[index]['Action'+str(1)])

            for action_index in range(1,10) :
                board_card_open = False
                if move_first == 0 :
                        
                    if count == flop_index or count == turn_index or count == river_index:
                        board_card_open = True
                        player1_hand,player2_hand = self.board_card(index,count,player1_hand,player2_hand,player1,player2)
                        move_first = big_blind
                        if move_first == 0:
                            if self.is_next_move_end(player1[index],action_index+1):
                                break
                        else:
                            if self.is_next_move_end(player2[index],action_index+1):
                                break
                    else :
                        if self.is_next_move_end(player2[index],action_index) :
                            break

                    if player1_show :
                        if board_card_open :
                            if move_first == 0:
                                x.append(self.check_strength(player1_hand[0:7])+player1_hand[:]+[-1]*(14-len(player1_hand)))
                                y.append(player1[index]['Action'+str(action_index+1)])
                            else :
                                x.append(self.check_strength(player1_hand[0:7])+player2_hand[:]+[-1]*(14-len(player2_hand)))
                                y.append(player2[index]['Action'+str(action_index+1)])
                        else:
                            x.append(self.check_strength(player1_hand[0:7])+player2_hand[:]+[-1]*(14-len(player2_hand)))
                            y.append(player2[index]['Action'+str(action_index)])
                    
                    if board_card_open:
                        count += 1
                        continue
                    count += 1
                    board_card_open = False

                    if count == flop_index or count == turn_index or count == river_index:
                        move_first = big_blind
                        board_card_open = True
                        player1_hand,player2_hand = self.board_card(index,count,player1_hand,player2_hand,player1,player2)
                    if move_first == 0:
                        if self.is_next_move_end(player1[index],action_index+1) :
                            break
                    else:
                        if self.is_next_move_end(player2[index],action_index+1) :
                            break
                    
                    if player2_show :
                        if move_first == 0:
                            x.append(self.check_strength(player1_hand[0:7])+player1_hand[:]+[-1]*(14-len(player1_hand)))
                            y.append(player1[index]['Action'+str(action_index+1)])
                        else :
                            x.append(self.check_strength(player1_hand[0:7])+player2_hand[:]+[-1]*(14-len(player2_hand)))
                            y.append(player2[index]['Action'+str(action_index+1)])

                    if board_card_open:
                        move_first = big_blind
                    count += 1
                    
                else:
                        
                    if count == flop_index or count == turn_index or count == river_index:
                        move_first = big_blind
                        board_card_open = True
                        player1_hand,player2_hand = self.board_card(index,count,player1_hand,player2_hand,player1,player2)
                        if move_first == 0:
                            if self.is_next_move_end(player1[index],action_index+1) :
                                break
                        else:
                            if self.is_next_move_end(player2[index],action_index+1) :
                                break
                    else:
                        if self.is_next_move_end(player1[index],action_index) :
                            break
                        
                    if player2_show :
                            
                        if board_card_open :
                            if move_first == 0:
                                x.append(self.check_strength(player1_hand[0:7])+player1_hand[:]+[-1]*(14-len(player1_hand)))
                                y.append(player1[index]['Action'+str(action_index+1)])
                            else :
                                x.append(self.check_strength(player1_hand[0:7])+player2_hand[:]+[-1]*(14-len(player2_hand)))
                                y.append(player2[index]['Action'+str(action_index+1)])
                        else :
                            x.append(self.check_strength(player1_hand[0:7])+player1_hand[:]+[-1]*(14-len(player1_hand)))
                            y.append(player1[index]['Action'+str(action_index)])

                    if board_card_open:
                        move_first = big_blind
                        count += 1
                        continue
                    count += 1
                    board_card_open = False

                    if count == flop_index or count == turn_index or count == river_index:
                        move_first = big_blind
                        player1_hand,player2_hand = self.board_card(index,count,player1_hand,player2_hand,player1,player2)

                    if move_first == 0:
                        if self.is_next_move_end(player1[index],action_index+1) :
                            break
                    else:
                        if self.is_next_move_end(player2[index],action_index+1) :
                            break
                        
                    if player1_show :
                            
                        if board_card_open:
                            if move_first == 0:
                                x.append(self.check_strength(player1_hand[0:7])+player1_hand[:]+[-1]*(14-len(player1_hand)))
                                y.append(player1[index]['Action'+str(action_index+1)])
                            else :
                                x.append(self.check_strength(player1_hand[0:7])+player2_hand[:]+[-1]*(14-len(player2_hand)))
                                y.append(player2[index]['Action'+str(action_index+1)])
                        else :
                            x.append(self.check_strength(player1_hand[0:7])+player2_hand[:]+[-1]*(14-len(player2_hand)))
                            y.append(player2[index]['Action'+str(action_index+1)])

                    if count == flop_index or count == turn_index or count == river_index:
                        move_first = big_blind
                    count += 1
        
        #行動的決策樹參數設定
        self.model = RandomForestClassifier(n_estimators=10,max_depth = 15,random_state=2)#30棵樹 10層 生成種子為1的同一批森林 真正訓練在fit()
        #self.model = RandomForestClassifier(n_estimators=2,max_depth = 15,random_state=2)#
        
        if 0 == 1:
            self.train(x,y)
        else:
            X_train, X_test, Y_train, Y_test = train_test_split(x, y,test_size=0.3, random_state=3)
            self.train(X_train,Y_train)
            self.score(X_test,Y_test)

        """
        two=0
        three=0
        four=0
        eight=0
        for i in range(len(y)):
            if int(float(y[i]))==2:
                two+=1
            if int(float(y[i]))==3:
                three+=1
            if int(float(y[i]))==4:
                four+=1
            if int(float(y[i]))==8:
                eight+=1
        print('2---')
        print(two)
        print('3---')
        print(three)
        print("4---")
        print(four)
        print("8---")
        print(eight)
        
        """
        print (len(y))
    
    def set_hands_level(self,hand1,hand2):
        hand1_suit = (hand1%4)  #花色
        hand2_suit = (hand2%4)
        hand1 = math.floor(hand1/4) #向下取整數，找不同花色同樣數字
        hand2 = math.floor(hand2/4)
        if  (hand1_suit == hand2_suit ):    #同花色
            if(hand1 > hand2):
                return int(self.set_level(hand1,hand2,1))
            else:
                return int(self.set_level(hand2,hand1,1))
        else :
            if(hand1 > hand2):
                return int(self.set_level(hand1,hand2,0))
            else:
                return int(self.set_level(hand2,hand1,0))

    def set_level(self,hand1,hand2,suit_same):  
        if(suit_same==1):
            if(abs(hand1-hand2)<4): #絕對值
                return 2
            elif(hand1>7 and hand2>10) :
                return 3
            elif((hand1>7 or hand2>10)or(hand1 == 1)) :
                return 4
            else:
                return 5
        else:
            if(hand1==hand2):
                return 1
            elif((abs(hand1-hand2)<3)or hand1==1):
                return 3
            elif(hand1>8 or hand2>10):
                return 4
            else :
                return 5
    
    def predict(self,input):
        output = int(float(self.model.predict(np.array(input).reshape(1, -1))))
        print("predict :",output)
        return output
    
    def train(self,X_train,Y_train):
        #決策樹使用X_train和Y_train training
        self.model.fit(X_train, Y_train)
    
    def score(self,X_test,Y_test):
        score = self.model.score(X_test,Y_test)
        print("score: ",score,"\n")
    
    def list_set(self,player1_hand,player2_hand,player_list,action_index,big_blind_amount,player_onmove):
        self.set_action(player1_hand,player2_hand,player_list,action_index,player_onmove)
        #self.set_remark(player1_hand,player2_hand,player_list,action_index,big_blind_amount)
        return player1_hand,player2_hand
    
    def set_action(self,player1_hand,player2_hand,player_list,action_index,player_onmove):
        player1_hand.append(int(float(player_list['Action'+str(action_index)])))
        player1_hand.append(player_onmove)
        player2_hand.append(int(float(player_list['Action'+str(action_index)])))
        player2_hand.append(player_onmove)
        return player1_hand,player2_hand
    
    def bargain(self,input,input2): #籌碼好像沒用到
        input1=[]
        empty_check=7
        for i in range(len(input)): #去除-1
            if input[i]!=-1:
                input1.append(input[i])
                empty_check-=1
        card=input1
        chip=input2[0]+input2[1]
        print("hands card:",card," chip:",chip,'empty :',empty_check)
        type=self.card_strength2(card)
        type.append(empty_check)
        my_raise=self.raise_decide(type,chip)

        return my_raise
    
    def check_strength(self,input): #檢查強度?
        input1=[]
        empty_check=7
        for i in range(len(input)): #去除-1
            if input[i]!=-1:
                input1.append(input[i])
                empty_check-=1
        card=input1
        temp=self.card_strength(card)
        type=[]
        type.append(temp[0])
        return type

    def raise_decide(self,type_in,chip):
        type=type_in[0]
        key=type_in[1]#用來判斷低階牌型的點數
        empty=type_in[2]
        odd_win=-1  #單數
    #------基礎勝率賦予---------
    #type 0高牌 1一對 2三條 3兩對 4順子 5同花 6葫蘆 7鐵支 8同花順 9同順缺1 10同花缺1 11同花缺2 12順缺1
        if(type==0):    #高牌
            odd_win=50  #機率50/100
        elif(type==1):  #一對
            odd_win=80
        elif(type==2):  #三條
            odd_win=90
        elif(type==3):  #兩對
            odd_win=100
        elif(type==4):  #順子
            odd_win=60
        elif(type==5):  #同花
            odd_win=70
        elif(type==6):  #葫蘆
            odd_win=80
        elif(type==7):  #鐵支
            odd_win=90
        elif(type==8):  #同花順
            odd_win=95
        elif(type==9):  #同花順缺1
            odd_win=1
        elif(type==10):  #同花缺1
            odd_win=30
        elif(type==11):  #同花缺2
            odd_win=3
        elif(type==12):  #順缺
            odd_win=2
        print("basic odd:", odd_win)
    #----低階牌型校正-----------
        if(type<=3):
            if(key==12): #A
                odd_win=odd_win*0.5
            elif(key==11): #K
                odd_win=odd_win*0.45
            elif(key==10): 
                odd_win=odd_win*0.4
            elif(key==9):
                odd_win=odd_win*0.35
            elif(key==8): #10
                odd_win=odd_win*0.3
            else:
                odd_win=odd_win*0.15
            print("lower fix:",odd_win)
    #-----未完成大型牌機率補正--------
        elif(type>=9 and type <= 12 and type != 11):
            if(empty==2):   #4
                odd_win=odd_win*2
            elif(empty==0): #2
                odd_win=50*0.15
            print("upper fix:",odd_win)
        elif(type == 11):   #K
            if(empty==2):
                odd_win=22
            else:
                odd_win=12
            print("upper fix:",odd_win)
    #-----用勝率決定raise量---------
        new_chip=0
        if(odd_win>=70):
            new_chip=10+chip*0.75
        elif(odd_win>=50):
            new_chip=10+chip*0.5
        elif(odd_win>30):
            new_chip=10+chip*0.3
        else:
            new_chip=10+(chip*0.25)
        print("new chip:",new_chip)
        return new_chip

    def card_strength(self,card):
        length=len(card) #目前場上牌量+手牌
        for i in range(length):
            card[i] = int(card[i])
        ranks = []
        suits = []
        type = []
        #0-51除以4 商數為點數 餘數為花色
        for i in range(length):
            ranks.append(card[i] // 4 )
            suits.append(card[i] % 4 )

        #判斷FLUSH(同花順或同花大順或同花)
        #產生重複的花色的key與value
        dictOf_suits =self.Duplicates(suits)
        flush = -1
        flush_suits = -1
        for key, value in dictOf_suits.items():

            #重複超過五次確定為FLUSH
            if(value >= 5) :
                flush_suits = key
                flush = 1
            elif(value==4):
                flush_suits = key
                flush = 2 #缺牌1
            elif(value==3):
                flush_suits = key
                flush = 3 #缺牌2

        #判斷STRAIGHT

        #點數排序
        rank_sorted = sorted(ranks)

        #刪除重複的點數
        rank_list = list(set(rank_sorted))

        #判斷
        straight = -1
        result = 0
        flag=0 #在[1 2 3 4] [5 6] [9]狀況下 1234的缺一能被保留紀錄不被洗掉
        for i in range(0, len(rank_list)):#統計相等的個數 或者是否為順子
            if rank_list[i]-rank_list[i-1] == 1:
                result += 1#如果為順子，則result=4
                if result == 4:
                    flag = 1
                elif result == 3:
                    flag = 2 
            else:
                result = 0 #中斷就歸零   
            if flag == 1 :
                straight=1
            elif flag == 2:
                straight=2


        #A起頭 5結尾 的順子
        if len(rank_list)>=4 : 
            if rank_list[len(rank_list)-1]==12 and rank_list[0]==0 and rank_list[1]==1 and rank_list[2]==2 and rank_list[3]==3:
                straight = 1
        
        #同花順
        if(flush == 1 and straight == 1):
            type.append(8)
            type.append(0)
            return type
        elif(flush == 1 and straight ==2):
            type.append(9)
            type.append(0)
            return type


        #ranks重複的判斷   0=none 2=pair 3=threeKind 4=fourKind 5=twoPairs 6=fullhouse 
        ranks_type = 0
        ranks_type_keys = -1
        dictOf_ranks = self.Duplicates(ranks)
        for key, value in dictOf_ranks.items(): #0高牌 2一對 3三條 4鐵支 5兩對 6葫蘆
            #重複超過四次確定為 FOUR OF A KIND(四條)
            if( value == 4 ) :
                ranks_type = 4
                break 

            #重複超過三次確定為 FULL HOUSE(葫蘆) or THREE OF A KIND 
            if( value == 3 ) :

                #已經有2 PAIRS 升級為 FULL HOUSE
                if (ranks_type == 5 ):
                    ranks_type = 6
                    break
                
                #已經有1 PAIR 升級為 FULL HOUSE
                elif (ranks_type == 2 or ranks_type == 3):
                    ranks_type = 6
                    break
                
                #THREE OF A KIND(三條)
                else :
                    ranks_type = 3
                    ranks_type_keys = key

            #重複超過兩次確定為 FULL HOUSE or 2 PAIRS or PAIR
            if( value == 2 ) :
                #已經有三條 升級為 葫蘆
                if (ranks_type == 3):
                    ranks_type = 6
                    break

                #已經有PAIR 升級為 2 PAIRS
                elif (ranks_type == 2) :
                    if(ranks_type==2 or ranks_type==5 or ranks_type==0):
                        ranks_type_keys=key
                    ranks_type = 5

                #PAIR
                elif(ranks_type==2):
                    if(ranks_type==2 or ranks_type==0): 
                        ranks_type_keys=key
                        ranks_type = 2
                else:
                    ranks_type = 2
                    ranks_type_keys = key
        if(ranks_type_keys == -1) and len(rank_sorted)>0:
            ranks_type_keys=rank_sorted[len(rank_sorted)-1]       
        #-------OUTPUT----------------
        #type 0高牌 1一對 2三條 3兩對 4順子 5同花 6葫蘆 7鐵支 8同花順 9同順缺1 10同花缺1 11同花缺2 12順缺1
        if(ranks_type == 4):#鐵支
            type.append(7)

        elif(ranks_type == 6):#葫蘆
            type.append(6)
        
        elif(flush == 1):#同花
            type.append(5)

        elif(straight == 1):#順
            type.append(4)

        elif(ranks_type == 3):#3條
            type.append(2)
        
        elif(flush == 2):
            type.append(10) #缺1
        elif(flush == 3):
            type.append(11) #缺2    

        elif(straight == 2):
            type.append(12) #缺1
        
        elif(ranks_type == 5):#2對
            type.append(3)

        elif(ranks_type == 2):#1對
            type.append(1)

        else :#高牌
            type.append(0)
        if type[0]<3:
            type.append(ranks_type_keys)
        else:
            type.append(0)
        #print("type code: ",type)
        return type

    def card_strength2(self,card):
        length=len(card) #目前場上牌量+手牌
        for i in range(length):
            card[i] = int(card[i])
        ranks = []
        suits = []
        type = []
        #0-51除以4 商數為點數 餘數為花色
        for i in range(length):
            ranks.append(card[i] // 4 )
            suits.append(card[i] % 4 )

        #判斷FLUSH
        #產生重複的花色的key與value
        dictOf_suits =self.Duplicates(suits)
        flush = -1
        flush_suits = -1
        for key, value in dictOf_suits.items():

            #重複超過五次確定為FLUSH
            if(value >= 5) :
                flush_suits = key
                flush = 1
            elif(value==4):
                flush_suits = key
                flush = 2 #缺牌1
            elif(value==3):
                flush_suits = key
                flush = 3 #缺牌2

        #判斷STRAIGHT

        #點數排序
        rank_sorted = sorted(ranks)

        #刪除重複的點數
        rank_list = list(set(rank_sorted))

        #判斷
        straight = -1
        result = 0
        flag=0 #在[1 2 3 4] [5 6] [9]狀況下 1234的缺一能被保留紀錄不被洗掉
        for i in range(0, len(rank_list)):#統計相等的個數 或者是否為順子
            if rank_list[i]-rank_list[i-1] == 1:
                result += 1#如果為順子，則result=4
                if result == 4:
                    flag = 1
                elif result == 3:
                    flag = 2 
            else:
                result = 0 #中斷就歸零   
            if flag == 1 :
                straight=1
            elif flag == 2:
                straight=2


        #A起頭 5結尾 的順子
        if len(rank_list)>=4 : 
            if rank_list[len(rank_list)-1]==12 and rank_list[0]==0 and rank_list[1]==1 and rank_list[2]==2 and rank_list[3]==3:
                straight = 1
        
        #同花順
        if(flush == 1 and straight == 1)and len(card)>=5:
            hands=sorted(card)
            if hands[len(card)-3]>=48 or hands[len(card)-2]>=48 or hands[len(card)-1]>=48 : #A開頭的同花順
                print("hey here ")
                for k in range(4,len(card)):#可能有[A2 A3 A4 A5 A1 B1 C1] 所以檢查第五張開始
                    for l in range(0,3): #只需檢查到第3張是否連得起來[A2 B2 [C2] C3 C4 C5 [C1]] 
                        print("hey : ",k," ",l)
                        if ((hands[k]+4)%52)==hands[l]:
                            #-----------------以下為連續檢查------------------
                            flag=0
                            for j in range(l,len(card)-2):
                                for m in range(j+1,len(card)-1):
                                    if (hands[j]+4)==hands[m]:
                                        flag=flag+1
                                    if flag==3 :
                                        type.append(8)
                                        type.append(0)
                                        print("type code: ",type)
                                        return type
            else : #普通同花順
                for i in range(6):#檢查到第6張就好 如[1 3 [5 6 7 [8 9]]]
                    for j in range(i+1,len(hands)):
                        if (hands[i]+4)==hands[j]:
                            flag=flag+1
                        if flag==4 :
                            type.append(8)
                            type.append(0)
                            print("type code: ",type)
                            return type
        elif(flush == 1 and straight ==2):
            type.append(9)
            type.append(0)
            print("type codes: ",type)
            return type

        #ranks重複的判斷   0=none 2=pair 3=threeKind 4=fourKind 5=twoPairs 6=fullhouse 
        ranks_type = 0
        ranks_type_keys = -1
        dictOf_ranks = self.Duplicates(ranks)
        for key, value in dictOf_ranks.items(): #0高牌 2一對 3三條 4鐵支 5兩對 6葫蘆
            #重複超過四次確定為 FOUR OF A KIND
            if( value == 4 ) :
                ranks_type = 4
                break 

            #重複超過三次確定為 FULL HOUSE or THREE OF A KIND 
            if( value == 3 ) :

                #已經有2 PAIRS 升級為 FULL HOUSE
                if (ranks_type == 5 ):
                    ranks_type = 6
                    break
                
                #已經有1 PAIR 升級為 FULL HOUSE
                elif (ranks_type == 2 or ranks_type == 3):
                    ranks_type = 6
                    break
                
                #THREE OF A KIND
                else :
                    ranks_type = 3
                    ranks_type_keys = key

            #重複超過兩次確定為 FULL HOUSE or 2 PAIRS or PAIR
            if( value == 2 ) :
                #已經有三條 升級為 葫蘆
                if (ranks_type == 3):
                    ranks_type = 6
                    break

                #已經有PAIR 升級為 2 PAIRS
                elif (ranks_type == 2) :
                    if(ranks_type==2 or ranks_type==5 or ranks_type==0):
                        ranks_type_keys=key
                    ranks_type = 5

                #PAIR
                elif(ranks_type==2):
                    if(ranks_type==2 or ranks_type==0): 
                        ranks_type_keys=key
                        ranks_type = 2
                else:
                    ranks_type = 2
                    ranks_type_keys = key
        if(ranks_type_keys == -1):
            if len(rank_sorted)>0:
                ranks_type_keys=rank_sorted[len(rank_sorted)-1]       
        #-------OUTPUT----------------
        #type 0高牌 1一對 2三條 3兩對 4順子 5同花 6葫蘆 7鐵支 8同花順 9同順缺1 10同花缺1 11同花缺2 12順缺1
        if(ranks_type == 4):#鐵支
            type.append(7)

        elif(ranks_type == 6):#葫蘆
            type.append(6)
        
        elif(flush == 1):#同花
            type.append(5)

        elif(straight == 1):#順
            type.append(4)

        elif(ranks_type == 3):#3條
            type.append(2)
        
        elif(flush == 2):
            type.append(10) #缺1
        elif(flush == 3):
            type.append(11) #缺2    

        elif(straight == 2):
            type.append(12) #缺1
        
        elif(ranks_type == 5):#2對
            type.append(3)

        elif(ranks_type == 2):#1對
            type.append(1)

        else :#高牌
            type.append(0)
        if type[0]<3:
            type.append(ranks_type_keys)
        else:
            type.append(0)
        print("type code: ",type)
        return type


    def Duplicates(self,listOfElems):
        #Get frequency count of duplicate elements in the given list
        dictOfElems = dict()
        # Iterate over each element in list
        for elem in listOfElems:
            # If element exists in dict then increment its value else add it in dict
            if elem in dictOfElems:
                dictOfElems[elem] += 1
            else:
                dictOfElems[elem] = 1    
    
        # Filter key-value pairs in dictionary. Keep pairs whose value is greater than 1 i.e. only duplicate elements from list.
        dictOfElems = { key:value for key, value in dictOfElems.items() if value > 1}
        # Returns a dict of duplicate elements and thier frequency count
        return dictOfElems


    def group(self,L):
        first = last = L[0]
        for n in L[1:]:
            if n - 1 == last: # Part of the group, bump the end
                last = n
            else: # Not part of the group, yield current group and start a new
                yield first, last
                first = last = n
        yield first, last # Yield the last group
