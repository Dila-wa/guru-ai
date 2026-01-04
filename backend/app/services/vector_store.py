"""
Vector store - manages embeddings and FAISS index for semantic search
"""
import logging
from typing import List, Tuple, Dict, Optional
import numpy as np
import joblib

try:
    import faiss
except ImportError:
    faiss = None

logger = logging.getLogger(__name__)


class VectorStore:
    """Manages embeddings and FAISS index for semantic search"""

    def __init__(self, embedding_dim: int = 384):
        """
        Initialize vector store

        Args:
            embedding_dim: Dimension of embeddings (default: 384 for sentence-transformers)
        """
        self.embedding_dim = embedding_dim
        self.index = None
        self.chunk_metadata = []
        self.embeddings = None

        if faiss is None:
            logger.warning(
                "FAISS not installed. Install with: pip install faiss-cpu or faiss-gpu"
            )

    def create_index(self, embeddings: np.ndarray) -> None:
        """
        Create FAISS index from embeddings

        Args:
            embeddings: Array of shape (n_samples, embedding_dim)
        """
        if faiss is None:
            raise RuntimeError("FAISS is not installed")

        if embeddings.shape[1] != self.embedding_dim:
            raise ValueError(
                f"Embedding dimension {embeddings.shape[1]} doesn't match "
                f"expected dimension {self.embedding_dim}"
            )

        self.embeddings = embeddings

        # Create index
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.index.add(embeddings.astype(np.float32))

        logger.info(f"Created FAISS index with {embeddings.shape[0]} vectors")

    def add_embeddings(self, embeddings: np.ndarray, metadata: List[Dict]) -> None:
        """
        Add embeddings to the index

        Args:
            embeddings: Array of shape (n_samples, embedding_dim)
            metadata: List of metadata dictionaries for each embedding
        """
        if faiss is None:
            raise RuntimeError("FAISS is not installed")

        if len(embeddings) != len(metadata):
            raise ValueError("Number of embeddings must match number of metadata entries")

        if self.index is None:
            self.create_index(embeddings)
        else:
            # Add to existing index
            self.index.add(embeddings.astype(np.float32))
            self.embeddings = np.vstack([self.embeddings, embeddings])

        self.chunk_metadata.extend(metadata)
        logger.info(f"Added {len(embeddings)} embeddings to index. Total: {self.index.ntotal}")

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[int, float, Dict]]:
        """
        Search for similar chunks

        Args:
            query_embedding: Query embedding vector
            k: Number of nearest neighbors to return

        Returns:
            List of (chunk_id, distance, metadata) tuples, sorted by relevance
        """
        if self.index is None:
            logger.warning("Index is empty, returning no results")
            return []

        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)

        distances, indices = self.index.search(query_embedding.astype(np.float32), k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.chunk_metadata):
                metadata = self.chunk_metadata[idx]
                results.append((idx, float(dist), metadata))

        return results

    def search_by_text(
        self, query_text: str, embedder, k: int = 5
    ) -> List[Tuple[int, float, Dict]]:
        """
        Search by text query (requires embedder)

        Args:
            query_text: Text query
            embedder: Function to convert text to embedding
            k: Number of neighbors to return

        Returns:
            List of (chunk_id, distance, metadata) tuples
        """
        query_embedding = embedder(query_text)
        return self.search(query_embedding, k)

    def save(self, index_path: str, metadata_path: str) -> None:
        """
        Save index and metadata to disk

        Args:
            index_path: Path to save FAISS index
            metadata_path: Path to save metadata
        """
        if self.index is None:
            logger.warning("Index is empty, nothing to save")
            return

        try:
            faiss.write_index(self.index, index_path)
            joblib.dump(
                {
                    "metadata": self.chunk_metadata,
                    "embedding_dim": self.embedding_dim,
                },
                metadata_path,
            )
            logger.info(f"Saved index to {index_path} and metadata to {metadata_path}")
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            raise

    def load(self, index_path: str, metadata_path: str) -> None:
        """
        Load index and metadata from disk

        Args:
            index_path: Path to FAISS index
            metadata_path: Path to metadata
        """
        try:
            self.index = faiss.read_index(index_path)

            data = joblib.load(metadata_path)
            self.chunk_metadata = data["metadata"]
            self.embedding_dim = data["embedding_dim"]

            logger.info(f"Loaded index from {index_path} with {self.index.ntotal} vectors")
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            raise

    def is_empty(self) -> bool:
        """Check if index is empty"""
        return self.index is None or self.index.ntotal == 0

    def get_stats(self) -> Dict:
        """Get index statistics"""
        return {
            "total_vectors": self.index.ntotal if self.index else 0,
            "embedding_dim": self.embedding_dim,
            "total_metadata": len(self.chunk_metadata),
            "is_empty": self.is_empty(),
        }
