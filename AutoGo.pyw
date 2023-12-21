import time
import math
import pyautogui
import keyboard
import tkinter as tk
import json
from tkinter import ttk

# File to store configuration
CONFIG_FILE = "config.json"

global_cursor_speed = 0.3  # Default cursor movement speed
VoidStoneNumber = 1
MapNumber = 1
VoidStoneSwap = False
delay_time = 1


DistanceBetweenSlots = 50 # mine is 50
RowsToClear = 6 # rows to clear
SpeedOfClear = 0 # mine is 0 and its still slow as f

# Positions with default values
default_config = {
        "global_cursor_speed": 0.3,
        "MapNumber": 1,
        "RowsToClear": 6,
        "OnlyVoidStone": False,
        "delay_time" :1,
        "hotkey_modifier": "",
        "hotkey_letter": "r",
        "positions_defaults": {
            "MapDeviceFromMapDevice": (989, 382),
            "MapStashFromMapDevice": (467, 623),
            "MapDeviceFromMapStash": (1321, 236),
            "FirstMapStashTabFromMapdevice": (542, 655),
            "ActivateMapDevice": (642, 859),
            "DumpTab": (692, 127),
            "RedVoidStone": (65, 729),
            "BlueVoidStone": (45, 710),
            "YellowVoidStone": (66, 692),
            "GreyVoidStone": (85, 710),
            "RedVoidStoneActive": (976, 927),
            "BlueVoidStoneActive": (959, 911),
            "YellowVoidStoneActive": (977, 893),
            "GreyVoidStoneActive": (995, 909),
            "PortalToGoFromStashTab": (1276, 425),
            "FirstItemInBagVeryMiddle": [1110, 602],  # VeryVey Middle
            "FirstItemInYourInventoryVeryMiddel": (1333, 600)  # VeryVey Middle
            }
}

# Function to load configuration from file
def load_config():
    global default_config
    try:
        with open(CONFIG_FILE, "r") as file:
            config_data = json.load(file)
        return config_data
    except (json.JSONDecodeError, FileNotFoundError):
        with open(CONFIG_FILE, "w") as file:
            json.dump(default_config, file, indent=2)
        
        return default_config

# Function to save configuration to file
def save_config(config_data):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_data, file)

# Load configuration at the beginning
config_data = load_config()

# Function to open the map
def open_map():
    pyautogui.press('g')

# Function to move and click
def move_and_click(x, y, duration=global_cursor_speed, right_click=False):
    pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)
    if right_click:
        pyautogui.rightClick()
    else:
        pyautogui.click()

