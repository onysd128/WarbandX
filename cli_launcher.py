import winreg
import os
import sys
import msvcrt
import subprocess
import ctypes

if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

COLOR_RESET = '\033[0m'
COLOR_ACCENT = '\033[38;2;255;165;0m'

TRANSLATIONS = {
    "en": {
        "warband_not_found": "Warband not found",
        "no_modules_found": "No modules found",
        "no_module_selected": "No module selected",
        "select_module": "Select module (use UP/DOWN arrows, ENTER to confirm)",
        "select_language": "Select language (use UP/DOWN arrows, ENTER to confirm)",
        "select_launcher_language": "Select launcher language (use UP/DOWN arrows, ENTER to confirm)",
        "multiple_installations": "Multiple Warband installations found. Select which one to use:",
        "play": "Play",
        "play_wse2": "Play (WSE2)",
        "select_module": "Select Module",
        "settings": "Settings",
        "exit": "Exit",
        "back": "Back",
        "game_language": "Game Language",
        "launcher_language": "Launcher Language",
        "game_settings": "Game Settings",
        "video_settings": "Video Settings",
        "audio_settings": "Audio Settings",
        "advanced_settings": "Advanced Settings",
        "module": "Module",
        "language": "Language",
        "press_enter": "Press ENTER to continue...",
        "error_launching": "Error launching game",
        "error": "Error",
        "warning": "WARNING",
        "language_warning": "The selected language \"{selected_lang}\" is not available in the root Languages folder.\n\nSome interface elements may not be translated and will remain in English.",
        "found_warband": "Found Warband",
        "steam_not_running": "Steam is not running.\n\nPlease start Steam and log in to your account before launching the game.",
        "launching": "Launching",
    },
    "uk": {
        "warband_not_found": "Warband не знайдено",
        "no_modules_found": "Модулі не знайдено",
        "no_module_selected": "Модуль не обрано",
        "select_module": "Оберіть модуль (використовуйте стрілки ВГОРУ/ВНИЗ, ENTER для підтвердження)",
        "select_language": "Оберіть мову (використовуйте стрілки ВГОРУ/ВНИЗ, ENTER для підтвердження)",
        "select_launcher_language": "Оберіть мову лаунчера (використовуйте стрілки ВГОРУ/ВНИЗ, ENTER для підтвердження)",
        "multiple_installations": "Знайдено кілька встановлень Warband. Оберіть яке використовувати:",
        "play": "Грати",
        "play_wse2": "Грати (WSE2)",
        "select_module": "Обрати модуль",
        "settings": "Налаштування",
        "exit": "Вихід",
        "back": "Назад",
        "game_language": "Мова гри",
        "launcher_language": "Мова лаунчера",
        "game_settings": "Налаштування гри",
        "video_settings": "Відео налаштування",
        "audio_settings": "Аудіо налаштування",
        "advanced_settings": "Розширені налаштування",
        "module": "Модуль",
        "language": "Мова",
        "press_enter": "Натисніть ENTER для продовження...",
        "error_launching": "Помилка запуску гри",
        "error": "Помилка",
        "warning": "ПОПЕРЕДЖЕННЯ",
        "language_warning": "Обрана мова \"{selected_lang}\" недоступна в кореневій папці Languages.\n\nДеякі елементи інтерфейсу можуть не бути перекладені і залишаться англійською.",
        "found_warband": "Знайдено Warband",
        "steam_not_running": "Steam не запущений.\n\nБудь ласка, запустіть Steam та увійдіть у свій профіль перед запуском гри.",
        "launching": "Запуск",
    },
    "be": {
        "warband_not_found": "Warband не знойдзена",
        "no_modules_found": "Модулі не знойдзены",
        "no_module_selected": "Модуль не абраны",
        "select_module": "Абярыце модуль (выкарыстоўвайце стрэлкі УГОРУ/УНИЗ, ENTER для пацверджання)",
        "select_language": "Абярыце мову (выкарыстоўвайце стрэлкі УГОРУ/УНИЗ, ENTER для пацверджання)",
        "select_launcher_language": "Абярыце мову лаўнчара (выкарыстоўвайце стрэлкі УГОРУ/УНИЗ, ENTER для пацверджання)",
        "multiple_installations": "Знойдзена некалькі ўстановак Warband. Абярыце якую выкарыстоўваць:",
        "play": "Гуляць",
        "play_wse2": "Гуляць (WSE2)",
        "select_module": "Абраць модуль",
        "settings": "Налады",
        "exit": "Выхад",
        "back": "Назад",
        "game_language": "Мова гульні",
        "launcher_language": "Мова лаўнчара",
        "game_settings": "Налады гульні",
        "video_settings": "Відэа налады",
        "audio_settings": "Аўдыё налады",
        "advanced_settings": "Пашыраныя налады",
        "module": "Модуль",
        "language": "Мова",
        "press_enter": "Націсніце ENTER для працягу...",
        "error_launching": "Памылка запуску гульні",
        "error": "Памылка",
        "warning": "ПАПЯРЭДЖАННЕ",
        "language_warning": "Абраная мова \"{selected_lang}\" недаступная ў каранёвай папцы Languages.\n\nНекаторыя элементы інтэрфейсу могуць не быць перакладзены і застануцца англійскай.",
        "found_warband": "Знойдзена Warband",
        "steam_not_running": "Steam не запушчаны.\n\nКалі ласка, запусціце Steam і ўвайдзіце ў свой профіль перад запускам гульні.",
        "launching": "Запуск",
    },
    "ro": {
        "warband_not_found": "Warband nu a fost găsit",
        "no_modules_found": "Nu s-au găsit module",
        "no_module_selected": "Niciun modul selectat",
        "select_module": "Selectați modulul (folosiți săgețile SUS/JOS, ENTER pentru confirmare)",
        "select_language": "Selectați limba (folosiți săgețile SUS/JOS, ENTER pentru confirmare)",
        "select_launcher_language": "Selectați limba launcher-ului (folosiți săgețile SUS/JOS, ENTER pentru confirmare)",
        "multiple_installations": "Au fost găsite mai multe instalări Warband. Selectați care să fie folosită:",
        "play": "Joacă",
        "play_wse2": "Joacă (WSE2)",
        "select_module": "Selectează Modul",
        "settings": "Setări",
        "exit": "Ieșire",
        "back": "Înapoi",
        "game_language": "Limba jocului",
        "launcher_language": "Limba launcher-ului",
        "game_settings": "Setări Joc",
        "video_settings": "Setări Video",
        "audio_settings": "Setări Audio",
        "advanced_settings": "Setări Avansate",
        "module": "Modul",
        "language": "Limbă",
        "press_enter": "Apăsați ENTER pentru a continua...",
        "error_launching": "Eroare la lansarea jocului",
        "error": "Eroare",
        "warning": "AVERTISMENT",
        "language_warning": "Limba selectată \"{selected_lang}\" nu este disponibilă în folderul rădăcină Languages.\n\nUnele elemente ale interfeței pot să nu fie traduse și vor rămâne în engleză.",
        "found_warband": "Warband găsit",
        "steam_not_running": "Steam nu rulează.\n\nVă rugăm să porniți Steam și să vă conectați la contul dvs. înainte de a lansa jocul.",
        "launching": "Lansare",
    },
    "pl": {
        "warband_not_found": "Nie znaleziono Warband",
        "no_modules_found": "Nie znaleziono modułów",
        "no_module_selected": "Nie wybrano modułu",
        "select_module": "Wybierz moduł (użyj strzałek GÓRA/DÓŁ, ENTER aby potwierdzić)",
        "select_language": "Wybierz język (użyj strzałek GÓRA/DÓŁ, ENTER aby potwierdzić)",
        "select_launcher_language": "Wybierz język launchera (użyj strzałek GÓRA/DÓŁ, ENTER aby potwierdzić)",
        "multiple_installations": "Znaleziono wiele instalacji Warband. Wybierz którą użyć:",
        "play": "Graj",
        "play_wse2": "Graj (WSE2)",
        "select_module": "Wybierz Moduł",
        "settings": "Ustawienia",
        "exit": "Wyjście",
        "back": "Wstecz",
        "game_language": "Język gry",
        "launcher_language": "Język launchera",
        "game_settings": "Ustawienia Gry",
        "video_settings": "Ustawienia Wideo",
        "audio_settings": "Ustawienia Audio",
        "advanced_settings": "Ustawienia Zaawansowane",
        "module": "Moduł",
        "language": "Język",
        "press_enter": "Naciśnij ENTER aby kontynuować...",
        "error_launching": "Błąd uruchamiania gry",
        "error": "Błąd",
        "warning": "OSTRZEŻENIE",
        "language_warning": "Wybrany język \"{selected_lang}\" nie jest dostępny w głównym folderze Languages.\n\nNiektóre elementy interfejsu mogą nie być przetłumaczone i pozostaną w języku angielskim.",
        "found_warband": "Znaleziono Warband",
        "steam_not_running": "Steam nie jest uruchomiony.\n\nProszę uruchomić Steam i zalogować się na swoje konto przed uruchomieniem gry.",
        "launching": "Uruchamianie",
    },
    "tr": {
        "warband_not_found": "Warband bulunamadı",
        "no_modules_found": "Modül bulunamadı",
        "no_module_selected": "Modül seçilmedi",
        "select_module": "Modül seçin (YUKARI/AŞAĞI ok tuşlarını kullanın, onaylamak için ENTER)",
        "select_language": "Dil seçin (YUKARI/AŞAĞI ok tuşlarını kullanın, onaylamak için ENTER)",
        "select_launcher_language": "Launcher dilini seçin (YUKARI/AŞAĞI ok tuşlarını kullanın, onaylamak için ENTER)",
        "multiple_installations": "Birden fazla Warband kurulumu bulundu. Hangisini kullanacağınızı seçin:",
        "play": "Oyna",
        "play_wse2": "Oyna (WSE2)",
        "select_module": "Modül Seç",
        "settings": "Ayarlar",
        "exit": "Çıkış",
        "back": "Geri",
        "game_language": "Oyun Dili",
        "launcher_language": "Launcher Dili",
        "game_settings": "Oyun Ayarları",
        "video_settings": "Video Ayarları",
        "audio_settings": "Ses Ayarları",
        "advanced_settings": "Gelişmiş Ayarlar",
        "module": "Modül",
        "language": "Dil",
        "press_enter": "Devam etmek için ENTER'a basın...",
        "error_launching": "Oyun başlatma hatası",
        "error": "Hata",
        "warning": "UYARI",
        "language_warning": "Seçilen dil \"{selected_lang}\" kök Languages klasöründe mevcut değil.\n\nBazı arayüz öğeleri çevrilmemiş olabilir ve İngilizce kalacaktır.",
        "found_warband": "Warband bulundu",
        "steam_not_running": "Steam çalışmıyor.\n\nLütfen oyunu başlatmadan önce Steam'i başlatın ve hesabınıza giriş yapın.",
        "launching": "Başlatılıyor",
    },
    "ja": {
        "warband_not_found": "Warbandが見つかりません",
        "no_modules_found": "モジュールが見つかりません",
        "no_module_selected": "モジュールが選択されていません",
        "select_module": "モジュールを選択してください（上下矢印キーを使用、ENTERで確認）",
        "select_language": "言語を選択してください（上下矢印キーを使用、ENTERで確認）",
        "select_launcher_language": "ランチャーの言語を選択してください（上下矢印キーを使用、ENTERで確認）",
        "multiple_installations": "複数のWarbandインストールが見つかりました。使用するものを選択してください：",
        "play": "プレイ",
        "play_wse2": "プレイ (WSE2)",
        "select_module": "モジュールを選択",
        "settings": "設定",
        "exit": "終了",
        "back": "戻る",
        "game_language": "ゲーム言語",
        "launcher_language": "ランチャー言語",
        "game_settings": "ゲーム設定",
        "video_settings": "ビデオ設定",
        "audio_settings": "オーディオ設定",
        "advanced_settings": "詳細設定",
        "module": "モジュール",
        "language": "言語",
        "press_enter": "続行するにはENTERキーを押してください...",
        "error_launching": "ゲームの起動エラー",
        "error": "エラー",
        "warning": "警告",
        "language_warning": "選択された言語「{selected_lang}」はルートLanguagesフォルダーで利用できません。\n\n一部のインターフェース要素は翻訳されず、英語のままになる可能性があります。",
        "found_warband": "Warbandが見つかりました",
        "steam_not_running": "Steamが実行されていません。\n\nゲームを起動する前に、Steamを起動してアカウントにログインしてください。",
        "launching": "起動中",
    },
    "zh": {
        "warband_not_found": "未找到Warband",
        "no_modules_found": "未找到模块",
        "no_module_selected": "未选择模块",
        "select_module": "选择模块（使用上下箭头键，ENTER确认）",
        "select_language": "选择语言（使用上下箭头键，ENTER确认）",
        "select_launcher_language": "选择启动器语言（使用上下箭头键，ENTER确认）",
        "multiple_installations": "找到多个Warband安装。选择要使用的：",
        "play": "游戏",
        "play_wse2": "游戏 (WSE2)",
        "select_module": "选择模块",
        "settings": "设置",
        "exit": "退出",
        "back": "返回",
        "game_language": "游戏语言",
        "launcher_language": "启动器语言",
        "game_settings": "游戏设置",
        "video_settings": "视频设置",
        "audio_settings": "音频设置",
        "advanced_settings": "高级设置",
        "module": "模块",
        "language": "语言",
        "press_enter": "按ENTER继续...",
        "error_launching": "启动游戏错误",
        "error": "错误",
        "warning": "警告",
        "language_warning": "所选语言「{selected_lang}」在根Languages文件夹中不可用。\n\n某些界面元素可能未翻译，将保持英语。",
        "found_warband": "找到Warband",
        "steam_not_running": "Steam未运行。\n\n请在启动游戏之前启动Steam并登录您的账户。",
        "launching": "启动中",
    },
    "ko": {
        "warband_not_found": "Warband를 찾을 수 없습니다",
        "no_modules_found": "모듈을 찾을 수 없습니다",
        "no_module_selected": "모듈이 선택되지 않았습니다",
        "select_module": "모듈을 선택하세요 (위/아래 화살표 사용, ENTER로 확인)",
        "select_language": "언어를 선택하세요 (위/아래 화살표 사용, ENTER로 확인)",
        "select_launcher_language": "런처 언어를 선택하세요 (위/아래 화살표 사용, ENTER로 확인)",
        "multiple_installations": "여러 개의 Warband 설치를 찾았습니다. 사용할 것을 선택하세요:",
        "play": "플레이",
        "play_wse2": "플레이 (WSE2)",
        "select_module": "모듈 선택",
        "settings": "설정",
        "exit": "종료",
        "back": "뒤로",
        "game_language": "게임 언어",
        "launcher_language": "런처 언어",
        "game_settings": "게임 설정",
        "video_settings": "비디오 설정",
        "audio_settings": "오디오 설정",
        "advanced_settings": "고급 설정",
        "module": "모듈",
        "language": "언어",
        "press_enter": "계속하려면 ENTER를 누르세요...",
        "error_launching": "게임 실행 오류",
        "error": "오류",
        "warning": "경고",
        "language_warning": "선택한 언어 \"{selected_lang}\"는 루트 Languages 폴더에서 사용할 수 없습니다.\n\n일부 인터페이스 요소는 번역되지 않을 수 있으며 영어로 유지됩니다.",
        "found_warband": "Warband를 찾았습니다",
        "steam_not_running": "Steam이 실행되고 있지 않습니다.\n\n게임을 시작하기 전에 Steam을 시작하고 계정에 로그인하세요.",
        "launching": "시작 중",
    },
}

