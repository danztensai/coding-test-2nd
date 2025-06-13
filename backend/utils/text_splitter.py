import spacy
from spacy_chunks import SpacyChunker

class SemanticChunker:
    def __init__(self, chunk_size=800, overlap=80):
        self.chunk_size = chunk_size
        self.overlap = overlap

        # Load spacy model and spacy-chunks
        self.nlp = spacy.load("en_core_web_sm")
        self.chunker = SpacyChunker(self.nlp)

    def chunk(self, text: str):
        doc = self.nlp(text)
        semantic_chunks = self.chunker.chunk_text(doc)

        # fallback if semantic chunks are too large → split again by char
        final_chunks = []
        for chunk in semantic_chunks:
            if len(chunk) > self.chunk_size:
                final_chunks.extend(self._split_by_char(chunk))
            else:
                final_chunks.append(chunk)
        return final_chunks

    def _split_by_char(self, text):
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.overlap):
            chunks.append(text[i:i+self.chunk_size])
        return chunks
