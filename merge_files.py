import os
import sys
import json
import datetime
import textwrap
import shlex
import urllib.parse
import time
import atexit
from pathlib import Path

C_BLUE = "\033[38;2;0;175;255m"
C_YELLOW = "\033[38;2;248;246;117m"
C_GRAY = "\033[38;2;110;110;110m"
C_WHITE = "\033[38;2;210;210;210m"
C_DARK_GRAY = "\033[38;2;80;80;80m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"
C_BG_INPUT = "\033[48;2;45;45;45m"

COLOR_NORMAL = {
    "blue": "\033[38;2;0;175;255m",
    "yellow": "\033[38;2;248;246;117m",
    "gray": "\033[38;2;110;110;110m",
    "white": "\033[38;2;210;210;210m",
    "dark_gray": "\033[38;2;80;80;80m",
    "bold": "\033[1m",
    "bg_input": "\033[48;2;45;45;45m"
}

COLOR_DIM = {
    "blue": "\033[38;2;0;65;95m",
    "yellow": "\033[38;2;95;94;45m",
    "gray": "\033[38;2;42;42;42m",
    "white": "\033[38;2;78;78;78m",
    "dark_gray": "\033[38;2;28;28;28m",
    "bold": "",
    "bg_input": "\033[48;2;22;22;22m"
}

def set_color_mode(dimmed=False):
    global C_BLUE, C_YELLOW, C_GRAY, C_WHITE, C_DARK_GRAY, C_BOLD, C_BG_INPUT
    palette = COLOR_DIM if dimmed else COLOR_NORMAL
    C_BLUE = palette["blue"]
    C_YELLOW = palette["yellow"]
    C_GRAY = palette["gray"]
    C_WHITE = palette["white"]
    C_DARK_GRAY = palette["dark_gray"]
    C_BOLD = palette["bold"]
    C_BG_INPUT = palette["bg_input"]

old_mode_in = None
old_mode_out = None

if sys.platform == 'win32':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    hStdIn = kernel32.GetStdHandle(-10)
    mode = ctypes.c_uint32()
    kernel32.GetConsoleMode(hStdIn, ctypes.byref(mode))
    old_mode_in = mode.value
    new_mode = (mode.value & ~0x0040) | 0x0010 | 0x0080 | 0x0200
    kernel32.SetConsoleMode(hStdIn, new_mode)
    
    hStdOut = kernel32.GetStdHandle(-11)
    mode_out = ctypes.c_uint32()
    kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode_out))
    old_mode_out = mode_out.value
    new_mode_out = mode_out.value | 0x0004
    kernel32.SetConsoleMode(hStdOut, new_mode_out)

def restore_console():
    if sys.platform == 'win32' and old_mode_in is not None:
        kernel32.SetConsoleMode(hStdIn, old_mode_in)
        kernel32.SetConsoleMode(hStdOut, old_mode_out)

atexit.register(restore_console)

MEMORY_FILE = Path.home() / ".merge_files_memory.json"

