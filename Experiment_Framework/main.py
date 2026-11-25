import inspect
import importlib
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import Experiment_Framework.funcion.file_manager as fm

import platform

os_name = platform.system()

print("os_name:", os_name)

CODE_GENERATION_TASKS = str(PROJECT_ROOT / fm.CODE_GENERATION_TASKS)


LLM_models = "Experiment_Framework.LLM_models"


from Experiment_Framework.funcion.file_manager import PRINTS_SHORTS


def LLM_providers(provider):
    providers = {
        "Gemini": "gemini_gen",
        "Ollama": "ollama_gen"
    }
    return providers.get(provider, None)

def test__folders(folder_path): #spracovanie vstupou v testovacom adresari
    print(f"\tProcessing folder: \033[90m{folder_path}\033[0m")
    files = fm.open_folder_return_files(folder_path)
    #print(files)
    promp=""
    if not any(file.endswith("promp.txt") for file in files):
        print(f"\033[93m'promp.txt' not found in {folder_path}\033[0m")
        return False
    else:
        promp = fm.read_file(os.path.join(folder_path, "promp.txt"))

    setup=""
    if not any(file.endswith("setup.txt") for file in files):
        print(f"\033[93m'setup.txt' not found in {folder_path}\033[0m")
        return False
    else:
        setup = fm.load_setup(os.path.join(folder_path, "setup.txt"))

    #print(f"\tSetup: {setup}")

    skip_value = setup.get('skip', False)
    should_skip = skip_value if isinstance(skip_value, bool) else str(skip_value).lower() == 'true'
    if should_skip:
        print(f"\033[92mSkipping setup for folder: {folder_path}\033[0m")
        return False
    
    #print(f"language: {setup.get('language', 'Not specified')}")
    if setup.get('models', None) is None:
        print(f"\033[93mmodels not specified in setup for folder: {folder_path}\033[0m")
        return False
    if setup.get('language', None) is None:
        print(f"\033[93mLanguage not specified in setup for folder: {folder_path}\033[0m")
        return False
    if fm.language_extension(setup.get('language', None)) is None:
        print(f"\033[93mUnsupported language '{setup.get('language', None)}' specified in setup for folder: {folder_path}\033[0m")
        return False
    
    if setup.get('num_generations', None) is None:
        print(f"\033[93mnum_generations not specified in setup for folder: {folder_path}\033[0m")
        return False
    print(f"\tgenerated code count for LLM: {setup.get('num_generations', 0)}\n")
    #print(f"\ttest: {fm.count_files_in_folder(folder_path,'promp')}")

    return generate_code_from_llm_model(promp, setup, folder_path)

def generate_code_from_llm_model(promp, setup, folder_path):

    print(Path(folder_path).name)

    folder_path = os.path.join(fm.RESULTS_FOLDER, os_name,Path(folder_path).name)
    #print("Save folder:", folder_path)

    #folder_path = folder_path.replace(CODE_GENERATION_TASKS, CODE_GENERATION_TASKS+"_"+os_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    any_model_processed = False
    LLM = {}
    for model in setup.get('models', []):
        #print(f"\nGenerating code with model: {model}")
        if "_" not in model:
            print(
                f"\033[93mInvalid model format '{model}' in setup for folder: {folder_path}. "
                "Expected format '<provider>_<model>'. Preskakujem.\033[0m"
            )
            continue

        provider_name, LLM_model = model.split('_', 1)
        if not LLM_model.strip():
            print(
                f"\033[93mInvalid model name '{model}' in setup for folder: {folder_path}. "
                "Model časť je prázdna. Preskakujem.\033[0m"
            )
            continue

        LLM_provider = provider_name
        #print(f"LLM_provider: {LLM_provider}, LLM_model: {LLM_model}")
        LLM_provider = LLM_providers(LLM_provider)
        if LLM_provider is None:
            print(f"\033[91mUnsupported LLM_provider '{provider_name}' specified in setup for folder: {folder_path}\033[0m")
            continue
        LLM[model] = {"provider": LLM_provider, "model": LLM_model, "num_generated": fm.count_code_genetate(folder_path, model, setup.get('language', None))}##-----------------
        #print(f"Using LLM_provider: {LLM_provider}")
        #safe_int = setup.get('num_generations', 0)
        #while setup.get('num_generations', 0) > fm.count_code_genetate(folder_path, model, setup.get('language', None)) and safe_int > 0:


    #print(json.dumps(LLM, indent=4, ensure_ascii=False))
    int_change = True
    while int_change:
        int_change = False
        if PRINTS_SHORTS:
            print(json.dumps(LLM, indent=4, ensure_ascii=False))

        for model in LLM:
            model_info = LLM[model]
            provider = model_info["provider"]
            llm_model = model_info["model"]
            if PRINTS_SHORTS:
                print(f"Calling LLM model: {model_info['model']} num_generated: {model_info['num_generated']}")

            if model_info["num_generated"] >= setup.get('num_generations', 0):
                if PRINTS_SHORTS:
                    print(f"\033[90mNo new code generated for model '{model}' in folder: {folder_path}\033[0m")
                any_model_processed = True
                continue
            code = call_llm(provider, llm_model, setup, promp)
            if code is None:
                continue

            saved_index = fm.save_code_to_file(
                folder_path, model, code, setup.get('language', None)
            )
            LLM[model]["num_generated"] = saved_index + 1
            any_model_processed = True
            int_change = True
        

    if not any_model_processed:
        print(f"\033[93mŽiadny model úspešne nespracoval generovanie vo folderi: {folder_path}\033[0m")
        return False

    return True


def call_llm(provider, LLM_model, setup, promp):
    if provider is None or LLM_model is None:
        print("\033[93mProvider and model must be specified.\033[0m")
        return None
    
    module_name = f"Experiment_Framework.LLM_models.{provider}"
    module = importlib.import_module(module_name)
    LLL_func = getattr(module, "generate_code", None)
    if LLL_func is None:
        print(f"\033[93mFunction 'generate_code' not found in LLM_provider '{provider}' for folder: {None}\033[0m")
        return None
    
    accepted_params = set(inspect.signature(LLL_func).parameters)
    
    inputs = {
        key: value
        for key, value in setup.items()
        if key not in {"models", "num_generations"} and key in accepted_params
    }
    inputs["prompt"] = promp
    inputs["model"] = LLM_model
    
    inputs = {
        key: value
        for key, value in inputs.items()
        if key in accepted_params or key in {"prompt", "model"}
    }
    try:
        code = LLL_func(**inputs)
    except RuntimeError as exc:
        print(
            f"\033[93mModel '{LLM_model}' zlyhal: {exc}. "
            "Preskakujem na ďalší model.\033[0m"
        )
        return None

    if code is None:
        print(f"\033[93mNo code generated by model '{LLM_model}'\033[0m")
        return None

    if PRINTS_SHORTS:
        print(f"Generated code: length {len(code)}")
    else:
        print(".", end="", flush=True)

    return code
    

def main():
    print("Zacinam prechadzat testovaciu zlozk:")

    folders = fm.open_folder_return_folders(fm.PROMPTS_FOLDER) #otvorenie hlavneh testovacieho adresara

    count = 0
    for folder in folders:
        #print(Path(folder).name)

        if not test__folders(folder):
            print(f"\033[91mTest failed for folder: {folder}\033[0m")
        else:
            print(f"\033[92mTest passed for folder: {folder}\033[0m")
        count += 1
        print(f"{count/len(folders)*100:.2f}%\n")

    pass

if __name__ == "__main__":
    main()