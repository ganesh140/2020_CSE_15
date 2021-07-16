from google.cloud import vision
import os
import cv2


def reduce_storeage(image):
    try:
        temp=10
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials.json"
        client = vision.ImageAnnotatorClient()
        success, encoded_image = cv2.imencode('.jpg', image)
        img = encoded_image.tobytes()
        img = vision.Image(content=img)
        response = client.text_detection(image=img)
        texts = response.text_annotations[0].description.split("\n")
        print(texts)
        cv2.imwrite("unreduced.jpeg",image)
        while temp<100:
            image=cv2.imread("unreduced.jpeg")
            cv2.imwrite("reduced.jpeg",image,[int(cv2.IMWRITE_JPEG_QUALITY), temp])
            img=cv2.imread("reduced.jpeg")
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials.json"
            client = vision.ImageAnnotatorClient()
            success, encoded_image = cv2.imencode('.jpg', img)
            img = encoded_image.tobytes()
            img = vision.Image(content=img)
            response = client.text_detection(image=img)
            texts1 = response.text_annotations[0].description.split("\n")
            print(texts1)
            count=0
            for i in texts1:
                if i in texts:
                    print(i)
                    count+=1
            if(count/len(texts)>0.9):
                print(temp)
                break
            temp+=10
        return True
    except:
        return False