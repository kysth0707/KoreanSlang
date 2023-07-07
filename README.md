# KoreanSlang
- 비속어 실태 및 우회 차단 프로그램

> 2023.07.07 ~ 

# 목표
1. 비속어 데이터 시각화
- 표, 그래프 등
2. 비속어 우회 처리
- 우회하는 비속어를 처리하기

# 1. 비속어 데이터 시각화
1. csv 등으로 데이터 가져옴
2. Jupyter Notebook 사용
3. matplotlib 또는 sns 으로 데이터 시각화

# 2. 비속어 우회 처리
시도) 이미지로 처리
- 단, 과적합 등의 문제로 기각

결론) 유사 단어 목록으로 우회된 비속어 유추

1. 우회 단어 DB 사용

ㄱ : R, r, ㄲ, ㄱ  
ㅆ : T, t, ㅆ, ㅅ, ^^, ^ㅅ, ^ㅅ  
  
2. 해당 데이터셋 기반으로 기존 단어 유추
3. 순화 단어 DB 사용