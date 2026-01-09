import winreg
import os
import sys
import msvcrt
import subprocess

def find_warband_path(path_to_exe=None):
    if path_to_exe:
        warband_path = os.path.join(path_to_exe, "mb_warband.exe")
        if os.path.exists(warband_path):
            return warband_path, True
    try:
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key_paths = [
            r'SOFTWARE\Mount&Blade Warband',
            r'SOFTWARE\Mount\&Blade Warband'
        ]
        
        for key_path in key_paths:
            try:
                a_key = winreg.OpenKey(a_reg, key_path)
                try:
                    default_value, _ = winreg.QueryValueEx(a_key, "")
                    if default_value and isinstance(default_value, str):
                        warband_path = os.path.join(default_value, "mb_warband.exe")
                        if os.path.exists(warband_path):
                            winreg.CloseKey(a_key)
                            return warband_path, True
                except (FileNotFoundError, OSError):
                    pass
                try:
                    install_path, _ = winreg.QueryValueEx(a_key, "Install_Path")
                    if install_path and isinstance(install_path, str):
                        warband_path = os.path.join(install_path, "mb_warband.exe")
                        if os.path.exists(warband_path):
                            winreg.CloseKey(a_key)
                            return warband_path, True
                except (FileNotFoundError, OSError):
                    pass
                
                winreg.CloseKey(a_key)
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"Error opening key {key_path}: {e}")
                continue
                
    except Exception as e:
        print(f"Error reading registry: {e}")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    warband_path = os.path.join(current_dir, "mb_warband.exe")
    if os.path.exists(warband_path):
        return warband_path, True
    
    try:
        steam_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        try:
            steam_key = winreg.OpenKey(steam_reg, r'SOFTWARE\WOW6432Node\Valve\Steam')
            steam_path, _ = winreg.QueryValueEx(steam_key, "InstallPath")
            winreg.CloseKey(steam_key)
            steam_paths = [
                os.path.join(steam_path, "steamapps", "common", "MountBlade Warband", "mb_warband.exe"),
                os.path.join(steam_path, "SteamApps", "common", "MountBlade Warband", "mb_warband.exe"),
            ]
            
            for steam_warband_path in steam_paths:
                if os.path.exists(steam_warband_path):
                    return steam_warband_path, True
        except (FileNotFoundError, OSError):
            pass
    except Exception:
        pass
    program_files_paths = [
        os.path.join(os.environ.get("ProgramFiles", ""), "Mount&Blade Warband", "mb_warband.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Mount&Blade Warband", "mb_warband.exe"),
        os.path.join(os.environ.get("ProgramFiles", ""), "Steam", "steamapps", "common", "MountBlade Warband", "mb_warband.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Steam", "steamapps", "common", "MountBlade Warband", "mb_warband.exe"),
    ]
    
    for program_path in program_files_paths:
        if program_path and os.path.exists(program_path):
            return program_path, True
    
    return "", False


def get_install_directory(warband_exe_path):
    return os.path.dirname(warband_exe_path)


def get_modules_list(install_directory=None):
    if install_directory is None:
        warband_path, success = find_warband_path()
        if not success:
            return []
        install_directory = get_install_directory(warband_path)
    
    modules_path = os.path.join(install_directory, "Modules")
    if not os.path.exists(modules_path):
        return []
    
    modules = []
    try:
        for item in os.listdir(modules_path):
            item_path = os.path.join(modules_path, item)
            if os.path.isdir(item_path):
                modules.append(item)
    except Exception as e:
        print(f"Error reading modules directory: {e}")
    
    return modules


def get_languages_list(install_directory, module_name):
    languages = ["en"]
    
    module_path = os.path.join(install_directory, "Modules", module_name)
    languages_path = os.path.join(module_path, "languages")
    
    if os.path.exists(languages_path):
        try:
            for item in os.listdir(languages_path):
                item_path = os.path.join(languages_path, item)
                if os.path.isdir(item_path):
                    languages.append(item)
        except Exception as e:
            print(f"Error reading languages directory: {e}")
    
    return languages


