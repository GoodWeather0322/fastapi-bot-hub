import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment
import secrets
import io
import azure.cognitiveservices.speech as speechsdk
import time
import string
import os

from app.utils.logging_config import logging

logger = logging.getLogger(__name__)


async def update_query_session(session):
    response_queryTime = session.get(
        "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip119/queryTime"
    )
    response_nonPicture = session.get(
        "https://www.railway.gov.tw/tra-tip-web/tip/player/nonPicture"
    )

    return response_queryTime, response_nonPicture


async def get_csrf_token(response_queryTime):
    soup = BeautifulSoup(response_queryTime.content, "html.parser")
    csrf_input = soup.find("form").find("input", {"name": "_csrf"})
    csrf_token = csrf_input.get("value")
    return csrf_token


async def get_captcha_audio(session):

    random_value = secrets.randbits(32)
    change_code_url = f"https://www.railway.gov.tw/tra-tip-web/tip/player/changeVoiceVerifyCode?pageRandom={random_value}"
    response = session.get(change_code_url)

    # 下載音頻
    random_value = secrets.randbits(32)
    audio_url = f"https://www.railway.gov.tw/tra-tip-web/tip/player/audio?pageRandom={random_value}"
    response = session.get(audio_url)

    audio = AudioSegment.from_mp3(io.BytesIO(response.content))

    start_time = 15500
    end_time = 32500
    audio_slice = audio[start_time:end_time]

    output_wav_path = f"captcha_audio_slice_{random_value}.wav"

    audio_slice.export(output_wav_path, format="wav")
    logger.info(f"已轉換: {output_wav_path}")

    return output_wav_path


async def speech_recognize_continuous_from_file(file_path):

    result_text = []

    def result_callback(event_type: str, evt: speechsdk.SpeechRecognitionEventArgs):
        """callback to display a translation result"""
        nonlocal result_text
        if event_type == "RECOGNIZING":
            pass
        elif event_type == "RECOGNIZED":
            result_text.append(evt.result.text)

    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(
        subscription="f9d5f7f373ab494b8a707016cdf994d7", region="eastasia"
    )
    speech_config.speech_recognition_language = "zh-TW"
    audio_config = speechsdk.audio.AudioConfig(filename=file_path)

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    done = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        logger.info("CLOSING on {}".format(evt))
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(
        lambda evt: result_callback("RECOGNIZING", evt)
    )
    speech_recognizer.recognized.connect(lambda evt: result_callback("RECOGNIZED", evt))
    # speech_recognizer.session_started.connect(lambda evt: logger.info('SESSION STARTED: {}'.format(evt)))
    # speech_recognizer.session_stopped.connect(lambda evt: logger.info('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(
        lambda evt: logger.info("CANCELED {}".format(evt))
    )
    # Stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    result_future = speech_recognizer.start_continuous_recognition_async()
    result_future.get()
    while not done:
        time.sleep(0.5)

    speech_recognizer.stop_continuous_recognition_async()

    return result_text


async def remove_punctuation(text):
    # 英文標點
    text = text.translate(str.maketrans("", "", string.punctuation))

    # 中文標點
    chinese_punc = '，。！？【】（）《》""' "；：、"
    text = text.translate(str.maketrans("", "", chinese_punc))

    # 去除多餘空格
    text = "".join(text.split())

    return text


async def get_captcha_code(output_wav_path):
    result_text = await speech_recognize_continuous_from_file(output_wav_path)
    result_text = " ".join(result_text)
    result_text = await remove_punctuation(result_text)
    if "現在" in result_text:
        result_text = result_text.split("現在")[0]
    else:
        logger.info(result_text)
        raise Exception("無法從音頻中識別出現在")

    if len(result_text) != 6:
        logger.info(result_text)
        raise Exception("驗證碼辨識，長度不正確")

    num_map = {
        "零": "0",
        "一": "1",
        "二": "2",
        "三": "3",
        "四": "4",
        "五": "5",
        "六": "6",
        "七": "7",
        "八": "8",
        "九": "9",
    }

    for word, num in num_map.items():
        result_text = result_text.replace(word, num)

    result_text = result_text.lower()
    logger.info(result_text)

    return result_text


async def analyze_query_table(content):
    result_query_time = []
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table", {"class": "itinerary-controls"})

    if table:
        logger.info("找到表格：")
        trips = table.find_all(class_="trip-column")
        if trips:
            logger.info("車次資訊：")
            for trip in trips:
                # 取得基本資訊（直接從 td 元素）
                tds = trip.find_all("td")

                # 取得車種車次（從 a 元素）
                train_info = trip.find("a", {"class": "links"})

                # 取得票價
                price = trip.find("span").text.strip() if trip.find("span") else "N/A"

                ticket_status_class_names = (
                    tds[6].find("div", {"class": "icon-fa"}).get("class")
                )
                if (
                    "times" in ticket_status_class_names
                    and "red" in ticket_status_class_names
                ):
                    ticket_status = "沒票"
                elif (
                    "exclamation-triangle" in ticket_status_class_names
                    and "color-red" in ticket_status_class_names
                ):
                    ticket_status = "有票 < 30"
                elif (
                    "green" in ticket_status_class_names
                    and "check-circle" in ticket_status_class_names
                ):
                    ticket_status = "有票 > 30"
                else:
                    ticket_status = "未知"

                # 整理資訊
                train_data = {
                    "出發時間": tds[0].text.strip(),
                    "抵達時間": tds[1].text.strip(),
                    "旅程時間": tds[2].text.strip(),
                    "車種車次": train_info.text.strip() if train_info else "N/A",
                    "經由": tds[4].text.strip(),
                    "餘票狀態": ticket_status,
                    "全票票價": tds[7].find("span").text.strip(),
                    "優待票價": tds[8].find("span").text.strip(),
                }
                result_query_time.append(train_data)
            return result_query_time
        else:
            raise Exception("找不到車次資訊")
    else:
        raise Exception("找不到指定的表格")


async def get_query_time(session, form_data):
    search_url = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip119/search"

    response = session.post(
        search_url,
        data=form_data,
    )
    # 檢查響應
    if response.status_code == 200:
        logger.info("請求成功")
        return await analyze_query_table(response.content)
    else:
        raise Exception(f"請求失敗: {response.status_code}")


async def query_time():
    session = requests.Session()
    response_queryTime, response_nonPicture = await update_query_session(session)
    csrf_token = await get_csrf_token(response_queryTime)

    for retry_time in range(5):
        logger.info(f"第 {retry_time + 1} 次嘗試")
        try:
            output_wav_path = await get_captcha_audio(session)
            captcha_code = await get_captcha_code(output_wav_path)

            form_data = {
                "_csrf": csrf_token,  # 從之前的請求中獲取
                "rideDate": "2024/11/23",
                "startStation": "1020-板橋",
                "endStation": "3300-臺中",
                "startOrEndTime": "true",
                "startTime": "08:00",
                "endTime": "12:00",
                "g-recaptcha-response": None,  # 這個需要從實際的 reCAPTCHA 響應中獲取
                "hiddenRecaptcha": "",
                "verifyType": "voice",
                "verifyCode": captcha_code,
            }
            result_query_time = await get_query_time(session, form_data)
            os.remove(output_wav_path)
            return result_query_time
        except Exception as e:
            logger.info(f"嘗試queryTime失敗: {e}")
            os.remove(output_wav_path)
            continue
    else:
        logger.info("嘗試queryTime失敗")
        return None
