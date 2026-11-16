import os

## load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()   

PRINTS_SHORTS = os.getenv("PRINTS_SHORTS", "false").lower() == "true"
PRINTS_SHORTS = bool(PRINTS_SHORTS)
print(PRINTS_SHORTS)


def open_folder_return_files(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

def open_folder_return_folders(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_setup(file_path):  # Načíta konfiguráciu zo súboru vo formáte key=value (json)
    setup = {}

    content = read_file(file_path)

    for line in content.splitlines():
        line = line.strip()

        if not line or "=" not in line:
            continue

        key, value = line.split("=", 1)

        key = key.strip()
        value = value.strip()

        if key == "models":
            value = [model.strip() for model in value.split(",") if model.strip()]
        elif value.lower() in {"true", "false"}:
            value = value.lower() == "true"
        elif value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:
                pass

        setup[key] = value

    return setup

def count_code_genetate(folder_path, model, language):
    safe_name = safe_file_name(model)
    folder_language = os.path.join(folder_path, language)
    if not os.path.exists(folder_language):
        return 0
    target_folder = os.path.join(folder_language, safe_name)
    if not os.path.exists(target_folder):
        return 0
    extension = language_extension(language)
    if extension is None:
        return 0
    code_files = [
        file_path for file_path in open_folder_return_files(target_folder)
        if file_path.lower().endswith(f".{extension.lower()}")
    ]

    return len(code_files)

def safe_file_name(model):
    safe_model = ''.join(
        ch if ch.isalnum() or ch in {'_', '-', ' '} else '_'
        for ch in model
    )
    return safe_model.strip('_-') or 'untitled'

def save_code_to_file(folder_path, model, content,language): # ulozenie suboru s obsahom a spravnou priponou podla jazyka
    safe_model = safe_file_name(model)

    folder_language = os.path.join(folder_path, language)
    if not os.path.exists(folder_language):
        os.makedirs(folder_language)

    ## vo felderi najdi priecinok s nazvom safe_model, ked nie tak vytvor
    target_folder = os.path.join(folder_language, safe_model)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    extension = language_extension(language)

    file_index = 0
    while True:
        target_file_name = f"{safe_model}_{file_index}"
        if extension:
            target_file_name += f".{extension}"
        target_file_path = os.path.join(target_folder, target_file_name)
        if not os.path.exists(target_file_path):
            break
        file_index += 1

    with open(target_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    if PRINTS_SHORTS:
        print(f"Saved code to file: {target_file_path}")
    return file_index
    



def save_file_to_folder(folder_path, file_name, content):
    file_path = os.path.join(folder_path, file_name)
    if isinstance(content, list):
        import csv
        with open(file_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in content:
                if isinstance(row, (list, tuple)):
                    writer.writerow(row)
                else:
                    writer.writerow([row])
    elif isinstance(content, str):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        raise TypeError(f"Unsupported content type for save_file_to_folder: {type(content).__name__}")
    print(f"Saved file to folder: {file_name}")

def load_csv_file(file_path):
    import csv
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

def language_extension(language):   # pre zistenie pripony suboru podla jazyka
    lang = {
        "Python": "py",
        "JavaScript": "js",
        "Java": "java",
        "C++": "cpp",
        "C#": "cs",
        "Go": "go",
        "Ruby": "rb",
        "PHP": "php"
    }
    return lang.get(language, None)