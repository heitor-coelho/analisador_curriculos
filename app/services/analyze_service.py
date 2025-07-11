from app.utils.ocr_utils import extract_text
from app.utils.llm_utils import rank_resumes, ResumeDict
from fastapi import UploadFile
from typing import List, Dict, Optional

def process_files(files: List[UploadFile], query: Optional[str] = None) -> Dict:
    processed = []

    for file in files:
        content = file.file.read()
        try:
            text = extract_text(file.filename, content)
            processed.append({
                "filename": file.filename,
                "text": text
            })
        except Exception as e:
            processed.append({
                "filename": file.filename,
                "error": str(e)
            })

    resumes_for_ranking: List[ResumeDict] = [r for r in processed if "text" in r]

    if query:
        ranked = rank_resumes(resumes_for_ranking, query)
        return {
            "ranked_results": ranked,
            "all_resumes": processed
        }
    else:
        return {
            "all_resumes": processed
        }
