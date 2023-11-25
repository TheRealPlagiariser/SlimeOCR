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
import time
import logging
import gc
from mss import mss
import ctypes
import threading
import keyboard

interval_between_clicks= 0.5
IMAGE_PATH = "images"
WINDOW_TITLE = "Legend of Slime"

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%d-%m-%Y %H:%M:%S')

def listen_for_esc():
    keyboard.wait('esc')
    unblock_mouse_input()
    print("Mouse input unblocked! Press ESC again to exit.")
    keyboard.wait('esc')
    exit(0)  # Exit the script if ESC is pressed again

def block_mouse_input():
    ctypes.windll.user32.BlockInput(True)  # Block input

def unblock_mouse_input():
    ctypes.windll.user32.BlockInput(False)  # Unblock input

def capture_with_mss(x, y, width, height):
    with mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        return sct_img

def capture_window():
    try:
        window = gw.getWindowsWithTitle(WINDOW_TITLE)[0]
        if window:
            if window.isMinimized or window.left < 0 or window.top < 0:
                # Window is minimized or not in the expected position
                window.restore()  # Attempt to restore the window from a minimized state
                window.activate()  # Bring the window to the front
                logging.info("Window reactivated and restored.")

            logging.info(f"Window position: {window.left}, {window.top}, {window.width}, {window.height}")
            return window
        else:
            logging.warning(f"Window titled '{WINDOW_TITLE}' not found.")
            return None
    except IndexError:
        logging.error(f"No window titled '{WINDOW_TITLE}' found.")
        return None

def find_and_click_image_on_screen(template_path, click_all_instances=False, post_click_delay=1.0, exclusion_margin=5):
    try:
        block_mouse_input()
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        w, h = template.shape[::-1]

        window = capture_window()
        if not window:
            logging.error("Unable to capture the window.")
            return False

        x, y, width, height = window.left, window.top, window.width, window.height
        sct_img = capture_with_mss(x, y, width, height)
        screen = np.array(sct_img)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB) 
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        threshold = 0.82
        found = False

        while True:
            res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            logging.info(f"Template match value: {max_val}")
            if max_val < threshold:
                break

            # Adjust the coordinates relative to the window
            center_x, center_y = max_loc[0] + w//2 + x, max_loc[1] + h//2 + y
            pyautogui.moveTo(center_x, center_y, duration=0.5)  # Slow down mouse movement

            # Check if cursor is at the intended position
            if pyautogui.position() == (center_x, center_y):
                time.sleep(0.1)  # Short delay before click
                pyautogui.click()
                found = True
            else:
                logging.warning("Cursor not at the intended position. Click skipped.")

            time.sleep(interval_between_clicks)

            # Exclude the area around the detected button to avoid repeated clicks
            x_start = max(max_loc[0] - exclusion_margin, 0)
            y_start = max(max_loc[1] - exclusion_margin, 0)
            x_end = min(max_loc[0] + w + exclusion_margin, screen_gray.shape[1])
            y_end = min(max_loc[1] + h + exclusion_margin, screen_gray.shape[0])
            screen_gray[y_start:y_end, x_start:x_end] = 0

            if not click_all_instances:
                break

            time.sleep(post_click_delay)

    finally:
        unblock_mouse_input()

    return found

def found_image_icon(image_icon, click_all_instances=False):
    logging.info(f" Matching {image_icon}")
    found_image = find_and_click_image_on_screen(image_icon, click_all_instances=click_all_instances)
    if found_image:
        logging.info(f" Found {image_icon} and clicked.")
        time.sleep(interval_between_clicks)
    
    return found_image

def monitor_screen_for_images(interval_monitoring=5.0, loot_interval=3600):
    last_loot_time = 0 

    try:
        while True:
            close_defeat_screen()
            get_idle_chest()
            get_blessings()

            current_time = time.time()
            if current_time - last_loot_time > loot_interval:
                get_loot()
                last_loot_time = current_time

            time.sleep(interval_monitoring)
            gc.collect()

    except KeyboardInterrupt:
        logging.debug("Monitoring stopped.")

def close_defeat_screen():
    found_image_icon(close_defeat_button)

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
                if found_image_icon(ok_looting_level_up_button):
                    found_image_icon(close_looting_level_up_rewards_button)
            if found_image_icon(production_boost_enabled):
                found_image_icon(add_one_hour_button)
                found_image_icon(close_production_boost_button)
            # missing production_boost_disabled icon
        found_image_icon(loot_back_button)
        found_image_icon(loot_back_button)
        found_image_icon(building_close_button)
     

def image_path(filename):
    return f"{IMAGE_PATH}/{filename}"


time.sleep(5.0)

listener_thread = threading.Thread(target=listen_for_esc)
listener_thread.start()

idle_chest_icon = image_path("idle_chest.png")
obtain_bonus_button = image_path("obtain_bonus_button.png")
free_button_icon = image_path("free_button.png")
ok_main_button_icon = image_path("ok_main_button.png")
ok_after_free_button_icon = image_path("ok_after_free_button.png")
blessings_icon = image_path("blessings.png")
receive_blessing = image_path("receive_blessing.png")
close_blessing_button = image_path("close_blessing_button.png")
building_notification_icon = image_path("building_notification.png")
building_icon = image_path("building.png")
loot_button = image_path("loot_button.png")
receive_all_button = image_path("receive_all_button.png")
tap_to_continue = image_path("tap_to_continue.png")
production_boost_enabled = image_path("production_boost_enabled.png")
close_production_boost_button = image_path("close_production_boost_button.png")
loot_back_button = image_path("loot_back_button.png")
building_close_button = image_path("building_close_button.png")
add_one_hour_button = image_path("add_one_hour_button.png")
ok_looting_level_up_button = image_path("ok_looting_level_up_button.png")
close_looting_level_up_rewards_button = image_path("close_looting_level_up_rewards_button.png")
close_defeat_button = image_path("close_defeat_button.png")


monitor_screen_for_images(interval_monitoring=60.0)