import numpy as np
import re
import sys

#초성
initial= ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ','ㄸ', 'ㄹ', 'ㅁ','ㅂ','ㅃ', 'ㅅ', 'ㅆ', 'ㅇ','ㅈ', 'ㅉ', 'ㅊ', 'ㅋ','ㅌ', 'ㅍ', 'ㅎ']

#중성
middle=['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ','ㅓ', 'ㅔ', 'ㅕ', 'ㅖ','ㅗ', 'ㅘ', 'ㅙ', 'ㅚ','ㅛ','ㅜ', 'ㅝ', 'ㅞ','ㅟ', 'ㅠ', 'ㅡ', 'ㅢ','ㅣ']

#종성
final= [' ', 'ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ', 'ㄻ', 'ㄼ','ㄽ', 'ㄾ', 'ㄿ', 'ㅀ','ㅁ', 'ㅂ', 'ㅄ', 'ㅅ','ㅆ', 'ㅇ', 'ㅈ', 'ㅊ','ㅋ','ㅌ', 'ㅍ', 'ㅎ']

#특수문자.,?!
special= ['.', ',', '?', '!']

#약자 한음절 abbreviation
abb=['가', '나', '다', '마', '바','사', '자', '카', '타', '파','하','것', '억', '언', '얼','연', '열', '영', '옥',
     '온','옹', '운', '울', '은', '을', '인']

# 긴 약자
longabb=["그래서", "그러나", "그러면", "그러므로", "그런데", "그리고", "그리하여"]

initialarr= [ [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #ㅇ은그냥다0
              [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]]  #19,12

middlearr= [[1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0], [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0],
            [1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0], [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]] #21,12

finalarr = [[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], # ' '은000000111111
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1], [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0], #약자에서 ㅆ받침은 그냥 종성으로 넣었음
            [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]] #28,12

speicalarr= [[0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]] #4,12

