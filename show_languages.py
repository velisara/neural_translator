from translator import NeuralTranslator
import sys

# Ensure proper encoding for special characters
sys.stdout.reconfigure(encoding='utf-8')

def show_all_languages():
    try:
        translator = NeuralTranslator()
        languages = translator.get_supported_languages()
        
        print("=" * 60)
        print(f"SUPPORTED LANGUAGES ({len(languages)} Total)")
        print("=" * 60)
        print(f"{'CODE':<10} | {'LANGUAGE NAME'}")
        print("-" * 60)
        
        # Sort by language name for easier reading
        sorted_langs = sorted(languages.items(), key=lambda x: x[1])
        
        for code, name in sorted_langs:
            print(f"{code:<10} | {name.title()}")
            
        print("=" * 60)
        
    except Exception as e:
        print(f"Error fetching languages: {e}")

if __name__ == "__main__":
    show_all_languages()
