from PIL import Image
import os

class Preprocess:

    """
    A class to preprocess images for input into the CLIP model.

    Attributes:
    - path (str): The directory path where raw and preprocessed images are stored.

    Methods:
    - rename_files(): Rename all files in the raw directory using an iterator.
    - get_filenames(): List all files in the raw directory.
    - preprocess_image(image_path): Preprocess an image for input into the CLIP model.
    - save_image(image, idx): Save the preprocessed image in the preprocessed directory.
    - run(): Execute the preprocessing pipeline.
    """

    def __init__(self) -> None:
        """Initialize the Preprocess class with the default directory path."""
        self.path = os.path.join(os.getcwd(),"/assets")

    def rename_files(self):
        """
        Rename all files in the raw directory using an iterator.

        Raises:
        - ValueError: If the raw directory path is invalid.
        """

        path = self.path + "/raw"
        if not os.path.isdir(path):
            raise ValueError(f"'{path}' is not a valid directory.")
        
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        
        for idx, filename in enumerate(files, start=1):
            file_extension = os.path.splitext(filename)[1]
            new_filename = f"{idx}{file_extension}"
            os.rename(os.path.join(path, filename), os.path.join(path, new_filename))


    def get_filenames(self):
        """
        List all files in the raw directory.

        Returns:
        - list: A list of filenames in the raw directory.

        Raises:
        - ValueError: If the raw directory path is invalid.
        """
        path = self.path + "/raw"
        if not os.path.isdir(path):
            raise ValueError(f"'{path}' is not a valid directory.")
        
        files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        
        return files


    def preprocess_image(self, image_path):
        """
        Preprocess an image for input into the CLIP model.

        Parameters:
        - image_path (str): Path to the image file.

        Returns:
        - Image.Image: A PIL Image object that's ready for input into the CLIP model.
        """
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        image = image.resize((224, 224))
        
        return image
    
    def save_image(self, image, idx):
        """
        Save the preprocessed image with a name based on the iterator (idx) in the preprocessed directory.

        Parameters:
        - image (Image.Image): The preprocessed image to be saved.
        - idx (int): Iterator value to be used as the filename.

        Raises:
        - ValueError: If the preprocessed directory path is invalid.
        """
        path = self.path + "/preprocessed"
        if not os.path.isdir(path):
            raise ValueError(f"'{path}' is not a valid directory.")
        
        file_extension = ".jpg"
        filename = f"{idx}{file_extension}"
        image.save(os.path.join(path, filename))

    def run(self):
        """
        Execute the preprocessing pipeline: rename raw images, preprocess them, and save the preprocessed images.
        """

        # self.rename_files()
        images = self.get_filenames()
        for i in range(len(images)):
            new_img = self.preprocess_image(images[i])
            self.save_image(new_img, i)


p = Preprocess()
p.run()