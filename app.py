import flask
from flask_cors import CORS
from pipeline import Pipeline
from google_photo_api import GooglePhotosHook
from net_cnn import Net

app = flask.Flask(__name__)
CORS(app)

token = "ya29.a0AXooCgtH59BeJ0HgntmYYYEjL7IF9xe_FHqBTg5pcfOAm0RQJl8Ltt0c7JfsgGhoAoboI13N2CujEpWRxfLjGHiG7cRWF0EYhNkIRoYUq6Qn_P1-9lb_GUKWwPXx3NCMOT2MMdhNdt6zk7IB12S-jzkf7hUfVd3xKKLHaCgYKAZYSARISFQHGX2Mi5w-jy5KoMljokFamACan6w0171"
# token = False

ghook = GooglePhotosHook("secret.json", ['https://www.googleapis.com/auth/photoslibrary.readonly'], token)
                         
model = Net()
pipeline = Pipeline(ghook, model)

# /new image
@app.route('/next')
def new_image():
    pipeline.load_one()
    return "New image loaded"

# /live
@app.route('/live')
def live():
    filepath = pipeline.current_image
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
    