LAUNCHER_LANGUAGES = ["en", "uk", "be", "ro", "pl", "tr", "ja", "zh", "ko"]

def get_launcher_language_name(lang_code):
    names = {
        "en": "English",
        "uk": "Українська",
        "be": "Беларуская",
        "ro": "Română",
        "pl": "Polski",
        "tr": "Türkçe",
        "ja": "日本語",
        "zh": "中文",
        "ko": "한국어",
    }
    return names.get(lang_code, lang_code.upper())

def t(key, lang="en", **kwargs):
    if lang not in TRANSLATIONS:
        lang = "en"
    translation = TRANSLATIONS[lang].get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        return translation.format(**kwargs)
    return translation

def save_launcher_language_to_registry(language):
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key_path = r'Software\MountAndBladeWarbandKeys'
        
        try:
            key = winreg.OpenKey(reg, key_path, 0, winreg.KEY_WRITE)
        except FileNotFoundError:
            key = winreg.CreateKey(reg, key_path)
        
        winreg.SetValueEx(key, "launcher_language", 0, winreg.REG_SZ, language)
        winreg.CloseKey(key)
        return True
    except Exception:
        return False

def load_launcher_language_from_registry():
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key_path = r'Software\MountAndBladeWarbandKeys'
        
        key = winreg.OpenKey(reg, key_path, 0, winreg.KEY_READ)
        language, _ = winreg.QueryValueEx(key, "launcher_language")
        winreg.CloseKey(key)
        if language in LAUNCHER_LANGUAGES:
            return language
        return "en"
    except (FileNotFoundError, OSError):
        return "en"
    except Exception:
        return "en"

