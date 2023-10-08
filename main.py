import ttkbootstrap as ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import ctypes

appid = 'TTheekshana.H9SID.1' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

app = ttk.Window(themename='superhero')
app.title('Himawari-9 Satellite Image Downloader')
app.geometry('800x600')
icon_16 = ttk.PhotoImage(file="imgs/16.png") #Creative Stall Premium - Flaticon https://www.flaticon.com/free-icons/satellite
icon_32 = ttk.PhotoImage(file="imgs/32.png")
icon_64 = ttk.PhotoImage(file="imgs/64.png")
app.iconphoto(False, icon_64, icon_32, icon_16)


area_options = {
    "Full Disk": "fd_",
    "Australia": "aus",
    "Central Asia": "cal",
    "New Zealand": "nzl",
    "Southeast Asia 1": "se1",
    "Southeast Asia 2": "se2",
    "Southeast Asia 3": "se3",
    "South Asia": "se4",
    "Hi-res Asia 1": "ha1",
    "Hi-res Asia 2": "ha2",
    "Hi-res Asia 3": "ha3",
    "Hi-res Asia 4": "ha4",
    "Sri Lanka": "ha5",
    "Timor-Leste": "ha6",
    "Pacific Islands 1": "pi1",
    "Pacific Islands 2": "pi2",
    "Pacific Islands 3": "pi3",
    "Pacific Islands 4": "pi4",
    "Pacific Islands 5": "pi5",
    "Pacific Islands 6": "pi6",
    "Pacific Islands 7": "pi7",
    "Pacific Islands 8": "pi8",
    "Pacific Islands 9": "pi9",
    "Pacific Islands 10": "pia",
    "Japan": "jpn",
    "Hi-res Pacific Islands 1": "hp1",
    "Hi-res Pacific Islands 2": "hp2",
    "Hi-res Pacific Islands 3": "hp3"
}

band_options = {
    "B13 Infrared": "b13",
    "B03 Visible": "b03",
    "B08 (Water Vapor)":"b08",
    "B07 (Short Wave Infrared)":"b07",
    "Day Microphysics RGB":"dms",
    "Night Microphysics RGB":"ngt",
    "Dust RGB":"dst",
    "Airmass RGB":"arm",
    "Day Snow-Fog RGB":"dsl",
    "Natural Color RGB":"dnc",
    "True Color RGB (Enhanced)":"tre",
    "True Color Reproduction Image":"trm",
    "Day Convective Storm RGB":"cve",
    "Sandwich":"snd",
    "B03 combined with B13":"vir",
    "B03 and B13 at night":"irv",
    "Heavy rainfall potential areas":"hrp" 
}

time_options = [f"{str(hour).zfill(2)}{str(minute).zfill(2)}" for hour in range(24) for minute in range(0, 60, 10)]

def update_live_image(event=None):
    selected_area = area_combo_var.get()
    selected_band = band_combo_var.get()
    selected_time = time_combo_var.get()

    area_code = area_options.get(selected_area, "")
    band_code = band_options.get(selected_band, "")

    region_image_path = f"imgs/regions/{area_code}.png"

    # Construct the URL for the image based on the selected time
    image_url = f"https://www.data.jma.go.jp/mscweb/data/himawari/img/{area_code}/{area_code}_{band_code}_{selected_time}.jpg"

    try:
        response = requests.get(image_url)
        image_data = BytesIO(response.content)

        image = Image.open(image_data)
        height = 450
        aspect_ratio = float(image.width) / float(image.height)
        width = int(height * aspect_ratio)

        image = image.resize((width, height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        live_label.config(image=photo)
        live_label.image = photo

    except Exception as e:
        print(e)
        live_label.config(text="Error loading images")

    try:
        region_image = Image.open(region_image_path)
        region_image = region_image.resize((182, 150), Image.LANCZOS)
        region_photo = ImageTk.PhotoImage(region_image)
        region_label.config(image=region_photo)
        region_label.image = region_photo
    except Exception as e:
        live_label.config(text="Error loading images")
area_label = ttk.Label(app, text="Select Area:")
band_label = ttk.Label(app, text="Select Band:")
time_label = ttk.Label(app, text="Select Time (UTC):")

area_combo_var = ttk.StringVar()
area_combo = ttk.Combobox(app, textvariable=area_combo_var, values=list(area_options.keys()), state="readonly")
area_combo_var.set("Full Disk")  
area_combo.bind("<<ComboboxSelected>>", update_live_image)

band_combo_var = ttk.StringVar()
band_combo = ttk.Combobox(app, textvariable=band_combo_var, values=list(band_options.keys()), state="readonly")
band_combo_var.set("B13 Infrared") 
band_combo.bind("<<ComboboxSelected>>", update_live_image)

time_combo_var = ttk.StringVar()
time_combo = ttk.Combobox(app, textvariable=time_combo_var, values=time_options, state="readonly")
time_combo_var.set("0000")  # Set the default time
time_combo.bind("<<ComboboxSelected>>", update_live_image)

region_label = ttk.Label(app)
region_label.grid(row=2, column=0, padx=10, pady=10, columnspan=1)
live_label = ttk.Label(app)
live_label.grid(row=2, column=1, padx=10, pady=10, columnspan=4)

area_label.grid(row=0, column=0, padx=(5, 0), pady=10)
area_combo.grid(row=0, column=1, padx=(2, 0), pady=10)  

band_label.grid(row=1, column=0, padx=(5, 0), pady=10)
band_combo.grid(row=1, column=1, padx=(5, 0), pady=10)  

time_label.grid(row=0, column=2, padx=(5, 0), pady=10)
time_combo.grid(row=0, column=3, padx=(5, 0), pady=10) 
update_live_image()  


app.mainloop()
