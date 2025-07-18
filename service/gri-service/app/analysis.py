import pandas as pd
import json
from konlpy.tag import Okt
from collections import Counter

# 텍스트 전처리 함수
def preprocess(text):
    okt = Okt()
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    # 명사만 추출
    nouns = okt.nouns(str(text))
    # 한 글자 단어 및 불용어 제거
    words = [n for n in nouns if len(n) > 1 and n not in stopwords]
    return words

# GRI 주제 매칭 및 빈도수 계산 함수
def count_gri_frequency(df, gri_dict):
    gri_counts = {topic: 0 for topic in gri_dict.keys()}
    
    for text in df['article_text']: # 'article_text'는 뉴스 본문이 있는 컬럼명
        processed_words = preprocess(text)
        # 각 기사마다 어떤 주제가 등장했는지 중복 없이 체크
        found_topics_in_article = set()
        for word in processed_words:
            for topic, keywords in gri_dict.items():
                if word in keywords:
                    found_topics_in_article.add(topic)
        
        # 기사에서 한 번이라도 등장한 주제의 카운트를 1씩 올림
        for topic in found_topics_in_article:
            gri_counts[topic] += 1
            
    return gri_counts