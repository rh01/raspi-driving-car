from bottle import route, run, template
import time
import RPi.GPIO as GPIO

#######################################
## Add your IP address here
#######################################
IP_ADDRESS = '192.168.1.5'
PORT = 8080
######################################


# Next we setup the pins for use!
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)


@route('/')
def hello():
    return '<b>Hi from RoboCar!</b>'

@route('/remote')
def remote():
    return '''
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="http://code.jquery.com/mobile/1.4.2/jquery.mobile-1.4.2.min.css">
<script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>
<script src="http://code.jquery.com/mobile/1.4.2/jquery.mobile-1.4.2.min.js"></script>
<script>
$(document).ready(function() {
  $("#moveleft").click(function() {
    $.ajax({
            url:  '/remote/left',
            type: 'GET',
            data: { command:'left' }
    });
  });
  
  $("#moveright").click(function() {
    $.ajax({
            url:  '/remote/right',
            type: 'GET',
            data: { command:'right' }
    });
  });

  $("#moveback").click(function() {
    var isRunning = $("#start").is(":checked") ? 1:0;
    $.ajax({
            url:  '/remote/back',
            type: 'GET',
            data: { command:'right' }
    });
  });

  $("#play").click(function() {
    var cmd ='start';
    $.ajax({
            url:  '/remote/play',
            type: 'GET',
            data: { command:cmd }
    });
  });
  
  $("#pause").click(function() {
    var cmd ='stop'; 
    $.ajax({
            url:  '/remote/pause',
            type: 'GET',
            data: { command:cmd }
    });
  });
});
</script>

<style>
#moveback {
  -webkit-transform: rotate(90deg);     /* Chrome and other webkit browsers */
  -moz-transform: rotate(90deg);        /* FF */
  -o-transform: rotate(90deg);          /* Opera */
  -ms-transform: rotate(90deg);         /* IE9 */
  transform: rotate(90deg);             /* W3C compliant browsers */

  /* IE8 and below */
  filter: progid:DXImageTransform.Microsoft.Matrix(M11=-1, M12=0, M21=0, M22=-1, DX=0, DY=0, SizingMethod='auto expand');
}

#moveleft {
  -webkit-transform: rotate(180deg);     /* Chrome and other webkit browsers */
  -moz-transform: rotate(180deg);        /* FF */
  -o-transform: rotate(180deg);          /* Opera */
  -ms-transform: rotate(180deg);         /* IE9 */
  transform: rotate(180deg);             /* W3C compliant browsers */

  /* IE8 and below */
  filter: progid:DXImageTransform.Microsoft.Matrix(M11=-1, M12=0, M21=0, M22=-1, DX=0, DY=0, SizingMethod='auto expand');
} 
</style>
</head>
<body>
<div data-role="page">
  <div data-role="main" class="ui-content">
    <form>
        <label for="switch">Start RoboCar</label>
        <img id="play" height="42" width="42" src='http://icons.iconarchive.com/icons/icons-land/vista-multimedia/256/Play-1-Hot-icon.png' />
        <img id="pause" height="42" width="42" src='https://www.chezyangco.fr/images/pause.png' />

        <br/>
        <img id="moveleft" height="42" width="42" src='http://s1.iconbird.com/ico/2014/1/598/w256h2561390846449right256.png' />
        <img id="moveright" height="42" width="42"  src='http://s1.iconbird.com/ico/2014/1/598/w256h2561390846449right256.png' />
        <img id="moveback" height="42" width="42"  src='http://s1.iconbird.com/ico/2014/1/598/w256h2561390846449right256.png' />
        
    </form>
 </div>
</div>
</body>
</html>
        '''


@route('/remote/play')
def play():
        GPIO.output(17, True)
        GPIO.output(18, False)    
        GPIO.output(22, True)
        GPIO.output(23, False)
        return 'Starting'


@route('/remote/pause')
def pause():
        GPIO.output(17, False)
        GPIO.output(18, False)
        GPIO.output(22, False)
        GPIO.output(23, False)
        return 'Stopping'


@route('/remote/left')
def left():
        GPIO.output(22, False)
        GPIO.output(23, False)

        GPIO.output(17, True)
        GPIO.output(18, False)
        time.sleep(1)
        GPIO.output(22, True)
        GPIO.output(23, False)
        return 'moving left..'

@route('/remote/right')
def right():
        GPIO.output(17, False)
        GPIO.output(18, False)

        GPIO.output(22, True)
        GPIO.output(23, False)
        time.sleep(1)
        GPIO.output(17, True)
        GPIO.output(18, False)
        return 'moving right'


@route('/remote/back')
def back():
        GPIO.output(17, False)
        GPIO.output(18, True)
        GPIO.output(22, Flase)
        GPIO.output(23, True)
        time.sleep(1)
        left()
        return 'reverse'


try:
    run(host = IP_ADDRESS, port= PORT)
except(KeyboardInterrupt):
    # If a keyboard interrupt is detected then it exits cleanly!
    print('Finishing up!')
    GPIO.output(17, False)
    GPIO.output(18, False)
    GPIO.output(22, False)
    GPIO.output(23, False)
    quit()

