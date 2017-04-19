# coding: utf-8

import os
from flask import Flask, render_template, request, url_for, abort,Blueprint, jsonify, Response
from flask.ext.bootstrap import Bootstrap
from flask import Flask, jsonify, render_template, request

from descriptor.descriptor import Descriptor
from searcher.searcher import Searcher

from config import config
from forms import *
from form_exec import *
import cryptlib
import chartkick
import cv2

app = Flask(__name__)
bootstrap = Bootstrap(app)

# 
app.config.from_object(config[os.getenv("FLASK_CONFIG") or "default"])
ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/')
app.jinja_env.add_extension("chartkick.ext.charts")




# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')



# 
def gen():
    i=1
    while i<10:
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+str(i)+b'\r\n')
        i+=1

def get_frame():

    camera_port=0

    ramp_frames=100

    camera=cv2.VideoCapture(camera_port) #this makes a web cam object

    
    i=1
    while True:
        retval, img = camera.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        
        imgencode=cv2.imencode('.jpg',img)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i+=1

    del(camera)
# 






@app.route('/')
def index():
    return render_template("index.html")



@app.route("/aboutass")
def aboutass():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contactme.html")

@app.route('/recognize')
def recongnize():
    return render_template('digitRecognition.html')

@app.route('/cam')
def cam():
    return render_template('camera.html')



@app.route('/calc')
def calc():
     return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/recogresult', methods = ['POST'])
def recog():
    try:
        import cv2
        from sklearn.externals import joblib
        from skimage.feature import hog
        import numpy as np

        # Load the classifier
        clf = joblib.load("digits_cls.pkl")

        # Read the input image 
        im = cv2.imread("photo_1.jpg")

        # Convert to grayscale and apply Gaussian filtering
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

        # Threshold the image
        ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)

        # Find contours in the image
        _, contours, _ = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        # ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Get rectangles contains each contour
        rects = [cv2.boundingRect(ctr) for ctr in contours]

        # For each rectangular region, calculate HOG features and predict
        # the digit using Linear SVM.
        for rect in rects:
            # Draw the rectangles
            cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3) 
            # Make the rectangular region around the digit
            leng = int(rect[3] * 1.6)
            pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
            pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
            roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
            # Resize the image
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            roi = cv2.dilate(roi, (3, 3))
            # Calculate the HOG features
            roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
            nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
            cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)

        cv2.imshow("Resulting Image with Rectangular ROIs", im)
        cv2.waitKey()
    except Exception, e:
        raise e

    pass



@app.route("/image")
def image_search():
    blah = '103100'
    return render_template('image.html')



@app.route('/search', methods = ['POST'])
def search():
  if request.method == 'POST':
    results_arr = []
    img_path = request.form.get('img')

    try:
      import cv2

      d = Descriptor((8, 12, 3))
      query = cv2.imread('static/images/' + img_path)
      features = d.describe(query)
      searcher = Searcher('index.csv')
      results = searcher.search(features)

      for (score, id) in results:
        results_arr.append({'image': str(id), 'score': str(score)})

      return jsonify(results = (results_arr[::-1][:5]))

    except:
      return jsonify({'sorry': 'Sorry, something went wrong! Please try again.'})

@app.route("/crypt/<crypt_type>", methods=["GET", "POST"])
def crypt(crypt_type):
    crypt_forms = {
        "classic": ClassicCryptForm,
        "des": DESCryptForm,
        "rsa": RSACryptForm,
        "lfsr": LFSRCryptForm,
        "dsa": DSASignForm,
    }
    subtitles = {
        "classic": u"古典加密——仿射密码",
        "des": u"DES加密",
        "rsa": u"RSA加密",
        "lfsr": u"序列密码",
        "dsa": u"DSA数字签名",
    }

    if crypt_type not in subtitles:
        abort(404)
    
    form = (crypt_forms[crypt_type])()                                          # 对提交的表单进行处理（如加密）
    other_params = {}

    if request.method == "POST":
        if form.validate_on_submit():
            form, other_params = exec_form(crypt_type, form)
    elif crypt_type == "lfsr":
        form, other_params = exec_form(crypt_type, form)

    return render_template(crypt_type+"_crypt.html", 
                        form=form,
                        subtitle=subtitles[crypt_type],
                        **other_params)



@app.route("/prime_test", methods=["POST"])
def prime_test():
    from cryptlib.RSA import is_prime
    try:
        number = int(request.form["number"])
        times = int(request.form["times"])
    except ValueError:
        abort(400)
    return str(is_prime(number, times))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



@app.errorhandler(500)
def interbal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run('0.0.0.0',debug=True)