T = {
    "en": {
        "commands": "Commands",
        "actions": "Actions",
        "start": "Start extraction",
        "settings": "Settings",
        "system": "System",
        "output_path": "Output path",
        "language": "Language",
        "lang_name": "English",
        "tip_main": "Type number to select, 'esc' to go back, or Ctrl+C to exit",
        "action": "Action:",
        "change_path": "Change output path",
        "change_lang": "Change language",
        "new_path": "New path:",
        "path_updated": "Path successfully updated.",
        "press_enter": "Press Enter to continue",
        "press_enter_return": "Press Enter to return",
        "lang_updated": "Language successfully updated.",
        "target_dir": "Target Directory",
        "input": "Input",
        "enter_path": "Enter path, or Drag & Drop folder/files here",
        "path": "Path:",
        "err_not_found": "Error: Path or file not found.",
        "err_permission": "Error: Access denied (PermissionError).",
        "err_empty": "Folder is empty.",
        "select_files": "Select Files",
        "dir": "Directory",
        "files": "Files",
        "selected": "Selected:",
        "of": "of",
        "tip_toggle": "Type numbers to toggle, 0 to start, or Drag & Drop additional files here",
        "toggle": "Toggle:",
        "err_no_selected": "No files selected.",
        "success": "Success",
        "success_msg": "Data extracted successfully.",
        "output_loc": "Output location",
        "err_save": "Save error:"
    },
    "ru": {
        "commands": "Команды",
        "actions": "Действия",
        "start": "Начать извлечение",
        "settings": "Настройки",
        "system": "Система",
        "output_path": "Путь сохранения",
        "language": "Язык",
        "lang_name": "Русский",
        "tip_main": "Введите номер для выбора, 'esc' для возврата, или Ctrl+C для выхода",
        "action": "Действие:",
        "change_path": "Изменить путь сохранения",
        "change_lang": "Изменить язык",
        "new_path": "Новый путь:",
        "path_updated": "Путь успешно обновлен.",
        "press_enter": "Нажмите Enter для продолжения",
        "press_enter_return": "Нажмите Enter для возврата",
        "lang_updated": "Язык успешно обновлен.",
        "target_dir": "Целевая папка",
        "input": "Ввод",
        "enter_path": "Введите путь, либо перетащите папку/файлы (Drag & Drop)",
        "path": "Путь:",
        "err_not_found": "Ошибка: Путь или файл не найден.",
        "err_permission": "Ошибка: Нет доступа к папке (PermissionError).",
        "err_empty": "Папка пуста.",
        "select_files": "Выбор файлов",
        "dir": "Директория",
        "files": "Файлы",
        "selected": "Выбрано:",
        "of": "из",
        "tip_toggle": "Введите номера для выбора, 0 для старта, или перетащите сюда еще файлы",
        "toggle": "Выбор:",
        "err_no_selected": "Файлы не выбраны.",
        "success": "Успешно",
        "success_msg": "Данные успешно извлечены.",
        "output_loc": "Место сохранения",
        "err_save": "Ошибка сохранения:"
    },
    "zh": {
        "commands": "命令",
        "actions": "操作",
        "start": "开始提取",
        "settings": "设置",
        "system": "系统",
        "output_path": "输出路径",
        "language": "语言",
        "lang_name": "中文",
        "tip_main": "输入数字进行选择，'esc' 返回，或按 Ctrl+C 退出",
        "action": "操作:",
        "change_path": "更改输出路径",
        "change_lang": "更改语言",
        "new_path": "新路径:",
        "path_updated": "路径已成功更新。",
        "press_enter": "按 Enter 键继续",
        "press_enter_return": "按 Enter 键返回",
        "lang_updated": "语言已成功更新。",
        "target_dir": "目标目录",
        "input": "输入",
        "enter_path": "输入路径，或将文件夹/文件拖放到此处 (Drag & Drop)",
        "path": "路径:",
        "err_not_found": "错误: 找不到路径或文件。",
        "err_permission": "错误: 拒绝访问 (PermissionError)。",
        "err_empty": "文件夹为空。",
        "select_files": "选择文件",
        "dir": "目录",
        "files": "文件",
        "selected": "已选择:",
        "of": "/",
        "tip_toggle": "输入数字进行切换，输入 0 提取，或拖放更多文件到此处",
        "toggle": "切换:",
        "err_no_selected": "未选择任何文件。",
        "success": "成功",
        "success_msg": "数据提取成功。",
        "output_loc": "输出位置",
        "err_save": "保存错误:"
    }
}

class RawInput:
    def __enter__(self):
        if sys.platform != 'win32':
            import tty, termios
            self.fd = sys.stdin.fileno()
            self.old = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
        return self

    def __exit__(self, *args):
        if sys.platform != 'win32':
            import termios
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)

def parse_vt_sequence(seq):
    if seq == '\x1b[A': return 'UP'
    if seq == '\x1b[B': return 'DOWN'
    if seq.startswith('\x1b[<') and seq.endswith(('M', 'm')):
        parts = seq[3:-1].split(';')
        if len(parts) == 3:
            cb, cx, cy = parts
            if cb == '0' and seq.endswith('M'):
                return ('CLICK', int(cx), int(cy))
    return seq

