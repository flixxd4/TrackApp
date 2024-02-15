import pygetwindow as gw
import pyautogui
import time

def get_active_window_title():
    active_window = gw.getActiveWindow()
    if active_window is not None:
        return active_window.title
    else:
        return None


daylog = {
    "workStart": time.time(),
    "workEnd": 0,
    "workApplications": []
}
last_mouse_position = pyautogui.position()
inactive_time = 0

def is_mouse_active():
    global inactive_time
    global last_mouse_position
    current_mouse_position = pyautogui.position()
    if current_mouse_position != last_mouse_position:
        last_mouse_position = current_mouse_position
        inactive_time = 0
    else:
        inactive_time += 1
        if inactive_time >= 300:  # 5 minutes (300 seconds)
            return False
    time.sleep(1)  # Check every second
    return True

def get_window_info(window_title):
    # Extract application name and information from the window title
    if window_title:
        parts = window_title.split(" – ")
        if len(parts) >= 2:
            return parts[-1], parts[-2]
    return None, None

def log_application_switch(current_window_name, current_window_info):
    # Log application switch and its information
    application_start_time = time.time()
    try:
        daylog["workApplications"][-1]["applicationEnd"] = application_start_time
    except:
        print("first row")

    daylog["workApplications"].append({
        "applicationStart": application_start_time,
        "applicationEnd": 0,
        "applicationName": current_window_name,
        "applicationInfos": [{
            "infoStart": application_start_time,
            "infoEnd": 0,
            "applicationInfoName": current_window_info
        }]
    })

def log_application_info(current_window_info):
    # Log additional information for the current application
    application_info_start_time = time.time()

    daylog["workApplications"][-1]["applicationInfos"][-1]["infoEnd"] = application_info_start_time

    daylog["workApplications"][-1]["applicationInfos"].append({
        "infoStart": application_info_start_time,
        "infoEnd": 0,
        "applicationInfoName": current_window_info
    })
    print(daylog)

def main():
    last_window_title = get_active_window_title()

    while True:
        current_window_title = get_active_window_title()

        if last_window_title != current_window_title and current_window_title is not None:
            last_window_name, last_window_info = get_window_info(last_window_title)
            current_window_name, current_window_info = get_window_info(current_window_title)

            if last_window_name != current_window_name:
                log_application_switch(current_window_name, current_window_info)
            else:
                log_application_info(current_window_info)

            last_window_title = current_window_title

if __name__ == "__main__":
    main()
