from google_photo_api import GooglePhotosHook
from net_cnn import Net
from image_manipulator import ImageManipulator
import random
import requests
import tempfile
import os
import time
from pillow_heif import register_heif_opener
register_heif_opener()

class Pipeline:
    def __init__(self, ghook: GooglePhotosHook, model: Net):
        self.ghook = ghook
        self.model = model
        
        self.temp_dir = tempfile.TemporaryDirectory(dir=".")
        
        self.original_image = None
        self.current_image_path = None
        
        self.arificial_training_pipeline = ArtificialTrainingPipeline()
        self.current_manipulated_image = tempfile.NamedTemporaryFile(delete=False, dir=".").name
        
        self.batch = []
        self.load_one()
        return
    
    def random_choice_if_manipulation(self):
        probablity = 0.9
        if random.random() < probablity:
            return True        
    
    async def load_one(self):
        
        if len(self.batch) == 0:
            self.load_batch()
            
        if not self.original_image:
            self.download_and_save_image(self.batch[0])
        
        if self.random_choice_if_manipulation():
            os.remove(self.current_manipulated_image)            
            image, rating = self.arificial_training_pipeline.make_training_image(self.original_image)
            # save PIL image to self.current_manipulated_image path          
            filename = self.batch[0]["filename"].replace(".HEIC", ".png")  
            image.save(filename)
            self.current_manipulated_image = filename
            self.current_image_path = self.current_manipulated_image
        else:           
            self.current_image_path = self.original_image
            self.batch.pop(0)
            os.remove(self.current_manipulated_image)
            os.remove(self.original_image)
            self.original_image = None
            self.current_manipulated_image = None
            self.current_image_path = None
        await time.sleep(1)
        return

    def download_and_save_image(self, media_item):
        image_url = media_item.get("baseUrl")
        file_name = media_item.get("filename")
        file_path = self.temp_dir.name + "/" + file_name
        download = requests.get(image_url)
        save = open(file_path, "wb")
        save.write(download.content)
        save.close()
        self.original_image = file_path

    def load_batch(self):
        self.batch = self.ghook.browse_images().get("mediaItems") #
        print("Batch loaded", self.batch)
        self.downloaded = False
        return      

    def set_user_rating_for_current_image(self, rating):
        self.current_image_rating = rating
        return  
    
    def ask_model_for_rating(self):
        return self.model.eval_image(self.original_image)
    
    def train_model_with_correct_rating(self):
        self.train_model_with_correct_rating(self.original_image, self.current_image_rating)
        return
    
    
class ArtificialTrainingPipeline:
    def __init__(self):
        self.manipulator = ImageManipulator()
    
    def make_training_image(self, path):
        rating = random.randint(0, 50)
        style_choice = random.choice(self.manipulator.choices)
        image = style_choice["method"](path, rating)
        print("made artificial training image with", style_choice["name"], "for rating", rating)
        return image, rating
    