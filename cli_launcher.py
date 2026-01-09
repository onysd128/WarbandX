import winreg
import os

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


if __name__ == "__main__":
    warband_path, success = find_warband_path()
    if success:
        print(f"Found Warband: {warband_path}")
    else:
        print("Warband not found")