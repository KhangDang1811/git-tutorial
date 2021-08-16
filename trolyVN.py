import os
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch

language = 'vi'
path = ChromeDriverManager().install()
wikipedia.set_lang('vi')

def speak(text):
    print("Bot: {}".format(text))
    #truyen vao text de doc len
    tts = gTTS(text=text, lang=language, slow = False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", False)
    os.remove("sound.mp3")


def get_voice():
     r = sr.Recognizer()
     with sr.Microphone() as source:
        print("Me: ", end = '')
        audio = r.listen(source, phrase_time_limit=5)
        time.sleep(3)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text
        except:
            print("...")
            time.sleep(3)
            return 0
        
def stop():
    speak("Hẹn gặp lại bạn nhé!")
    
    
def get_text():
    for i in range(3):
        text = get_voice()
        if text:
            return text.lower()
        elif i < 2:
            speak("Nói lớn lên để người ta còn nghe nữa, nói gì nói lại coi")
    time.sleep(10)
    stop()
    return 0

def talk(name):
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng {}. Chúc bạn ngày mới tốt lành!".format(name))
    elif day_time < 18:
        speak("Chào buổi chiều {}!".format(name))
    else:
        speak("Chào buổi tối {}!".format(name))
    time.sleep(5)
    speak("Bạn có khỏe không ?")
    time.sleep(3)
    ans = get_voice()
    if ans:
        if "có" in ans or "yes" in ans:
            speak("Thật là tốt!")
        else:
            speak("Vậy à, bạn nên tập thể dục đi!")
            
def open_website(text):
    regex = re.search ('mở (.+)', text)
    if regex:
        domain = regex.group(1)
        url = 'https://www.' + domain
        webbrowser.open(url)
        speak("Trang web của bạn đã được mở lên!")
        return True
    else:
        return False
    
    
def google_search(text):
    search_for = text.split("kiếm", 1)[1]
    speak("Oke la")
    driver = webdriver.Chrome(path)
    driver.get("http://www.google.com")
    query = driver.find_element_by_xpath("//input[@name='q']")
    query.send_keys(str(search_for))
    query.send_keys(Keys.RETURN)

def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak("Bây giờ là %d giờ %d phút" % (now.hour, now.minute))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d " % (now.day, now.month, now.year))
    else:
        speak("Bot không hiểu")
    


def play_youtube():
    speak("Xin mời bạn chọn bài hát")
    time.sleep(4)
    my_song = get_text()
    while True:
        result = YoutubeSearch(my_song, max_results = 10).to_dict()
        if result:
            break;
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    webbrowser.open(url)
    speak("Bài hát của bạn đã được mở, hãy thưởng thức nó!")
    
    
    
def weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ!")
    time.sleep(3)
    url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temp = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        sun_time  = data["sys"]
        sun_rise = datetime.datetime.fromtimestamp(sun_time["sunrise"])
        sun_set = datetime.datetime.fromtimestamp(sun_time["sunset"])
        wther = data["weather"]
        weather_des = wther[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day, month = now.month, year= now.year, hourrise = sun_rise.hour, minrise = sun_rise.minute,
                                                                           hourset = sun_set.hour, minset = sun_set.minute, 
                                                                           temp = current_temp, pressure = current_pressure, humidity = current_humidity)
        speak(content)
        time.sleep(25)
    else:
        speak("Không tìm thấy thành phố!")

def tell_me():
    try:
        speak("Bạn muốn nghe về gì ạ!")
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        time.sleep(30)
        for content in contents[1:]:
            speak("Bạn muốn nghe tiếp hay không ?")
            ans = get_text()
            if "không" in ans or "thôi" in ans or"im" in ans:
                break
            speak(content)
            time.sleep(30)
            
        speak("Cảm ơn bạn đã lắng nghe!")
    except:
        speak("Sen không định nghĩa được ngôn ngữ của bạn!")
        
def help():
    speak("""Tôi có thể làm những việc sau:
    1. Chào hỏi
    2. Hiển thị giờ
    3. Mở website, application
    4. Tìm kiếm trên Google
    5. Dự báo thời tiết
    6. Mở video nhạc
    7. Thay đổi hình nền máy tính
    8. Đọc báo hôm nay
    9. Tìm định nghĩa """)
    time.sleep(20)

def call_sen():
    speak("Xin chào, bạn tên là gì nhỉ?")
    time.sleep(1)
    name = get_text()
    if name:
        speak("Chào bạn {}".format(name))
        time.sleep(2)
        speak("Bạn cần Sen giúp gì ạ!")
        time.sleep(3)
        while True:
            text = get_text()
            if not text:
                break
            elif "trò chuyện" in text or "nói chuyện" in text:
                talk(name)
            elif "dừng" in text or "thôi" in text or "stop" in text or "bye bye " in text or"im đi" in text or "nói nhiều" in text:
                stop()
                break
            elif "Google" in text:
                if "mở google và tìm kiếm" in text:
                    google_search(text)
                elif "." in text:
                    open_website(text)
                else:
                    open_application(text)       
            elif "ngày" in text  or "giờ" in text:
                get_time(text)
                time.sleep(5)
            elif "mở nhạc" in text or "mở youtube" in text or "youtube" in text or "đổi nhạc" in text:
                play_youtube()
                time.sleep(60)
            elif "thời tiết" in text or "nhiệt độ" in text:
                weather()
                time.sleep(5)
            elif "định nghĩa" in text or "đọc" in text:
                tell_me()
                time.sleep(5)
            elif "có thể làm gì" in text or "Sen có thể" in text:
                help()

call_sen()            