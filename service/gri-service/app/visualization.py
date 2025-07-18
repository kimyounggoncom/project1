import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 워드 클라우드 생성 함수
def create_wordcloud(word_counts, output_path):
    wc = WordCloud(font_path='/usr/share/fonts/truetype/nanum/NanumGothic.ttf', # Docker 이미지에 맞는 폰트 경로
                   background_color='white', width=800, height=600)
    cloud = wc.generate_from_frequencies(word_counts)
    cloud.to_file(output_path)
    print(f"Word cloud saved to {output_path}")

# 중대성 평가 매트릭스 생성 함수
def create_materiality_matrix(gri_freq, business_impact, output_path):
    topics = list(gri_freq.keys())
    media_scores = list(gri_freq.values()) # Y축: 미디어 관심도 (뉴스 빈도)
    business_scores = [business_impact.get(topic, 0) for topic in topics] # X축: 비즈니스 영향도

    plt.figure(figsize=(12, 8))
    plt.scatter(business_scores, media_scores)
    
    plt.title('Materiality Assessment Matrix')
    plt.xlabel('Business Impact')
    plt.ylabel('Media & Stakeholder Interest')
    
    # 각 점에 라벨 추가
    for i, topic in enumerate(topics):
        plt.text(business_scores[i], media_scores[i], topic.split(':')[0], fontsize=9)
        
    plt.grid(True)
    plt.savefig(output_path)
    print(f"Materiality matrix saved to {output_path}")