import chromadb
import os
from .datatypes import DataDict


class Chroma():

    def __init__(self) -> None:
        self.path = self.get_project_root('creativec')
        self.database_path = os.path.join(self.path, "server", "src", "api", "database")
        self.client = chromadb.PersistentClient(self.database_path)
        self.collections = {
            "img-text" : {
                "image" : self.collection("img-text-image"),
                "text" : self.collection("img-text-text"),
            },
            "text": {
                "category":self.collection("text-category"),
                "sentence": self.collection("text-sentence"),
            }
        }

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
   
        
    def collection(self,name: str):
        return self.client.get_or_create_collection(name=name)
    

    def add_embed(self, data: DataDict):

        if not isinstance(data["img-text"],type(None)):


            if not isinstance(data["img-text"]["image"],type(None)):
                self.collections["img-text"]["image"].add(
                    embeddings= [data["img-text"]["image"]["embedding"]],
                    documents= [data["img-text"]["image"]["document"]],
                    ids=[data["img-text"]["image"]["id"]]
                )
            if not isinstance(data["img-text"]["text"],type(None)):
                
                self.collections["img-text"]["text"].add(
                    embeddings= [data["img-text"]["text"]["embedding"]],
                    documents= [data["img-text"]["text"]["document"]],
                    ids=[data["img-text"]["text"]["id"]]
                )
                
        if not isinstance(data["text"],type(None)):


            if not isinstance(data["text"]["sentence"],type(None)):
                self.collections["text"]["sentence"].add(
                    embeddings= [data["text"]["sentence"]["embedding"]],
                    documents= [data["text"]["sentence"]["document"]],
                    metadatas=[data["text"]["sentence"]["metadata"]],
                    ids=[data["text"]["sentence"]["id"]]
                )
            
            if not isinstance(data["text"]["category"],type(None)):
                self.collections["text"]["category"].add(
                    embeddings= [data["text"]["category"]["embedding"]],
                    documents= [data["text"]["category"]["document"]],
                    ids=[data["text"]["category"]["id"]]
                )
            

            
    def delete_from(self, data: list[str]|None = None):

        if not isinstance(data, type(None)):
            collections = data
        else:
            collections = ["img-text-image", "img-text-text", "text-sentence", "text-category"]

        for i in range(len(collections)):
            self.collection(collections[i]).delete()