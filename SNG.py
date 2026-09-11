import tkinter as tk
from tkinter import ttk
import vlc
from datetime import datetime
import time
import random
from ctypes import windll
from subprocess import call
import CombinedScript as cs
# Enable system DPI awareness (Windows 10/11) (to avoid making the GUI blurry or pixelated)
windll.shcore.SetProcessDpiAwareness(1)
r = tk.Tk() #this is the root , probs the whole gui if you would 
r.title("Smart Nursery Guardian") 
r.geometry("1500x1100") #I chose those two numbers for absolutely no reason , will change them later
parameters = {"temperature": tk.StringVar(value="27.0 °C"),    
            "motion": tk.StringVar(value="0"),
            "baby_state": tk.StringVar(value="Sleeping"),
            "light": tk.StringVar(value="Bright"),
            "gas": tk.StringVar(value="Safe"),
            "fan": tk.StringVar(value="Half Speed"),
            "servo": tk.StringVar(value="Stopped"),
            "connection": tk.StringVar(value="Connected"),
            "cry": tk.StringVar(value="No cry detected"),
            "classification": tk.StringVar(value="—"),
            "last_event": tk.StringVar(value="System started"),}
# as the name suggests , the parameters that determine the outcome

status=ttk.Frame(r,padding=(25,5)) 
status.pack(fill="x")
style = ttk.Style()
style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"))
style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
style.configure("Card.TFrame", relief="solid", borderwidth=1)
style.configure("CardTitle.TLabel", font=("Segoe UI", 11, "bold"))
style.configure("Value.TLabel", font=("Segoe UI", 20, "bold"))
style.configure("Small.TLabel", font=("Segoe UI", 9))
style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=8)
connection=1 
#connection=int(input()) # this is supposed to check if the chip is connected , somehow 
#will be changed once everything is assembled
#there should be a function that gets called here that checks if the thing is connected , if it isn't it should return 0
if connection == 0 :
    parameters["connection"]=tk.StringVar(value="Not connected")
ttk.Label(status, textvariable=parameters["connection"],font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
ttk.Label(status, text=" | Serial: BlackPill",style="Small.TLabel").pack(side="left")
ttk.Separator(r).pack(fill="x", padx=2, pady=8)
content = ttk.Frame(r, padding=(22, 8))
content.pack(fill="both", expand=False)
left = ttk.Frame(content)
left.pack( fill="both", expand=False, padx=(0, 10))
ttk.Label(left, text="Live Monitoring",font=("Segoe UI", 16, "bold")).pack(anchor='center', pady=(0, 10))
cards = ttk.Frame(left)
cards.pack(fill="x")

def make_card(parent, col, row, title, variable, subtitle):
    card = ttk.Frame(parent, style="Card.TFrame", padding=14)
    card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
    parent.columnconfigure(col, weight=1)
    ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor='center')
    ttk.Label(card, textvariable=variable, style="Value.TLabel").pack(anchor='center', pady=(8, 2))
    ttk.Label(card, text=subtitle, style="Small.TLabel").pack(anchor='center')
temp = 0
#temp = int(input()) ,  a function to get the temperature from the chip , still unwritten 
parameters["temperature"] = tk.StringVar(value=(str(temp)+".0 °C")) if (temp > 0) else parameters["temperature"] 
mot = 0
#mot = int(input()) , a function to get the motion each 8 seconds from the chip , still unwritten 
parameters["motion"] = tk.StringVar(value=str(mot)) if (mot > 0) else parameters["motion"]
li = "0"
#li = input()       , a function to get the light intensity  from the chip , still unwritten 
parameters["light"] = tk.StringVar(value=li) if (li != "0") else parameters["light"]
g = "0"
#g = input()   
parameters["gas"] = tk.StringVar(value=g) if (g != "0") else parameters["gas"]
#the chip should communicate with the GUI for all that info 
parameters["classification"] = tk.StringVar(value=cs.AudioProc_MLClass()) if (g != "N") else parameters["classification"]

if(parameters["classification"] != "—"):
    parameters["cry"]=tk.StringVar(value="Cry detected")

make_card(cards, 0, 0, "Temperature", parameters["temperature"], "Thermistor")
make_card(cards, 1, 0, "Motion", parameters["motion"], "PIR / 8 sec")
make_card(cards, 0, 1, "Room Light", parameters["light"], "LDR")
make_card(cards, 1, 1, "Gas / Smoke", parameters["gas"], "Gas sensor")
state = ttk.LabelFrame(left, text="System State", padding=14)
state.pack(fill="x", pady=12)
rows = [
            ("Baby state", "baby_state"),
            ("Cry detection", "cry"),
            ("ML classification", "classification"),
            ("Cooling fan", "fan"),
            ("Servo", "servo"),
        ]
for i, (label, key) in enumerate(rows):
    ttk.Label(state, text=label + ":", font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", pady=5,padx=70)
    ttk.Label(state, textvariable=parameters[key]).grid(row=i, column=1, sticky="w", padx=700, pady=5)
r.mainloop()
# now the display is over , let's cut to action

def Hungry():    
    vidr = tk.Tk()
    vidr.title("Hungry_kiddo")
    vidr.attributes('-fullscreen', True)
    vidr.bind('<Escape>', lambda e: vidr.attributes('-fullscreen', False))
    vidframe = tk.Frame(vidr)
    vidframe.pack(fill=tk.BOTH, expand=True)
    vidr.update_idletasks()
    instance = vlc.Instance()
    player = instance.media_player_new()
    player.set_hwnd(vidframe.winfo_id())

    list_player = instance.media_list_player_new()
    list_player.set_media_player(player)  # <-- links the two together
    media_list = instance.media_list_new()
    media_list.add_media(instance.media_new("video.mp4"))
    list_player.set_media_list(media_list)
    list_player.set_playback_mode(vlc.PlaybackMode.loop)
    list_player.play()
    vidr.mainloop()

def save_the_baby():  #SNG: 1 , Linsey Clancy : -3
    call(["python" , "tele.py"])


if(parameters["gas"] != "Safe"):
    save_the_baby()

if(parameters["classification"] == "Hungry"):
    Hungry()

