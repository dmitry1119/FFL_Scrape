import time
from time import strftime, gmtime, localtime, strptime, sleep
import datetime
from bs4 import BeautifulSoup
import requests
import dicttoxml
from xml.etree.ElementTree import *
import shelve
import os.path


for i in range(1,31,2):
    url = ''
    def scrape(url, i):
    
        gameList = []
        gametime = []
        awayTeams = []
        homeTeams = []
        teams=[]
        scores=[]
        clean={}
        gameTime = []
        scheduleTime = []
        dayNum = i      
        today = datetime.datetime.today()
        d = datetime.timedelta(days=i)
        nextDay = today+d
        tomDateGame = datetime.datetime.strftime(nextDay,'%m/%d/%Y')
        tomDateGame = tomDateGame[1:]
        tomDateFile = datetime.datetime.strftime(nextDay,'%Y-%m-%d')
        print 'tomDateFile = ' + str(tomDateFile)
        url='http://sports.yahoo.com/mlb/scoreboard/?date=%(day)s' % {'day':tomDateFile}
        currentTime=strftime('%H%M',localtime())
        fileDate=strftime('%Y%m%d',localtime())
        dayOfWeek=strftime('%A',localtime())   
        r=requests.get(url)
        soup=BeautifulSoup(r.content)
        homesoup = soup.find_all('tr', {'class': 'team home '})
        awaysoup = soup.find_all('tr', {'class': 'team away '})
        timeSoup = soup.find_all('span',{'class': 'time'})
        for players in homesoup:
            team = players.em.text
            team = team.replace('Chi', 'Chicago')
            homeTeams.append(team)
        
        for players in awaysoup:
            team = players.em.text
            team = team.replace('Chi', 'Chicago')
            awayTeams.append(team)
            
        for num in timeSoup:
            if 'span' in str(num):
                time = num.text
                time = time.replace(' EDT', '')
                scheduleTime.append(time)
            else:
                print 'Go back to your hole Yankees!'
        return scheduleTime,gameTime,awayTeams,homeTeams,gameList,tomDateGame,dayNum

    def dataScrub(scheduleTime,gameTime,awayTeams,homeTeams,gameList):

        for stat in scheduleTime:

            timeStamp = time.strptime(stat, '%I:%M %p')
            timeStamp = time.strftime('%H%M',timeStamp)
            hour = int(timeStamp[:2]) - 2
            mTime = str(hour) + timeStamp[-2:]
            mTime = time.strptime(mTime, '%H%M')
            timeStamp = time.strftime('%I:%M %p', mTime)
            if timeStamp[0] == '0':
                timeStamp = timeStamp[1:]   
            gameTime.append(timeStamp)
        
        for i in range(len(scheduleTime)):
                    num = 'game' + str(i + 1)
                    gameList.append(num)

    def makeSchedule(gameTime,homeTeams,awayTeams,tomDateGame,dayNum):
        day = Element('day')
        day.attrib['dayNumber'] = 'day' + str(dayNum)
        for i in range(len(scheduleTime)):
            game = Element('game')
            game.attrib['gameNumber']=gameList[i]
            hometeam = SubElement(game, 'homeTeam')
            hometeam.text = homeTeams[i]
            awayteam = SubElement(game, 'awayTeam')
            awayteam.text = awayTeams[i]
            gametime = SubElement(game, 'startTime')
            gametime.text = gameTime[i]            
            startdate = SubElement(game, 'startDate')
            startdate.text = tomDateGame
            day.insert(i,game)
        scheduleXML = tostring(day)
        completeName = os.path.join('./site/wwwroot/TestFiles/', 'scheduleFileMLB'+str(dayNum)+'.XML')
        with open(completeName,'w') as scoreData:
            scoreData.write(str(scheduleXML))
##        dayShelve = shelve.open('days.dat', writeback=True)
##        dayShelve[str(dayNum)] = day
##        dayShelve.close()
##        sleep(5)
##        return dayShelve, dayNum
    
              
    scheduleTime,gameTime,awayTeams,homeTeams,gameList,tomDateGame,dayNum = scrape(url,i)
    dataScrub(scheduleTime,gameTime,awayTeams,homeTeams,gameList)
    makeSchedule(gameTime,homeTeams,awayTeams,tomDateGame,dayNum)
##def writeFile(dayShelve,dayNum):
##    schedule = Element('schedule')
##    dayShelve = shelve.open('days.dat', writeback=True)
##    for i in range(1,(2 *len(dayShelve))+1,2):
##        schedule.insert(i, dayShelve[str(i)])
##    
####    scheduleXML = tostring(schedule)
####    with open('scheduleFileMLB.xml','w') as scoreData:
####            scoreData.write(str(scheduleXML))
##    for i in dayShelve:
##        del dayShelve[i]
##    dayShelve.close()
##    print 'I have finished scraping your schedule!'
##writeFile(dayShelve,dayNum)
##

##def gamesCheck(gameList,scores,homeTeams,awayTeams,teams,gametime,gameday):
##    if len(gameList) != 0:
##        makeSchedule(gameList,scores,homeTeams,awayTeams,teams,gametime,gameday)       
##    else:
##        print 'No games tomorrow'
##        sleep(18000)
##        gamesCheck(gameList,scores,homeTeams,awayTeams,teams,gametime,gameday)
##gamesCheck(gameList,scores,homeTeams,awayTeams,teams,gametime,gameday)

