from analysis import preprocess, count_gri_frequency
from visualization import create_wordcloud, create_materiality_matrix
import pandas as pd
import json
from collections import Counter

def run_analysis():
    # --- 1. 데이터 로드 ---
    print("Loading data...")
    df = pd.read_csv('data/crawled_news.csv')
    with open('data/gri_keyword_dict.json', 'r', encoding='utf-8') as f:
        gri_dict = json.load(f)

    # --- 2. 전체 키워드 추출 및 워드 클라우드 생성 ---
    print("Generating word cloud...")
    all_words = []
    for text in df['article_text']:
        all_words.extend(preprocess(text))
    
    word_counts = Counter(all_words)
    create_wordcloud(word_counts, 'output/esg_wordcloud.png')

    # --- 3. GRI 주제별 빈도수 계산 ---
    print("Counting GRI topic frequencies...")
    gri_freq = count_gri_frequency(df, gri_dict)
    print("GRI Frequencies:", gri_freq)

    # --- 4. 중대성 평가 매트릭스 생성 ---
    # 비즈니스 영향도 (이 부분은 프로젝트의 가상 시나리오에 따라 수동으로 점수 부여)
    business_impact = {
        "GRI 305: Emissions": 5,
        "GRI 403: Safety": 5,
        "GRI 414: Supplier": 4,
        "GRI 205: Corruption": 3,
    }

    print("Generating materiality matrix...")
    create_materiality_matrix(gri_freq, business_impact, 'output/materiality_matrix.png')
    
    print("Analysis complete!")


if __name__ == '__main__':
    run_analysis()