from backend.rag.knowledge_base import get_historical_precedent
from backend.rag.vector_store import vector_store


async def retrieve_context(query: str, corridor: str = None) -> dict:
    historical = await get_historical_precedent(corridor=corridor)
    vector_results = await vector_store.similarity_search(query, k=3)

    return {
        "historical_precedents": historical[:3],
        "vector_matches": vector_results,
        "query": query,
    }
