from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
from .chroma import Chroma
import os


class Sentence():
    """
    A class to represent a Sentence for embedding purposes.

    Attributes
    ----------
    model : SentenceTransformer
        The SentenceTransformer model used for encoding sentences.

    Methods
    -------
    run(sentences: List[str], cat: str) -> Dict[str, List[Tuple[Any, str]]]:
        Encodes the given sentences and returns them categorized under the provided category.
    """

    def __init__(self) -> None:
        """
        Initializes the Sentence object with a specific SentenceTransformer model.
        """
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        self.path = self.get_project_root('creativec')
        self.data_path = os.path.join(self.path, "server", "assets", "data")
        self.chroma = Chroma()

    def get_project_root(self, root_folder_name: str):
        # Start at the current working directory
        current_path = os.getcwd()

        # Loop until the root of the file system is reached
        while current_path != os.path.dirname(current_path):
            # Check if the folder name 'creativec' is part of the path
            if os.path.basename(current_path) == root_folder_name:
                return current_path
            # Go up one directory
            current_path = os.path.dirname(current_path)

        raise FileNotFoundError(f"Project root '{root_folder_name}' not found.")


    def extract_phrases_from_file(self,filename: str) -> list[str]:
        
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        phrases = [line.split('. ', 1)[-1].strip() for line in lines if '. ' in line]
        
        return phrases
    
    def list_filenames(self, directory_path: str) -> list[str]:
        """List all filenames in the given directory."""
        try:
            return [filename for filename in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, filename))]
        except FileNotFoundError:
            print(f"Directory '{directory_path}' not found.")
            return []

    def embed(self, sentence: str, id_sentence: str, category: str):
        """
        Encodes the given sentences using the SentenceTransformer model.

        Parameters
        ----------
        sentences : str
            The list of sentences to be encoded.
        
        Returns
        -------
        Dict[str, List[Tuple[Any, str]]]
            A dictionary containing the category as the key and the list of tuples 
            (encoded sentence, original sentence) as the value.
        """
        encoded = self.model.encode(sentence, output_value=None)
        data = {"img-text":None, "text":{"sentence":None,"token":None,"category":None}}
        data["text"]["sentence"] = {
            "embedding":encoded["sentence_embedding"].tolist(),
            "document":sentence,
            "metadata":{"category":category},
            "id":id_sentence
        }

        return data
    
    def run(self):
        """
        Executes the main process of embedding sentences from different categories.
        This method performs the following steps:
        1. Defines a list of categories.
        2. Initializes a sentence ID counter.
        3. Iterates over each category to:
            a. List filenames in the category's directory.
            b. Extract sentences from each file.
            c. Embed each sentence and add the embedding to the chroma database.
            d. Increment the sentence ID counter.
        4. Creates and adds a category result embedding to the chroma database.
        Attributes:
            categories (list): List of categories to process.
            sentence_id (int): Counter for sentence IDs.
        """
        categories = ["food","music","food-music"]
        sentence_id = 0

        for i in range(len(categories)):
            category = categories[i]
            category_path = os.path.join(self.path, "server", "assets", "sentences", category)
            filenames = self.list_filenames(category_path)
            for filename in filenames:
                sentences = self.extract_phrases_from_file(os.path.join(category_path, filename))
                for j in range(len(sentences)):
                    sentence_id += 1
                    result = self.embed(sentences[j], str(sentence_id), category)
                    self.chroma.add_embed(result)
            category_result = {
                "img-text":None,
                "text":{
                    "sentence":None,
                    "category":{
                        "embedding": self.model.encode(category).tolist(),
                        "document": category,
                        "id":str(i)
                    }
                }
            }
            self.chroma.add_embed(category_result)