# Function to put items in stash
def PutInStash(firstItemInYourInventoryVeryMiddel):
    move_and_click(*default_config["positions_defaults"]["DumpTab"])
    x = firstItemInYourInventoryVeryMiddel[0]
    y = firstItemInYourInventoryVeryMiddel[1]
    pyautogui.moveTo(x, y, duration=global_cursor_speed, tween=pyautogui.easeInOutQuad)
    pyautogui.keyDown("f2")
    for i in range(5):
        pyautogui.moveTo(x + (i * DistanceBetweenSlots), y, duration=global_cursor_speed/2, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(x + (i * DistanceBetweenSlots), y + (4 * DistanceBetweenSlots), duration=global_cursor_speed*1.5, tween=pyautogui.easeInOutQuad)
    pyautogui.keyUp("f2")

# function to put a map in mapdeivce
def PutMapInMapDevice():
    column = MapNumber%5
    row = math.floor(MapNumber/5)

    NewX = (row * DistanceBetweenSlots) + default_config["positions_defaults"]["FirstItemInBagVeryMiddle"][0]
    NewY = (column * DistanceBetweenSlots) + default_config["positions_defaults"]["FirstItemInBagVeryMiddle"][1]

    pyautogui.keyDown('ctrl')
    move_and_click(NewX,NewY)
    pyautogui.keyUp('ctrl')

# Function to calculate the voidstone number to put
def PutInTheVoidStone():
    VoidStone = math.ceil(MapNumber/4)

    pyautogui.keyDown('ctrl')

    if VoidStone == 1 or VoidStone == 3:
        move_and_click(*default_config["positions_defaults"]["RedVoidStone"])
        move_and_click(*default_config["positions_defaults"]["GreyVoidStone"])
    elif VoidStone == 2 or VoidStone == 4:
        move_and_click(*default_config["positions_defaults"]["YellowVoidStone"])
        move_and_click(*default_config["positions_defaults"]["BlueVoidStone"])

    pyautogui.keyUp('ctrl')

# Function to calculate the voidstone number to putout
def PutOutTheVoidStone():
    VoidStone = math.ceil(MapNumber/4)

    pyautogui.keyDown('ctrl')

    if VoidStone == 1 or VoidStone == 3:
        move_and_click(*default_config["positions_defaults"]["RedVoidStoneActive"])
        move_and_click(*default_config["positions_defaults"]["GreyVoidStoneActive"])
    elif VoidStone == 2 or VoidStone == 4:
        move_and_click(*default_config["positions_defaults"]["YellowVoidStoneActive"])
        move_and_click(*default_config["positions_defaults"]["BlueVoidStoneActive"])

    pyautogui.keyUp('ctrl')


# Function to to only swap void stones
def SwapVoidStones():
    global VoidStoneSwap
    pyautogui.keyDown('ctrl')
    if VoidStoneSwap:
        move_and_click(*default_config["positions_defaults"]["RedVoidStoneActive"])
        move_and_click(*default_config["positions_defaults"]["GreyVoidStoneActive"])
        VoidStoneSwap =  not VoidStoneSwap
    else:
        move_and_click(*default_config["positions_defaults"]["RedVoidStone"])
        move_and_click(*default_config["positions_defaults"]["GreyVoidStone"])
        VoidStoneSwap =  not VoidStoneSwap
    pyautogui.keyUp('ctrl')


# Function to run the map
def RunTheMap():
    global MapNumber,VoidStoneNumber,global_cursor_speed  # Declare MapNumber as a global variable
    OnlyVoidStone = only_void_stone_var.get()

    if OnlyVoidStone:
        SwapVoidStones()
    else:
        global delay_time
        delay_time = config_data["delay_time"]

        if MapNumber > 16:
            MapNumber = 1
            VoidStoneNumber = 1
        open_map()  # to open the map
        PutInTheVoidStone()  # click on the void stone
        open_map()  # to close the map
        if MapNumber == 1:
            move_and_click(*default_config["positions_defaults"]["MapDeviceFromMapStash"])
            time.sleep(delay_time)
        else:
            move_and_click(*default_config["positions_defaults"]["MapDeviceFromMapDevice"])  # open the map device
        PutMapInMapDevice()  # put a map in mapdevice
        move_and_click(*default_config["positions_defaults"]["ActivateMapDevice"])  # Click the activate btn
        if MapNumber == 1:
            move_and_click(*default_config["positions_defaults"]["FirstMapStashTabFromMapdevice"])
            time.sleep(delay_time)
        else:
            move_and_click(*default_config["positions_defaults"]["MapStashFromMapDevice"])  # open to stash tab
        time.sleep(delay_time)  # wait until you get to stash tab
        PutInStash(default_config["positions_defaults"]["FirstItemInYourInventoryVeryMiddel"])  # To empty your stash tab
        open_map()  # to open the map
        PutOutTheVoidStone()  # to put out the void stone
        open_map()  # to close the map
        move_and_click(*default_config["positions_defaults"]["PortalToGoFromStashTab"])

        MapNumber += 1  # Increment the global variable

        map_number_entry.delete(0, tk.END)
        map_number_entry.insert(0, str(MapNumber))

        update_map_number()



# Function to update MapNumber from the UI
def update_map_number():
    global MapNumber
    MapNumber = int(map_number_entry.get())
    config_data["MapNumber"] = MapNumber
    save_config(config_data)

# Function to update RowsToClear from the UI
def update_rows_to_clear():
    global RowsToClear
    RowsToClear = int(rows_to_clear_entry.get())
    config_data["RowsToClear"] = RowsToClear
    save_config(config_data)

# Function to update global_cursor_speed from the UI
def update_cursor_speed():
    global global_cursor_speed
    global_cursor_speed = float(cursor_speed_entry.get())
    config_data["global_cursor_speed"] = global_cursor_speed
    save_config(config_data)

# Function to update positions from the UI
def update_positions():
    for position_name, entry in positions_entries.items():
        config["positions_defaults"][position_name] = tuple(map(int, entry.get().split(',')))

    # Save the updated configuration to the file
    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)

