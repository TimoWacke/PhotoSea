import flask
from flask_cors import CORS
from pipeline import Pipeline
from google_photo_api import GooglePhotosHook
from net_cnn import Net

app = flask.Flask(__name__)
CORS(app)

token = "ya29.a0AXooCgvIab6Ji4UZFwXNm_fxpnHaxPmPYDA75fKKAkaBJ5iy9Ny1BrjfJlbSep5E6bhbTIe8yHcbZ053Wjd-Fc0XvY9MKMLEj6pwVxfgHzoczPEGT3J15jPFWm9lxezujzWuQX6H7ImT3NsyNBcCiVnFB0YtflzeeSelaCgYKAQASARISFQHGX2Mit6OYiTfWIZKOl9e90hr7Lw0171"
# token = False

ghook = GooglePhotosHook("secret.json", ['https://www.googleapis.com/auth/photoslibrary.readonly'], token)
                         
model = Net()
pipeline = Pipeline(ghook, model)

# /new image
@app.route('/next')
async def new_image():
    await pipeline.load_one()
    return "New image loaded"

# /live
@app.route('/live')
def live():
    print("/live sents", pipeline.current_image_path)
    filepath = pipeline.current_image_path
    return flask.send_file(filepath)

# /rate
@app.route('/rate/<rating>')
def rate():
    rating = flask.request.view_args['rating']
    pipeline.set_user_rating_for_current_image(rating)
    return "Rating set to " + rating

# /ai-rating
@app.route('/ai-rating')
def ai_rating():
    rating = pipeline.ask_model_for_rating()
    return {"ai_rating": rating}

# host
if __name__ == '__main__':
    app.run(port=3000)
    
