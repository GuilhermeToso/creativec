from typing import TypedDict, Any


# Define the custom type for the data dictionary

class ImageTextData(TypedDict, total=False):  # total=False means all keys are optional
    embedding: Any
    metadata: Any
    document: Any
    id: Any


class ImgTextDict(TypedDict, total=False):
    image: ImageTextData
    text: ImageTextData
    all_text: ImageTextData


class TextData(TypedDict, total=False):
    embedding: Any
    metadata: Any
    document: Any
    metadata: Any
    id: Any


class TextDict(TypedDict, total=False):
    sentence: TextData
    token: TextData


class DataDict(TypedDict, total=False):
    img_text: ImgTextDict
    text: TextDict
