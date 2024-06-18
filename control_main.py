import qrcode
import random
import string
import os
import smtplib
from email import encoders
from email.utils import formataddr
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import subprocess

def generate_unique_string():
   
    rand_num = ''.join(random.choices(string.digits, k=15))
    random_alphabet = random.choice(string.ascii_uppercase)
    return random_alphabet + rand_num

def create_qr_code():
   
    qr_string = generate_unique_string()
    print("생성된 QR 코드 문자열:", qr_string)

    img = qrcode.make(qr_string)
    image_path = 'QRimage.png'
    img.save(image_path)

    return qr_string, image_path

def send_email(address, attachment_path, qr_string):
    from_addr = formataddr(('QR코드 발신', 'manhyun7355@gmail.com'))
    to_addr = formataddr(('QR코드 수신', address))

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.set_debuglevel(True)
    session.ehlo()
    session.starttls()
    session.login('manhyun7355@gmail.com', 'nvnx eexs kkfg wbej')

    message = MIMEMultipart("mixed")
    message.set_charset('utf-8')
    message['From'] = from_addr
    message['To'] = to_addr
    message['Subject'] = '[QR code] 출입을 위한 QR코드입니다.'

    body = f'''
    <h4>첨부된 QR코드를 카메라에 인식시켜 주십시오.</h4>
    <p>QR 코드 내용: {qr_string}</p>
    '''
    bodyPart = MIMEText(body, 'html', 'utf-8')
    message.attach(bodyPart)

    attach_binary = MIMEBase("application", "octet-stream")
    binary = open(attachment_path, "rb").read()
    attach_binary.set_payload(binary)
    encoders.encode_base64(attach_binary)
    filename = os.path.basename(attachment_path)
    attach_binary.add_header("Content-Disposition", 'attachment', filename=('utf-8', '', filename))
    message.attach(attach_binary)

    session.sendmail(from_addr, to_addr, message.as_string())
    session.quit()

def read_qr_code(expected_qr_string):
   
    camera = PiCamera()
    camera.resolution = (640, 480)
    raw_capture = PiRGBArray(camera, size=(640, 480))

    
    time.sleep(0.1)

    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        qr_decoder = cv2.QRCodeDetector()

        data, bbox, _ = qr_decoder.detectAndDecode(image)
        
        if data:
            print("QR 코드가 감지되었습니다:", data)
            if data == expected_qr_string:
                print("맞습니다")
                
                subprocess.run(['sudo', 'python', 'mt_1.py'])
            else:
                print("QR 코드가 일치하지 않습니다.")
               
                subprocess.run(['sudo', 'python', 'led.py'])

        
        raw_capture.truncate(0)

        if data:
            break  

    camera.close()


qr_string, qr_image_path = create_qr_code()


recipient_email = 'manhyun7355@gmail.com'
send_email(recipient_email, qr_image_path, qr_string)


read_qr_code(qr_string)
