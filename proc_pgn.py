import sys
f = open(sys.argv[1], mode="rb")
sumsChess,sumsChpok = {},{}
curW = curB = curRes = curLog = ""
numGames = numMoves = numProms = numChecks = numPro0 = numChk0 = 0
numDrawsChess = numWinsChessW = numWinsChessB = 0
numDrawsChpok = numWinsChpokW = numWinsChpokB = 0
nSK1 = nSK2 = nSK3 = nSK4 = nSK5 = 0

def findName(n, n1):
	#if n.startswith(n1) or n1.startswith(n):  # need?
	#	if n in sumsChess:  return n
	#	sumsChess[n],sumsChpok[n] = 0,0
	#	return n
	names = n.split(',')
	if len(names)==1:  names = n.split(' ')
	if len(names) > 1:
		lastName = names[0].strip()
		firstName = names[1].strip()
		n = lastName + ', ' + firstName
		if len(names) > 2:  n += ' ' + names[2].strip()
		if len(names) > 3:  n += ' ' + names[3].strip()
	if n in sumsChess:  return n
	if 0:  # Enable this if your input file is not too large
		for k in sumsChess.keys():
			if k.startswith(n):  # k is longer than n
				return k
			if n.startswith(k):  # n is longer than k
				sumsChess[n] = sumsChess[k]
				sumsChpok[n] = sumsChpok[k]
				if k==n1:  return n
				sumsChess.pop(k)  # remove the shorter one
				sumsChpok.pop(k)
				return n
	sumsChess[n],sumsChpok[n] = 0,0
	return n

while 1:
	li = f.readline()
	if len(li)==0: break
	li = li.decode('utf-8', errors='ignore').strip()
	if len(li) and li[0]=='[':
		if   li[1:7]=='White ':  curW = li[8:-2]
		elif li[1:7]=='Black ':  curB = li[8:-2]
		elif li[1:7]=='Result':  curRes,curLog = li[9:-2],""
	elif len(li):
		for c in '(){}$':
			if c in li:
				curLog = li = '$'
				break
		curLog += li.strip() + ' '
	elif len(curLog):
		if ('$' in curLog):
			#print("skipped1", curLog)
			nSK1 += 1
			continue

		moves = curLog.strip().split(' ')
		if moves[-1] != curRes:
			print("Error! result is unclear,", curRes, "or", moves[-1])
			nSK2 += 1
			continue
		if len(moves) < 8:
			#print("skipped2", curLog)
			nSK2 += 1
			continue
		#print(curLog)
		hadError = nMoves = nProms = nChecks = 0
		scoreW = scoreB = 0
		for i in range(len(moves)-1):
			m = moves[i]
			if i%3==0:
				if m[-1]!='.':
					print("Error! Invalid move", i/3+1, "in this line:", curLog)
					hadError = 1
					break
				continue
			s = m.strip('+#')
			if len(s) < len(m):  nChecks += 1
			m = s.split('=')[0]
			if len(m) < len(s):  nProms += 1

			if i%3==1 and i==len(moves)-2:  break
			nMoves+=1
			if m[0]=='O':  continue
			if m[0]=='Z':
				hadError = 1
				break
			row = ord(m[-1]) - ord('0')
			if not 1 <= row <= 8:
				hadError = 1
				break
			if i%3==1:  scoreW += max(0, row-4)
			else:       scoreB += max(0, 5-row)

		if hadError:
			#print("skipped3", curLog)
			nSK3 += 1
			continue

		curW = findName(curW, '_notaplc')
		curB = findName(curB, curW)
		if curW==curB:
			#print("skipped4", curW)
			nSK4 += 1
			continue

		#print(curW, curB, curRes, curLog)
		if curRes=='1/2-1/2':  upd1,upd2,numDrawsChess = curW,curB,numDrawsChess+1
		elif curRes=='1-0':    upd1,upd2,numWinsChessW = curW,curW,numWinsChessW+1
		elif curRes=='0-1':    upd1,upd2,numWinsChessB = curB,curB,numWinsChessB+1
		else:
			#print("Error! result is:", curRes)
			nSK5 += 1
			continue
		sumsChess[upd1] += 1
		sumsChess[upd2] += 1

		numMoves += nMoves
		numProms += nProms
		numChecks+= nChecks
		numGames += 1
		#if (numGames&1023)==0:  print(numGames, nSK1, nSK2, nSK3, nSK4, nSK5)

		if   scoreW>scoreB:  upd1,upd2,numWinsChpokW = curW,curW,numWinsChpokW+1
		elif scoreW<scoreB:  upd1,upd2,numWinsChpokB = curB,curB,numWinsChpokB+1
		else:                upd1,upd2,numDrawsChpok = curW,curB,numDrawsChpok+1
		sumsChpok[upd1] += 1
		sumsChpok[upd2] += 1

		for x in curLog:
			if x=="=":     numPro0 += 1
			if x in "+#":  numChk0 += 1

#print(numChk0, numPro0, numMoves)
assert(numChk0==numChecks)
assert(numPro0==numProms)
assert(numMoves%2==0)
numSkipped = nSK1 + nSK2 + nSK3 + nSK4 + nSK5
if numSkipped:  print(numSkipped, "games were skipped: ", nSK1, nSK2, nSK3, nSK4, nSK5)
print(numGames, "games.", numChecks, "checks,", numProms, "promotions.", numMoves>>1, "pairs of moves =>", round(50*numMoves/numGames)/100, "per game.", end='')
print(" Draws-Chess:", numDrawsChess, "=>", round(10000*numDrawsChess/numGames)/100, "%,", end='')
print(" Draws-Chpok:", numDrawsChpok, "=>", round(10000*numDrawsChpok/numGames)/100, "%.")
if 1:
	print(" Chess White/Black wins:", numWinsChessW, "/", numWinsChessB, "=>", round(1000*numWinsChessW/numWinsChessB)/1000)
	print(" Chpok White/Black wins:", numWinsChpokW, "/", numWinsChpokB, "=>", round(1000*numWinsChpokW/numWinsChpokB)/1000)
if 1:
	def printSorted(inp,game):
		res = []
		for x in inp.keys():
			x1 = str(inp[x])
			res.append('     '[len(x1):] + x1 + "  " + x)
		res = reversed(sorted(res))
		print(game)
		i = 1
		for x in res:
			print("%6d   %s" % (i, x))
			i+=1
	printSorted(sumsChess,"Chess:")
	printSorted(sumsChpok,"Chpok:")