def normalize_path(path):
    return os.path.normpath(os.path.normcase(path))


def find_all_warband_paths(path_to_exe=None):
    found_paths = []
    normalized_paths = set()
    
    if path_to_exe:
        warband_path = os.path.join(path_to_exe, "mb_warband.exe")
        if os.path.exists(warband_path):
            normalized = normalize_path(warband_path)
            if normalized not in normalized_paths:
                normalized_paths.add(normalized)
                found_paths.append(warband_path)
    
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
                            normalized = normalize_path(warband_path)
                            if normalized not in normalized_paths:
                                normalized_paths.add(normalized)
                                found_paths.append(warband_path)
                except (FileNotFoundError, OSError):
                    pass
                try:
                    install_path, _ = winreg.QueryValueEx(a_key, "Install_Path")
                    if install_path and isinstance(install_path, str):
                        warband_path = os.path.join(install_path, "mb_warband.exe")
                        if os.path.exists(warband_path):
                            normalized = normalize_path(warband_path)
                            if normalized not in normalized_paths:
                                normalized_paths.add(normalized)
                                found_paths.append(warband_path)
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
        normalized = normalize_path(warband_path)
        if normalized not in normalized_paths:
            normalized_paths.add(normalized)
            found_paths.append(warband_path)
    
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
                    normalized = normalize_path(steam_warband_path)
                    if normalized not in normalized_paths:
                        normalized_paths.add(normalized)
                        found_paths.append(steam_warband_path)
        except (FileNotFoundError, OSError):
            pass
    except Exception:
        pass
    
    program_files_paths = [
        os.path.join(os.environ.get("ProgramFiles", ""), "Mount&Blade Warband", "mb_warband.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Mount&Blade Warband", "mb_warband.exe"),
        os.path.join(os.environ.get("ProgramFiles", ""), "Steam", "steamapps", "common", "MountBlade Warband", "mb_warband.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Steam", "steamapps", "common", "MountBlade Warband", "mb_warband.exe"),
        r"C:\GOG Games\Mount and Blade - Warband\mb_warband.exe",
    ]
    
    for program_path in program_files_paths:
        if program_path and os.path.exists(program_path):
            normalized = normalize_path(program_path)
            if normalized not in normalized_paths:
                normalized_paths.add(normalized)
                found_paths.append(program_path)
    
    return found_paths


def find_warband_path(path_to_exe=None, lang="en"):
    current_working_dir = os.getcwd()
    warband_exe_in_current = os.path.join(current_working_dir, "mb_warband.exe")
    
    if os.path.exists(warband_exe_in_current):
        return warband_exe_in_current, True
    
    found_paths = find_all_warband_paths(path_to_exe)
    
    if not found_paths:
        return "", False
    
    if len(found_paths) == 1:
        return found_paths[0], True
    
    path_display = []
    for path in found_paths:
        install_dir = os.path.dirname(path)
        path_display.append(f"{install_dir}")
    
    selected_index = select_from_menu(t("multiple_installations", lang), path_display, lang=lang)
    
    if selected_index == -1:
        return "", False
    
    return found_paths[selected_index], True


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


def check_language_in_root(install_directory, lang_code):
    root_languages_path = os.path.join(install_directory, "Languages")
    if not os.path.exists(root_languages_path):
        return False
    
    lang_path = os.path.join(root_languages_path, lang_code)
    return os.path.isdir(lang_path)


def get_languages_list(install_directory, module_name):
    languages = []
    
    module_path = os.path.join(install_directory, "Modules", module_name)
    languages_path = os.path.join(module_path, "languages")
    
    has_en_folder = False
    
    if os.path.exists(languages_path):
        try:
            for item in os.listdir(languages_path):
                item_path = os.path.join(languages_path, item)
                if os.path.isdir(item_path):
                    languages.append(item)
                    if item == "en":
                        has_en_folder = True
        except Exception as e:
            print(f"Error reading languages directory: {e}")
    
    if not has_en_folder:
        languages.insert(0, "en")
    
    return languages


def select_from_menu(title, options, prefix="", lang="en"):
    selected_index = 0
    BOLD = '\033[1m'
    global COLOR_RESET
    global COLOR_ACCENT
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        if prefix:
            print(prefix)
            print()
        print(f"{BOLD}{title}{COLOR_RESET}\n")
        
        for i, option in enumerate(options):
            if i == selected_index:
                print(f"{COLOR_ACCENT}{BOLD}  ▶ {option} ◀{COLOR_RESET}")
            else:
                print(f"    {option}")
        print()
        
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


def select_module(modules, lang="en"):
    if not modules:
        print(t("no_modules_found", lang))
        return None
    
    art = print_warband_art()
    options = modules + [t("back", lang)]
    selected_index = select_from_menu(t("select_module", lang), options, prefix=art, lang=lang)
    
    if selected_index == -1:
        return None
    
    if selected_index == len(modules):
        return None
    
    return modules[selected_index]


def save_language_to_file(language):
    """Save language to Documents folder (for regular game)"""
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

