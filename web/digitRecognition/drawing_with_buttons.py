from openni import *
import cv2.cv as cv

def translate_coordinates(openni_point):
  opencv_point = depth.to_projective([openni_point])
  return (int(opencv_point[0][0]), int(opencv_point[0][1]))

def overlap(point, button):
  global buttons
  return point[0] >= buttons[button]['start'][0] and point[0] <= buttons[button]['end'][0] and point[1] >= buttons[button]['start'][1] and point[1] <= buttons[button]['end'][1]

def gesture_detected(src, gesture, id, end_point):
    global hands, buttons

    if gesture == 'Click':
      no_button_clicked = True
      for button in buttons:
        if overlap(translate_coordinates(end_point), button):
          for id in hands:
            hands[id]['color']['name'] = button
            hands[id]['color']['cv'] = buttons[button]['color']
            hands[id]['drawing'] = False
            no_button_clicked = False
            break

      if no_button_clicked:
        for id in hands:
          hands[id]['drawing'] = not hands[id]['drawing']

    hands_generator.start_tracking(end_point)

def gesture_progress(src, gesture, point, progress): pass

def create(src, id, pos, time):
    global hands
    ponto = depth.to_projective([pos])
    centro = (int(ponto[0][0]), int(ponto[0][1])) 
    hands[id] = {'current_position': centro, 'drawing': False, 'color': {'name': 'Choose a Color', 'cv': cv.CV_RGB(255,255,255)}}

def update(src, id, pos, time):
    global hands
    hands[id]['previous_position'] = hands[id]['current_position']
    hands[id]['current_position'] = translate_coordinates(pos)

def destroy(src, id, time):
    global hands
    del hands[id]

def update_video_with(image):
    cv.SetData(cv_image, image)
    if hands:
      if hands[1]['drawing']:
        update_notification_with('Click to Stop Drawing')
      else:
        update_notification_with('Click to Start Drawing')

      for id in hands:
        cv.PutText(cv_image, hands[id]['color']['name'], hands[id]['current_position'] ,text_font , cv.CV_RGB(255,255,255))
    else:
      update_notification_with('Wave to Interact')
    for button in buttons:
      cv.Rectangle(cv_image, buttons[button]['start'], buttons[button]['end'] , buttons[button]['color'], -1, cv.CV_AA, 0)
    cv.ShowImage('Video', cv_image)

def update_notification_with(text):
    cv.PutText(cv_image, text, (240,30) ,text_font , cv.CV_RGB(255,255,255))

def update_drawing():
    blink = cv.CloneImage(drawing)
    if hands:
      for id in hands:
        cv.Circle(blink, hands[id]['current_position'], 10, hands[id]['color']['cv'], -1, cv.CV_AA, 0)
        if hands[id]['drawing'] == True:
          cv.Line(drawing, hands[id]['previous_position'], hands[id]['current_position'], hands[id]['color']['cv'], 10, cv.CV_AA, 0) 
    cv.ShowImage('Drawing', blink)

########################### MAIN ##################################

cv.NamedWindow('Video',1)
cv.MoveWindow('Video',0,0)
cv.NamedWindow('Drawing',1)
cv.MoveWindow('Drawing',720,0)

text_font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.6, 0.6, 0, 1, 4)

drawing = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
cv.Set(drawing, (255.0,255.0,255.0))

cv_image = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
hands = {}
buttons_size = (100, 60)
buttons = {'White': {'color': cv.CV_RGB(255,255,255), 'start': (500, 30), 'end': (500 + buttons_size[0], 30 + buttons_size[1])},
          'Black': {'color': cv.CV_RGB(0,0,0), 'start': (500, 100), 'end': (500 + buttons_size[0], 100 + buttons_size[1])},
          'Red': {'color': cv.CV_RGB(255,0,0), 'start': (500, 170), 'end': (500 + buttons_size[0], 170 + buttons_size[1])},
          'Green': {'color': cv.CV_RGB(0,255,0), 'start': (500, 240), 'end': (500 + buttons_size[0], 240 + buttons_size[1])},
          'Blue': {'color': cv.CV_RGB(0,0,255), 'start': (500, 310), 'end': (500 + buttons_size[0], 310 + buttons_size[1])},
          }

ni = Context()
ni.init()
ni.init_from_xml_file("OpenniConfig.xml")
video = ni.find_existing_node(NODE_TYPE_IMAGE)
depth = ni.find_existing_node(NODE_TYPE_DEPTH)

gesture_generator = GestureGenerator()
gesture_generator.create(ni)
gesture_generator.add_gesture('Wave')
gesture_generator.add_gesture('Click')

hands_generator = HandsGenerator()
hands_generator.create(ni)

ni.start_generating_all()

gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
hands_generator.register_hand_cb(create, update, destroy)

key = -1
while (key < 0):
    ni.wait_any_update_all()
    image = video.get_raw_image_map_bgr()
    update_video_with(image)
    update_drawing()
    key = cv.WaitKey(1)

cv.DestroyAllWindows()
cv.SaveImage("Drawing.jpg", drawing)
