import io
import pytest
from unittest.mock import MagicMock, patch
from app.services.analyze_service import process_files  # ajuste para seu módulo real


class DummyUploadFile:
    def __init__(self, filename, content_bytes):
        self.filename = filename
        self.file = io.BytesIO(content_bytes)

@pytest.mark.parametrize("query", [None, "some query"])
def test_process_files_success_and_error(query):
    # Mock para extrair texto
    def fake_extract_text(filename, content):
        if filename == "good_image.png":
            return "Texto extraído da imagem"
        elif filename == "good_pdf.pdf":
            return "Texto extraído do PDF"
        else:
            raise RuntimeError("Erro simulado de extração")

    # Criar arquivos dummy
    files = [
        DummyUploadFile("good_image.png", b"fake image bytes"),
        DummyUploadFile("good_pdf.pdf", b"fake pdf bytes"),
        DummyUploadFile("bad_file.txt", b"conteudo invalido"),
    ]

    with patch("app.services.analyze_service.extract_text", side_effect=fake_extract_text):
        result = process_files(files, query=query)

    # Verifica que os arquivos foram processados
    all_files = result["all_resumes"]
    filenames = [f["filename"] for f in all_files]
    assert set(filenames) == {"good_image.png", "good_pdf.pdf", "bad_file.txt"}

    for f in all_files:
        if f["filename"] in ("good_image.png", "good_pdf.pdf"):
            assert "text" in f
            assert len(f["text"].strip()) > 0
        else:
            assert "error" in f
            assert "Erro simulado" in f["error"]

    # Se query foi passada, deve ter 'ranked_results'
    if query:
        assert "ranked_results" in result
        assert isinstance(result["ranked_results"], list)
        assert len(result["ranked_results"]) <= len(all_files) - 1  # menos o arquivo com erro
        # Cada item deve ter similaridade e filename
        for r in result["ranked_results"]:
            assert "filename" in r
            assert "similarity" in r
            assert isinstance(r["similarity"], float)
    else:
        # Sem query, não tem ranked_results
        assert "ranked_results" not in result
