import os
import sys
import json
from pathlib import Path

P_RGB = (217, 119, 87)
C_P = f'\033[38;2;{P_RGB[0]};{P_RGB[1]};{P_RGB[2]}m'
C_BOLD = '\033[1m'
C_DIM = '\033[2m'
C_RESET = '\033[0m'

C_ON = f'\033[38;2;{P_RGB[0]};{P_RGB[1]};{P_RGB[2]}m'
C_OFF = '\033[38;2;{120;100;90}m'

if sys.platform == 'win32':
    os.system('')

MEMORY_FILE = Path.home() / ".merge_files_memory.json"

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

def get_term_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80

def clear_screen():
    os.system('cls' if sys.platform == 'win32' else 'clear')

def draw_separator():
    width = get_term_width()
    print(f"{C_DIM}{'─' * width}{C_RESET}")

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

def main_menu(output_dir):
    while True:
        clear_screen()
        draw_separator()
        print(f"{C_BOLD}{C_P}  ◆  МЕНЮ{C_RESET}")
        draw_separator()
        
        dir_display = truncate_text(output_dir, get_term_width() - 18)
        print(f"\n  {C_DIM}Путь сохранения:{C_RESET} {C_P}{dir_display}{C_RESET}\n")
        
        options = {"1": "Запуск", "2": "Выбрать путь", "3": "Выход"}
        for key, value in options.items():
            print(f"  {C_P}{key}{C_RESET}) {value}")
        
        print()
        draw_separator()
        choice = input(f"  {C_P}❯{C_RESET} ").strip()
        
        if choice == '1':
            run_script(output_dir)
        elif choice == '2':
            print(f"\n  {C_DIM}Новый путь (или Enter для отмены):{C_RESET}")
            new_path = input(f"  {C_P}❯{C_RESET} ").strip()
            if new_path:
                try:
                    os.makedirs(new_path, exist_ok=True)
                    output_dir = new_path
                    print(f"\n  {C_P}Путь успешно обновлен!{C_RESET}")
                    input(f"  {C_DIM}Нажмите Enter чтобы продолжить...{C_RESET}")
                except Exception as e:
                    print(f"\n  {C_P}Ошибка: {e}{C_RESET}")
                    input(f"  {C_DIM}Нажмите Enter чтобы продолжить...{C_RESET}")

def run_script(output_dir):
    clear_screen()
    draw_separator()
    print(f"{C_BOLD}{C_P}  ◆  ЗАПУСК{C_RESET}")
    draw_separator()
    
    print(f"\n  {C_DIM}Укажите путь до папки с файлами:{C_RESET}")
    target_dir = input(f"  {C_P}❯{C_RESET} ").strip()

    if not os.path.isdir(target_dir):
        print(f"\n  {C_P}Ошибка: Папка не найдена!{C_RESET}")
        input(f"  {C_DIM}Нажмите Enter чтобы вернуться...{C_RESET}")
        return

    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    
    if not files:
        print(f"\n  {C_P}Папка пуста!{C_RESET}")
        input(f"  {C_DIM}Нажмите Enter чтобы вернуться...{C_RESET}")
        return

    memory = load_memory()
    abs_dir = os.path.abspath(target_dir)
    disabled_files = memory.get(abs_dir, {}).get("disabled_files", [])
    
    disabled_files = [f for f in disabled_files if f in files]
    
    selected = [file not in disabled_files for file in files]

    while True:
        clear_screen()
        draw_separator()
        print(f"{C_BOLD}{C_P}  ◆  ВЫБОР ФАЙЛОВ{C_RESET}")
        draw_separator()
        
        dir_display = truncate_text(target_dir, get_term_width() - 10)
        print(f"\n  {C_DIM}Папка: {dir_display}{C_RESET}\n")
        
        term_width = get_term_width()
        max_name_len = term_width - 12
        
        for i, file in enumerate(files):
            status_icon = f"{C_ON}✚{C_RESET}" if selected[i] else f"{C_OFF}✖{C_RESET}"
            file_display = truncate_text(file, max_name_len)
            print(f"  {C_DIM}{i + 1:>2}.{C_RESET} [{status_icon}] {file_display}")
        
        selected_count = sum(selected)
        total_count = len(files)
        
        print()
        draw_separator()
        print(f"  {C_DIM}Выбрано: {C_BOLD}{C_P}{selected_count}{C_RESET}{C_DIM} из {total_count}{C_RESET}")
        print(f"  {C_DIM}Введите номер, чтобы переключить статус.{C_RESET}")
        print(f"  {C_DIM}{'0':>2} — Продолжить  |  {'q':>2} — Отмена{C_RESET}")
        draw_separator()
        
        choice = input(f"  {C_P}❯{C_RESET} ").strip().lower()
        
        if choice == 'q':
            return
        elif choice == '0':
            break
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                selected[idx] = not selected[idx]

    disabled_to_save = [files[i] for i in range(len(files)) if not selected[i]]
    save_memory(target_dir, disabled_to_save)

    result_data = []
    for i, file in enumerate(files):
        if selected[i]:
            filepath = os.path.join(target_dir, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                result_data.append(f"{file}:\n{content}")
            except Exception as e:
                result_data.append(f"{file}:\n[Ошибка чтения файла: {e}]")

    if not result_data:
        print(f"\n  {C_P}Вы не выбрали ни одного файла!{C_RESET}")
        input(f"  {C_DIM}Нажмите Enter чтобы вернуться...{C_RESET}")
        return

    final_content = "\n\n\n".join(result_data)
    out_file = os.path.join(output_dir, "extracted_data.txt")
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        clear_screen()
        draw_separator()
        print(f"{C_BOLD}{C_P}  ◆  ГОТОВО{C_RESET}")
        draw_separator()
        print(f"\n  {C_ON}✚{C_RESET} Данные успешно извлечены!")
        print(f"  {C_DIM}Файл сохранен как:{C_RESET}")
        out_display = truncate_text(out_file, get_term_width() - 4)
        print(f"  {C_BOLD}{C_P}{out_display}{C_RESET}\n")
    except Exception as e:
        print(f"\n  {C_P}Ошибка сохранения: {e}{C_RESET}")

    input(f"  {C_DIM}Нажмите Enter чтобы вернуться в меню...{C_RESET}")

if __name__ == "__main__":
    default_out = get_default_download_path()
    main_menu(default_out)