def select_from_menu(title, options, prefix=""):
    selected_index = 0
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        if prefix:
            print(prefix)
            print()
        print(f"{title}\n")
        
        for i, option in enumerate(options):
            if i == selected_index:
                print(f"> {option} <")
            else:
                print(f"  {option}")
        
        key = msvcrt.getch()
        
        if key == b'\xe0' or key == b'\x00':
            key2 = msvcrt.getch()
            if key2 == b'H':
                selected_index = max(0, selected_index - 1)
            elif key2 == b'P':
                selected_index = min(len(options) - 1, selected_index + 1)
        elif key == b'\r' or key == b'\n':
            return selected_index
        elif key == b'\x1b':
            return -1
        elif key == b'w' or key == b'W':
            selected_index = max(0, selected_index - 1)
        elif key == b's' or key == b'S':
            selected_index = min(len(options) - 1, selected_index + 1)


def select_module(modules):
    if not modules:
        print("No modules found")
        return None
    
    selected_index = select_from_menu("Select module (use UP/DOWN arrows, ENTER to confirm)", modules)
    
    if selected_index == -1:
        return None
    return modules[selected_index]


def save_language_to_file(language):
    try:
        user_profile = os.environ.get("USERPROFILE", os.path.expanduser("~"))
        warband_dir = os.path.join(user_profile, "Documents", "Mount&Blade Warband")
        
        os.makedirs(warband_dir, exist_ok=True)
        
        language_file = os.path.join(warband_dir, "language.txt")
        with open(language_file, "w", encoding="utf-8") as f:
            f.write(language)
        return True
    except Exception as e:
        print(f"Error saving language to file: {e}")
        return False


def save_language_to_registry(language):
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key_path = r'Software\MountAndBladeWarbandKeys'
        
        try:
            key = winreg.OpenKey(reg, key_path, 0, winreg.KEY_WRITE)
        except FileNotFoundError:
            key = winreg.CreateKey(reg, key_path)
        
        winreg.SetValueEx(key, "language", 0, winreg.REG_SZ, language)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error saving language to registry: {e}")
        return False


def load_language_from_file():
    try:
        user_profile = os.environ.get("USERPROFILE", os.path.expanduser("~"))
        language_file = os.path.join(user_profile, "Documents", "Mount&Blade Warband", "language.txt")
        
        if os.path.exists(language_file):
            with open(language_file, "r", encoding="utf-8") as f:
                language = f.read().strip()
                return language if language else "en"
        return "en"
    except Exception as e:
        print(f"Error loading language from file: {e}")
        return "en"


def save_module_to_file(module_name):
    try:
        user_profile = os.environ.get("USERPROFILE", os.path.expanduser("~"))
        warband_dir = os.path.join(user_profile, "Documents", "Mount&Blade Warband")
        
        os.makedirs(warband_dir, exist_ok=True)
        
        module_file = os.path.join(warband_dir, "last_module.txt")
        with open(module_file, "w", encoding="utf-8") as f:
            f.write(module_name)
        return True
    except Exception as e:
        print(f"Error saving module to file: {e}")
        return False


def load_module_from_file():
    try:
        user_profile = os.environ.get("USERPROFILE", os.path.expanduser("~"))
        module_file = os.path.join(user_profile, "Documents", "Mount&Blade Warband", "last_module.txt")
        
        if os.path.exists(module_file):
            with open(module_file, "r", encoding="utf-8") as f:
                module = f.read().strip()
                return module if module else None
        return None
    except Exception as e:
        print(f"Error loading module from file: {e}")
        return None


