import PIL

class ImageManipulator:
    def __init__(self):
        self.choices = [
            {"name": "increase_brightness", "method": self.increase_brightness},
            {"name": "decrease_brightness", "method": self.decrease_brightness},
            {"name": "increase_contrast", "method": self.increase_contrast},
            {"name": "decrease_contrast", "method": self.decrease_contrast},
            {"name": "decrease_sharpness", "method": self.decrease_sharpness}
        ]

    def increase_brightness(self, image_path, rating):
        image = PIL.Image.open(image_path)
        min_rating_at = 3
        # if rating is 0 then adjust the brightness to min_rating_at
        # if rating is 50 or higher then don't adjust the brightness
        enhancer = PIL.ImageEnhance.Brightness(image)
        if rating >= 50:
            return self.get_image()
        else:
            factor = (1*(rating) + min_rating_at*(50-rating)) / 50
            return enhancer.enhance(factor)
    
    def decrease_brightness(self, image_path, rating):        
        image = PIL.Image.open(image_path)
        min_rating_at = 0.33
        # if rating is 0 then don't adjust the brightness
        # if rating is 50 or higher then adjust the brightness to max_rating_at
        enhancer = PIL.ImageEnhance.Brightness(image)
        if rating >= 50:
            return self.get_image()
        else:
            factor = (1*(rating) + min_rating_at*(50-rating)) / 50
            return enhancer.enhance(factor)
    
    def increase_contrast(self, image_path, rating):        
        image = PIL.Image.open(image_path)
        min_rating_at = 3
        enhancer = PIL.ImageEnhance.Contrast(image)
        if rating >= 50:
            return self.get_image()
        else:
            factor = (1*(rating) + min_rating_at*(50-rating)) / 50
            return enhancer.enhance(factor)
    
    def decrease_contrast(self, image_path, rating):
        image = PIL.Image.open(image_path)
        min_rating_at = 0.33
        enhancer = PIL.ImageEnhance.Contrast(image)
        if rating <= 0:
            return self.get_image()
        else:
            factor = (1*(rating) + min_rating_at*(50-rating)) / 50
            return enhancer.enhance(factor)
    
    def decrease_sharpness(self, image_path, rating):
        image = PIL.Image.open(image_path)
        min_rating_at = 0.8
        enhancer = PIL.ImageEnhance.Sharpness(image)
        if rating <= 0:
            return self.get_image()
        else:
            factor = (1*(rating) + min_rating_at*(50-rating)) / 50
            return enhancer.enhance(factor)