def save_language_to_appdata(language):
    """Save language to AppData folder (for WSE2 launcher)"""
    try:
        appdata = os.environ.get("APPDATA", os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "AppData", "Roaming"))
        wse2_dir = os.path.join(appdata, "Mount&Blade Warband WSE2")
        
        os.makedirs(wse2_dir, exist_ok=True)
        
        language_file = os.path.join(wse2_dir, "language.txt")
        with open(language_file, "w", encoding="utf-8") as f:
            f.write(language)
        return True
    except Exception as e:
        print(f"Error saving language to AppData: {e}")
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


def save_module_to_registry(module_name):
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key_path = r'Software\MountAndBladeWarbandKeys'
        
        try:
            key = winreg.OpenKey(reg, key_path, 0, winreg.KEY_WRITE)
        except FileNotFoundError:
            key = winreg.CreateKey(reg, key_path)
        
        winreg.SetValueEx(key, "last_module_warband", 0, winreg.REG_SZ, module_name)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error saving module to registry: {e}")
        return False

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


def get_language_name(lang_code):
    language_names = {
        "en": "English",
        "cns": "简体中文",
        "cnt": "繁體中文",
        "cz": "Čeština",
        "de": "Deutsch",
        "es": "Español",
        "fr": "Français",
        "hu": "Magyar",
        "pl": "Polski",
        "tr": "Türkçe",
        "ru": "Русский",
        "uk": "Українська",
        "it": "Italiano",
        "pt": "Português",
        "pt_br": "Português (Brasil)",
        "ja": "日本語",
        "ko": "한국어",
        "ar": "العربية",
        "nl": "Nederlands",
        "sv": "Svenska",
        "no": "Norsk",
        "da": "Dansk",
        "fi": "Suomi",
        "ro": "Română",
        "bg": "Български",
        "sr": "Српски",
        "hr": "Hrvatski",
        "sk": "Slovenčina",
        "sl": "Slovenščina",
        "el": "Ελληνικά",
        "he": "עברית",
        "th": "ไทย",
        "vi": "Tiếng Việt",
        "id": "Bahasa Indonesia",
        "ms": "Bahasa Melayu",
        "hi": "हिन्दी",
    }
    
    return language_names.get(lang_code, lang_code.upper())


def show_warning(message, lang="en"):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(message)
    print(f"\n{t('press_enter', lang)}")
    msvcrt.getch()


def select_language(install_directory, module_name, launcher_lang="en"):
    languages = get_languages_list(install_directory, module_name)
    language_names = []
    
    for lang_code in languages:
        lang_name = get_language_name(lang_code)
        language_names.append(f"{lang_name} ({lang_code})")
    
    selected_index = select_from_menu(t("select_language", launcher_lang), language_names, lang=launcher_lang)
    
    if selected_index == -1:
        return None
    
    selected_language = languages[selected_index]
    
    if not check_language_in_root(install_directory, selected_language):
        lang_name = get_language_name(selected_language)
        warning_message = f"""{t("warning", launcher_lang)}

{t("language_warning", lang=launcher_lang, selected_lang=f"{lang_name} ({selected_language})")}"""
        show_warning(warning_message, launcher_lang)
    
    save_language_to_registry(selected_language)
    save_language_to_file(selected_language)
    return selected_language


def select_launcher_language(launcher_lang="en"):
    language_names = []
    for lang_code in LAUNCHER_LANGUAGES:
        lang_name = get_launcher_language_name(lang_code)
        language_names.append(f"{lang_name} ({lang_code})")
    
    selected_index = select_from_menu(t("select_launcher_language", launcher_lang), language_names, lang=launcher_lang)
    
    if selected_index == -1:
        return None
    
    selected_language = LAUNCHER_LANGUAGES[selected_index]
    save_launcher_language_to_registry(selected_language)
    return selected_language


def is_steam_version(install_directory):
    normalized_path = install_directory.lower()
    return "steamapps" in normalized_path or "steam" in normalized_path

def is_steam_running():
    if os.name != 'nt':
        return True
    try:
        result = subprocess.run(['tasklist'], 
                              capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        output_lower = result.stdout.lower()
        return 'steam.exe' in output_lower
    except Exception:
        return False

def show_steam_warning(lang="en"):
    os.system('cls' if os.name == 'nt' else 'clear')
    art = print_warband_art()
    print(art)
    print()
    global COLOR_RESET
    global COLOR_ACCENT
    BOLD = '\033[1m'
    print(f"{COLOR_ACCENT}{BOLD}{t('warning', lang)}{COLOR_RESET}")
    print()
    print(t('steam_not_running', lang))
    print()
    input(f"{t('press_enter', lang)}")

def push_play_button():
    """Find the launcher dialog and click the Play button"""
    user32 = ctypes.windll.user32
    
    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    MK_LBUTTON = 0x0001
    IDC_PLAY_BUTTON = 1029
    
    FindWindowW = user32.FindWindowW
    FindWindowW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
    FindWindowW.restype = ctypes.c_void_p
    
    GetDlgItem = user32.GetDlgItem
    GetDlgItem.argtypes = [ctypes.c_void_p, ctypes.c_int]
    GetDlgItem.restype = ctypes.c_void_p
    
    SendMessageW = user32.SendMessageW
    SendMessageW.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p]
    SendMessageW.restype = ctypes.c_void_p
    
    h_dialog = None
    while h_dialog is None or h_dialog == 0:
        h_dialog = FindWindowW("#32770", "Mount&Blade Warband")
        if h_dialog is None or h_dialog == 0:
            import time
            time.sleep(0.1)
    
    h_play_button = None
    while h_play_button is None or h_play_button == 0:
        h_play_button = GetDlgItem(h_dialog, IDC_PLAY_BUTTON)
        if h_play_button is None or h_play_button == 0:
            import time
            time.sleep(0.1)
    
    SendMessageW(h_play_button, WM_LBUTTONDOWN, MK_LBUTTON, 0)
    SendMessageW(h_play_button, WM_LBUTTONUP, MK_LBUTTON, 0)

def launch_wse2(install_directory, module_name, lang="en"):
    """Launch mb_warband_wse2.exe with module parameter"""
    wse2_exe = os.path.join(install_directory, "mb_warband_wse2.exe")
    
    if not os.path.exists(wse2_exe):
        print(f"{t('error', lang)}: mb_warband_wse2.exe not found at {wse2_exe}")
        input(f"{t('press_enter', lang)}")
        return False
    
    try:
        # Save language before launching (same as regular launch)
        # WSE2 launcher reads from AppData, while regular game reads from Documents
        # Save to both locations to ensure compatibility
        save_language_to_registry(lang)
        save_language_to_file(lang)  # For regular game
        save_language_to_appdata(lang)  # For WSE2 launcher (reads from %APPDATA%\Mount&Blade Warband WSE2\language.txt)
        
        # Use cmd.exe /c start to launch WSE2 with module parameter
        # Module name is passed without quotes, preserving spaces
        # WSE2 reads language from AppData folder, so we don't need --language parameter
        command = f'start mb_warband_wse2.exe --module {module_name} --no-intro'
        
        subprocess.Popen(
            command,
            shell=True,
            cwd=install_directory
        )
        return True
    except Exception as e:
        print(f"{t('error_launching', lang)}: {e}")
        input(f"{t('press_enter', lang)}")
        return False