def get_event():
    if sys.platform == 'win32':
        import msvcrt
        if msvcrt.kbhit():
            ch = msvcrt.getwch()
            if ch == '\x1b':
                seq = "\x1b"
                time.sleep(0.01)
                while msvcrt.kbhit():
                    seq += msvcrt.getwch()
                if seq == '\x1b': return 'ESC'
                return parse_vt_sequence(seq)
            elif ch in ('\r', '\n'): return 'ENTER'
            elif ch == '\b': return 'BACKSPACE'
            elif ch == '\x03': raise KeyboardInterrupt
            elif ch in ('\x00', '\xe0'):
                ch2 = msvcrt.getwch()
                if ch2 == 'H': return 'UP'
                elif ch2 == 'P': return 'DOWN'
            else: return ch
        time.sleep(0.01)
        return None
    else:
        import select
        r, _, _ = select.select([sys.stdin], [], [], 0.05)
        if r:
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                r2, _, _ = select.select([sys.stdin], [], [], 0.02)
                if r2:
                    seq = '\x1b' + sys.stdin.read(1)
                    if seq[1] in ('[', 'O'):
                        while True:
                            r3, _, _ = select.select([sys.stdin], [], [], 0.01)
                            if r3:
                                seq += sys.stdin.read(1)
                                if seq[-1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~M':
                                    break
                            else:
                                break
                    return parse_vt_sequence(seq)
                else:
                    return 'ESC'
            elif ch in ('\n', '\r'): return 'ENTER'
            elif ch in ('\x7f', '\b'): return 'BACKSPACE'
            elif ch == '\x03': raise KeyboardInterrupt
            elif ch == '\x04': raise EOFError
            else: return ch
        return None

def clean_path(p):
    if not p:
        return p
    p = p.strip(' "\'\r\n\t')
    if p.startswith("file://"):
        p = p[7:]
        p = urllib.parse.unquote(p)
        if sys.platform == 'win32' and p.startswith('/') and len(p) > 2 and p[2] == ':':
            p = p[1:]
    p = os.path.expanduser(p)
    p = os.path.normpath(p)
    return p

def parse_dropped_paths(raw_input):
    c_path = clean_path(raw_input)
    if os.path.exists(c_path):
        return [c_path]
    try:
        tokens = shlex.split(raw_input, posix=(os.name == 'posix'))
    except ValueError:
        tokens = raw_input.split()
    
    valid = []
    for t in tokens:
        ct = clean_path(t)
        if os.path.exists(ct):
            valid.append(ct)
    return valid

def detect_encoding(filepath):
    try:
        with open(filepath, 'rb') as f:
            raw = f.read(8192)
    except Exception:
        return 'utf-8'
        
    for enc in ['utf-8-sig', 'utf-8', 'utf-16', 'cp1252']:
        try:
            raw.decode(enc)
            return enc
        except UnicodeDecodeError:
            continue
    return 'utf-8'

def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_memory(target_dir, disabled_files):
    memory = load_memory()
    abs_dir = os.path.abspath(target_dir)
    memory[abs_dir] = {"disabled_files": disabled_files}
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=4)
    except IOError:
        pass

def load_config():
    mem = load_memory()
    conf = mem.get("_config_", {})
    lang = conf.get("lang", "en")
    out = conf.get("out", get_default_download_path())
    return lang, clean_path(out)

def save_config(lang, out):
    mem = load_memory()
    mem["_config_"] = {"lang": lang, "out": out}
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(mem, f, ensure_ascii=False, indent=4)
    except IOError:
        pass

def get_term_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80

