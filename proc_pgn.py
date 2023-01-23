import sys
f = open(sys.argv[1], "r")
sumsChess,sumsChpok = {},{}
curW = curB = curRes = curLog = ""
numGames = numMoves = numProms = numChecks = numPro0 = numChk0 = 0
numDrawsChess = numWinsChessW = numWinsChessB = 0
numDrawsChpok = numWinsChpokW = numWinsChpokB = 0

def findName(n):
	names = n.split(',')
	if len(names)==1:  names = n.split(' ')
	lastName = names[0].strip()
	firstName = names[1].strip()
	n = lastName + ', ' + firstName
	if n in sumsChess:  return n
	for k in sumsChess.keys():
		if k.startswith(n):  # k is longer than n
			return k
		if n.startswith(k):  # n is longer than k
			sumsChess[n] = sumsChess[k]
			sumsChpok[n] = sumsChpok[k]
			sumsChess.pop(k)  # remove the shorter one
			sumsChpok.pop(k)
			return n
	sumsChess[n],sumsChpok[n] = 0,0
	return n
	
for li in f:
	if li[0]=='[':
		if   li[1:7]=='White ':  curW = li[8:-3]
		elif li[1:7]=='Black ':  curB = li[8:-3]
		elif li[1:7]=='Result':  curRes,curLog = li[9:-3],""
	elif len(li)!=1:  curLog += li.strip() + ' '
	elif len(curLog):
		#print(curW, curB, curRes, curLog)
		for x in curLog:
			if x=="=":     numPro0 += 1
			if x in "+#":  numChk0 += 1
		curW = findName(curW)
		curB = findName(curB)

		if curRes=='1/2-1/2':  upd1,upd2,numDrawsChess = curW,curB,numDrawsChess+1
		elif curRes=='1-0':    upd1,upd2,numWinsChessW = curW,curW,numWinsChessW+1
		elif curRes=='0-1':    upd1,upd2,numWinsChessB = curB,curB,numWinsChessB+1
		else:
			print("Error! result is:", curRes)
			break
		sumsChess[upd1] += 1
		sumsChess[upd2] += 1

		moves = curLog.strip().split(' ')
		if moves[-1] != curRes:
			print("Error!! result is unclear,", curRes, "or", moves[-1])
			break
		if len(moves)==1:  continue
		numGames += 1
		scoreW = scoreB = 0
		for i in range(len(moves)-1):
			m = moves[i]
			if i%3==0:
				if m[-1]!='.':  print("Error! Invalid move", i/3+1, "in this line:", curLog)
				continue
			s = m.strip('+#')
			if len(s) < len(m):  numChecks += 1
			m = s.split('=')[0]
			if len(m) < len(s):  numProms += 1

			if i%3==1 and i==len(moves)-2:  continue
			numMoves+=1
			if m[0]=='O':  continue
			row = int(m[-1])
			assert(1 <= row <= 8)
			if i%3==1:  scoreW += max(0, row-4)
			else:       scoreB += max(0, 5-row)

		if   scoreW>scoreB:  upd1,upd2,numWinsChpokW = curW,curW,numWinsChpokW+1
		elif scoreW<scoreB:  upd1,upd2,numWinsChpokB = curB,curB,numWinsChpokB+1
		else:                upd1,upd2,numDrawsChpok = curW,curB,numDrawsChpok+1
		sumsChpok[upd1] += 1
		sumsChpok[upd2] += 1

assert(numPro0==numProms and numChk0==numChecks and numMoves%2==0)
print(numGames, "games.", numChecks, "checks,", numProms, "promotions.", numMoves>>1, "pairs of moves =>", round(50*numMoves/numGames)/100, "per game.", end='')
print(" Draws-Chess:", numDrawsChess, "=>", round(10000*numDrawsChess/numGames)/100, "%.", end='')
print(" Draws-Chpok:", numDrawsChpok, "=>", round(10000*numDrawsChpok/numGames)/100, "%.")
if 1:
	print(" Chess White/Black wins:", numWinsChessW, "/", numWinsChessB, "=>", round(1000*numWinsChessW/numWinsChessB)/1000)
	print(" Chpok White/Black wins:", numWinsChpokW, "/", numWinsChpokB, "=>", round(1000*numWinsChpokW/numWinsChpokB)/1000)
if 1:
	def printSorted(inp,game):
		res = []
		for x in inp.keys():
			x1 = str(inp[x])
			res.append('    '[len(x1):] + x1 + "  " + x)
		res = reversed(sorted(res))
		print(game)
		for x in res: print('    ', x)
	printSorted(sumsChess,"Chess:")
	printSorted(sumsChpok,"Chpok:")