def launch_game(install_directory, module_name, lang="en"):
    if is_steam_version(install_directory):
        if not is_steam_running():
            show_steam_warning(lang)
            return False
    
    warband_exe = os.path.join(install_directory, "mb_warband.exe")
    
    if not os.path.exists(warband_exe):
        print(f"{t('error', lang)}: mb_warband.exe not found at {warband_exe}")
        input(f"{t('press_enter', lang)}")
        return False
    
    try:
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        
        HIGH_PRIORITY_CLASS = 0x00000080
        INFINITE = 0xFFFFFFFF
        
        class STARTUPINFO(ctypes.Structure):
            _fields_ = [
                ("cb", ctypes.c_uint),
                ("lpReserved", ctypes.c_wchar_p),
                ("lpDesktop", ctypes.c_wchar_p),
                ("lpTitle", ctypes.c_wchar_p),
                ("dwX", ctypes.c_uint),
                ("dwY", ctypes.c_uint),
                ("dwXSize", ctypes.c_uint),
                ("dwYSize", ctypes.c_uint),
                ("dwXCountChars", ctypes.c_uint),
                ("dwYCountChars", ctypes.c_uint),
                ("dwFillAttribute", ctypes.c_uint),
                ("dwFlags", ctypes.c_uint),
                ("wShowWindow", ctypes.c_ushort),
                ("cbReserved2", ctypes.c_ushort),
                ("lpReserved2", ctypes.c_void_p),
                ("hStdInput", ctypes.c_void_p),
                ("hStdOutput", ctypes.c_void_p),
                ("hStdError", ctypes.c_void_p),
            ]
        
        class PROCESS_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("hProcess", ctypes.c_void_p),
                ("hThread", ctypes.c_void_p),
                ("dwProcessId", ctypes.c_uint),
                ("dwThreadId", ctypes.c_uint),
            ]
        
        CreateProcessW = kernel32.CreateProcessW
        CreateProcessW.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_bool,
            ctypes.c_uint,
            ctypes.c_void_p,
            ctypes.c_wchar_p,
            ctypes.POINTER(STARTUPINFO),
            ctypes.POINTER(PROCESS_INFORMATION)
        ]
        CreateProcessW.restype = ctypes.c_bool
        
        WaitForInputIdle = user32.WaitForInputIdle
        WaitForInputIdle.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        WaitForInputIdle.restype = ctypes.c_uint
        
        si = STARTUPINFO()
        si.cb = ctypes.sizeof(STARTUPINFO)
        pi = PROCESS_INFORMATION()
        
        save_module_to_registry(module_name)
        save_module_to_file(module_name)
        
        warband_path = os.path.abspath(warband_exe)
        
        if not CreateProcessW(
            warband_path,
            None,
            None,
            None,
            False,
            HIGH_PRIORITY_CLASS,
            None,
            install_directory,
            ctypes.byref(si),
            ctypes.byref(pi)
        ):
            error_code = kernel32.GetLastError()
            print(f"{t('error_launching', lang)}: CreateProcess failed with error {error_code}")
            input(f"{t('press_enter', lang)}")
            return False
        
        WaitForInputIdle(pi.hProcess, INFINITE)
        
        import time
        time.sleep(0.5)
        
        push_play_button()
        
        import time
        time.sleep(1.0)
        
        return True
    except Exception as e:
        print(f"{t('error_launching', lang)}: {e}")
        input(f"{t('press_enter', lang)}")
        return False


def print_warband_art():
    global COLOR_ACCENT
    global COLOR_RESET
    
    art_lines = [
        " /$$      /$$                     /$$                                 /$$ /$$   /$$",
        "| $$  /$ | $$                    | $$                                | $$| $$  / $$",
        "| $$ /$$$| $$  /$$$$$$   /$$$$$$ | $$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$$|  $$/ $$/",
        "| $$/$$ $$ $$ |____  $$ /$$__  $$| $$__  $$ |____  $$| $$__  $$ /$$__  $$ \\  $$$$/ ",
        "| $$$$_  $$$$  /$$$$$$$| $$  \\__/| $$  \\ $$  /$$$$$$$| $$  \\ $$| $$  | $$  >$$  $$ ",
        "| $$$/ \\  $$$ /$$__  $$| $$      | $$  | $$ /$$__  $$| $$  | $$| $$  | $$ /$$/\\  $$",
        "| $$/   \\  $$|  $$$$$$$| $$      | $$$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$$| $$  \\ $$",
        "|__/     \\__/ \\_______/|__/      |_______/  \\_______/|__/  |__/ \\_______/|__/  |__/"
    ]
    
    colored_art = "\n".join([f"{COLOR_ACCENT}{line}{COLOR_RESET}" for line in art_lines])
    return colored_art


def get_rgl_config_path():
    user_profile = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    return os.path.join(user_profile, "Documents", "Mount&Blade Warband", "rgl_config.txt")


def read_rgl_config():
    config = {}
    config_path = get_rgl_config_path()
    
    if not os.path.exists(config_path):
        return config
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    try:
                        if "." in value:
                            config[key] = float(value)
                        else:
                            config[key] = int(value)
                    except ValueError:
                        config[key] = value
    except Exception:
        pass
    
    return config


