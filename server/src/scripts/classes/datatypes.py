from typing import TypedDict, Optional, Any


# Define the custom type for the data dictionary

class ChromaData(TypedDict, total=False):  # total=False means all keys are optional
    embedding: Any
    metadata: Any
    document: Any
    id: Any

class ImgTextDict(TypedDict, total=False):
    image: ChromaData
    text: ChromaData
    all_text: ChromaData


class TextDict(TypedDict, total=False):
    sentence: ChromaData
    token: ChromaData


class DataDict(TypedDict, total=False):
    img_text: ImgTextDict
    text: TextDict
