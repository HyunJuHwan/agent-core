# rag/qdrant_client.py
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchAny
from sentence_transformers import SentenceTransformer

class QdrantHandler:
    def __init__(self, host="localhost", port=6333):
        self.client = QdrantClient(host=host, port=port)
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    
    def create_collection(self, collection_name="search_history"):
        """Qdrant에 컬렉션을 생성합니다."""
        self.client.recreate_collection(
            collection_name=collection_name,
            vectors_config={"size": 384, "distance": "Cosine"}  # 벡터 차원 및 거리 계산 방법 설정
        )
    
    def upsert_data(self, collection_name, data):
        """벡터 데이터를 Qdrant에 저장합니다."""
        print(f"Upserting data into collection: {collection_name}")
        print(f"Data to upsert: {data}")
        points = []
        for entry in data:
            # entry['text']가 실제 문자열인지 확인
            text = entry.get('text', '')  # 'text'가 없으면 빈 문자열로 기본 설정
            if isinstance(text, str):
                # 문자열이면 벡터화
                vector = self.model.encode([text])[0].tolist()
            elif isinstance(text, dict):
                # dict이면 문자열로 변환하여 벡터화
                text = str(text)  # dict를 문자열로 변환
                vector = self.model.encode([text])[0].tolist()
            else:
                print(f"Invalid entry['text']: {entry['text']}")
                continue  # 문자열이 아닌 경우에는 건너뜁니다.

            # PointStruct에 벡터와 메타데이터 추가
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,  # 벡터화된 데이터
                payload=entry  # 메타데이터
            )
            points.append(point)

        if not points:
            print("No valid points to upsert")
            return
        
        self.client.upsert(collection_name=collection_name, points=points)
    
    def search_data(self, collection_name, user_query, user_id, limit=3):
        """주어진 쿼리와 user_id로 Qdrant에서 유사한 데이터를 검색합니다."""
        query_vector = self.model.encode([user_query])[0].tolist()

        # 필터링 조건 추가: user_id가 일치하는 데이터만 조회
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchAny(any=[str(user_id)])
                )
            ]
        )
        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=query_filter
        )

        return results
