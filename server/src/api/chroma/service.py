import chromadb
import os
from server.src.api.types.chroma import DataDict


class Chroma():

    def __init__(self) -> None:
        self.path = os.path.join(os.getcwd(),"database")
        self.client = chromadb.PersistentClient(self.path)

        self.collections = {
            "img-text" : {
                "image" : self.collection("img-text-image"),
                "text" : self.collection("img-text-text"),
                "all-text":self.collection("img-text-all-text")
            },
            "text": {
                "category":self.collection("text-category"),
                "sentence": self.collection("text-sentence"),
                "token":self.collection("text-token")
            }
        }

    def collection(self,name: str):
        return self.client.get_or_create_collection(name=name)


    def add_embed(self, data: DataDict):

        if not isinstance(data["img-text"],type(None)):


            if not isinstance(data["img-text"]["image"],type(None)):
                self.collections["img-text"]["image"].add(
                    embeddings= data["img-text"]["image"]["embedding"],
                    documents= data["img-text"]["image"]["document"],
                    ids=data["img-text"]["image"]["id"]
                )
            if not isinstance(data["img-text"]["text"],type(None)):
                self.collections["img-text"]["text"].add(
                    embeddings= data["img-text"]["text"]["embedding"],
                    documents= data["img-text"]["text"]["document"],
                    ids=data["img-text"]["text"]["id"]
                )

            if not isinstance(data["img-text"]["all-text"],type(None)):
                self.collections["img-text"]["all-text"].add(
                    embeddings= data["img-text"]["all-text"]["embedding"],
                    documents= data["img-text"]["all-text"]["document"],
                    ids=data["img-text"]["all-text"]["id"]
                )

        if not isinstance(data["text"],type(None)):


            if not isinstance(data["text"]["sentence"],type(None)):
                self.collections["text"]["sentence"].add(
                    embeddings= data["text"]["sentence"]["embedding"],
                    documents= data["text"]["sentence"]["document"],
                    metadatas=data["text"]["sentence"]["metadata"],
                    ids=data["text"]["sentence"]["id"]
                )
            if not isinstance(data["text"]["token"],type(None)):
                self.collections["text"]["token"].add(
                    embeddings= data["text"]["token"]["embedding"],
                    documents= data["text"]["token"]["document"],
                    metadatas= data["text"]["token"]["metadata"],
                    ids=data["text"]["token"]["id"]
                )

            if not isinstance(data["text"]["category"],type(None)):
                self.collections["text"]["category"].add(
                    embeddings= data["text"]["category"]["embedding"],
                    documents= data["text"]["category"]["document"],
                    ids=data["text"]["category"]["id"]
                )



    def delete_from(self, data: list[str]|None = None):

        if not isinstance(data, type(None)):
            collections = data
        else:
            collections = ["img-text-image", "img-text-text", "img-text-all-text", "text-sentence", "text-token"]

        for i in range(len(collections)):
            self.collection(collections[i]).delete()
