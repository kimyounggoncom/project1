"""
ESG Analysis Service Package

이 패키지는 ESG 관련 뉴스 분석 및 시각화 기능을 제공합니다.
"""

from .analysis import preprocess, count_gri_frequency
from .visualization import create_wordcloud, create_materiality_matrix

__version__ = "1.0.0"
__author__ = "ESG Analysis Team"

__all__ = [
    "preprocess",
    "count_gri_frequency", 
    "create_wordcloud",
    "create_materiality_matrix"
]
