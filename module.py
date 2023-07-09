from jamo import h2j, j2hcj
from hanguel_utils.unicode import join_jamos

BADWORD = '비속어'
PADRIP = '패드립'
ELSE = '그외'

# ================== 자모 분리, 합 ==================

def splitHan(txt : str) -> str:
    """
    한글을 분해해줍니다.  
    splitHan('안')  
    ->  
    'ㅇㅏㄴ'  
	"""
    return j2hcj(h2j(txt))

def joinHan(txt : str) -> str:
    """
    분리된 한글을 합쳐줍니다.  
    joinHan('ㅇㅏㄴ')  
    ->  
    '안'  
    """
    return join_jamos(txt)

def getChoseong(originalText : str) -> str:
	"""
	초성을 받습니다.
	※ 오직 한글만 가능합니다.
	getChoseong('안녕')
	->
	ㅇㄴ
	"""
	returnText = ""
	for txt in originalText:
		returnText += splitHan(txt)[0]
	return returnText

# ================== 우회 단어 복구 ==================

def restoreSplitedWord(originalText : str, circumventDict : dict) -> str:
	"""
	분리된 우회단어를 복구합니다.
	restoreSplitedWord('Lㄱㅁ', getCircumventDict())
	->
	'ㄴㄱㅁ'
	"""
	recoveredText = []
	for txt in originalText:
		if circumventDict.get(txt) == None:
			recoveredText.append([txt])
		else:
			recoveredText.append(circumventDict.get(txt))
	return recoveredText

def __toHappyWord(txt : str, badToHappyDict : dict) -> tuple:
	"""
	# ※ 더 이상 사용되지 않음.
	### 긍정어로 변환합니다.

	#### 욕설 및 비속어 -> (긍정어, 0)
	#### 패드립 -> ('', 1)
	#### 그 외 -> (입력단어, 2)

	1. toHappyWord('ㅅㅂ', getBadToHappyDict())
	->
	('아니', 0)

	2. toHappyWord('ㄴㄱㅁ', getBadToHappyDict())
	->
	('', 1)

	3. toHappyWord('반가워~', getBadToHappyDict())
	->
	('반가워~', 2)
	"""
	check = badToHappyDict.get(txt)
	if check == None:
		# 그 외
		return (txt, ELSE)
	elif check == False:
		# 패드립
		return ('', PADRIP)
	else:
		# 비속어
		return (check, BADWORD)
	
def convertToGoodWriting(originalText : str, circumventDict : dict, badToHappyDict : dict) -> tuple:
	"""
	### 입력된 문장을 (순화어, 수정된자모, 출력가능여부, 수정단어수)로 반환합니다.
	"이런Tlqkf?"
	->
	("이런아니?", "이런씨발?" True, 2)

	### 텍스트 변환 가중치
	#### -1 * (조합된 텍스트의 길이) + (수정 단어 수)
	"""
	boolBoxLen = []
	recoveredText = []
	for txt in originalText:
		if circumventDict.get(txt) == None:
			recoveredText.append(txt)
		else:
			a = circumventDict.get(txt)
			if len(a) == 1:
				recoveredText.append(a[0])
			else:
				boolBoxLen.append(len(a))
				recoveredText.append(a)


	newRecoveredText = []
	lastNum = 0
	for i, txt in enumerate(recoveredText):
		if type(txt) == list:
			if lastNum - i != 0:
				newRecoveredText.append("".join(recoveredText[lastNum:i]))
			newRecoveredText.append(recoveredText[i])
			lastNum = i+1
	if lastNum - len(recoveredText) - 1 != 0:
		newRecoveredText.append("".join(recoveredText[lastNum:len(recoveredText)]))


	listPoses = []
	for i, item in enumerate(newRecoveredText):
		if type(item) == list:
			listPoses.append(i)

	if len(listPoses) == 0:
		# 변형 가능한 단어가 한 개일 경우
		# print(newRecoveredText[0])
		joinedJamo = join_jamos(newRecoveredText[0])

		a=toHappyWriting(joinedJamo, badToHappyDict)
		return (a[0],joinedJamo,a[1],a[2])
	else:
		# 변형 가능한 단어가 여러 개일 경우
		fullCount = 1
		for x in boolBoxLen:
			fullCount *= x

		convertedTxts = []
		intBox = [0 for _ in range(len(boolBoxLen))]
		for _ in range(fullCount):
			for i in range(len(boolBoxLen)):
				if intBox[-i] >= boolBoxLen[-i]:
					intBox[-i] = 0
					intBox[-i-1] += 1
			tmp = newRecoveredText.copy()
			for i in range(len(boolBoxLen)):
				tmp[listPoses[i]] = newRecoveredText[listPoses[i]][intBox[i]]
			joinedJamo = joinHan("".join(tmp))
			convertedTxts.append((toHappyWriting(joinedJamo, badToHappyDict), (-len(joinedJamo), joinedJamo)))

			intBox[-1] += 1
		convertedText = sorted(convertedTxts, key=lambda x : x[0][2] + x[1][0], reverse=True)[0]
		return (convertedText[0][0], convertedText[1][1],convertedText[0][1],convertedText[0][2])



