import cv2
import numpy as np
import pyautogui
import time

import cv2
import numpy as np
import pyautogui
import time

interval_between_clicks= 5.0

def find_and_click_image_on_screen(template_path, click_all_instances=False, post_click_delay=1.0):
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    found = False
    for pt in zip(*loc[::-1]):
        center_x, center_y = pt[0] + w//2, pt[1] + h//2
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        found = True
        time.sleep(interval_between_clicks)

        if click_all_instances:
            time.sleep(post_click_delay)  # Wait after each click
        else:
            break

    return found

def found_image_icon(image_icon, click_all_instances=False):
    found_image = find_and_click_image_on_screen(image_icon, click_all_instances=click_all_instances)
    if found_image:
        print(f"Found {image_icon} and clicked.")
        time.sleep(interval_between_clicks)
    
    return found_image

def monitor_screen_for_images(interval_monitoring=5.0):
    try:
        while True:
            found_idle_chest = find_and_click_image_on_screen(idle_chest_icon)
            if found_idle_chest:
                print("Found idle chest icon and clicked.")
                time.sleep(interval_between_clicks)

            found_obtain_bonus_icon = find_and_click_image_on_screen(obtain_bonus_icon)
            if found_obtain_bonus_icon:
                print("Found obtain bonus icon and clicked.")
                time.sleep(interval_between_clicks)
            else:
                found_ok_main_button_icon = find_and_click_image_on_screen(ok_main_button_icon)
                if found_ok_main_button_icon:
                    print("Found ok main button icon and clicked.")
                    time.sleep(interval_between_clicks)
            
            found_free_button_icon = find_and_click_image_on_screen(free_button_icon)
            if found_free_button_icon:
                print("Found free button icon and clicked.")
                time.sleep(interval_between_clicks)
                found_ok_after_free_button_icon = find_and_click_image_on_screen(ok_after_free_button_icon)
                if found_ok_after_free_button_icon:
                    print("Found ok after free button icon and clicked.")
                    time.sleep(interval_between_clicks)
                    found_ok_main_button_icon = find_and_click_image_on_screen(ok_main_button_icon)
                    if found_ok_main_button_icon:
                        print("Found ok main button icon and clicked.")
                        time.sleep(interval_between_clicks)

            found_blessings_icon = find_and_click_image_on_screen(blessings_icon)
            if found_blessings_icon:
                print("Found blessings icon and clicked.")
                time.sleep(interval_between_clicks)
                found_receive_blessing_icon = find_and_click_image_on_screen(receive_blessing, click_all_instances=True)
                if found_receive_blessing_icon:
                    print("Found receive blessing icon and clicked.")
                    time.sleep(interval_between_clicks)
                found_close_blessing_button = find_and_click_image_on_screen(close_blessing_button)
                if found_close_blessing_button:
                    print("Found close blessing button and clicked.")
                    time.sleep(interval_between_clicks)



            time.sleep(interval_monitoring)
    except KeyboardInterrupt:
        print("Monitoring stopped.")

idle_chest_icon = "images/idle_chest.png"
obtain_bonus_icon = "images/obtain_bonus.png"
free_button_icon = "images/free_button.png"
ok_main_button_icon = "images/ok_main_button.png"
ok_after_free_button_icon = "images/ok_after_free_button.png"
blessings_icon = "images/blessings.png"
receive_blessing = "images/receive_blessing.png"
close_blessing_button = "images/close_blessing_button.png"


time.sleep(2.0)

monitor_screen_for_images(interval_monitoring=10.0)