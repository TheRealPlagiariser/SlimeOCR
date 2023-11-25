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
WINDOW_TITLE = "Legend of Slime"

def capture_window():
    try:
        window = gw.getWindowsWithTitle(WINDOW_TITLE)[0]
        if window:
            window.activate()  # Optional: Bring the window to the front
            return window
        else:
            print(f"Window titled '{WINDOW_TITLE}' not found.")
            return None
    except IndexError:
        print(f"No window titled '{WINDOW_TITLE}' found.")
        return None

def find_and_click_image_on_screen(template_path, click_all_instances=False, post_click_delay=1.0, exclusion_margin=5):
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    window = capture_window()
    if not window:
        return False

    x, y, width, height = window.left, window.top, window.width, window.height
    screen = pyautogui.screenshot(region=(x, y, width, height))
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    threshold = 0.8
    found = False

    while True:
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if max_val < threshold:
            break

        # Adjust the coordinates relative to the window
        center_x, center_y = max_loc[0] + w//2 + x, max_loc[1] + h//2 + y
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
            get_idle_chest()
            get_blessings()
            get_loot()

            time.sleep(interval_monitoring)
    except KeyboardInterrupt:
        print("Monitoring stopped.")

def get_idle_chest():
    if found_image_icon(idle_chest_icon):
        if found_image_icon(obtain_bonus_button):
            if found_image_icon(free_button_icon):
                found_image_icon(ok_after_free_button_icon)
        found_image_icon(ok_main_button_icon)

def get_blessings():
    if found_image_icon(blessings_icon):
        found_image_icon(receive_blessing, click_all_instances=True)
        found_image_icon(close_blessing_button)

def get_loot():
    if found_image_icon(building_icon):
        if found_image_icon(loot_button):
            if found_image_icon(receive_all_button):
                found_image_icon(tap_to_continue)
            if found_image_icon(production_boost_enabled):
                # missing add hours icon
                found_image_icon(close_production_boost_button)
            # missing production_boost_disabled icon
        if found_image_icon(loot_back_button):
            found_image_icon(building_close_button)
     

def image_path(filename):
    return f"{IMAGE_PATH}/{filename}"


time.sleep(2.0)

idle_chest_icon = image_path("idle_chest.png")
obtain_bonus_button = image_path("obtain_bonus_button.png")
free_button_icon = image_path("free_button.png")
ok_main_button_icon = image_path("ok_main_button.png")
ok_after_free_button_icon = image_path("ok_after_free_button.png")
blessings_icon = image_path("blessings.png")
receive_blessing = image_path("receive_blessing.png")
close_blessing_button = image_path("close_blessing_button.png")
building_icon = image_path("building.png")
loot_button = image_path("loot_button.png")
receive_all_button = image_path("receive_all_button.png")
tap_to_continue = image_path("tap_to_continue.png")
production_boost_enabled = image_path("production_boost_enabled.png")
close_production_boost_button = image_path("close_production_boost_button.png")
loot_back_button = image_path("loot_back_button.png")
building_close_button = image_path("building_close_button.png")


monitor_screen_for_images(interval_monitoring=10.0)