def write_rgl_config(config):
    config_path = get_rgl_config_path()
    config_dir = os.path.dirname(config_path)
    os.makedirs(config_dir, exist_ok=True)
    
    try:
        existing_config = read_rgl_config()
        existing_config.update(config)
        
        if os.path.exists(config_path):
            lines = []
            with open(config_path, "r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if not stripped or stripped.startswith("#"):
                        lines.append((line.rstrip("\n\r"), None))
                    elif "=" in stripped:
                        key = stripped.split("=", 1)[0].strip()
                        if key in existing_config:
                            value = existing_config[key]
                            if isinstance(value, float):
                                lines.append((None, f"{key} = {value}"))
                            else:
                                lines.append((None, f"{key} = {value}"))
                        else:
                            lines.append((line.rstrip("\n\r"), None))
                    else:
                        lines.append((line.rstrip("\n\r"), None))
            
            with open(config_path, "w", encoding="utf-8") as f:
                for original, new_line in lines:
                    if new_line:
                        f.write(new_line + "\n")
                    else:
                        f.write(original + "\n")
        else:
            with open(config_path, "w", encoding="utf-8") as f:
                for key, value in existing_config.items():
                    if isinstance(value, float):
                        f.write(f"{key} = {value}\n")
                    else:
                        f.write(f"{key} = {value}\n")
        return True
    except Exception:
        return False


def select_toggle_option(title, options_with_keys, prefix="", lang="en"):
    selected_index = 0
    BOLD = '\033[1m'
    global COLOR_RESET
    global COLOR_ACCENT
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        if prefix:
            print(prefix)
            print()
        print(f"{BOLD}{title}{COLOR_RESET}\n")
        
        for i, (option_text, config_key) in enumerate(options_with_keys):
            current_value = get_config_value(config_key, 0)
            checkbox = "[✓]" if current_value == 1 else "[ ]"
            
            if i == selected_index:
                print(f"{COLOR_ACCENT}{BOLD}  ▶ {checkbox} {option_text} ◀{COLOR_RESET}")
            else:
                print(f"    {checkbox} {option_text}")
        
        key = msvcrt.getch()
        
        if key == b'\xe0' or key == b'\x00':
            key2 = msvcrt.getch()
            if key2 == b'H':
                selected_index = max(0, selected_index - 1)
            elif key2 == b'P':
                selected_index = min(len(options_with_keys) - 1, selected_index + 1)
        elif key == b'\r' or key == b'\n':
            config_key = options_with_keys[selected_index][1]
            toggle_config_value(config_key)
        elif key == b'\x1b':
            return
        elif key == b'w' or key == b'W':
            selected_index = max(0, selected_index - 1)
        elif key == b's' or key == b'S':
            selected_index = min(len(options_with_keys) - 1, selected_index + 1)


def get_config_value(key, default=0):
    config = read_rgl_config()
    return config.get(key, default)


def set_config_value(key, value):
    return write_rgl_config({key: value})


def toggle_config_value(key, default=0):
    current = get_config_value(key, default)
    new_value = 1 if current == 0 else 0
    set_config_value(key, new_value)
    return new_value


def settings_menu(install_directory, modules, module_name, current_language, launcher_lang="en"):
    art = print_warband_art()
    while True:
        options = [
            t("game_language", launcher_lang),
            t("launcher_language", launcher_lang),
            t("game_settings", launcher_lang),
            t("video_settings", launcher_lang),
            t("audio_settings", launcher_lang),
            t("advanced_settings", launcher_lang),
            t("back", launcher_lang)
        ]
        selected = select_from_menu(t("settings", launcher_lang), options, art, lang=launcher_lang)
        
        if selected == -1:
            return current_language, launcher_lang
        
        if selected == 0:
            new_language = select_language(install_directory, module_name, launcher_lang)
            if new_language:
                current_language = new_language
        elif selected == 1:
            new_launcher_lang = select_launcher_language(launcher_lang)
            if new_launcher_lang:
                launcher_lang = new_launcher_lang
        elif selected == 2:
            game_settings_menu(launcher_lang)
        elif selected == 3:
            video_settings_menu(launcher_lang)
        elif selected == 4:
            audio_settings_menu(launcher_lang)
        elif selected == 5:
            advanced_settings_menu(launcher_lang)
        elif selected == 6:
            return current_language, launcher_lang


def game_settings_menu(launcher_lang="en"):
    art = print_warband_art()
    options_with_keys = [
        ("Hide Blood", "enable_blood"),
        ("Enable Cheats", "cheat_mode")
    ]
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(art)
        print()
        BOLD = '\033[1m'
        global COLOR_RESET
        global COLOR_ACCENT
        print(f"{BOLD}{t('game_settings', launcher_lang)}{COLOR_RESET}\n")
        
        selected_index = 0
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(art)
            print()
            print(f"{BOLD}{t('game_settings', launcher_lang)}{COLOR_RESET}\n")
            
            for i, (option_text, config_key) in enumerate(options_with_keys):
                current_value = get_config_value(config_key, 0)
                if config_key == "enable_blood":
                    current_value = 0 if current_value == 1 else 1
                checkbox = "[✓]" if current_value == 1 else "[ ]"
                
                if i == selected_index:
                    print(f"{COLOR_ACCENT}{BOLD}  ▶ {checkbox} {option_text} ◀{COLOR_RESET}")
                else:
                    print(f"    {checkbox} {option_text}")
            
            if len(options_with_keys) == selected_index:
                print(f"{COLOR_ACCENT}{BOLD}  ▶ {t('back', launcher_lang)} ◀{COLOR_RESET}")
            else:
                print(f"    {t('back', launcher_lang)}")
            
            key = msvcrt.getch()
            
            if key == b'\xe0' or key == b'\x00':
                key2 = msvcrt.getch()
                if key2 == b'H':
                    selected_index = max(0, selected_index - 1)
                elif key2 == b'P':
                    selected_index = min(len(options_with_keys), selected_index + 1)
            elif key == b'\r' or key == b'\n':
                if selected_index == len(options_with_keys):
                    return
                config_key = options_with_keys[selected_index][1]
                if config_key == "enable_blood":
                    current = get_config_value(config_key, 1)
                    set_config_value(config_key, 0 if current == 1 else 1)
                else:
                    toggle_config_value(config_key)
            elif key == b'\x1b':
                return
            elif key == b'w' or key == b'W':
                selected_index = max(0, selected_index - 1)
            elif key == b's' or key == b'S':
                selected_index = min(len(options_with_keys), selected_index + 1)


def select_from_list(title, options, current_index=0, prefix="", lang="en"):
    selected_index = current_index
    BOLD = '\033[1m'
    global COLOR_RESET
    global COLOR_ACCENT
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        if prefix:
            print(prefix)
            print()
        print(f"{BOLD}{title}{COLOR_RESET}\n")
        
        for i, option in enumerate(options):
            if i == selected_index:
                print(f"{COLOR_ACCENT}{BOLD}  ▶ {option} ◀{COLOR_RESET}")
            else:
                print(f"    {option}")
        
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


def select_number(title, min_val, max_val, current_val, prefix="", lang="en"):
    value = current_val
    BOLD = '\033[1m'
    global COLOR_RESET
    global COLOR_ACCENT
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        if prefix:
            print(prefix)
            print()
        print(f"{BOLD}{title}{COLOR_RESET}\n")
        print(f"    {COLOR_ACCENT}{BOLD}Value: {value}{COLOR_RESET}")
        print()
        print("Use UP/DOWN arrows or +/- to change value")
        print(f"{t('press_enter', launcher_lang)}")
        print(f"{t('back', lang)} (ESC)")
        
        key = msvcrt.getch()
        
        if key == b'\xe0' or key == b'\x00':
            key2 = msvcrt.getch()
            if key2 == b'H':
                value = min(max_val, value + 1)
            elif key2 == b'P':
                value = max(min_val, value - 1)
        elif key == b'+' or key == b'=':
            value = min(max_val, value + 1)
        elif key == b'-' or key == b'_':
            value = max(min_val, value - 1)
        elif key == b'\r' or key == b'\n':
            return value
        elif key == b'\x1b':
            return None
        elif key == b'w' or key == b'W':
            value = min(max_val, value + 1)
        elif key == b's' or key == b'S':
            value = max(min_val, value - 1)


def video_settings_menu(launcher_lang="en"):
    art = print_warband_art()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(art)
        print()
        BOLD = '\033[1m'
        global COLOR_RESET
        global COLOR_ACCENT
        
        use_pixel_shaders = get_config_value("use_pixel_shaders", 1)
        start_windowed = get_config_value("start_windowed", 0)
        show_framerate = get_config_value("show_framerate", 1)
        force_vsync = get_config_value("force_vsync", 1)
        use_ondemand_textures = get_config_value("use_ondemand_textures_", 0)
        texture_detail = get_config_value("texture_detail", 100)
        max_framerate = get_config_value("max_framerate", 100)
        
        display_width = get_config_value("display_width", 0)
        display_height = get_config_value("display_height", 0)
        resolution_text = "Use Desktop Resolution" if display_width == 0 and display_height == 0 else f"{display_width}x{display_height}"
        
        antialiasing = get_config_value("antialiasing", 0)
        antialiasing_options = ["Off", "2x", "4x", "8x"]
        antialiasing_text = antialiasing_options[min(antialiasing, len(antialiasing_options) - 1)] if antialiasing < len(antialiasing_options) else "Off"
        
        shadowmap_quality = get_config_value("shadowmap_quality", 1)
        shadow_options = ["Low", "Medium", "High"]
        shadow_text = shadow_options[min(shadowmap_quality, len(shadow_options) - 1)] if shadowmap_quality < len(shadow_options) else "High"
        
        options = [
            f"{'[✓]' if use_pixel_shaders == 1 else '[ ]'} Use Pixel Shaders",
            f"{'[✓]' if start_windowed == 1 else '[ ]'} Start Windowed",
            f"{'[✓]' if show_framerate == 1 else '[ ]'} Show Framerate",
            f"{'[✓]' if force_vsync == 1 else '[ ]'} Force Vertical Sync",
            f"{'[✓]' if use_ondemand_textures == 1 else '[ ]'} Load Textures On Demand",
            f"Texture Detail: {texture_detail}",
            f"Max Frame Rate: {max_framerate}",
            f"Screen Resolution: {resolution_text}",
            f"Antialiasing: {antialiasing_text}",
            f"Shadow Quality: {shadow_text}",
            t("back", launcher_lang)
        ]
        
        print(f"{BOLD}{t('video_settings', launcher_lang)}{COLOR_RESET}\n")
        
        selected_index = 0
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(art)
            print()
            print(f"{BOLD}{t('video_settings', launcher_lang)}{COLOR_RESET}\n")
            
            use_pixel_shaders = get_config_value("use_pixel_shaders", 1)
            start_windowed = get_config_value("start_windowed", 0)
            show_framerate = get_config_value("show_framerate", 1)
            force_vsync = get_config_value("force_vsync", 1)
            use_ondemand_textures = get_config_value("use_ondemand_textures_", 0)
            texture_detail = get_config_value("texture_detail", 100)
            max_framerate = get_config_value("max_framerate", 100)
            
            display_width = get_config_value("display_width", 0)
            display_height = get_config_value("display_height", 0)
            resolution_text = "Use Desktop Resolution" if display_width == 0 and display_height == 0 else f"{display_width}x{display_height}"
            
            antialiasing = get_config_value("antialiasing", 0)
            antialiasing_options = ["Off", "2x", "4x", "8x"]
            antialiasing_text = antialiasing_options[min(antialiasing, len(antialiasing_options) - 1)] if antialiasing < len(antialiasing_options) else "Off"
            
            shadowmap_quality = get_config_value("shadowmap_quality", 1)
            shadow_options = ["Low", "Medium", "High"]
            shadow_text = shadow_options[min(shadowmap_quality, len(shadow_options) - 1)] if shadowmap_quality < len(shadow_options) else "High"
            
            options = [
                f"{'[✓]' if use_pixel_shaders == 1 else '[ ]'} Use Pixel Shaders",
                f"{'[✓]' if start_windowed == 1 else '[ ]'} Start Windowed",
                f"{'[✓]' if show_framerate == 1 else '[ ]'} Show Framerate",
                f"{'[✓]' if force_vsync == 1 else '[ ]'} Force Vertical Sync",
                f"{'[✓]' if use_ondemand_textures == 1 else '[ ]'} Load Textures On Demand",
                f"Texture Detail: {texture_detail}",
                f"Max Frame Rate: {max_framerate}",
                f"Screen Resolution: {resolution_text}",
                f"Antialiasing: {antialiasing_text}",
                f"Shadow Quality: {shadow_text}",
                t("back", launcher_lang)
            ]
            
            for i, option in enumerate(options):
                if i == selected_index:
                    print(f"{COLOR_ACCENT}{BOLD}  ▶ {option} ◀{COLOR_RESET}")
                else:
                    print(f"    {option}")
            
            key = msvcrt.getch()
            
            if key == b'\xe0' or key == b'\x00':
                key2 = msvcrt.getch()
                if key2 == b'H':
                    selected_index = max(0, selected_index - 1)
                elif key2 == b'P':
                    selected_index = min(len(options) - 1, selected_index + 1)
            elif key == b'\r' or key == b'\n':
                if selected_index == len(options) - 1:
                    return
                elif selected_index == 0:
                    toggle_config_value("use_pixel_shaders", 1)
                elif selected_index == 1:
                    toggle_config_value("start_windowed", 0)
                elif selected_index == 2:
                    toggle_config_value("show_framerate", 1)
                elif selected_index == 3:
                    toggle_config_value("force_vsync", 1)
                elif selected_index == 4:
                    toggle_config_value("use_ondemand_textures_", 0)
                elif selected_index == 5:
                    new_value = select_number("Texture Detail", 10, 100, texture_detail, art, launcher_lang)
                    if new_value is not None:
                        set_config_value("texture_detail", new_value)
                elif selected_index == 6:
                    new_value = select_number("Max Frame Rate", 30, 200, max_framerate, art, launcher_lang)
                    if new_value is not None:
                        set_config_value("max_framerate", new_value)
                elif selected_index == 7:
                    resolutions = [
                        "Use Desktop Resolution",
                        "640x480 32 bits",
                        "800x600 32 bits",
                        "1024x768 32 bits",
                        "1280x720 32 bits",
                        "1280x1024 32 bits",
                        "1366x768 32 bits",
                        "1920x1080 32 bits"
                    ]
                    current_res_index = 0
                    if display_width == 640 and display_height == 480:
                        current_res_index = 1
                    elif display_width == 800 and display_height == 600:
                        current_res_index = 2
                    elif display_width == 1024 and display_height == 768:
                        current_res_index = 3
                    elif display_width == 1280 and display_height == 720:
                        current_res_index = 4
                    elif display_width == 1280 and display_height == 1024:
                        current_res_index = 5
                    elif display_width == 1366 and display_height == 768:
                        current_res_index = 6
                    elif display_width == 1920 and display_height == 1080:
                        current_res_index = 7
                    
                    selected_res = select_from_list("Screen Resolution", resolutions, current_res_index, art, launcher_lang)
                    if selected_res >= 0:
                        if selected_res == 0:
                            set_config_value("display_width", 0)
                            set_config_value("display_height", 0)
                        elif selected_res == 1:
                            set_config_value("display_width", 640)
                            set_config_value("display_height", 480)
                        elif selected_res == 2:
                            set_config_value("display_width", 800)
                            set_config_value("display_height", 600)
                        elif selected_res == 3:
                            set_config_value("display_width", 1024)
                            set_config_value("display_height", 768)
                        elif selected_res == 4:
                            set_config_value("display_width", 1280)
                            set_config_value("display_height", 720)
                        elif selected_res == 5:
                            set_config_value("display_width", 1280)
                            set_config_value("display_height", 1024)
                        elif selected_res == 6:
                            set_config_value("display_width", 1366)
                            set_config_value("display_height", 768)
                        elif selected_res == 7:
                            set_config_value("display_width", 1920)
                            set_config_value("display_height", 1080)
                elif selected_index == 8:
                    current_aa = get_config_value("antialiasing", 0)
                    aa_options = ["Off", "2x", "4x", "8x"]
                    selected_aa = select_from_list("Antialiasing", aa_options, min(current_aa, len(aa_options) - 1), art, launcher_lang)
                    if selected_aa >= 0:
                        set_config_value("antialiasing", selected_aa)
                elif selected_index == 9:
                    current_shadow = get_config_value("shadowmap_quality", 1)
                    shadow_options = ["Low", "Medium", "High"]
                    selected_shadow = select_from_list("Shadow Quality", shadow_options, min(current_shadow, len(shadow_options) - 1), art, launcher_lang)
                    if selected_shadow >= 0:
                        set_config_value("shadowmap_quality", selected_shadow)
            elif key == b'\x1b':
                return
            elif key == b'w' or key == b'W':
                selected_index = max(0, selected_index - 1)
            elif key == b's' or key == b'S':
                selected_index = min(len(options) - 1, selected_index + 1)


def audio_settings_menu(launcher_lang="en"):
    art = print_warband_art()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(art)
        print()
        BOLD = '\033[1m'
        global COLOR_RESET
        global COLOR_ACCENT
        
        disable_frequency_variation = get_config_value("disable_frequency_variation", 0)
        disable_sound = get_config_value("disable_sound", 0)
        disable_music = get_config_value("disable_music", 0)
        
        options = [
            f"{'[✓]' if disable_frequency_variation == 0 else '[ ]'} Enable Sound Variation",
            f"{'[✓]' if disable_sound == 0 else '[ ]'} Enable Sound",
            f"{'[✓]' if disable_music == 0 else '[ ]'} Enable Music",
            t("back", launcher_lang)
        ]
        
        print(f"{BOLD}{t('audio_settings', launcher_lang)}{COLOR_RESET}\n")
        
        selected_index = 0
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(art)
            print()
            print(f"{BOLD}{t('audio_settings', launcher_lang)}{COLOR_RESET}\n")
            
            disable_frequency_variation = get_config_value("disable_frequency_variation", 0)
            disable_sound = get_config_value("disable_sound", 0)
            disable_music = get_config_value("disable_music", 0)
            
            options = [
                f"{'[✓]' if disable_frequency_variation == 0 else '[ ]'} Enable Sound Variation",
                f"{'[✓]' if disable_sound == 0 else '[ ]'} Enable Sound",
                f"{'[✓]' if disable_music == 0 else '[ ]'} Enable Music",
                t("back", launcher_lang)
            ]
            
            for i, option in enumerate(options):
                if i == selected_index:
                    print(f"{COLOR_ACCENT}{BOLD}  ▶ {option} ◀{COLOR_RESET}")
                else:
                    print(f"    {option}")
            
            key = msvcrt.getch()
            
            if key == b'\xe0' or key == b'\x00':
                key2 = msvcrt.getch()
                if key2 == b'H':
                    selected_index = max(0, selected_index - 1)
                elif key2 == b'P':
                    selected_index = min(len(options) - 1, selected_index + 1)
            elif key == b'\r' or key == b'\n':
                if selected_index == 0:
                    toggle_config_value("disable_frequency_variation", 0)
                elif selected_index == 1:
                    toggle_config_value("disable_sound", 0)
                elif selected_index == 2:
                    toggle_config_value("disable_music", 0)
                elif selected_index == 3:
                    return
            elif key == b'\x1b':
                return
            elif key == b'w' or key == b'W':
                selected_index = max(0, selected_index - 1)
            elif key == b's' or key == b'S':
                selected_index = min(len(options) - 1, selected_index + 1)


def advanced_settings_menu(launcher_lang="en"):
    art = print_warband_art()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(art)
        print()
        BOLD = '\033[1m'
        global COLOR_RESET
        global COLOR_ACCENT
        
        enable_edit_mode = get_config_value("enable_edit_mode", 0)
        force_single_threading = get_config_value("force_single_threading", 0)
        
        options = [
            f"{'[✓]' if enable_edit_mode == 1 else '[ ]'} Enable Edit Mode (Be warned, this slows down the game.)",
            f"{'[✓]' if force_single_threading == 1 else '[ ]'} Force Single Threading",
            t("back", launcher_lang)
        ]
        
        print(f"{BOLD}{t('advanced_settings', launcher_lang)}{COLOR_RESET}\n")
        
        selected_index = 0
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(art)
            print()
            print(f"{BOLD}{t('advanced_settings', launcher_lang)}{COLOR_RESET}\n")
            
            enable_edit_mode = get_config_value("enable_edit_mode", 0)
            force_single_threading = get_config_value("force_single_threading", 0)
            
            options = [
                f"{'[✓]' if enable_edit_mode == 1 else '[ ]'} Enable Edit Mode (Be warned, this slows down the game.)",
                f"{'[✓]' if force_single_threading == 1 else '[ ]'} Force Single Threading",
                t("back", launcher_lang)
            ]
            
            for i, option in enumerate(options):
                if i == selected_index:
                    print(f"{COLOR_ACCENT}{BOLD}  ▶ {option} ◀{COLOR_RESET}")
                else:
                    print(f"    {option}")
            
            key = msvcrt.getch()
            
            if key == b'\xe0' or key == b'\x00':
                key2 = msvcrt.getch()
                if key2 == b'H':
                    selected_index = max(0, selected_index - 1)
                elif key2 == b'P':
                    selected_index = min(len(options) - 1, selected_index + 1)
            elif key == b'\r' or key == b'\n':
                if selected_index == 0:
                    toggle_config_value("enable_edit_mode", 0)
                elif selected_index == 1:
                    toggle_config_value("force_single_threading", 0)
                elif selected_index == 2:
                    return
            elif key == b'\x1b':
                return
            elif key == b'w' or key == b'W':
                selected_index = max(0, selected_index - 1)
            elif key == b's' or key == b'S':
                selected_index = min(len(options) - 1, selected_index + 1)


def main_menu(install_directory, modules, module_name, current_language="en", launcher_lang="en"):
    art = print_warband_art()
    wse2_exists = os.path.exists(os.path.join(install_directory, "mb_warband_wse2.exe"))
    
    while True:
        options = [t("play", launcher_lang)]
        if wse2_exists:
            options.append(t("play_wse2", launcher_lang))
        options.extend([t("select_module", launcher_lang), t("settings", launcher_lang), t("exit", launcher_lang)])
        
        selected = select_from_menu(f"{t('module', launcher_lang)}: {module_name} | {t('language', launcher_lang)}: {current_language}", options, art, lang=launcher_lang)
        
        if selected == -1:
            continue
        
        if selected == 0:
            if launch_game(install_directory, module_name, launcher_lang):
                sys.exit(0)
        elif selected == 1:
            if wse2_exists:
                if launch_wse2(install_directory, module_name, current_language):
                    sys.exit(0)
            else:
                new_module = select_module(modules, launcher_lang)
                if new_module and new_module != module_name:
                    module_name = new_module
                    save_module_to_file(module_name)
                    save_language_to_file("en")
                    current_language = "en"
        elif selected == 2:
            if wse2_exists:
                new_module = select_module(modules, launcher_lang)
                if new_module and new_module != module_name:
                    module_name = new_module
                    save_module_to_file(module_name)
                    save_language_to_file("en")
                    current_language = "en"
            else:
                new_language, new_launcher_lang = settings_menu(install_directory, modules, module_name, current_language, launcher_lang)
                current_language = new_language
                if new_launcher_lang != launcher_lang:
                    launcher_lang = new_launcher_lang
        elif selected == 3:
            if wse2_exists:
                new_language, new_launcher_lang = settings_menu(install_directory, modules, module_name, current_language, launcher_lang)
                current_language = new_language
                if new_launcher_lang != launcher_lang:
                    launcher_lang = new_launcher_lang
            else:
                return
        elif selected == 4:
            return


if __name__ == "__main__":
    launcher_lang = load_launcher_language_from_registry()
    
    warband_path, success = find_warband_path(lang=launcher_lang)
    if success:
        print(f"{t('found_warband', launcher_lang)}: {warband_path}")
    else:
        print(t("warband_not_found", launcher_lang))
        input(f"{t('press_enter', launcher_lang)}")
        exit()

    install_directory = get_install_directory(warband_path)
    modules = get_modules_list(install_directory)
    
    if not modules:
        print(t("no_modules_found", launcher_lang))
        input(f"{t('press_enter', launcher_lang)}")
        exit()
    
    saved_module = load_module_from_file()
    selected_module = saved_module if saved_module and saved_module in modules else None
    
    if not selected_module:
        selected_module = select_module(modules, launcher_lang)
        if not selected_module:
            print(f"\n{t('no_module_selected', launcher_lang)}")
            input(f"{t('press_enter', launcher_lang)}")
            exit()
        save_module_to_file(selected_module)
        save_language_to_file("en")
        saved_language = "en"
    else:
        saved_language = load_language_from_file()
    
    main_menu(install_directory, modules, selected_module, saved_language, launcher_lang)