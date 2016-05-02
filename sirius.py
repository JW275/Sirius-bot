# -*- coding: utf-8 -*-

from react import *
from ircmessage import IRCMessage
from setting import botnick
from queue import Queue
import re, random, sqlite3
import time

#여기 밑에는 아래에서 쓰일 리스트나 자료들이 위치할 곳 입니당~
m = 'MODE'
p = 'PRIVMSG'
blacklist = ['gs12117', 'gs12117_c', '효퓨터', '최석환', 'bono']
notlist = ['진우','우진','카와이','ㅈㅇㅈ','ㅋㅇㅇ','jw','JW','주인','가장','세젤귀','커여워','kw','술','펌프','부자킹','ㅂㅈㅋ','와이','@','Jin']

class Bot():
    irc = None
    msgQueue = Queue()
    channel_list = ['#jwtest', '#snucse16']

    def __init__(self):
        from ircconnector import IRCConnector
        self.irc = IRCConnector(self.msgQueue)
        self.irc.setDaemon(True)
        self.irc.start()

    def run(self):
        self.irc.joinchan('#jwpasschan70')
        self.irc.sendmsg('#jwpasschan70', 'join!')
        key = 0
        password = 234234
        duetime = time.time()
        tempmaster = ''
        masterlist = ['JW275', tempmaster]
        while True:
            packet = self.msgQueue.get()
            if packet['type'] == 'msg':
                msg = packet['content']
                for channel in self.channel_list:
                    self.irc.sendmsg(channel, msg)

            elif packet['type'] == 'irc':
                message = packet['content']
                print(message)
                if message.msgType == 'INVITE' and message.sender == 'JW275':
                    self.irc.joinchan(message.channel)

                elif message.msgType == 'JOIN' and message.sender == '치즈':
                    if message.channel != '#jwchan':
                        self.irc.giveop(message.channel, message.sender)

                elif message.msgType == 'NOTICE':
                    if message.sender == 'JW275' and message.channel == botnick:
                        self.irc.semdmsg('#jwtest', message.msg)
                        continue
                elif message.msgType == 'MODE':
                    if (message.msg == '+o ' + botnick) and (message.sender != 'JJing_e'):
                        say = op()
                        self.irc.sendmsg(message.channel, say)
                    elif message.msg == '-o ' + botnick:
                        say = deop()
                        self.irc.sendmsg(message.channel, say)

                elif (message.msgType == 'PRIVMSG') and (message.sender not in blacklist):
                    if message.sender in [r'\b','C','bryan_a','cubeIover','VBChunguk_bot','gn','kcm1700-bot','Diet-bot','Flareon','Delphox']:
                        continue
                    
                    if (message.msg.find('시리우스 옵줘') != -1) and (message.sender not in blacklist):
                        if message.channel == '#jwchan':
                            if message.sender == 'JW275':
                                self.irc.giveop(message.channel, message.sender)
                                say = giop()
                                self.irc.sendmsg(message.channel, say)
                        else:
                            self.irc.giveop(message.channel, message.sender)
                            say = giop()
                            self.irc.sendmsg(message.channel, say)


                    
                    elif message.msg.find('시리우스 나 주인할래') != -1:
                        key = 1
                        password = random.randint(100000, 999999)
                        self.irc.sendmsg('#jwpasschan70', '%d' % password)
                    elif key == 1:
                        if message.msg.find('%d' % password) != -1:
                            tempmaster = message.sender
                            masterlist = ['JW275', tempmaster]
                            duetime = time.time() + 3600
                            ifmaster = 0
                            self.irc.sendmsg('#jwpasschan70', 'start! %s' % tempmaster)
                    elif time.time() > duetime:
                        tempmaster = ''
                        masterlist = ['JW275', tempmaster]
                        #self.irc.sendmsg('#jwpasschan70', 'end!')
    
                    if message.msg.find('냐아앙♡') != -1:
                        self.irc.sendmsg(message.channel, '으르릉..')
                    elif message.msg.find('참치 먹자') != -1:
                        self.irc.sendmsg(message.channel, '퉤퉷')
                    elif message.msg.find('브라이언') != -1:
                        check = random.randint(1,5)
                        if check == 1:
                            self.irc.sendmsg(message.channel, '거짓말쟁이..크르릉..')
                    elif (message.msg.find('좋은아침입니다여러분') != -1) and (message.sender in masterlist):
                        self.irc.sendmsg(message.channel, '헥헥! 주인님 잘자써오?')
                    elif (message.msg.find('좋은아침입니다여러분') != -1) and (message.sender == '이진우ㅤ'):
                        self.irc.sendmsg(message.channel, '헥헥! 주인님 잘자써오?')

                    elif message.msg.find('고기 먹고싶다') != -1:
                        self.irc.sendmsg(message.channel, '꼬기! 꼬기주라멍!')
                    elif message.msg.find('고양이 키우고싶다') != -1:
                        self.irc.sendmsg(message.channel, '크오아아아앙!!!!')

                    elif (message.msg.find('그치 시리우스야?') != -1) and (message.sender in masterlist):
                        self.irc.sendmsg(message.channel, '멍!ฅ^•ﻌ•^ฅ')



                    parse = re.match('^시리우스\s(\S+)\s물어!$', message.msg)
                    if parse and (message.sender not in blacklist):
                        who = parse.group(1)
                        check = 0
                        for i in notlist:
                            if who.find('%s' % i) != -1:
                                check = 1
                        if check == 1:
                            self.irc.sendmsg(message.channel, 'ㅡㅅㅡ 저리가라 멍!')
                            check = 0
                        elif (who in blacklist) and (who != '치즈'):
                            say = angry()
                            self.irc.sendmsg(message.channel, say)
                        elif (who.find('1') != -1):
                            self.irc.sendmsg(message.channel, 'ㅡㅅㅡ 저리가라 멍!')
                        elif (who.find('시리우스') != -1) or (who.find('자신') != -1) or (who.find('sirius') != -1) or (who.find('너') != -1):
                            self.irc.sendmsg(message.channel, '바보새오? 꺄하하')
                        elif who.find('부스터') != -1:
                            continue
                        elif (who.find('치즈') != -1) or (who.find('고양이') != -1):
                            self.irc.sendmsg(message.channel, '냥냥이는 저리가라 멍!')
                        elif (who.find('예지') != -1):
                            self.irc.sendmsg(message.channel, '퓨터님의 여자분?')
                        elif (who.find('브랸') != -1) or (who.find('bryan') != -1) or (who.find('승현') != -1) or (who.find('조조교') != -1) or (who.find('마조') != -1):
                            self.irc.sendmsg(message.channel, '무서워오..끼이잉..')
                        else:
                            say = attack()
                            self.irc.sendmsg(message.channel, say)

                    parse = re.match('^시리우스! (\S+)$', message.msg)
                    if parse:
                        act = parse.group(1)
                        if act == '공물어와!':
                            self.irc.sendmsg(message.channel, '던저쥬새오!멍!')
                            f = open("active.txt",'w')
                            f.write('on')
                            f.close()
                        elif act == '이리와!':
                            say = happy()
                            self.irc.sendmsg(message.channel, say)
                        elif act == '짖어!':
                            say = random.choice(['멍멍','왈왈'])
                            self.irc.sendmsg(message.channel, say)    


                    parse = re.match('^시리우스! 치즈 괴롭혀!$', message.msg)
                    if parse:
                        if message.sender in masterlist:
                            self.irc.sendmsg(message.channel, '바보 냥이!멍!')
                            self.irc.deop(message.channel, '치즈')

                    parse = re.match('^시리우스! 치즈한테 사과해!$', message.msg)
                    if parse:
                        if message.sender in masterlist:
                            self.irc.sendmsg(message.channel, 'ＵＴｪＴＵ미아내오..쓰담쓰담..')
                            self.irc.giveop(message.channel, '치즈')


                    if message.msg.find('끙차!') != -1:
                        f = open("active.txt", 'r')
                        check = f.readline()
                        f.close()
                        if check == 'on':
                            f = open("active.txt", 'w')
                            f.write('off')
                            f.close()
                            self.irc.partchan(message.channel)
                            how = random.randint(10,30)
                            time.sleep(how)
                            self.irc.joinchan(message.channel)
                            self.irc.sendmsg(message.channel, '헥헥!ฅ^•ﻌ•^ฅ 공 여기이써오')
                        elif check == 'off':
                            continue

