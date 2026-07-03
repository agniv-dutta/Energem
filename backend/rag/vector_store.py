from typing import Optional


class VectorStore:
    def __init__(self):
        self._documents: list[dict] = []

    async def add_documents(self, documents: list[dict]):
        self._documents.extend(documents)

    async def similarity_search(self, query: str, k: int = 3) -> list[dict]:
        query_lower = query.lower()
        scored = []
        for doc in self._documents:
            text = (doc.get("title", "") + " " + doc.get("content", "")).lower()
            score = sum(1 for word in query_lower.split() if word in text)
            scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:k]]

    async def get_all(self) -> list[dict]:
        return self._documents


vector_store = VectorStore()
