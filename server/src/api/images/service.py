from server.src.api.chroma.registry import registry
from .types import ChromaResponse, SearchParameters
import numpy as np

class ImageTextService:
    """
    A service class for handling image-text related operations using Chroma.
    Methods
    -------
    __init__() -> None
        Initializes the ImageTextService with a Chroma instance from the registry.
    get_texts() -> ChromaResponse
        Retrieves texts from the Chroma collection "img-text-text".
    get_results(selected_docs: SearchParameters) -> ChromaResponse
        Retrieves results based on selected documents and their semantics.
    """

    def __init__(self) -> None:
        """
        Initializes the service with a chroma instance from the registry.

        Attributes:
            chroma: An instance of chroma retrieved from the registry.
        """
        self.chroma = registry["chroma"]

    def get_texts(self) -> ChromaResponse:
        """
        Retrieves text documents from the Chroma collection "img-text-text".
        Returns:
            ChromaResponse: An object containing the IDs and documents retrieved from the collection.
        """

        texts = self.chroma.collection("img-text-text").get(include=["documents"])
        return ChromaResponse(ids=texts["ids"], documents=texts["documents"])
    
    def get_results(self, selected_docs: SearchParameters) -> ChromaResponse:
        """
        Retrieves search results based on the provided search parameters.
        Args:
            selected_docs (SearchParameters): The search parameters containing modality and documents.
        Returns:
            ChromaResponse: The response containing the IDs and documents of the search results.
        """

        modality = selected_docs.modality
        collection = f"img-text-{modality}"
        print(collection)
        
        components = []
        
        for doc in selected_docs.documents:
            print(doc)
            try:
                embedding = self.chroma.collection(collection).get(
                    where_document={"$contains": doc.document},
                    include=["embeddings"]
                )
                print(embedding)
                components.append(embedding["embeddings"][0])
            except Exception as e:
                print(e)
                components.append(np.zeros(768))
        
        components = np.array(components)


        
        resultant_vector = np.zeros(components[0].shape)

        for i in range(len(components)):
            resultant_vector = resultant_vector + selected_docs.documents[i].semantic*components[i]

        
        results = self.chroma.collection("img-text-image").query(
            query_embeddings=resultant_vector.tolist(),
            n_results=7,
            include=["documents"]
        )

        # Remove the selected documents from the results
        for doc in selected_docs.documents:
            try:
                idx = results["ids"][0].index(doc.id)
                results["ids"][0].pop(idx)
                results["documents"][0].pop(idx)
            except Exception as e:
                print(e)

        return ChromaResponse(ids=results["ids"][0], documents=results["documents"][0])