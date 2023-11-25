import cv2
import numpy as np
import pyautogui
import time
import cv2
import numpy as np
import pyautogui
import time
import pygetwindow as gw
import pyautogui

interval_between_clicks= 1.5
IMAGE_PATH = "images"

def find_and_click_image_on_screen(template_path, click_all_instances=False, post_click_delay=1.0, exclusion_margin=5):
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    threshold = 0.8
    found = False

    while True:
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if max_val < threshold:
            break

        center_x, center_y = max_loc[0] + w//2, max_loc[1] + h//2
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        found = True
        time.sleep(interval_between_clicks)

        # Exclude the area around the detected button
        x_start = max(max_loc[0] - exclusion_margin, 0)
        y_start = max(max_loc[1] - exclusion_margin, 0)
        x_end = min(max_loc[0] + w + exclusion_margin, screen_gray.shape[1])
        y_end = min(max_loc[1] + h + exclusion_margin, screen_gray.shape[0])
        screen_gray[y_start:y_end, x_start:x_end] = 0

        if not click_all_instances:
            break

        time.sleep(post_click_delay)

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
            found_image_icon(idle_chest_icon)
            found_image_icon(obtain_bonus_icon)
            found_image_icon(ok_main_button_icon)

            if found_image_icon(free_button_icon):
                found_image_icon(ok_after_free_button_icon)
                found_image_icon(ok_main_button_icon)

            if found_image_icon(blessings_icon):
                found_image_icon(receive_blessing, click_all_instances=True)
                found_image_icon(close_blessing_button)

            time.sleep(interval_monitoring)
    except KeyboardInterrupt:
        print("Monitoring stopped.")

def image_path(filename):
    return f"{IMAGE_PATH}/{filename}"


time.sleep(2.0)

idle_chest_icon = image_path("idle_chest.png")
obtain_bonus_icon = image_path("obtain_bonus.png")
free_button_icon = image_path("free_button.png")
ok_main_button_icon = image_path("ok_main_button.png")
ok_after_free_button_icon = image_path("ok_after_free_button.png")
blessings_icon = image_path("blessings.png")
receive_blessing = image_path("receive_blessing.png")
close_blessing_button = image_path("close_blessing_button.png")

monitor_screen_for_images(interval_monitoring=10.0)