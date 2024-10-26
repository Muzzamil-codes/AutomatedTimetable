import pygetwindow as gw
from time import sleep
from datetime import datetime
from plyer import notification
import webbrowser
import subprocess
import pyautogui
import logging
from TimeTableBuilder import my_timetable

logging.basicConfig(filename="log.log",level=logging.INFO)

def lecture_link():
    #chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    webbrowser.open(r"https://www.pw.live/study/batches/649fe28b394101001896bb9a/batch-overview?came_from=study&activeSection=All%20classes")


def close_all_windows():
    # Get a list of all open windows
    windows = gw.getAllTitles()

    # Close each window
    for window_title in windows:
        execution_time = datetime.now().strftime('%H:%M:%S')
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            window.close()
            logging.info(f"[{execution_time}]Closing the window: {window}")
        except Exception as e:
            print(f"Failed to close window {window_title}: {e}")
            logging.error(f"[{execution_time}]Failed to close window {window_title}: {e}")


def open_gimp():
    execution_time = datetime.now().strftime('%H:%M:%S')
    try:
        subprocess.Popen([r"C:\Program Files\GIMP 2\bin\gimp-2.10.exe"], shell=True)
        print(f"Opened Gimp")
        logging.info(f"[{execution_time}]Successfully started the program: GIMP")
    except Exception as e:
        print(f"Failed to open gimp: {e}")
        logging.error(f"[{execution_time}]Failed ot start the program: GIMP")


def open_opera(value):
    execution_time = datetime.now().strftime('%H:%M:%S')
    if value:
        webbrowser.open(r"https://app.flocus.com/?utm_medium=organic&utm_source=swm&utm_campaign=notion_landing")
        sleep(3)
        pyautogui.press('f11')
        logging.info(f"[{execution_time}]Succesfully started the program: Promodoro")
    else:
        try:
            subprocess.Popen([r"C:\Users\mdmuz\AppData\Local\Programs\Opera GX\launcher.exe"], shell=True)
            logging.info(f"[{execution_time}]Sucessfully started the program: Opera")
        except Exception as e:
            print(f"Failed to open opera: {e}")
            logging.error(f"[{execution_time}]Failed to start the program: Opera")


my_timetable = my_timetable()

def send_notification(message):
    notification.notify(
        title='Event Notification',
        message=message,
        app_name='Timetable Reminder',
        timeout=10
    )

def check_timetable(timetable):
    for time in timetable:
        print('inside the loop')
        current_time = datetime.now().strftime('%H:%M')
        time1 = datetime.strptime(time[:5], '%H:%M')
        time2 = datetime.strptime(time[6:], '%H:%M')
        current_time = datetime.strptime(current_time, '%H:%M')
        print(f'{current_time} and {time}')
        if time1 <= current_time <= time2:
            print("inside if statement")
            event = timetable[time]
            send_notification(f"It's time for {event}!")
            if event == 'lecture time':
                close_all_windows()
                sleep(1.5)
                lecture_link()
            elif event == 'Side work':
                close_all_windows()
                sleep(0.5)
                open_gimp()
                open_opera(False)
            elif event == 'Revission':
                close_all_windows()
                sleep(0.5)
                open_opera(True)
            print(f"{current_time}; {time2}")
            while True:
                time2 = datetime.strptime(time[6:], '%H:%M')
                current_time = datetime.now().strftime('%H:%M')
                current_time = datetime.strptime(current_time, '%H:%M')
                if current_time > time2:
                    execution_time = datetime.now().strftime('%H:%M:%S')
                    logging.info(f"[execution_time]Time over, moving to next time slot.")
                    print("next slot")
                    break
                else:
                    sleep(1)
                    print(f"waiting for {time2}")
                    print(f"{current_time}; {time2}")
                    pass

if __name__ == '__main__':
    check_timetable(my_timetable)