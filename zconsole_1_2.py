import os
import ctypes
import platform
import json
from pathlib import Path
from datetime import datetime
import requests
import random
from PIL import Image
import time
import sys
import configparser
import atexit
import curses

current_time = datetime.now()

class Prog:
    prefix = "> "
    name = "ZConsole"
    version = "1.2"
    #authors = [
    #f"{name} TEAM",
    #"• Bezzh (ysinzz) - Coding",
    #"• Blackbox AI - Additional help"
    #]

DEBUG_MODE = "False"

args = []
cmd = []
user_input = ""
r_format = f"$DIR >>>"
str_format = r_format.replace("$DIR", os.getcwd())
ctypes.windll.kernel32.SetConsoleTitleW(f"{Prog.name} - {Prog.version} - {os.getcwd()}")

quote_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format("best")
response = requests.get(quote_url, headers={'X-Api-Key': 'hozEXlopbcCKTRIXA78TBw==3JXOmkPCt2HGIL82'})

def exit_handler():
    print(f"{config[messages_link]["exit_from_program"]}")
    with open(f"{script_directory}/latest.log", "w", encoding="utf-8-sig") as log_file:
        log_file.truncate(0)
        if DEBUG_MODE == "True": log_file.write("DEBUG_MODE\n")
        ex = "\n".join(config["history"])
        log_file.write(ex)

    time.sleep(0.2)

history = []
atexit.register(exit_handler)

#commands_list = [
#f"{Prog.name} {Prog.version}",
#"help - Показывает помощь по командам.",
#f"authors - Показывает список авторов {Prog.name}.",
#"_hello - Печатает Hello, World!",
#"dir - Печатает все доступные папки и файлы в текущем каталоге.",
#"mkdir <path> - Создаёт папку по пути.",
#"pid (/p) - Показывает ID процесса. /p - Показывает ID родительского процесса.",
#"env (/l) <id> - Показывает контент среды через ID. /l - Показывает все среды.",
#"setenv <id> <content> - Создаёт среду.",
#"os (/d) - Показывает характеристики системы. /d - Показывает дополнительную информацию.",
#"cls - Очищает консоль.",
#"win <command> - Выполняет команду от консоли Windows.",
#"execute <command> - Выполняет команду ZConsole.",
#"add <number> <number> - Складывает 2 числа.",
#"math <operator> <number> .. - Использует оператор математический действий на несколько чисел.",
#"exit (/q) - Завершает работу программы. /q - Завершает работу программы без вопроса."
#]
messages_link = "messages_ru"
script_directory = Path(__file__).parent.resolve()

def add_to_history(stat, text):
    formatted_time = current_time.strftime("%d.%m.%Y %H:%M:%S")
    formatt = f"{formatted_time} [{stat}]: {text}"
    history.append(f"{formatt}")
    
    with open(f"{script_directory}/zconsole_1_2.json", "r", encoding="utf-8-sig") as config_file:
        config = json.load(config_file)
    config["history"].append(f"{formatt}")

    with open(f"{script_directory}/zconsole_1_2.json", "w", encoding="utf-8") as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=4)

def clear_history():
    history.clear()
    config["history"].clear()

    with open(f"{script_directory}/zconsole_1_2.json", "w", encoding="utf-8") as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=4)

def load_config(path, key="test", new="0"):
    with open(f"{script_directory}/{path}", "r", encoding="utf-8-sig") as config_file:
        config = json.load(config_file)
    config[key] = new

    with open(f"{script_directory}/{path}", "w", encoding="utf-8") as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=4)
    return config

def load_ini():
    if DEBUG_MODE == "True": print("Loading ini cfg")
    script_dir = Path(__file__).parent.resolve()
    script_name = Path(__file__).stem
    ini = configparser.ConfigParser()
    ini.read(f"{script_dir}/{script_name}.ini", encoding="utf-8")
    return ini
ini = load_ini()
for section in ini.sections(): # vars
    for key in ini[section]:
        ini[section][key] = ini[section][key].format(prog_name=ini["Prog"]["name"])