abbarr = [[1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
          [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
          [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]] #26,12

longabbarr= [[1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0], [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0], [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0], [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1]] #7,12

#한글 초중종성 나누기
#이미 바뀐 긴약자를 제외한 나머지를 분리하자!
def disassemble(distext):
    r_lst = []
    int_lst = []
    tmp = False
    for w in distext:   #distext라는 배열안의 요소를 w
        for i, word in enumerate(w): #w의 인덱스는 i 요소는 word
            if type(word) is str:
                for j, oneword in enumerate(word):
                    if '가' <= oneword <= '힣':
                        ## 588개 마다 초성이 바뀜.
                        ch1 = (ord(oneword) - ord('가')) // 588
                        ## 중성은 총 28가지 종류
                        ch2 = ((ord(oneword) - ord('가')) - (588 * ch1)) // 28
                        ch3 = (ord(oneword) - ord('가')) - (588 * ch1) - 28 * ch2
                        r_lst.append([initial[ch1], middle[ch2], final[ch3]])
                    elif word == '.' or word == ',' or word == '?' or word == '!': #특수문자도 하나의 배열로 넣자!
                        r_lst.append([word])
            else:
                int_lst.append(word)
                tmp = True
        if tmp == True:
            r_lst.append(int_lst)
            tmp = False
    return r_lst

#짧은 약자를 찾기 위해 다 나누었던 앞 두글자만 합쳐서 보자!
def firstcheckshortabb(text):
    r_lst=[]
    for w in text:
        try:
            if w == [[1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0]] or w == [[1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]] or w==[[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]] or w==[[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]] or w==[[1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0]] or w==[[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1]] or w==[[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1]]:
                 r_lst.append(w)
            elif w == ['.'] or w == [','] or w == ['?'] or w == ['!']:
                r_lst.append(w)
            else:
                ab = w[0]+w[1]
                r_lst.append([ab, w[2]])
        except IndexError:
            pass
    #print(r_lst)
    return(r_lst)

def secondcheckshortabb(text):
    r_lst = []
    global abbarr
    global speicalarr
    for i, w in enumerate(text):
        try:
            if w[0] == '.':
                r_lst.append([speicalarr[0]])
            elif w[0] == ',':
                r_lst.append([speicalarr[1]])
            elif w[0] == '?':
                r_lst.append([speicalarr[2]])
            elif w[0] == '!':
                r_lst.append([speicalarr[3]])
            elif type(w[0]) is not int:
                if w[0] == 'ㄱㅏ':
                    r_lst.append([abbarr[0], w[1]])
                elif w[0] == 'ㄴㅏ':
                    r_lst.append([abbarr[1], w[1]])
                elif w[0] == 'ㄷㅏ':
                    r_lst.append([abbarr[2], w[1]])
                elif w[0] == 'ㅁㅏ':
                    r_lst.append([abbarr[3], w[1]])
                elif w[0] == 'ㅂㅏ':
                    r_lst.append([abbarr[4], w[1]])
                elif w[0] == 'ㅅㅏ':
                    r_lst.append([abbarr[5], w[1]])
                elif w[0] == 'ㅈㅏ':
                    r_lst.append([abbarr[6], w[1]])
                elif w[0] == 'ㅋㅏ':
                    r_lst.append([abbarr[7], w[1]])
                elif w[0] == 'ㅌㅏ':
                    r_lst.append([abbarr[8], w[1]])
                elif w[0] == 'ㅍㅏ':
                    r_lst.append([abbarr[9], w[1]])
                elif w[0] == 'ㅎㅏ':
                    r_lst.append([abbarr[10], w[1]])
                elif w[0] + w[1] == 'ㄱㅓㅅ':
                    r_lst.append([abbarr[11], w[1]])
                elif w[0] + w[1] == 'ㅇㅓㄱ':
                    r_lst.append([abbarr[12], w[1]])
                elif w[0] + w[1] == 'ㅇㅓㄴ':
                    r_lst.append([abbarr[13], w[1]])
                elif w[0] + w[1] == 'ㅇㅓㄹ':
                    r_lst.append([abbarr[14], w[1]])
                elif w[0] + w[1] == 'ㅇㅕㄴ':
                    r_lst.append([abbarr[15], w[1]])
                elif w[0] + w[1] == 'ㅇㅕㄹ':
                    r_lst.append([abbarr[16], w[1]])
                elif w[0] + w[1] == 'ㅇㅕㅇ':
                    r_lst.append([abbarr[17], w[1]])
                elif w[0] + w[1] == 'ㅇㅗㄱ':
                    r_lst.append([abbarr[18], w[1]])
                elif w[0] + w[1] == 'ㅇㅗㄴ':
                    r_lst.append([abbarr[19], w[1]])
                elif w[0] + w[1] == 'ㅇㅗㅇ':
                    r_lst.append([abbarr[20], w[1]])
                elif w[0] + w[1] == 'ㅇㅜㄴ':
                    r_lst.append([abbarr[21], w[1]])
                elif w[0] + w[1] == 'ㅇㅜㄹ':
                    r_lst.append([abbarr[22], w[1]])
                elif w[0] + w[1] == 'ㅇㅡㄴ':
                    r_lst.append([abbarr[23], w[1]])
                elif w[0] + w[1] == 'ㅇㅡㄹ':
                    r_lst.append([abbarr[24], w[1]])
                elif w[0] + w[1] == 'ㅇㅣㄴ':
                    r_lst.append([abbarr[25], w[1]])
                else:
                    r_lst.append(w)
            else:
                r_lst.append(w)
        except IndexError:
            pass
    #print(r_lst)
    return r_lst

#합친 두글자만 다시 나누자!
def redis(redis):
    r_lst = []
    for i, w in enumerate(redis):
        for j, v in enumerate(w):
            if type(v) is not list:
                if len(v)==2:
                    r_lst.append([v[0],v[1],w[1]])
            else:
                r_lst.append(w)
    print(r_lst)
    return r_lst

def convert(third):
    r_lst=[]
    tmp = False
    global initial
    global middle
    global final
    global initialarr
    global middlearr
    global finalarr
    for i, w in enumerate(third):
        for j, v in enumerate(w):
            if type(v) is not list:

                if j == 0:
                    for k1 in range(0,19):
                        if v[j] == initial[k1]:
                            r_lst.append(initialarr[k1])
                elif j == 1:
                    for k2 in range(0,21):
                        if v[j-1] == middle[k2]:
                            r_lst.append(middlearr[k2])
                        else:
                            tmp=True

                    if tmp==True:
                        for k3 in range(0, 28):
                            if v[j - 1] == final[k3]:
                                r_lst.append(finalarr[k3])


                elif j==2:
                    for k3 in range(0,28):
                        if v[j-2] == final[k3]:
                            r_lst.append(finalarr[k3])
            else:
                if j == 0:
                    r_lst.append(v)
                elif j==1:
                    for k3 in range(0, 28):
                        if v[j-1] == final[k3]:
                            r_lst.append(finalarr[k3])
    #print(r_lst)
    return(r_lst)



file_path = "input.txt" #파일 경로

#파일을 단어로 잘라서 배열로 넣기
with open(file_path) as f:
    word=f.read().split()
#print(word)
#'그래서' or '그러나' or '그러면'or'그러므로'or '그런데' or '그리고' or '그리하여'
#잘라진 단어와 longabb 비교해서 대치시키기
for i, wordi in enumerate(word):
    for n in range(0,7):
        compare=(wordi == longabb[n%7])
        if compare==True:
            word[i]=[longabbarr[n%7]]
#print(word)
dis=disassemble(word)
first=firstcheckshortabb(dis)
second=secondcheckshortabb(first)
third=redis(second)
lastchange=convert(third)
print(lastchange)





