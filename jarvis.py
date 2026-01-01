import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import pyautogui
import os
import qrcode
import time

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def speak_time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak(f"{Time}")

def speak_date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().strftime("%B")
    day = datetime.datetime.now().day
    speak(f"{day} {month} {year}")

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {
        1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday",
        5: "Friday", 6: "Saturday", 7: "Sunday"
    }
    if day in day_dict:
        speak(f"{day_dict[day]}")

def wishme():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good morning BOSS.")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon BOSS.")
    elif hour >= 18 and hour < 24:
        speak("Good evening BOSS.")
    else:
        speak("Are you an alien?.")

def listen_for_name(target_name="jarvis"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    attempts = 0
    print(f"Say the wake word")
    speak("Say the wake word")
    speak("Listening...")

    while attempts < 2:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = recognizer.listen(source, timeout=30, phrase_time_limit=1.0)
                text = recognizer.recognize_google(audio).lower()
                print("You said:", text)
                if target_name.lower() in text:
                    print(f"Detected the name: {target_name}")
                    return True
                else:
                    attempts += 1
                    print(f"Wake word not detected. Attempt {attempts} of 2.")
            except sr.UnknownValueError:
                print("Could not understand audio.")
                attempts += 1
            except Exception as e:
                print(f"Error: {e}")
                attempts += 1
                speak(f"Wake word not detected. Attempt {attempts} of 2.")
    speak("Wake word not detected twice. Exiting.")
    return False

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.energy_threshold = 4000
        r.dynamic_energy_threshold = True
        speak("Listening...")
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)
    except Exception as e:
        print(e)
        return "none"
    return query

def do_command(command):
    command = command.lower()
    if "website" in command:
        speak("Boss, what website do you want to open?")
        search_query = take_command()
        if search_query.lower() != "none":
            speak(f"Opening {search_query}")
            webbrowser.open(f"https://www.{search_query}.com")
            return True

    elif 'what is the date' in command:
        speak("Today's date is")
        speak_date()
        return True

    elif "what is the time" in command:
        speak("The time is")
        speak_time()
        return True

    elif "what day is it" in command:
        speak("It's")
        cal_day()
        return True

    elif "exit" in command:
        speak("Ok Exiting. Enjoy your day!")
        return True

    elif "open" in command:
        attempts = 0
        while attempts < 2:
            speak("Boss, what do you want to open?")
            search_query = take_command()
            if search_query.lower() != "none":
                try:
                    installed_apps = os.popen(
                        'powershell "Get-StartApps | Select-Object -ExpandProperty Name"'
                    ).read().splitlines()
                    matched_apps = [app for app in installed_apps if search_query.lower() in app.lower()]
                    if matched_apps:
                        speak(f"Opening {matched_apps[0]}")
                        open(matched_apps[0])
                        return True
                    else:
                        speak("Sorry, I couldn't find that application.")
                        attempts += 1
                except Exception:
                    speak("Sorry, there was an error finding applications.")
                    attempts += 1
            else:
                speak("No application name detected. Please try again.")
                attempts += 1
        speak("No valid application name given after 2 attempts.")
        return True

    elif 'information' in command:
        speak("Boss, what do you want to search for?")
        search_query = take_command()
        if search_query.lower() != "none":
            speak(f"Searching for {search_query} on Google")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            return True

    elif "qr code" in command:
        def generate_qr(data, filename="qrcode.png", fill_color="black", back_color="white"):
            try:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=5
                )
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color=fill_color, back_color=back_color)
                img.save(filename)
                speak(f"QR code saved as '{filename}'")
            except Exception:
                speak(f"Error generating QR code.")

        speak("Boss, which QR code do you want to generate?")
        search_query = take_command()
        if search_query and search_query.lower() != "none":
            url = f"https://www.{search_query}.com"
            speak(f"Generating QR code for {search_query}")
            filename = f"{search_query}_qr.png"
            generate_qr(url, filename)
            return True

    elif "screenshot" in command:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        speak("Screenshot taken and saved as screenshot.png")
        return True

    elif "are you well" in command:
        speak("Locking the system")
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return True

    elif 'play music' in command:
        speak("Ok boss, playing music")
        music_path = "C:\\path\\to\\your\\music\\file.mp3"
        try:
            os.startfile(music_path)
            speak("Playing music now")
            return True
        except Exception:
            speak("Sorry boss, I couldn't find the music file.")
            return False

    else:
        speak("I am sorry, give me a command or stop by saying 'exit'")
        return False

def main():
    if listen_for_name("jarvis"):
        wishme()
        speak("Welcome back!")
        speak("Jarvis at your service. How can I help you?")
        count = 0
        while True:
            command = take_command()
            result = do_command(command)
            if result is True:
                speak("Command executed successfully. Exiting now.")
                break
            elif result is False:
                count += 1
                if count >= 3:
                    speak("I am sorry, no command recognized. Please try again later.")
                    break

if __name__ == "__main__":
    main()