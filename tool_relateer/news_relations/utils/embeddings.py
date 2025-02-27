"""
Utilities for generating and managing embeddings.
"""

import os
import numpy as np
import faiss
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple, Any, Optional

from utils.config import VECTOR_DB_PATH, EMBEDDING_MODEL

class EmbeddingManager:
    """
    Manages the creation, storage, and retrieval of embeddings for news articles.
    Uses sentence-transformers for generating embeddings and FAISS for efficient similarity search.
    """
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """
        Initialize the embedding manager.
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.index_path = VECTOR_DB_PATH / "faiss_index.bin"
        self.metadata_path = VECTOR_DB_PATH / "metadata.pkl"
        self.index = None
        self.metadata = []
        
        # Load existing index and metadata if available
        self._load_index()
    
    def _load_index(self) -> None:
        """Load the FAISS index and metadata if they exist."""
        if self.index_path.exists() and self.metadata_path.exists():
            try:
                self.index = faiss.read_index(str(self.index_path))
                with open(self.metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                print(f"Loaded existing index with {len(self.metadata)} articles")
            except Exception as e:
                print(f"Error loading index: {e}")
                self._create_new_index()
        else:
            self._create_new_index()
    
    def _create_new_index(self) -> None:
        """Create a new FAISS index."""
        # Get the embedding dimension from the model
        dimension = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []
        print(f"Created new index with dimension {dimension}")
    
    def _save_index(self) -> None:
        """Save the FAISS index and metadata to disk."""
        if self.index is not None:
            faiss.write_index(self.index, str(self.index_path))
            with open(self.metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)
            print(f"Saved index with {len(self.metadata)} articles")
    
    def add_document(self, text: str, metadata: Dict[str, Any]) -> int:
        """
        Add a document to the index.
        
        Args:
            text: The text content to embed
            metadata: Additional information about the document
            
        Returns:
            The index of the added document
        """
        # Generate embedding
        embedding = self.model.encode([text])[0].reshape(1, -1).astype('float32')
        
        # Add to index
        self.index.add(embedding)
        
        # Store metadata
        doc_id = len(self.metadata)
        self.metadata.append(metadata)
        
        # Save updated index
        self._save_index()
        
        return doc_id
    
    def add_documents(self, texts: List[str], metadatas: List[Dict[str, Any]]) -> List[int]:
        """
        Add multiple documents to the index.
        
        Args:
            texts: List of text contents to embed
            metadatas: List of metadata dictionaries
            
        Returns:
            List of document IDs
        """
        if not texts:
            return []
        
        # Generate embeddings
        embeddings = self.model.encode(texts).astype('float32')
        
        # Add to index
        self.index.add(embeddings)
        
        # Store metadata
        start_id = len(self.metadata)
        self.metadata.extend(metadatas)
        
        # Save updated index
        self._save_index()
        
        return list(range(start_id, len(self.metadata)))
    
    def search(self, query: str, k: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query: The query text
            k: Number of results to return
            
        Returns:
            List of dictionaries containing document metadata and similarity scores
        """
        if self.index is None or self.index.ntotal == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query])[0].reshape(1, -1).astype('float32')
        
        # Search index
        k = min(k, self.index.ntotal)
        distances, indices = self.index.search(query_embedding, k)
        
        # Format results
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):
                # Convert distance to similarity score (1 - normalized distance)
                similarity = 1.0 - min(dist / 2.0, 1.0)
                result = {
                    "id": int(idx),
                    "similarity": float(similarity),
                    **self.metadata[idx]
                }
                results.append(result)
        
        return results
    
    def get_document_by_id(self, doc_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a document by its ID.
        
        Args:
            doc_id: The document ID
            
        Returns:
            The document metadata or None if not found
        """
        if 0 <= doc_id < len(self.metadata):
            return self.metadata[doc_id]
        return None
    
    def get_document_count(self) -> int:
        """
        Get the number of documents in the index.
        
        Returns:
            The number of documents
        """
        return len(self.metadata)
    
    def clear_index(self) -> None:
        """Clear the index and metadata."""
        self._create_new_index()
        self._save_index()
        print("Index cleared") 