# Function to update hotkey from the UI
def update_hotkey():
    keyboard.remove_all_hotkeys()
    hotkey_modifier = hotkey_modifier_entry.get()
    hotkey_letter = hotkey_entry.get()
    config_data["hotkey_modifier"] = hotkey_modifier
    config_data["hotkey_letter"] = hotkey_letter
    check_hotkey()
    save_config(config_data)
# Create the main window
root = tk.Tk()
root.title("Map Automation")

def update_only_void_stone():
    global OnlyVoidStone
    OnlyVoidStone = only_void_stone_var.get()
    config_data["OnlyVoidStone"] = OnlyVoidStone
    save_config(config_data)

# Function to update delay times from the UI
def update_delays():
    global config_data

    # Retrieve delay time values from the UI elements
    delay_time = float(delay_time_entry.get())

    # Save delay time values to the configuration file
    config_data["delay_time"] = delay_time

    # Save the updated configuration to the file
    save_config(config_data)

# Create tabs
tabs = ttk.Notebook(root)
tab_settings = ttk.Frame(tabs)
tab_values = ttk.Frame(tabs)
tabs.add(tab_settings, text='Settings')
tabs.add(tab_values, text='Values')
tabs.pack(expand=1, fill="both")

# Add UI elements to the Settings tab
map_number_label = ttk.Label(tab_settings, text="Map Number:")
map_number_entry = ttk.Entry(tab_settings)
map_number_button = ttk.Button(tab_settings, text="Update Map Number", command=update_map_number)

cursor_speed_label = ttk.Label(tab_settings, text="Cursor Speed:")
cursor_speed_entry = ttk.Entry(tab_settings)
cursor_speed_button = ttk.Button(tab_settings, text="Update Cursor Speed", command=update_cursor_speed)

rows_to_clear_label = ttk.Label(tab_settings, text="Rows To Clear:")
rows_to_clear_entry = ttk.Entry(tab_settings)
rows_to_clear_button = ttk.Button(tab_settings, text="Update Rows To Clear", command=update_rows_to_clear)

hotkey_modifier_label = ttk.Label(tab_settings, text="Hotkey Modifier:")
hotkey_modifier_var = tk.StringVar(value="")
hotkey_modifier_entry = ttk.Entry(tab_settings, textvariable=hotkey_modifier_var)

hotkey_letter_label = ttk.Label(tab_settings, text="Hotkey Letter:")
hotkey_entry = ttk.Entry(tab_settings)
hotkey_button = ttk.Button(tab_settings, text="Update Hotkey", command=update_hotkey)

# Add the radio button for OnlyVoidStone
only_void_stone_label = ttk.Label(tab_settings, text="Only Void Stone:")
only_void_stone_var = tk.BooleanVar(value=config_data["OnlyVoidStone"])
only_void_stone_button = ttk.Checkbutton(tab_settings, variable=only_void_stone_var)

# Add UI elements for delay times in the Settings tab
delay_time_label = ttk.Label(tab_settings, text="Delay Time:")
delay_time_entry = ttk.Entry(tab_settings)
delay_time_button = ttk.Button(tab_settings, text="Update Delay Time", command=update_delays)


