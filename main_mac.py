import pygetwindow as gw
import pyautogui
import time
import math
import json

def get_active_window_title():
    active_window = gw.getActiveWindow()
    if active_window is not None:
        return active_window
    else:
        return None

daylog = {
    "workStart": time.time(),
    "workEnd": 0,
    "userAgent": "mac",
    "workApplications": []
}

def get_window_info(window_title):
    if window_title:
        try:
            parts = window_title.split(" – ")
            return parts[-1], parts[-2]
        except:
            return window_title, window_title
    return None, None

def log_application_switch(current_window_name, total_mouse, inactive_times, min_pixel, max_pixel):
    application_start_time = time.time()
    try:
        daylog["workApplications"][-1].update({
            "applicationEnd": application_start_time,
            "totalPixelMoved": total_mouse,
            "totalKeysPressed": 0,
            "inactiveTime": inactive_times,
            "maxAcceptedInactivity": 300,
            "maxWindowSize": [max_pixel[0], max_pixel[1]],
            "minWindowSize": [min_pixel[0], min_pixel[1]],
            "mouseActivity": []
        })
    except IndexError:
        print("first row")

    daylog["workApplications"].append({
        "applicationStart": application_start_time,
        "applicationEnd": 0,
        "applicationName": current_window_name,
    })

def main(run_duration):
    start_time = time.time()
    inactive_time = 0
    total_inactive_time = 0
    total_mouse_moved = 0
    last_window_title = get_active_window_title()
    max_win_size = [0, 0]
    min_win_size = [10000, 100000]

    while time.time() - start_time < run_duration:
        last_mouse_position = pyautogui.position()
        time.sleep(1)
        current_mouse_position = pyautogui.position()

        _, _, length, height = gw.getWindowGeometry(gw.getActiveWindow())

        if (max_win_size[0]*max_win_size[1]) < (length*height):
            max_win_size = [length, height]

        if (min_win_size[0]*min_win_size[1]) > (length*height):
            min_win_size = [length, height]

        if last_mouse_position == current_mouse_position:
            inactive_time += 1
            if inactive_time >= 10:
                total_inactive_time += 1
        else:
            x1, y1 = current_mouse_position
            x2, y2 = last_mouse_position
            distance_moved = math.sqrt(((x1 - x2)**2)+((y1 - y2)**2))
            total_mouse_moved += distance_moved
            inactive_time = 0

        current_window_title = get_active_window_title()

        if last_window_title != current_window_title and current_window_title is not None:
            log_application_switch(current_window_title, total_mouse_moved, total_inactive_time, min_win_size, max_win_size)
            last_window_title = current_window_title
            total_inactive_time = 0
            total_mouse_moved = 0
            inactive_time = 0
            max_win_size = [0, 0]
            min_win_size = [10000, 100000]

    daylog["workEnd"] = time.time()
    log_application_switch(current_window_title, total_mouse_moved, total_inactive_time, min_win_size, max_win_size)

    # Save daylog to a JSON file
    with open("daylog.json", "w") as f:
        json.dump(daylog, f)

if __name__ == "__main__":
    duration = int(input("Enter the duration (in seconds) for which you want to run the program: "))
    print("Program started.")
    main(duration)
    print("Program finished. daylog saved to 'daylog.json'.")