# ================== 문장을 순화어로 변환 ==================

def toHappyWriting(joinedJamo : str, badToHappyDict : dict) -> str:
	"""
	### 입력된 문장을 (순화어, 출력가능여부, 수정단어수)로 반환합니다.
	toHappyWriting("이런tlqkf?")
	->
	("이런아니?", True, 2)
	"""

	checkedBadwords = []
	for a in badToHappyDict.keys():
		if a in joinedJamo:
			checkedBadwords.append((joinedJamo.find(a), a, badToHappyDict[a]))
	checkedBadwords.sort(key=lambda x : x[0])
	newCheckedBadwords = []
	i = 0
	while True:
		if i >= len(checkedBadwords):
			break
		a = checkedBadwords[i]
		zipIt = []
		zipIt.append(a)
		ii = 0
		while True:
			ii += 1
			if ii + i >= len(checkedBadwords):
				break
			b = checkedBadwords[i + ii]
			if a[0] != b[0]:
				break
			else:
				zipIt.append(b)
				i+=1
				ii-=1
		if len(zipIt) != 1:
			newCheckedBadwords.append(sorted(zipIt, key=lambda x : len(x[1]), reverse=True)[0])
		else:
			newCheckedBadwords.append(zipIt[0])
		i+=1

	splitPoses = []
	for item in newCheckedBadwords:
		start,end=item[0], item[0] + len(item[1])
		# print(joinedJamo[start:end])
		splitPoses.append(start)
		splitPoses.append(end)
	try:
		if splitPoses[0] != 0:
			splitPoses.insert(0, 0)
	except:
		splitPoses.append(0)
	if splitPoses[:-1] != len(joinedJamo):
		splitPoses.append(len(joinedJamo))

	canSend = True

	changedWordCount = 0
	toGoodWords = []
	for i in range(len(splitPoses) - 1):
		txt = joinedJamo[splitPoses[i] : splitPoses[i+1]]
		if badToHappyDict.get(txt) == False:
			canSend = False
		elif badToHappyDict.get(txt) == None:
			toGoodWords.append(txt)
		else:
			changedWordCount += len(txt)
			toGoodWords.append(badToHappyDict[txt])

	return ("".join(toGoodWords), canSend, changedWordCount)


# ================== DB 로드 ==================

def __rSpace(txt : str) -> str:
    return txt.replace(' ','',9999)

def __refreshCircumvent() -> dict:
	CircumventingWordPath = "./datasets/CircumventingWords.txt"
	# 우회단어 위치

	CircumventText = []
	with open(CircumventingWordPath, 'r', encoding='utf8') as f:
		CircumventText = f.readlines()
	tmp = {}
	for txt in CircumventText:
		a, b = __rSpace(txt).rstrip().split(':')
		b=b.split(',')
		for c in b:
			if tmp.get(c) == None:
				tmp[c] = [a]
			else:
				e : list = tmp[c]
				e.append(a)
				tmp[c] = e
	return tmp

Circumvent = __refreshCircumvent()
def getCircumventDict() -> dict:
    """
    우회 초성 목록을 가져옵니다.
    {
		"r" : "ㄱ",
		"r" : "ㄲ",
		...
    }
    """
    return Circumvent


def __refreshBadToHappy() -> dict:
	alphabets = "abcdefghijklmnopqrtuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	ToHappyWordPath = "./datasets/ToHappyWords.txt"
	BadToHappyText = []
	with open(ToHappyWordPath, 'r', encoding='utf8') as f:
		BadToHappyText = f.readlines()
		
	tmp = {}
	for txt in BadToHappyText:
		a, b = __rSpace(txt).rstrip().split(':')
		if a[0] in alphabets:
			# 영어
			tmp[a.upper()] = False if b == "X" else b
			tmp[a.lower()] = False if b == "X" else b
		else:
			# 한국어
			tmp[a] = False if b == "X" else b
			# tmp[getChoseong(a)] = False if b == "X" else b
	return tmp

BadToHappy = __refreshBadToHappy()
def getBadToHappyDict() -> dict:
    """
    #### 비속어 -> 긍정어 목록을 가져옵니다.
    ### 패드립은 False 를 반환합니다.
    {
		"(비속어)" : "(긍정어)",
        "(패드립)" : False,
        ...
	}
    """
    return BadToHappy


# ==============================

if __name__ == "__main__":
	print("임포트로 사용해주세요")