# src/utils/config.py
# ----------------------------------------------------------
# Loads and validates all environment variables in one place.
# Every other module imports from here — no os.getenv scattered
# across the codebase.
# ----------------------------------------------------------

import os
from dotenv import load_dotenv

# Load the .env file from the project root
load_dotenv()


class Config:
    """
    Central configuration class.
    Reads all environment variables and exposes them as
    typed class attributes with sensible defaults.
    """

    # --- API Keys ---
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")

    # --- Model Names ---
    EMBEDDING_MODEL_NAME: str = os.getenv(
        "EMBEDDING_MODEL_NAME",
        "BAAI/bge-large-en-v1.5"
    )
    LLM_MODEL_NAME: str = os.getenv(
        "LLM_MODEL_NAME",
        "gemini-2.5-flash"
    )
    RERANKER_MODEL_NAME: str = os.getenv(
        "RERANKER_MODEL_NAME",
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    # --- Chunking ---
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    # --- Retriever ---
    RETRIEVER_TOP_K: int = int(os.getenv("RETRIEVER_TOP_K", "10"))

    # --- Reranker ---
    RERANKER_TOP_N: int = int(os.getenv("RERANKER_TOP_N", "5"))

    @classmethod
    def validate(cls) -> None:
        """
        Call this at startup to catch missing keys early.
        Raises a clear error instead of a cryptic API failure later.
        """
        missing = []

        if not cls.GOOGLE_API_KEY:
            missing.append("GOOGLE_API_KEY")

        if not cls.HUGGINGFACE_TOKEN:
            missing.append("HUGGINGFACE_TOKEN")

        if missing:
            raise EnvironmentError(
                f"\n\n Missing required environment variables:\n"
                f"  {', '.join(missing)}\n\n"
                f"  Please add them to your .env file.\n"
            )

    @classmethod
    def display(cls) -> None:
        """
        Prints config summary at startup (masks secrets).
        Useful for debugging without exposing keys.
        """
        print("=" * 50)
        print("  RAG Agent — Configuration Summary")
        print("=" * 50)
        print(f"  LLM Model       : {cls.LLM_MODEL_NAME}")
        print(f"  Embedding Model : {cls.EMBEDDING_MODEL_NAME}")
        print(f"  Reranker Model  : {cls.RERANKER_MODEL_NAME}")
        print(f"  Chunk Size      : {cls.CHUNK_SIZE}")
        print(f"  Chunk Overlap   : {cls.CHUNK_OVERLAP}")
        print(f"  Retriever Top-K : {cls.RETRIEVER_TOP_K}")
        print(f"  Reranker Top-N  : {cls.RERANKER_TOP_N}")
        print(f"  Google API Key  : {'SET' if cls.GOOGLE_API_KEY else 'MISSING'}")
        print(f"  HF Token        : {'SET' if cls.HUGGINGFACE_TOKEN else 'MISSING'}")
        print("=" * 50)