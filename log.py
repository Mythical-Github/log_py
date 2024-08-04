import os
import sys
import logging
import json
from datetime import datetime
from shutil import get_terminal_size
from colorama import Fore, Style, init

init(autoreset=True)

logger = logging.getLogger(__name__)

if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(SCRIPT_DIR)

def load_theme_colors():
    colors_file = os.path.join(SCRIPT_DIR, 'log_colors.json')
    if not os.path.isfile(colors_file):
        raise FileNotFoundError(f"Theme colors file not found: {colors_file}")
    with open(colors_file, 'r') as f:
        return json.load(f)

colors_config = load_theme_colors()
theme_colors = colors_config.get('theme_colors', {})
default_color = colors_config.get('default_color', Fore.LIGHTBLUE_EX)
background_color = colors_config.get('background_color', '\033[48;2;40;42;54m')

def log_message(message: str):
    logger.info(message)
    color = default_color
    for keyword, assigned_color in theme_colors.items():
        if keyword in message:
            color = assigned_color
            break
    terminal_width = get_terminal_size().columns
    padded_message = (message[:terminal_width] if len(message) > terminal_width else message.ljust(terminal_width))
    print(f"{background_color}{color}{padded_message}{Style.RESET_ALL}")

def rename_latest_log(log_dir):
    latest_log_path = os.path.join(log_dir, 'latest.log')
    if os.path.isfile(latest_log_path):
        try:
            timestamp = datetime.now().strftime('%m_%d_%Y_%H%M_%S')
            new_name = f'unreal_auto_mod_{timestamp}.log'
            new_log_path = os.path.join(log_dir, new_name)
            os.rename(latest_log_path, new_log_path)
        except PermissionError as e:
            log_message(f"Error renaming log file: {e}")
            return

def configure_logging():
    log_dir = os.path.join(SCRIPT_DIR, 'logs')
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    rename_latest_log(log_dir)

    log_file = os.path.join(log_dir, 'latest.log')

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(message)s'))

    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

configure_logging()