def get_layout():
    tw = get_term_width()
    bw = max(10, min(tw - 4, 70))
    m_len = max(0, (tw - bw) // 2)
    return tw, bw, " " * m_len

def clear_screen(lines=18):
    sys.stdout.write(f"{C_RESET}\033[2J\033[H")
    try:
        th = os.get_terminal_size().lines
        v_pad = max(0, (th - lines) // 2)
        if v_pad > 0:
            sys.stdout.write("\n" * v_pad)
    except OSError:
        pass
    sys.stdout.flush()

def truncate_text(text, max_len):
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."

def get_default_download_path():
    if sys.platform == 'win32':
        return os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads')
    elif 'ANDROID_ROOT' in os.environ:
        return '/storage/emulated/0/Download'
    else:
        return os.path.join(str(Path.home()), 'Downloads')

def draw_logo():
    ASCII_LOGO = [
        "██^^^^ ██ ██     ██^^^^   ▄█████ ██     ██ ",
        "██^^   ██ ██     ██^^     ██~~~~ ██     ██ ",
        "██     ██ ██████ ██████   ▀█████ ██████ ██ ",
        "~~     ~~ ~~~~~~ ~~~~~~    ~~~~~ ~~~~~~ ~~ "
    ]
    
    C_SHADOW_FG = "\033[38;2;90;90;40m"
    C_SHADOW_BG = "\033[48;2;90;90;40m"
    
    if C_YELLOW == COLOR_DIM["yellow"]:
        C_SHADOW_FG = "\033[38;2;34;34;16m"
        C_SHADOW_BG = "\033[48;2;34;34;16m"
    
    tw = get_term_width()
    logo_width = len(ASCII_LOGO[0])
    indent = " " * max(0, (tw - logo_width) // 2)
    
    print()
    for line in ASCII_LOGO:
        rendered_line = indent
        for char in line:
            if char == '_':
                rendered_line += f"{C_SHADOW_BG} {C_RESET}"
            elif char == '^':
                rendered_line += f"{C_YELLOW}{C_SHADOW_BG}▀{C_RESET}"
            elif char == '~':
                rendered_line += f"{C_SHADOW_FG}▀{C_RESET}"
            else:
                rendered_line += f"{C_YELLOW}{char}{C_RESET}"
                
        print(rendered_line)
    print("\n")

def print_tip(text, m, bw):
    lines = textwrap.wrap(text, width=max(10, bw - 6))
    if lines:
        print(f"\n{m}{C_YELLOW}● Tip{C_RESET} {C_GRAY}{lines[0]}{C_RESET}")
        for line in lines[1:]:
            print(f"{m}      {C_GRAY}{line}{C_RESET}")
    print()

def show_floating_modal(title, items, bg_draw_func):
    max_len = len(title) + 10
    for item in items:
        l = len(item["label"]) + (len(item.get("shortcut", "")) + 4 if item.get("shortcut") else 0)
        if l > max_len: max_len = l
    mw = min(80, max(40, max_len + 6))
    mh = len(items) + 4
    
    sys.stdout.write("\033[?1000h\033[?1015h\033[?1006h\033[?25l")
    sys.stdout.flush()
    
    selectable = [i for i, it in enumerate(items) if it["type"] == "item"]
    if not selectable:
        sys.stdout.write("\033[?1000l\033[?1015l\033[?1006l\033[0m")
        sys.stdout.flush()
        return None
        
    sel_pos = 0
    last_size = (-1, -1)
    
    def draw_dimmed_background():
        try:
            set_color_mode(True)
            bg_draw_func()
        finally:
            set_color_mode(False)
    
    with RawInput():
        while True:
            tw = get_term_width()
            try: th = os.get_terminal_size().lines
            except: th = 24
            
            if (tw, th) != last_size:
                draw_dimmed_background()
                last_size = (tw, th)
                
            sx = max(1, (tw - mw) // 2)
            sy = max(1, (th - mh) // 2)
            
            sys.stdout.write(f"\033[{sy};{sx}H")
            sys.stdout.write(f"\033[48;2;30;30;30m\033[38;2;210;210;210m  {title}{' ' * (mw - len(title) - 7)}\033[38;2;110;110;110mesc  \033[0m")
            sys.stdout.write(f"\033[{sy+1};{sx}H\033[48;2;30;30;30m{' ' * mw}\033[0m")
            
            for i, item in enumerate(items):
                sys.stdout.write(f"\033[{sy+2+i};{sx}H")
                is_sel = (selectable[sel_pos] == i)
                
                if item["type"] == "category":
                    sys.stdout.write(f"\033[48;2;30;30;30m\033[38;2;0;175;255m  {item['label']}{' ' * (mw - len(item['label']) - 2)}\033[0m")
                else:
                    bg = "\033[48;2;248;246;117m" if is_sel else "\033[48;2;30;30;30m"
                    fg = "\033[38;2;0;0;0m" if is_sel else "\033[38;2;210;210;210m"
                    s_fg = "\033[38;2;80;80;80m" if is_sel else "\033[38;2;110;110;110m"
                    
                    lbl = item["label"]
                    sh = item.get("shortcut", "")
                    sp = mw - len(lbl) - len(sh) - 4
                    sys.stdout.write(f"{bg}{fg}  {lbl}{' ' * sp}{s_fg}{sh}  \033[0m")
                    
            sys.stdout.write(f"\033[{sy+2+len(items)};{sx}H\033[48;2;30;30;30m{' ' * mw}\033[0m")
            sys.stdout.write(f"\033[{sy+3+len(items)};{sx}H\033[48;2;30;30;30m{' ' * mw}\033[0m")
            sys.stdout.flush()
            
            ev = get_event()
            if ev == 'UP': sel_pos = (sel_pos - 1) % len(selectable)
            elif ev == 'DOWN': sel_pos = (sel_pos + 1) % len(selectable)
            elif ev == 'ESC':
                sys.stdout.write("\033[?1000l\033[?1015l\033[?1006l\033[0m")
                sys.stdout.flush()
                return None
            elif ev == 'ENTER':
                sys.stdout.write("\033[?1000l\033[?1015l\033[?1006l\033[0m")
                sys.stdout.flush()
                return items[selectable[sel_pos]]["id"]
            elif isinstance(ev, tuple) and ev[0] == 'CLICK':
                _, mx, my = ev
                if sx <= mx < sx + mw:
                    row = my - sy - 2
                    if 0 <= row < len(items):
                        if items[row]["type"] == "item":
                            sys.stdout.write("\033[?1000l\033[?1015l\033[?1006l\033[0m")
                            sys.stdout.flush()
                            return items[row]["id"]

def kilo_input(prompt, redraw_callback):
    chars = []
    try:
        sys.stdout.write(f"{C_RESET}\033[?25l")
        tw, bw, m = redraw_callback()
        
        def draw_prompt():
            prefix = f" {prompt} "
            avail = max(1, bw - len(prefix))
            disp = ''.join(chars)
            if len(disp) > avail:
                disp = disp[-avail:]
            spaces = max(0, bw - len(prefix) - len(disp))
            
            box_render = f"\r{m}{C_BLUE}▌{C_BG_INPUT}{C_GRAY}{prefix}{C_WHITE}{disp}{' ' * spaces}{C_RESET}"
            sys.stdout.write(box_render)
            if spaces > 0:
                sys.stdout.write(f"\033[{spaces}D")
            sys.stdout.flush()

        draw_prompt()
        sys.stdout.write(f"{C_WHITE}\033[?25h")
        sys.stdout.flush()

        last_size = get_term_width()
        
        with RawInput():
            while True:
                ev = get_event()
                curr_size = get_term_width()
                if curr_size != last_size:
                    last_size = curr_size
                    sys.stdout.write(f"{C_RESET}\033[?25l")
                    tw, bw, m = redraw_callback()
                    sys.stdout.write(f"{C_WHITE}\033[?25h")
                    draw_prompt()
                
                if ev == 'ESC':
                    sys.stdout.write(f"{C_RESET}\033[?25l")
                    return 'esc'
                elif ev == 'ENTER':
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                    sys.stdout.write(f"{C_RESET}\033[?25l")
                    return ''.join(chars)
                elif ev == 'BACKSPACE':
                    if chars:
                        chars.pop()
                        draw_prompt()
                elif isinstance(ev, str) and len(ev) == 1:
                    chars.append(ev)
                    draw_prompt()

    except KeyboardInterrupt:
        sys.stdout.write(f"{C_RESET}\033[?1049l\033[?25h\n")
        sys.stdout.flush()
        sys.exit(0)
    except EOFError:
        sys.stdout.write(f"{C_RESET}\033[?25l")
        sys.stdout.flush()
        return 'esc'

def is_esc(val):
    return val.lower() in ('esc', 'q', '\x1b', 'exit')

def draw_header(m, bw, title):
    spaces = " " * max(1, bw - len(title) - 3)
    print(f"{m}{C_WHITE}{C_BOLD}{title}{C_RESET}{spaces}{C_GRAY}esc{C_RESET}\n")

def draw_menu_item(m, num, text):
    print(f"{m}{C_YELLOW}{num}{C_RESET}  {C_WHITE}{text}{C_RESET}")

def draw_sys_item(m, bw, label, value):
    label_disp = label + "   "
    val_disp = truncate_text(value, bw - len(label_disp))
    print(f"{m}{C_WHITE}{label_disp}{C_RESET}{C_GRAY}{val_disp}{C_RESET}")

def settings_menu(lang, output_dir):
    while True:
        t = T[lang]
        def draw_bg():
            clear_screen(18)
            draw_logo()
            tw, bw, m = get_layout()
            draw_header(m, bw, t["commands"])
            print(f"{m}{C_BLUE}{t['actions']}{C_RESET}")
            draw_menu_item(m, "1", t["start"])
            draw_menu_item(m, "2", t["settings"])
            print()
            print(f"{m}{C_BLUE}{t['system']}{C_RESET}")
            draw_sys_item(m, bw, t["output_path"], output_dir)
            print_tip(t["tip_main"], m, bw)
            
        items = [
            {"type": "category", "label": t["settings"]},
            {"type": "item", "id": "path", "label": t["change_path"]},
            {"type": "item", "id": "lang", "label": t["change_lang"]}
        ]
        
        choice = show_floating_modal(t["settings"], items, draw_bg)
        
        if not choice:
            break
        elif choice == 'path':
            def draw_path_bg():
                clear_screen(15)
                draw_logo()
                tw, bw, m = get_layout()
                draw_header(m, bw, t["settings"])
                print()
                return tw, bw, m
            raw_path = kilo_input(t["new_path"], draw_path_bg)
            if not is_esc(raw_path) and raw_path:
                new_path = clean_path(raw_path)
                try:
                    os.makedirs(new_path, exist_ok=True)
                    output_dir = new_path
                    save_config(lang, output_dir)
                except Exception:
                    pass
        elif choice == 'lang':
            lang_items = [
                {"type": "category", "label": t["language"]},
                {"type": "item", "id": "en", "label": "English"},
                {"type": "item", "id": "ru", "label": "Русский"},
                {"type": "item", "id": "zh", "label": "中文"}
            ]
            new_lang = show_floating_modal(t["change_lang"], lang_items, draw_bg)
            if new_lang:
                lang = new_lang
                save_config(lang, output_dir)

    return lang, output_dir

def main_menu(lang, output_dir):
    while True:
        t = T[lang]
        
        def draw_main():
            clear_screen(18)
            draw_logo()
            tw, bw, m = get_layout()
            draw_header(m, bw, t["commands"])
            print(f"{m}{C_BLUE}{t['actions']}{C_RESET}")
            draw_menu_item(m, "1", t["start"])
            draw_menu_item(m, "2", t["settings"])
            print()
            print(f"{m}{C_BLUE}{t['system']}{C_RESET}")
            draw_sys_item(m, bw, t["output_path"], output_dir)
            print_tip(t["tip_main"], m, bw)
            return tw, bw, m

        choice = kilo_input(t["action"], draw_main)
        
        if is_esc(choice):
            continue
        elif choice == '1':
            run_script(lang, output_dir)
        elif choice == '2':
            lang, output_dir = settings_menu(lang, output_dir)

def run_script(lang, output_dir):
    t = T[lang]
    
    def draw_target():
        clear_screen(13)
        draw_logo()
        tw, bw, m = get_layout()
        draw_header(m, bw, t["target_dir"])
        print(f"{m}{C_BLUE}{t['input']}{C_RESET}")
        print(f"{m}{C_GRAY}{t['enter_path']}{C_RESET}\n")
        return tw, bw, m

    raw_path = kilo_input(t["path"], draw_target)

    if is_esc(raw_path):
        return

    paths = parse_dropped_paths(raw_path)
    if not paths:
        def draw_not_found():
            clear_screen(13)
            draw_logo()
            tw, bw, m = get_layout()
            draw_header(m, bw, t["target_dir"])
            print(f"\n{m}{C_YELLOW}{t['err_not_found']}{C_RESET}\n")
            return tw, bw, m
            
        kilo_input(f"{t['press_enter_return']}:", draw_not_found)
        return

    first_path = paths[0]
    
    try:
        if os.path.isdir(first_path):
            target_dir = first_path
            all_items = os.listdir(target_dir)
            dropped_files = []
        else:
            target_dir = os.path.dirname(first_path)
            all_items = os.listdir(target_dir)
            dropped_files = [os.path.abspath(p) for p in paths if os.path.isfile(p)]
    except PermissionError:
        def draw_perm():
            clear_screen(13)
            draw_logo()
            tw, bw, m = get_layout()
            draw_header(m, bw, t["target_dir"])
            print(f"\n{m}{C_YELLOW}{t['err_permission']}{C_RESET}\n")
            return tw, bw, m
            
        kilo_input(f"{t['press_enter_return']}:", draw_perm)
        return

    file_data = []
    for f in all_items:
        full_p = os.path.join(target_dir, f)
        if os.path.isfile(full_p) and not (f.startswith("extracted_data_") and f.endswith(".txt")):
            if os.path.isdir(first_path):
                file_data.append({"path": full_p, "name": f, "selected": True})
            else:
                is_sel = os.path.abspath(full_p) in dropped_files
                file_data.append({"path": full_p, "name": f, "selected": is_sel})

    if not file_data and not dropped_files:
        def draw_empty():
            clear_screen(13)
            draw_logo()
            tw, bw, m = get_layout()
            draw_header(m, bw, t["target_dir"])
            print(f"\n{m}{C_YELLOW}{t['err_empty']}{C_RESET}\n")
            return tw, bw, m
            
        kilo_input(f"{t['press_enter_return']}:", draw_empty)
        return

    if os.path.isdir(first_path):
        memory = load_memory()
        abs_dir = os.path.abspath(target_dir)
        disabled_files = memory.get(abs_dir, {}).get("disabled_files", [])
        for item in file_data:
            if item["name"] in disabled_files:
                item["selected"] = False

    def add_or_select_file(f_list, new_path):
        abs_p = os.path.abspath(new_path)
        for i in f_list:
            if os.path.abspath(i["path"]) == abs_p:
                i["selected"] = True
                return
        f_list.append({
            "path": abs_p,
            "name": os.path.basename(abs_p),
            "selected": True
        })

    while True:
        def draw_selection():
            total_lines = 17 + len(file_data)
            clear_screen(total_lines)
            draw_logo()
            tw, bw, m = get_layout()
            
            draw_header(m, bw, t["select_files"])
            
            dir_display = truncate_text(target_dir, bw)
            print(f"{m}{C_BLUE}{t['dir']}{C_RESET}")
            print(f"{m}{C_WHITE}{dir_display}{C_RESET}\n")
            
            print(f"{m}{C_BLUE}{t['files']}{C_RESET}")
            
            for i, item in enumerate(file_data):
                file_disp = truncate_text(item["name"], bw - 6)
                num = str(i + 1)
                if item["selected"]:
                    print(f"{m}{C_WHITE}{num:<2}{C_RESET}  {C_WHITE}{file_disp}{C_RESET}")
                else:
                    print(f"{m}{C_DARK_GRAY}{num:<2}  {file_disp}{C_RESET}")
            
            selected_count = sum(1 for item in file_data if item["selected"])
            total_count = len(file_data)
            
            print(f"\n{m}{C_GRAY}{t['selected']} {C_WHITE}{selected_count}{C_GRAY} {t['of']} {total_count}{C_RESET}")
            
            print_tip(t["tip_toggle"], m, bw)
            return tw, bw, m

        choice = kilo_input(t["toggle"], draw_selection).strip()
        
        if is_esc(choice):
            return
        elif choice == '0':
            break
        elif choice:
            c_choice = clean_path(choice)
            if os.path.exists(c_choice) and os.path.isfile(c_choice):
                add_or_select_file(file_data, c_choice)
            else:
                try:
                    tokens = shlex.split(choice, posix=(os.name == 'posix'))
                except ValueError:
                    tokens = choice.split()
                
                for tok in tokens:
                    if tok.isdigit():
                        idx = int(tok) - 1
                        if 0 <= idx < len(file_data):
                            file_data[idx]["selected"] = not file_data[idx]["selected"]
                    else:
                        ct = clean_path(tok)
                        if os.path.exists(ct) and os.path.isfile(ct):
                            add_or_select_file(file_data, ct)

    if not any(item["selected"] for item in file_data):
        def draw_no_sel():
            clear_screen(13)
            draw_logo()
            tw, bw, m = get_layout()
            draw_header(m, bw, t["select_files"])
            print(f"\n{m}{C_YELLOW}{t['err_no_selected']}{C_RESET}\n")
            return tw, bw, m
            
        kilo_input(f"{t['press_enter_return']}:", draw_no_sel)
        return

    disabled_to_save = [
        item["name"] for item in file_data 
        if not item["selected"] and os.path.dirname(os.path.abspath(item["path"])) == os.path.abspath(target_dir)
    ]
    save_memory(target_dir, disabled_to_save)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = os.path.join(output_dir, f"extracted_data_{timestamp}.txt")
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        with open(out_file, 'w', encoding='utf-8') as outfile:
            for item in file_data:
                if item["selected"]:
                    filepath = item["path"]
                    outfile.write(f"--- {item['name']} ---\n")
                    enc = detect_encoding(filepath)
                    try:
                        with open(filepath, 'r', encoding=enc, errors='replace') as infile:
                            while True:
                                chunk = infile.read(1024 * 1024)
                                if not chunk:
                                    break
                                outfile.write(chunk)
                    except Exception as e:
                        outfile.write(f"[Read error: {e}]")
                    outfile.write("\n\n\n")
        
        def draw_success():
            clear_screen(15)
            draw_logo()
            tw, bw, m = get_layout()
            draw_header(m, bw, t["success"])
            print(f"{m}{C_WHITE}{t['success_msg']}{C_RESET}\n")
            print(f"{m}{C_BLUE}{t['output_loc']}{C_RESET}")
            out_display = truncate_text(out_file, bw)
            print(f"{m}{C_WHITE}{out_display}{C_RESET}\n")
            return tw, bw, m
            
        kilo_input(f"{t['press_enter_return']}:", draw_success)
    except Exception as e:
        def draw_save_err():
            clear_screen(15)
            draw_logo()
            tw, bw, m = get_layout()
            draw_header(m, bw, t["system"])
            print(f"\n{m}{C_YELLOW}{t['err_save']} {e}{C_RESET}\n")
            return tw, bw, m
            
        kilo_input(f"{t['press_enter_return']}:", draw_save_err)

if __name__ == "__main__":
    sys.stdout.write("\033[?1049h\033[?25l")
    sys.stdout.flush()
    try:
        init_lang, init_out = load_config()
        main_menu(init_lang, init_out)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(f"{C_RESET}\033[?1049l\033[?25h")
        sys.stdout.flush()
