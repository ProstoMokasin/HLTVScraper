import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint
import time
from datetime import datetime
import ast
import os

while True:

	session = requests.session()

	req = session.get('https://www.hltv.org/matches')

	doc = BeautifulSoup(req.content, 'lxml')

	todayMatches = []
	tomorrowMatches = []

	upcomingMatchDays = doc.findAll('div', {'class' : 'match-day' })

	liveMatches = doc.findAll('div', {'class' : 'live-match' })
	todayMatches = upcomingMatchDays[0].findAll('table', {'class' : 'table'})
	tomorrowMatches = upcomingMatchDays[1].findAll('table', {'class' : 'table'})

	todayMatchLinks = upcomingMatchDays[0].findAll('a', {'class' : 'upcoming-match'})
	tomorrowMatchLinks = upcomingMatchDays[1].findAll('a', {'class' : 'upcoming-match'})

	liveMatchDicts = []
	todayMatchDicts = []
	tomorrowMatchDicts = []
	completedMatchDicts = []
	cancelledMatchDicts = []

	todayLinks = []
	tomorrowLinks = []

	print(str(datetime.now().hour) + ':' + str(datetime.now().minute))

	completed = open('txt/live.txt','r+')
	completedDoc = open('txt/completed.txt', 'w')
	cancelledDoc = open('txt/cancelled.txt', 'w')

	if os.stat("txt/live.txt").st_size != 0:
		completedInfo = ast.literal_eval(completed.read())
		for i in range(0,len(completedInfo)):
			link = 'https://www.hltv.org' + str(completedInfo[i]['link'])
			req = session.get(link)
			doc = BeautifulSoup(req.content, 'lxml')
			matchInfo = doc.findAll('div', {'class' : 'teamsBox' })
			matchState = doc.find('div', {'class' : 'countdown'})
			matchState = re.search(r'">(.+)</div>', str(matchState), flags=re.DOTALL).group(1)
			i = {
			'link': completedInfo[i]['link'],
			'matchState': matchState
			}
			if str(matchState) == 'Match over':
				completedMatchDicts.append(i)
			elif str(matchState) == 'Cancelled':
				cancelledMatchDicts.append(i)
		completedDoc.write(str(completedMatchDicts))
		cancelledDoc.write(str(cancelledMatchDicts))
		print('\nCompleted matches updated. :)')
	else:
		print('\nCompleted matches have not been updated. :(')

	liveDoc = open('txt/live.txt','w')

	for i in range(0,len(liveMatches)-1):
		match = str(liveMatches[i])
		teams = liveMatches[i].findAll('td', {'class' : 'teams'})
		link = re.search(r'href="(.+)">\n<div class="standard', match, flags=re.DOTALL)
		team1 = re.search(r'<div class="logo-container"><img alt="(.+)" class="logo" src="https://static.hltv.or', str(teams[0]), flags=re.DOTALL)
		team2 = re.search(r'<div class="logo-container"><img alt="(.+)" class="logo" src="https://static.hltv.or', str(teams[1]), flags=re.DOTALL)
		i = {
		'link': link.group(1),
		'teamOne': team1.group(1),
		'teamTwo': team2.group(1),
		}
		liveMatchDicts.append(i)
	liveDoc.write(str(liveMatchDicts))
	#pprint(liveMatchDicts)
	print('\nLive matches updated. :)')

	todayDoc = open('txt/today.txt', 'w')

	for n in range(0,len(todayMatchLinks)):
		todayLinks.append(re.search(r'href="(.+)">\n</a>', str(todayMatchLinks[n]), flags=re.DOTALL))

	for u in range(0,len(todayMatches)):
		match = todayMatches[u]
		teams = match.findAll('div', {'class': 'team'})
		if len(teams):
			team1 = re.search(r'<div class="team">(.+)</div>', str(teams[0]), flags=re.DOTALL)
			team2 = re.search(r'<div class="team">(.+)</div>', str(teams[1]), flags=re.DOTALL)
			matchTime = match.find('div', {'class': 'time'})
			matchTime = re.search(r'">(.+)</div>', str(matchTime), flags=re.DOTALL)
			u = {
			'link': todayLinks[u].group(1),
			'teamOne': team1.group(1),
			'teamTwo': team2.group(1),
			'matchTime': matchTime.group(1)
			}
			todayMatchDicts.append(u)
	todayDoc.write(str(todayMatchDicts))
	#pprint(todayMatchDicts)
	print('\nToday matches updated. :)')

	tomorrowDoc = open('txt/tomorrow.txt', 'w')

	for n in range(0,len(tomorrowMatchLinks)):
		tomorrowLinks.append(re.search(r'href="(.+)">\n</a>', str(tomorrowMatchLinks[n]), flags=re.DOTALL))

	for u in range(0,len(tomorrowMatches)):
		match = tomorrowMatches[u]
		teams = match.findAll('div', {'class': 'team'})
		if len(teams) > 0:
			team1 = re.search(r'<div class="team">(.+)</div>', str(teams[0]), flags=re.DOTALL)
			team2 = re.search(r'<div class="team">(.+)</div>', str(teams[1]), flags=re.DOTALL)
			matchTime = match.find('div', {'class': 'time'})
			matchTime = re.search(r'">(.+)</div>', str(matchTime), flags=re.DOTALL)
			u = {
			'link': tomorrowLinks[u].group(1),
			'teamOne': team1.group(1),
			'teamTwo': team2.group(1),
			'matchTime': matchTime.group(1)
			}
			tomorrowMatchDicts.append(u)
	tomorrowDoc.write(str(tomorrowMatchDicts))
	#pprint(tomorrowMatchDicts)
	print('\nTomorrow matches updated. :)\n\n')
	time.sleep(20)