def select_language(install_directory, module_name):
    languages = get_languages_list(install_directory, module_name)
    language_names = []
    
    for lang_code in languages:
        if lang_code == "en":
            language_names.append("English (en)")
        elif lang_code == "cns":
            language_names.append("Chinese Simplified (cns)")
        elif lang_code == "cnt":
            language_names.append("Chinese Traditional (cnt)")
        elif lang_code == "cz":
            language_names.append("Czech (cz)")
        elif lang_code == "de":
            language_names.append("German (de)")
        elif lang_code == "es":
            language_names.append("Spanish (es)")
        elif lang_code == "fr":
            language_names.append("French (fr)")
        elif lang_code == "hu":
            language_names.append("Hungarian (hu)")
        elif lang_code == "pl":
            language_names.append("Polish (pl)")
        elif lang_code == "tr":
            language_names.append("Turkish (tr)")
        else:
            language_names.append(f"{lang_code}")
    
    selected_index = select_from_menu("Select language (use UP/DOWN arrows, ENTER to confirm)", language_names)
    
    if selected_index == -1:
        return None
    
    selected_language = languages[selected_index]
    save_language_to_registry(selected_language)
    save_language_to_file(selected_language)
    return selected_language


def launch_game(module_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    launcher_exe = os.path.join(script_dir, "Launcher.exe")
    
    if not os.path.exists(launcher_exe):
        print(f"Error: Launcher.exe not found at {launcher_exe}")
        input("Press ENTER to continue...")
        return False
    
    try:
        subprocess.run([launcher_exe, module_name], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error launching game: {e}")
        input("Press ENTER to continue...")
        return False
    except Exception as e:
        print(f"Error: {e}")
        input("Press ENTER to continue...")
        return False


def print_warband_art():
    art = """ /$$      /$$                     /$$                                 /$$ /$$   /$$
| $$  /$ | $$                    | $$                                | $$| $$  / $$
| $$ /$$$| $$  /$$$$$$   /$$$$$$ | $$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$$|  $$/ $$/
| $$/$$ $$ $$ |____  $$ /$$__  $$| $$__  $$ |____  $$| $$__  $$ /$$__  $$ \\  $$$$/ 
| $$$$_  $$$$  /$$$$$$$| $$  \\__/| $$  \\ $$  /$$$$$$$| $$  \\ $$| $$  | $$  >$$  $$ 
| $$$/ \\  $$$ /$$__  $$| $$      | $$  | $$ /$$__  $$| $$  | $$| $$  | $$ /$$/\\  $$
| $$/   \\  $$|  $$$$$$$| $$      | $$$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$$| $$  \\ $$
|__/     \\__/ \\_______/|__/      |_______/  \\_______/|__/  |__/ \\_______/|__/  |__/"""
    return art


def main_menu(install_directory, modules, module_name, current_language="en"):
    art = print_warband_art()
    while True:
        options = ["Play", "Select Module", "Settings", "Exit"]
        selected = select_from_menu(f"Module: {module_name} | Language: {current_language}", options, art)
        
        if selected == -1:
            continue
        
        if selected == 0:
            if launch_game(module_name):
                sys.exit(0)
        elif selected == 1:
            new_module = select_module(modules)
            if new_module and new_module != module_name:
                module_name = new_module
                save_module_to_file(module_name)
                save_language_to_file("en")
                current_language = "en"
        elif selected == 2:
            new_language = select_language(install_directory, module_name)
            if new_language:
                current_language = new_language
        elif selected == 3:
            return


if __name__ == "__main__":
    warband_path, success = find_warband_path()
    if success:
        print(f"Found Warband: {warband_path}")
    else:
        print("Warband not found")
        exit()

    install_directory = get_install_directory(warband_path)
    modules = get_modules_list(install_directory)
    
    if not modules:
        print("No modules found")
        exit()
    
    saved_module = load_module_from_file()
    selected_module = saved_module if saved_module and saved_module in modules else None
    
    if not selected_module:
        selected_module = select_module(modules)
        if not selected_module:
            print("\nNo module selected")
            exit()
        save_module_to_file(selected_module)
        save_language_to_file("en")
        saved_language = "en"
    else:
        saved_language = load_language_from_file()
    
    main_menu(install_directory, modules, selected_module, saved_language)