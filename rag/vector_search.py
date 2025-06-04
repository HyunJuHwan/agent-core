# rag/vector_search.py
from rag.qdrant_client import QdrantHandler

class VectorSearch:
    def __init__(self, collection_name="search_history"):
        self.qdrant = QdrantHandler()
        self.collection_name = collection_name

    def search_similar_history(self, user_query, user_id):
        """주어진 쿼리와 user_id로 Qdrant에서 유사한 질문과 답변을 검색합니다."""
        # Qdrant에서 유사한 데이터 검색
        results = self.qdrant.search_data(self.collection_name, user_query, user_id)
        
        # 유사한 질문과 답변 추출
        similar_history = [
            {
                "question": result.payload.get('text', ''),  # 'payload'에서 'text'를 'question'으로 사용
                "answer": result.payload.get('llm_answer', '')  # 'llm_answer'를 'answer'로 사용
            }
            for result in results  # 결과 리스트 순회
        ]
        return similar_history
