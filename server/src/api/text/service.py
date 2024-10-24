from .types import ChromaResponse, Document
from server.src.api.chroma.registry import registry
import numpy as np

np.random.seed(0)   

class TextService:

    """
    Service class for handling text-related operations using the Chroma collection.
    """

    def __init__(self):
        """
        Initializes the TextService with the Chroma registry.
        """
        self.chroma = registry["chroma"]

    def get_categories(self) -> ChromaResponse:
        """
        Retrieves text categories from the Chroma collection.

        Returns:
            ChromaResponse: A response object containing category IDs and documents.
        """
        categories = self.chroma.collection("text-category").get(include=["documents"])
        return ChromaResponse(ids=categories["ids"], documents=categories["documents"])

    def get_docs(self, category: str = '') -> ChromaResponse:
        """
        Retrieves documents from the Chroma collection based on the specified category.

        Args:
            category (str): The category to filter documents by. Defaults to an empty string.

        Returns:
            ChromaResponse: A response object containing document IDs and documents.
        """

        # If there is '-' in the category, split it into two categories and get the documents for both

        if "-" in category:
            categories = category.split("-")
            data = {
                "ids": [],
                "documents": []
            }
            for cat in categories:
                category_docs = self.chroma.collection("text-sentence").get(include=["documents", "metadatas"],
                                                                            where={"category": {"$eq":cat.lower()}})
                data["ids"] += category_docs["ids"]
                data["documents"] += category_docs["documents"]

            # Shuffle the ids, then use the ids to shuffle the documents so that the order is the same
            ids = data["ids"]
            docs = data["documents"]
            zipped = list(zip(ids, docs))
            np.random.shuffle(zipped)
            ids, docs = zip(*zipped)


            return ChromaResponse(ids=list(ids), documents=list(docs))

        categories = self.chroma.collection("text-sentence").get(include=["documents", "metadatas"],
                                                            where={"category": {"$eq":category.lower()}})
        return ChromaResponse(ids=categories["ids"], documents=categories["documents"])

    def process(self, docs: list[Document] )  -> np.ndarray:
        """
        Processes a document to retrieve its embeddings from the Chroma collection.

        Args:
            doc (Document): The document to process.

        Returns:
            np.ndarray: An array of embeddings for the document. Returns a zero array if no embeddings are found.
            :param docs:
        """
        print("Docs: ", docs)
        # Log the documents we're querying for
        embeddings = []
        for doc in docs:
            try:
                result = self.chroma.collection("text-sentence").get(
                    where_document={"$contains": doc.document},
                    include=["embeddings"]
                )
                print("Result: ", result)
                embeddings.append(result["embeddings"][0])
            except Exception as e:
                print(e)
                embeddings.append(np.zeros(384))

        print("Embeddings: ", embeddings)

        return np.array(embeddings)

    def get_similar(self, selected_docs: list[Document]) -> ChromaResponse:
        """
        Retrieves documents similar to the selected documents based on their embeddings.

        Args:
            selected_docs (list[Document]): A list of documents to find similarities for.

        Returns:
            ChromaResponse: A response object containing IDs and documents of similar documents.
        """
        print("Docs: ", selected_docs)
        embeddings = self.process(selected_docs)

        for j in range(len(embeddings)):
            print("Shape: ", embeddings[j].shape)
            print("Document: ", selected_docs[j].document)
            print("Semantica: ", selected_docs[j].semantic)

        embedding_query = np.zeros((1, 384))
        for i in range(len(embeddings)):
            embedding_query = embedding_query + selected_docs[i].semantic * embeddings[i]

        print("Query: ", embedding_query)

        try:
            docs_results = self.chroma.collection("text-sentence").query(
                query_embeddings=embedding_query.tolist(),
                n_results=7,
                include=["documents"]
            )

            # Remove the selected documents from the results
            for doc in selected_docs:
                try:
                    idx = docs_results["ids"][0].index(doc.id)
                    docs_results["ids"][0].pop(idx)
                    docs_results["documents"][0].pop(idx)
                except Exception as e:
                    print(e)


            return ChromaResponse(ids=docs_results["ids"][0], documents=docs_results["documents"][0])
        except Exception as e:
            print(e)
            return ChromaResponse(ids=[], documents=[])


