from sentence_transformers import SentenceTransformer, util
from typing import List, Dict, Optional, TypedDict
import logging

logger = logging.getLogger(__name__)

class ResumeDict(TypedDict):
    filename: str
    text: str

_model = SentenceTransformer('all-MiniLM-L6-v2')
_query_cache: Optional[Dict[str, any]] = None
_resume_cache: Dict[str, any] = {}

def compute_similarity(text_embedding, query_embedding) -> float:
    return util.pytorch_cos_sim(query_embedding, text_embedding).item()

def rank_resumes(resumes: List[ResumeDict], query: str, top_k: int = 3) -> List[Dict]:
    global _query_cache

    try:
        if _query_cache is None or _query_cache.get("query") != query:
            query_embedding = _model.encode(query, convert_to_tensor=True, normalize_embeddings=True)
            _query_cache = {"query": query, "embedding": query_embedding}
        else:
            query_embedding = _query_cache["embedding"]

        results = []
        for r in resumes:
            text = r.get('text')
            filename = r.get('filename')
            if not text or not filename:
                continue  

            if filename in _resume_cache:
                text_embedding = _resume_cache[filename]
            else:
                text_embedding = _model.encode(text, convert_to_tensor=True, normalize_embeddings=True)
                _resume_cache[filename] = text_embedding

            similarity = compute_similarity(text_embedding, query_embedding)

            results.append({
                "filename": filename,
                "similarity": similarity,
                "justification": f"O currículo contém termos relevantes à sua busca '{query}', com similaridade de {similarity:.2f}."
            })

        return sorted(results, key=lambda x: x['similarity'], reverse=True)[:top_k]

    except Exception as e:
        logger.exception("Erro ao rankear currículos")
        return []