def image_to_ascii(image_path, width=100):
    if DEBUG_MODE == "True": print("Converting image to ascii text")
    # Открываем изображение
    img = Image.open(image_path)
    img = img.resize((width, int((width / img.width) * img.height)))
    img = img.convert('L')  # Преобразуем в градации серого

    # Определяем символы для отображения
    chars = "@%#*+=-:. "
    if DEBUG_MODE == "True": print(f"Ascii current symbols: {chars}")
    pixels = img.getdata()
    ascii_str = ''.join([chars[pixel // 25] for pixel in pixels])
    
    # Форматируем строку в виде строк
    img_width = img.width
    ascii_str_len = len(ascii_str)
    ascii_image = "\n".join([ascii_str[i:i + img_width] for i in range(0, ascii_str_len, img_width)])
    print(ascii_image)

def countdown(sec):
    while sec:
        mins, secs = divmod(sec, 60)
        timer = f"{mins}:{sec}"
        print(timer, end="\r")
        time.sleep(1)
        sec -= 1
    print_cmd(f"{config[messages_link]["timer_out"]}")

def print_text(text):
    return print(text)

def print_cmd(text):
    return print(Prog.prefix + text)

def guess_number_game():
    print(f"{config[messages_link]["game_guess_1"]}")
    print(f"{config[messages_link]["game_guess_2"]}")
            
    number_to_guess = random.randint(1, 100)
    if DEBUG_MODE == "True": print(f"Number to guess: {number_to_guess}")
    attempts = 0

    try:
        while True:
            user_guess = int(input(f"{config[messages_link]["game_guess_quest"]}"))
            attempts += 1
            if user_guess < number_to_guess:
                print(f"{config[messages_link]["game_guess_small"]}")
            elif user_guess > number_to_guess:
                print(f"{config[messages_link]["game_guess_more"]}")
            else:
                print(f"{config[messages_link]["game_guess_win"].format(number_to_guess=number_to_guess, attempts=attempts)}")
                break
    except ValueError:
        print(config[messages_link]["int_num"])

class ZPages:
    working = True
    choosedPrefix = "> "
    currentSelect = 0
    selectedFormat = "You selected: {curselected}"

    @staticmethod
    def New(objects: list, on_select=None, on_cancel=None):
        def main(stdscr):
            curses.curs_set(0)  # Скрыть курсор
            stdscr.clear()  # Очистить экран

            while ZPages.working:
                stdscr.clear()  # Очистить экран
                for index, key in enumerate(objects):
                    if index == ZPages.currentSelect:
                        stdscr.addstr(index, 0, f"{ZPages.choosedPrefix}{key}")  # Выделяем выбранный элемент
                    else:
                        stdscr.addstr(index, 0, f" {key}")  # Печатаем остальные элементы

                stdscr.refresh()  # Обновить экран

                key = stdscr.getch()  # Получить нажатую клавишу
                if key == curses.KEY_DOWN:
                    ZPages.currentSelect = (ZPages.currentSelect + 1) % len(objects)  # Циклический выбор вниз
                elif key == curses.KEY_UP:
                    ZPages.currentSelect = (ZPages.currentSelect - 1) % len(objects)  # Циклический выбор вверх
                elif key == 10:  # Обработка нажатия клавиши Enter
                    if on_select:
                        selected_item = objects[ZPages.currentSelect]
                        on_select(selected_item)  # Вызов функции обратного вызова
                    stdscr.addstr(len(objects), 0, f"{ZPages.selectedFormat.format(curselected=objects[ZPages.currentSelect])}")  # Показать выбранный элемент
                    stdscr.refresh()  # Обновить экран
                    stdscr.getch()  # Ожидание нажатия клавиши перед продолжением
                elif key == ord('q'):  # Выход при нажатии 'q'
                    if on_cancel:
                        selected_item = objects[ZPages.currentSelect]
                        on_cancel(selected_item)  # Вызов функции обратного вызова
                    ZPages.working = False  # Завершить работу

        curses.wrapper(main)

def key_exists(list, key, value): # Required for args+
    for item in list:
        if key in item and item[key] == value:
            return True
    return False

def process_command(command):
    global messages_link
    global history
    if command != "" or " ": add_to_history("EXECUTE", command)
    try:
        parts = command.split()
        cmd = parts[0] # Command name
        args = parts[1:] # Command args

        if cmd == "_hello":
            if DEBUG_MODE == "True": print("Hello!!!!!!!")
            print_cmd("Hello, World!") # DO NOT CREATE TRANSLATES!!!!

        elif cmd == "dir":
            if DEBUG_MODE == "True": print("Dir list")
            ex = ",\n".join(os.listdir(os.getcwd()))
            print(ex)

        elif cmd == "print":
            if DEBUG_MODE == "True": print(f"Unformatted: {args}")
            if len(args) >= 1:
                ex = " ".join(args)
                print_cmd(ex)
            else:
                add_to_history("WARN", f"{config[messages_link]["args_equals_1"]}")
                print(f"{config[messages_link]["args_equals_1"]}")

        elif cmd == "ascii":
            if len(args) >= 1:
                ex = fr"{script_directory}\{args[0]}"
                image_to_ascii(ex)
            else:        
                add_to_history("WARN", f"{config[messages_link]["args_equals_1"]}")
                print(f"{config[messages_link]["args_equals_1"]}")

        elif cmd == "printvar":
            if len(args) == 1:
                if args[0] == "help":
                    ex = "\n".join(config[messages_link]["printvar_help"])
                    print(f"{ex}")

                elif args[0] == "username":
                    print_cmd(user)
                elif args[0] == "prog.ver":
                    print_cmd(Prog.version)
                elif args[0] == "prog.name":
                    print_cmd(Prog.name)
                else:
                    ex2 = args[0]
                    if ex2 == str:
                        exec(f"print_cmd({ex2})")
                    else:
                        ex3 = "\n".join(args[0])
                        str(ex3)
                        exec(f"print_cmd({ex3})")
            else:
                add_to_history("WARN", f"{config[messages_link]["args_equals_1"]}")
                print(f"{config[messages_link]["args_equals_1"]}")

        elif cmd == "mkdir":
            if len(args) >= 1:
                ex = " ".join(args)
                os.mkdir(ex)
                if "/q" in args == False: print(f"{config[messages_link]["folder_created"]}")

        elif cmd == "restart" or cmd == "reload":
            if DEBUG_MODE == "True": print("RELOADING")
            os.system("cls")
            print(config[messages_link]["restart"])
            os.execv(sys.executable, ['python'] + sys.argv)

        elif cmd == "pid":
            if "/p" in args: print_cmd(os.getppid())
            else: print_cmd(os.getpid())

        elif cmd == "env":
            if len(args) == 1:
                if "/l" in args:
                    ex = ",\n".join(os.environ)
                    print(ex)
                else:
                    print(os.environ(args[0]))

        elif cmd == "setenv":
            if len(args) >= 2:
                ex = " ".join(args[1, 2, 3, 4])
                os.environ[args[0]] = ex

        elif cmd == "parse":
            if len(args) >= 1:
                ex = " ".join(args)
                access_denied = [ # Do not remove this line
                    "os", "sys", "shutil.", "with open(",
                    "access_denied", "virus", "del", "os", "win",
                    "log", "args[", "request", "add_to_history",
                    "open(", "getattr", ".close", "remove", "pass"
                ]
                if any(item in ex for item in access_denied):
                    add_to_history("ACCESS_DENIED", f"Parsing command: {ex}")
                    print("[ ACCESS_DENIED ]")

                else:
                    exec(ex)
            else:
                add_to_history("WARN", f"{config[messages_link]["args_equals_1"]}")
                print(f"{config[messages_link]["args_equals_1"]}")

        elif cmd == "os":
            print_cmd(f"{config[messages_link]["system"]["sys_id"].format(name=os.name)}")
            print_cmd(f"{config[messages_link]["system"]["sys_sep"].format(sep=os.sep)}")
            print_cmd(f"{config[messages_link]["system"]["cur_path"].format(path=os.getcwd())}")
            print_cmd(f"{config[messages_link]["system"]["sys_name"].format(sys=platform.system())}")
            print_cmd(f"{config[messages_link]["system"]["sys_ver"].format(ver=platform.version())}")
            print_cmd(f"{config[messages_link]["system"]["plat_name"].format(plat=platform.platform())}")
            print_cmd(f"{config[messages_link]["system"]["proc_inf"].format(proc=platform.processor())}")
            print_cmd(f"{config[messages_link]["system"]["sys_arch"].format(arch=platform.architecture())}")
            print_cmd(f"{config[messages_link]["system"]["sys_debug"]}")
            try:
                if "/d" in args:
                    import psutil #type:ignore
                    print_cmd(f"{config[messages_link]["system"]["proc_count"].format(proc=psutil.cpu_count(logical=True))}")
                    print_cmd(f"{config[messages_link]["system"]["proc_per"].format(proc=psutil.cpu_percent(interval=1))}")
                    ex = psutil.virtual_memory()
                    ex2 = f"{ex.total / (1024 ** 2):.2f}"
                    print_cmd(f"{config[messages_link]["system"]["total_d"].format(d=ex2)}")
                    ex3 = f"{ex.used / (1024 ** 2):.2f}"
                    print_cmd(f"{config[messages_link]["system"]["use_d"].format(d=ex3)}")
                    ex2 = f"{ex.available / (1024 ** 2):.2f}"
                    print_cmd(f"{config[messages_link]["system"]["free_d"].format(d=ex2)}")
                    ex2 = psutil.disk_usage('/')
                    ex3 = f"{ex2.total / (1024 ** 3):.2f}"
                    print_cmd(f"{config[messages_link]["system"]["total_disk"].format(disk=ex3)}")
                    ex = f"{ex2.used / (1024 ** 3):.2f}"
                    print_cmd(f"{config[messages_link]["system"]["use_disk"].format(disk=ex)}")
                    ex3 = f"{ex2.free / (1024 ** 3):.2f}"
                    print_cmd(f"{config[messages_link]["system"]["free_disk"].format(disk=ex3)}")
            except ModuleNotFoundError:
                print(f"{config[messages_link]["system"]["psutil_no"]}")
                main()

        elif cmd == "help":
            ex = "\n".join(config[messages_link]["help"])
            print_cmd(ex)

        elif cmd == "authors":
            ex = "\n".join(config[messages_link]["authors"])
            print_cmd(ex)

        elif cmd == "history":
            ex = "\n".join(history)
            print(ex)

        elif cmd == "clearhistory":
            history.clear()
            clear_history()

        elif cmd == "cls":
            if DEBUG_MODE == "True": print("Clearing")
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")

        elif cmd == "win":
            if DEBUG_MODE == "True": print(f"EXECUTING {args}")
            ex = " ".join(args)
            os.system(ex)
            add_to_history("WIN_EXECUTE", ex)

        elif cmd == "execute":
            if len(args) >= 1:
                try:
                    ex = " ".join(args)
                    process_command(ex)
                except Exception as e:
                    add_to_history("ERROR", e)
                    print(f"{config[messages_link]["error_in_command"].format(arg0=args[0], err=e)}")
            else:
                print(f"{config[messages_link]["args_more_than_0"]}")


        elif cmd == "add":
            # Function add with 2 args
            if len(args) == 2:
                try:
                    num1 = float(args[0])
                    num2 = float(args[1])
                    print_cmd(f"{config[messages_link]["result"]}: {num1 + num2}")
                except ValueError:
                    print(f"{config[messages_link]["args_should_int"]}")
            else:
                print(f"{config[messages_link]["args_equals_2"]}")

        elif cmd == "translate":
            if len(args) == 2:
                try:
                    num1 = float(args[0])
                    num2 = float(args[1])
                    print_cmd(f"{config[messages_link]["result"]}: {num1 + num2}")
                except ValueError:
                    print(f"{config[messages_link]["args_should_int"]}")
            else:
                print(f"{config[messages_link]["args_equals_2"]}")

        elif cmd == "timer":
            countdown(int(args[0]))

        elif cmd == "game_guess":
            guess_number_game()

        elif cmd == "lang":
            if len(args) == 1:
                if args[0] == "ru":
                    messages_link = "messages_ru"
                    load_config("zconsole_1_2.json", key="lang", new="ru")
                else:
                    messages_link = "messages_en"
                    load_config("zconsole_1_2.json", key="lang", new="en")

                print_cmd(f"{config[messages_link]["lang_changed"]}")
            else:
                add_to_history("WARN", f"{config[messages_link]["args_equals_1"]}")
                print(f"{config[messages_link]["args_equals_1"]}")

        elif cmd == "setvar":
            if len(args) == 2:
                try:
                    load_config("zconsole_1_2.json", key=args[0], new=args[1])
                    print_cmd(f"{config[messages_link]["varchanged"].format(var=args[0], value=args[1])}")
                except Exception as e:
                    print(f"{config[messages_link]["skip_error"].format(err=e)}")
                    add_to_history("ERROR", e)
                    main()
            else:
                add_to_history("WARN", f"{config[messages_link]["args_equals_2"]}")
                print(f"{config[messages_link]["args_equals_2"]}")

        elif cmd == "name":
            if len(args) >= 1:
                ex = " ".join(args)
                load_config("zconsole_1_2.json", key="login", new=ex)
                add_to_history("INFO", f"{config[messages_link]["name_changed"]}")
                print_cmd(f"{config[messages_link]["name_changed"]}")
            else:
                add_to_history("WARN", f"{config[messages_link]["args_equals_1"]}")
                print(f"{config[messages_link]["args_equals_1"]}")

        elif cmd == "zcss":
            def on_select(item):
                if item == "Back": main()
            page = ZPages.New(["Back", "Config.."], on_select=on_select)

        elif cmd == "math":
            try:
                if len(args) < 2:
                    add_to_history("WARN", f"{config[messages_link]["args_equals_2"]}")
                    print(f"{config[messages_link]["args_equals_2"]}")

                operation = args[0] # Операция (add, sub, mul, div)
                numbers = list(map(float, args[1:])) # Преобразуем аргументы в числа

                if operation == "add":
                    result = sum(numbers)
                    print_cmd(f"{config[messages_link]["sum"]}: {result}")

                elif operation == "sub":
                    result = numbers[0]
                    for num in numbers[1:]:
                        result -= num
                        print_cmd(f"{config[messages_link]["sub"]}: {result}")

                elif operation == "mul":
                    result = 1
                    for num in numbers:
                        result *= num
                    print_cmd(f"{config[messages_link]["mul"]}: {result}")

                elif operation == "div":
                    result = numbers[0]
                    try:
                        for num in numbers[1:]:
                            result /= num
                    except ZeroDivisionError:
                        print(f"{config[messages_link]["div0"]}")
                    print_cmd(f"{config[messages_link]["div"]}: {result}")
                else:
                    add_to_history("WARN", f"{config[messages_link]["unknown_operator"]}")
                    print(f"{config[messages_link]["unknown_operator"]}")

            except IndexError as e:
                None

        elif cmd == "exit":
            if "/q" in args: # args+ using
                add_to_history("EXIT", "")
            else:
                exit_answer = input(f"{config[messages_link]["exit_answer"]}")
                if exit_answer.lower() == "yes":
                    add_to_history("EXIT", "")
                else:
                    print(f"{config[messages_link]["exit_canceled"]}")
                    return main()
            return False
                
        else:
            print(f"{config[messages_link]["unknown_command"]}")
            
        return True
    except Exception as e:
        print(f"{config[messages_link]["skip_error"].format(err=e)}")
        add_to_history("ERROR", e)
        main()

def main():
    while True:
        str_format = r_format.replace("$DIR", os.getcwd())
        user_input = input(str_format)
        if not process_command(user_input):
            break


if __name__ == "__main__":
    config = load_config("zconsole_1_2.json")
    add_to_history("RUN", "")
    DEBUG_MODE = config["debug"]
    if DEBUG_MODE == "True": print("Starting prog")
    if config["lang"] == "ru":
        messages_link = "messages_ru"
    elif config["lang"] == "en":
        messages_link = "messages_en"

    history = config["history"]

    user = config["login"]
    print(f"{config[messages_link]["welcome_1"].format(name=Prog.name, version=Prog.version, user=user)}")
    print(f"{config[messages_link]["welcome_2"]}")
    print(f"{config[messages_link]["welcome_3"]}")
    print(f"{config[messages_link]["welcome_4"].format(config_len=len(config), script_directory=script_directory)}")
    print(f"{config[messages_link]["welcome_5"]}")
    main()