map_number_label.grid(row=0, column=0, padx=10, pady=10)
map_number_entry.grid(row=0, column=1, padx=10, pady=10)
map_number_button.grid(row=0, column=2, padx=10, pady=10)

cursor_speed_label.grid(row=1, column=0, padx=10, pady=10)
cursor_speed_entry.grid(row=1, column=1, padx=10, pady=10)
cursor_speed_button.grid(row=1, column=2, padx=10, pady=10)

rows_to_clear_label.grid(row=2, column=0, padx=10, pady=10)
rows_to_clear_entry.grid(row=2, column=1, padx=10, pady=10)
rows_to_clear_button.grid(row=2, column=2, padx=10, pady=10)

hotkey_modifier_label.grid(row=3, column=0, padx=10, pady=10)
hotkey_modifier_entry.grid(row=3, column=1, padx=10, pady=10)

hotkey_letter_label.grid(row=4, column=0, padx=10, pady=10)
hotkey_entry.grid(row=4, column=1, padx=10, pady=10)
hotkey_button.grid(row=4, column=2, padx=10, pady=10)

delay_time_label.grid(row=5, column=0, padx=10, pady=10)
delay_time_entry.grid(row=5, column=1, padx=10, pady=10)
delay_time_button.grid(row=5, column=2, padx=10, pady=10)

# Add the radio button to the layout
only_void_stone_label.grid(row=6, column=0, padx=10, pady=10)
only_void_stone_button.grid(row=6, column=1, padx=10, pady=10)


# Call the update_only_void_stone function when the radio button state changes
only_void_stone_button.configure(command=update_only_void_stone)


# Add UI elements to the Values tab
positions_values = {position_name: position_value for position_name, position_value in default_config["positions_defaults"].items()}
positions_entries = {}

row_num = 0
for position_name, position_value in default_config["positions_defaults"].items():
    label = ttk.Label(tab_values, text=f"{position_name}:")
    entry = ttk.Entry(tab_values)
    label.grid(row=row_num, column=0, padx=10, pady=5)
    entry.grid(row=row_num, column=1, padx=10, pady=5)
    positions_entries[position_name] = entry
    row_num += 1

update_positions_button = ttk.Button(tab_values, text="Update Positions", command=update_positions)
update_positions_button.grid(row=row_num, column=0, columnspan=2, pady=10)

# Read configuration from file or use default values
try:
    with open("config.json", "r") as file:
        config = json.load(file)
except (json.JSONDecodeError, FileNotFoundError):
    # If the file doesn't exist or is not valid JSON, use the default configuration
    config = default_config

# Update UI with initial values
map_number_entry.insert(0, str(config["MapNumber"]))
cursor_speed_entry.insert(0, str(config["global_cursor_speed"]))
rows_to_clear_entry.insert(0, str(config["RowsToClear"]))
hotkey_entry.insert(0,str(config["hotkey_letter"]))
hotkey_modifier_entry.insert(0,str(config["hotkey_modifier"]))
delay_time_entry.insert(0,str(config["delay_time"]))

for position_name, position_value in config["positions_defaults"].items():
    positions_entries[position_name].insert(0, f"{position_value[0]}, {position_value[1]}")

# Function to check if hotkey is pressed
def check_hotkey():
    modifier = hotkey_modifier_var.get()
    
    # Load the hotkey letter and modifier from the configuration
    hotkey_letter = config_data.get("hotkey_letter", "")
    modifier = config_data.get("hotkey_modifier", "")

    # Check if both modifier and key are not empty
    if modifier:
        hotkey_combination = f"{modifier}+{hotkey_letter}"
    else:
        hotkey_combination = hotkey_letter

    keyboard.add_hotkey(hotkey_combination, RunTheMap)

# Start listening for hotkey
check_hotkey()

# Keep the script running
try:
    root.mainloop()
except:
    pass