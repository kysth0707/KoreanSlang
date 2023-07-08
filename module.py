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
	recoveredText = ""
	for txt in originalText:
		if circumventDict.get(txt) == None:
			recoveredText += txt
		else:
			recoveredText += circumventDict.get(txt) 
	return recoveredText

def toHappyWord(txt : str, badToHappyDict : dict) -> tuple:
	"""
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

# ================== 비속어 포함 체크 ==================

# def checkBadword(txt : str) -> str:

# 	return ""


# ================== DB 로드 ==================

def __rSpace(txt : str) -> str:
    return txt.replace(' ','',9999)

def __refreshCircumvent() -> dict:
	CircumventingWordPath = r'E:\GithubProjects\KoreanSlang\datasets\CircumventingWords.txt'
	# 우회단어 위치

	CircumventText = []
	with open(CircumventingWordPath, 'r', encoding='utf8') as f:
		CircumventText = f.readlines()
	tmp = {}
	for txt in CircumventText:
		a, b = __rSpace(txt).rstrip().split(':')
		b=b.split(',')
		for c in b:
			tmp[c] = a
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
	ToHappyWordPath = r'E:\GithubProjects\KoreanSlang\datasets\ToHappyWords.txt'
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
			tmp[getChoseong(a)] = False if b == "X" else b
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