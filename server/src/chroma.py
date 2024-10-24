import chromadb
import os

class Chroma:

    def __init__(self) -> None:
        self.path = os.path.join(os.getcwd(),"database")
        self.client = chromadb.PersistentClient(self.path)
        self.img_col = self.get_col("image_embedidngs")
        self.text_col = self.get_col("text_embedidngs")
        self.all_texts = self.get_col("all_texts")

    def create_col(self,name: str):
        self.client.create_collection(name=name)

    def get_col(self,name: str):
        return self.client.get_or_create_collection(name=name)

    def add_image_embed(self, image_name: str, image_embeding: list[float], id: str):

        self.img_col.add(
            embeddings=image_embeding,
            metadatas={"name":image_name},
            ids=id
        )

    def add_text_embed(self, text: str, text_embed: list[float], id: str):
        
        self.text_col.add(
            embeddings=text_embed,
            documents=text,
            ids=id            
        )

    def add_all_texts(self, text: str, text_embed: list[float], id: str, metadata: str):

        self.all_texts.add(
            embeddings=text_embed,
            documents=text,
            metadatas={"source":metadata},
            ids=id
        )

c = Chroma()
print(len(c.img_col.get(include=["embeddings"])["embeddings"]))