from google_photo_api import GooglePhotosHook
from net_cnn import Net
import tempfile
import requests

class Pipeline:
    def __init__(self, ghook: GooglePhotosHook, model: Net):
        self.ghook = ghook
        self.model = model
        self.current_image = tempfile.NamedTemporaryFile(delete=False, dir=".").name
        self.batch = []
        self.load_one()
        return
    
    def load_one(self):
        if len(self.batch) == 0:
            self.load_batch()
        image = self.batch.pop()
        image_url = image["baseUrl"]
        download = requests.get(image_url)
        save = open(self.current_image, "wb")
        save.write(download.content)

    def load_batch(self):
        self.batch = self.ghook.browse_images().get("mediaItems")    
        return      

    def set_user_rating_for_current_image(self, rating):
        self.current_image_rating = rating
        return  
    
    def ask_model_for_rating(self):
        return self.model.eval_image(self.current_image)
    
    def train_model_with_correct_rating(self):
        self.train_model_with_correct_rating(self.current_image, self.current_image_rating)
        return