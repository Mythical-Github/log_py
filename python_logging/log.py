import os
import sys
import json
import logging
from datetime import datetime
from shutil import get_terminal_size
from colorama import Fore, Style, init

init(autoreset=True)

logger = logging.getLogger(__name__)

def get_resource_path(relative_path):
    """Get the absolute path to a resource in the package."""
    try:
        base_path = getattr(sys, '_MEIPASS', os.getcwd())
        return os.path.join(base_path, relative_path)
    except Exception as e:
        log_message(f"Error obtaining resource path: {e}")
        return relative_path

# Initialize global variables
log_base_dir = os.getcwd()
colors_json_path = get_resource_path('log_colors.json')
cli_json_path = get_resource_path('cli.json')  # Initialize CLI JSON path
colors_config = ''
theme_colors = ''
default_color = ''
background_color = ''
log_prefix = ''

def module_setup():
    """Initial setup for modules."""
    return

def set_log_base_dir(base_dir: str):
    """Set the base directory for logs."""
    global log_base_dir
    log_base_dir = base_dir

def set_colors_json_path(json_path: str):
    """Set the path for the colors JSON file."""
    global colors_json_path
    colors_json_path = get_resource_path(json_path)  # Ensure path resolution

def set_cli_json_path(json_path: str):
    """Set the path for the CLI JSON file."""
    global cli_json_path
    cli_json_path = get_resource_path(json_path)  # Ensure path resolution

def load_theme_colors():
    """Load the theme colors from the JSON file."""
    try:
        resolved_path = colors_json_path
        log_message(f"Resolved path for colors JSON: {resolved_path}")
        if not os.path.isfile(resolved_path):
            raise FileNotFoundError(f"Theme colors file not found: {resolved_path}")
        with open(resolved_path, 'r') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Theme colors file should contain a JSON object.")
            return data
    except Exception as e:
        log_message(f"Error loading theme colors: {e}")
        raise

def log_message(message: str):
    """Log a message with color and style."""
    try:
        logger.info(message)
        color = default_color
        for keyword, assigned_color in theme_colors.items():
            if keyword in message:
                color = assigned_color
                break
        terminal_width = get_terminal_size().columns
        padded_message = (message[:terminal_width] if len(message) > terminal_width else message.ljust(terminal_width))
        print(f"{background_color}{color}{padded_message}{Style.RESET_ALL}")
    except Exception as e:
        print(f"Error in log_message: {e}")

def rename_latest_log(log_dir):
    """Rename the latest log file with a timestamp."""
    latest_log_path = os.path.join(log_dir, 'latest.log')
    if os.path.isfile(latest_log_path):
        try:
            timestamp = datetime.now().strftime('%m_%d_%Y_%H%M_%S')
            new_name = f'{log_prefix}{timestamp}.log'
            new_log_path = os.path.join(log_dir, new_name)
            os.rename(latest_log_path, new_log_path)
        except PermissionError as e:
            log_message(f"Error renaming log file: {e}")
            return

def configure_logging():
    """Configure logging with file handler and color settings."""
    global colors_config
    global theme_colors
    global default_color
    global background_color
    global log_prefix

    try:
        colors_config = load_theme_colors()
        theme_colors = colors_config.get('theme_colors', {})
        default_color = colors_config.get('default_color', Fore.WHITE)
        background_color = colors_config.get('background_color', '')
        log_prefix = colors_config.get('log_name_prefix', '')

        log_dir = os.path.join(log_base_dir, 'logs')
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

        rename_latest_log(log_dir)

        original_path = os.path.join(log_dir, 'latest.log')

        global inter_log
        inter_log = original_path

        log_file = inter_log

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(message)s'))

        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
    except Exception as e:
        log_message(f"Error configuring logging: {e}")