"""                 
        global key
        global duetime
        global password
        global tempmaster
        global masterlist
        global notlist
        global blacklist



        elif message.msg.find('시리우스 나 주인할래') != -1:
                        key = 1
                        password = random.randint(100000, 999999)
                        self.irc.sendmsg('#jwpasschan70', '%d' % password)
                    elif key == 1:
                        if message.msg.find('%d' % password) != -1:
                            tempmaster = message.sender
                            duetime = time.time() + 3600
                            ifmaster = 0
                    elif time.time() > duetime:
                        tempmaster = ''
    
                    elif (message.sender == '치즈') and (message.msg == ''):
                        self.irc.sendmsg(message.channel, '컹컹!')
                        con = sqlite3.connect("count.db")
                        c = con.cursor()
                        c.execute()

                    parse = re.match('!piu(\w+)(\W+)\s(\w*)', message.msg)
                    if parse and message.sender == '치즈':
                        nick = parse.group(1)
                        case = parse.group(2)
                        thing = parse.group(3)
                        if case == '+':
                            con = sqlite3.connect("memblist.db")
                            c = con.cursor()
                            c.execute("insert into %s values('%s')" % (nick, thing))
                            con.commit()
                            con.close()
                            self.irc.sendmsg(message.channel, '추가됐슴당')
                        elif case == '-':
                            continue
                            #향후 추가예정 && 멤버리스트에 있는지 확인하고 없으면 메세지내보내기 만들기
                        elif case == '?':
                            con = sqlite3.connect("count.db")
                            c = con.cursor()
                            c.execute("select * from %s" % nick)
                            things = []
                            for i in c:
                                things.append(i[0])
                            temp = random.choice(things)
                            self.irc.sendmsg(message.channel, '%s' % temp)
                            con.close()
"""



#running
if __name__ == '__main__':
    bot = Bot()
    bot.run()
