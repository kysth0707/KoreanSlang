from jamo import h2j, j2hcj
from hanguel_utils.unicode import join_jamos

__all__ = ["splitHan", "joinHan", "getCircumventDict", "getBadToHappyDict"]

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


CircumventingWordPath = r'E:\GithubProjects\KoreanSlang\datasets\CircumventingWords.txt'
# 우회단어 위치

CircumventText = []
with open(CircumventingWordPath, 'r', encoding='utf8') as f:
    CircumventText = f.readlines()

def __rSpace(txt : str):
    return txt.replace(' ','',9999)

Circumvent = {}
for txt in CircumventText:
    a, b = __rSpace(txt).rstrip().split(':')
    b=b.split(',')
    for c in b:
        Circumvent[c] = a

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


ToHappyWordPath = r'E:\GithubProjects\KoreanSlang\datasets\ToHappyWords.txt'
BadToHappyText = []
with open(ToHappyWordPath, 'r', encoding='utf8') as f:
    BadToHappyText = f.readlines()
    
BadToHappy = {}
for txt in BadToHappyText:
    a, b = __rSpace(txt).rstrip().split(':')
    if b == "X":
        BadToHappy[a] = False
    else:
    	BadToHappy[a] = b

def getBadToHappyDict() -> dict:
    """
    비속어 -> 긍정어 목록을 가져옵니다.
    패드립은 False 를 반환합니다.
    {
		"(비속어)" : "(긍정어)",
        "(패드립)" : False,
        ...
	}
    """
    return BadToHappy