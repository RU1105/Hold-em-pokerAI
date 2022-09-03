import threading
import webbrowser
from wsgiref.simple_server import make_server
import random
import sys
import os
path1 = str(os.path.abspath('..')) + ('\latina') #當前上一層目錄的絕對路徑，os.path.abspath('..')
sys.path.insert(1, path1)
import latina

FILE = str(os.path.abspath('..')) + (r'\HighTwo\welcome.html')
PORT = 8080
latina = latina.latina()

def request(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = environ['wsgi.input'].read(request_body_size)
            input = tokensplit(request_body)
            type = input.pop(0)
            type = type.replace('type=','')
            print(type)
            if (type=="predict") :
                print("---input---")
                input = [ int(x) for x in input ]
                print("html input :",input)
                if input[7] == 0:
                    hand1 = int(float(input[5]))
                    hand2 = int(float(input[6]))
                    level = latina.set_hands_level(hand1,hand2)
                    input[7] = level
                    print(level)
                    if level == 5:
                        if (random.randrange(1,100,1)>=40):
                            output = (action_predict(input))
                        else:
                            output = [8,-1]
                    elif level == 4 :
                        if (random.randrange(1,100,1)>=35):
                            output = (action_predict(input))
                        else:
                            output = [8,-1]
                    elif level == 3 :
                        if (random.randrange(1,100,1)>=25):
                            output = (action_predict(input))
                        else:
                            output = [8,-1]
                    elif level == 2 :
                        if (random.randrange(1,100,1)>=10):
                            output = (action_predict(input))
                        else:
                            output = [8,-1]
                    else :
                        output = (action_predict(input))
                    output.append(level)
                else:
                    output = (action_predict(input))
                #print(input)
                print("---output---")
                print(output)
            elif (type=="hands"):
                print("hands_strength")
                player = input[:2] + input[4:]
                player_strength = hand_strength(player)
                computer = input[2:]
                computer_strength = hand_strength(computer)
                print("player_strength :",player_strength)
                print("computer_strength :",computer_strength)
                for i in range(len(player_strength)):
                    if player_strength[i] > computer_strength[i]:
                        output = 0
                        break
                    elif player_strength[i] < computer_strength[i]:
                        output = 1
                        break
                    elif player_strength[i] == computer_strength[i]:
                        output = 2
                        continue
                print(output)
            else :
                print("unknown type")
                output = type
        except (TypeError, ValueError):
            request_body = "0"
        try:
            response_body = str(output)
        except:
            response_body = "error"
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [response_body.encode()]
    else:
        response_body = open(FILE).read()
        status = '200 OK'
        headers = [('Content-type', 'text/html'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body.encode()]

def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open(FILE)
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

def start_server():
    """Start the server."""
    print("start the server....")
    httpd = make_server("127.0.0.1", PORT, request)
    httpd.serve_forever()

def tokensplit(input):
    input = str(input)
    input = input.replace(r"b'","")
    input = input.replace(r"'","")
    input = input.replace(r"input%5B%5D=","")
    token = input.split('&')
    return token

def action_predict(input):
    new_input = []
    for i in range(0,len(input)) :
        if i <= 9:
            if i == 8 or i == 9:
                new_input.append((input[i]/input[12]))
            else:
                new_input.append(input[i])
        elif (i%3) == 1 and input[i] == -1:
            break
        elif (i%3) == 0 and input[i] != -1:
            new_input.append((input[i]/input[12]))
        else :
            new_input.append(input[i])
    
    action_list = latina.check_strength(new_input[0:7])+new_input[:]+[-1]*(14-len(new_input))#牌型判斷參數加入
    print("action :",action_list)
    new_move = latina.predict(action_list)
    #latina.splinter_predict(action_list)#各樹predict 
    new_input.append(new_move)
    new_input.append(0)
    print("new input :",new_input)
    output = [new_move , latina.bargain(input[0:7],input[8:10])]
    #output = [ 2 , latina.bargain(input[0:7],input[8:10])] #此為測試用
    return output

def getDuplicatesWithCount(listOfElems):
        ''' Get frequency count of duplicate elements in the given list '''
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

def group(L):
    first = last = L[0]
    for n in L[1:]:
        if n - 1 == last: # Part of the group, bump the end
            last = n
        else: # Not part of the group, yield current group and start a new
            yield first, last
            first = last = n
    yield first, last # Yield the last group

def hand_strength(hands): #阿修阿修 這邊有bug 同花跟同花順跟順子判斷有問題
    for i in range(len(hands)):
        hands[i] = int(hands[i])
    hands_ranks = []
    hands_suits = []
    hands_type = []
    #0-51除以4 商數為點數 餘數為花色 餘數0為2,12為A,11為K
    for i in range(len(hands)):
        hands_ranks.append(hands[i] // 4 )
        hands_suits.append(hands[i] % 4 )

    #判斷FLUSH
    #產生重複的花色的key與value
    dictOf_suits = getDuplicatesWithCount(hands_suits)
    flush = -1
    flush_suits = -1
    for key, value in dictOf_suits.items():

        #重複超過五次確定為FLUSH
        if(value >= 5) :
            flush_suits = key
            flush = 1

    #判斷STRAIGHT

    #點數排序
    rank_sorted = sorted(hands_ranks)

    #刪除重複的點數
    rank_list = list(set(rank_sorted))
    print(rank_list)

    #判斷
    straight = -1
    result = 0
    straight_key=-1
    flag=0 #在[1 2 3 4] [5 6] [9]狀況下 被保留紀錄不被洗掉
    for i in range(0, len(rank_list)):#統計相等的個數 或者是否為順子
        if rank_list[i]-rank_list[i-1] == 1:
            result += 1#如果為順子，則result=4
            if result == 4:
                flag = 1
                straight_key=rank_list[i]
                
        else:
            result = 0 #中斷就歸零   

        if flag == 1 :
            straight=1

    #A起頭 5結尾 的順子
    if rank_list[len(rank_list)-1]==12 and rank_list[0]== 0 and rank_list[1]==1 and rank_list[2]==2 and rank_list[3]==3:
        straight = 1
        straight_key=12

    #同花順

    if (flush == 1 and straight != -1) :#避免同花和順子並非為同組牌 如[A2 A3 B4 A5 A6 C7 A1]
        hands=sorted(hands)
        if hands[4]>=48 or hands[5]>=48 or hands[6]>=48 : #A開頭的同花順
            print("hey here ")
            for k in range(4,7):#可能有[A2 A3 A4 A5 A1 B1 C1] 所以檢查第五張開始
                for l in range(0,3): #只需檢查到第3張是否連得起來[A2 B2 [C2] C3 C4 C5 [C1]] 
                    print("hey : ",k," ",l)
                    if ((hands[k]+4)%52)==hands[l]:
                        #-----------------以下為連續檢查------------------
                        flag=0
                        for j in range(l,5):
                            for m in range(j+1,6):
                                if (hands[j]+4)==hands[m]:
                                    flag=flag+1
                                if flag==3 :
                                    print("FLUSH STRAIGHT : ", end = '')
                                    print(straight_key)
                                    hands_type.append(10)
                                    hands_type.append(straight_key)
                                    return hands_type
            
            
        else : #普通同花順
            for i in range(6):#檢查到第6張就好 如[1 3 [5 6 7 [8 9]]]
                for j in range(i+1,len(hands)):
                    if (hands[i]+4)==hands[j]:
                        flag=flag+1
                    if flag==4 :
                        print("FLUSH STRAIGHT : ", end = '')
                        print(straight_key)
                        hands_type.append(10)
                        hands_type.append(straight_key)
                        return hands_type

    #ranks重複的判斷   0=none 2=pair 3=threeKind 4=fourKind 5=twoPairs 6=fullhouse 
    ranks_type = 0
    ranks_type_keys = []
    dictOf_ranks = getDuplicatesWithCount(hands_ranks)
    for key, value in dictOf_ranks.items():

        #重複超過四次確定為 FOUR OF A KIND
        if( value == 4 ) :
            ranks_type = 4
            ranks_type_keys.clear()
            ranks_type_ranks = key
            break 

        #重複超過四次確定為 FULL HOUSE or THREE OF A KIND 
        if( value == 3 ) :

            #已經有2 PAIRS 升級為 FULL HOUSE
            if (ranks_type == 5 ):
                ranks_type_keys.remove(min(ranks_type_keys))
                ranks_type_keys.insert(0,key)
                ranks_type = 6
                break
            
            #已經有1 PAIR 升級為 FULL HOUSE
            elif (ranks_type == 2 or ranks_type == 3):
                ranks_type_keys.append(key)
                ranks_type = 6
                break
            
            #THREE OF A KIND
            else :
                ranks_type_keys.append(key)
                ranks_type = 3

        #重複超過兩次確定為 FULL HOUSE or 2 PAIRS or PAIR
        if( value == 2 ) :

            #已經有2 PAIRS 升級為 FULL HOUSE
            if(ranks_type == 5):
                ranks_type_keys.append(key)
                ranks_type_keys.remove(min(ranks_type_keys))

            #已經有THREE oF A KIND 升級為 FULL HOUSE
            elif (ranks_type == 3):
                ranks_type_keys.append(key)
                ranks_type = 6
                break

            #已經有PAIR 升級為 2 PAIRS
            elif (ranks_type == 2) :
                ranks_type_keys.append(key)
                ranks_type = 5

            #PAIR
            else :
                ranks_type_keys.append(key)
                ranks_type = 2
                
    #OUTPUT
    
    
    if(ranks_type == 4):
        print("FOUR OF A KIND : ", end = '')
        print(ranks_type_ranks)
        hands_type = [6,ranks_type_ranks]

    elif(ranks_type == 6):
        print(ranks_type_keys)
        print("FULL HOUSE : ", end = '')
        print(ranks_type_keys[0] , end = ',')
        print(ranks_type_keys[1])
        hands_type = [6,ranks_type_keys[0],ranks_type_keys[1]]
    
    elif(flush == 1):
        print("FLUSH : ", end = '')
        print(flush_suits)
        hands_type = [5,flush_suits]

    elif(straight != -1):
        print("STRAIGHT : ", end = '')
        print(straight_key)
        hands_type = [4,straight_key]

    elif(ranks_type == 3):
        print("THREE OF A KIND : ", end = '')
        print(ranks_type_keys[0])
        hands_type = [2,ranks_type_keys[0]]

    elif(ranks_type == 5):
        print("TWO PAIRS : ", end = '')
        print(max(ranks_type_keys) , end = ',')
        print(min(ranks_type_keys))
        hands_type = [3,max(ranks_type_keys),min(ranks_type_keys)]

    elif(ranks_type == 2):
        print("PAIR : ", end = '')
        print(ranks_type_keys[0])
        hands_type = [1,ranks_type_keys[0],max(hands)]

    else :
        print("HIGH CARD : ", end = '')
        print(max(hands))
        hands_type = [0,max(hands)]
    return hands_type
    
def model_train():
    latina.set()

if __name__ == "__main__":
    model_train()
    print("trainig end, thank you.")
    open_browser()
    start_server()
'''
    #點數排序
    hands_rank_sorted = sorted(hands_ranks)


    #刪除重複的點數
    hands_rank_dict = list(dict.fromkeys(hands_rank_sorted))

    #把連續的點數分組
    hands_rank_group=list(group(hands_rank_dict))
    straight = -1
    for i in range(len(hands_rank_group)):
        if (hands_rank_group[i][1] - hands_rank_group[i][0] >= 4):
            straight = hands_rank_group[i][1]

    #A起頭 5結尾 的順子
    if(hands_rank_group[0][0] == 0 and hands_rank_group[0][1] == 3 and max(hands_rank_dict)):
        straight = 3
'''