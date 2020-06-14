from PIL import ImageGrab, ImageOps, Image
import pyautogui
import time
import pytesseract
from googleapiclient.discovery import build

my_api_key = "enter you own key"
my_cse_id = "enter your own id"

def google_search(search_term, api_key, cse_id, **kwargs):
      service = build("customsearch", "v1", developerKey=api_key)
      res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
      return res['items']



def getGrid():
    #image = ImageGrab.grab()
    image = ImageGrab.grab(bbox=(650,200,1200,900))
    image.show()
    return image

def img_to_text(img):
    #text = pytesseract.image_to_string(img)
    txt = pytesseract.image_to_string(img, lang='tur')
    print(txt)
    return txt
    #print(pytesseract.image_to_string(Image.open('test2.jpg'), lang='tur'))


def getScore(grid):
    score = 0

    return score


def performMove(move):

    if move == UP:
        pyautogui.keyDown('up')
        time.sleep(0.05)
        pyautogui.keyUp('up')



def main():
    time.sleep(1)
    image = getGrid()
    text = img_to_text(image)
    print('type')
    print(type(text))
    time.sleep(0.1)

    results= google_search(text,my_api_key,my_cse_id,num=10)

    for result in results:
          print(result["link"])


if __name__ == '__main__':
    main()
