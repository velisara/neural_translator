from translator import NeuralTranslator, LANGUAGES, CODES_TO_LANGUAGES
import sys
import os

def main():
    # Force UTF-8 encoding for Windows console
    try:
        # Change code page to UTF-8
        os.system('chcp 65001 > nul')
        # Reconfigure stdout and stdin for UTF-8
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stdin.reconfigure(encoding='utf-8')
    except Exception:
        pass
    
    translator = NeuralTranslator()
    
    print("=" * 80)
    print("  MULTILINGUAL NEURAL TRANSLATOR")
    print("=" * 80)
    print("  Supports 245 languages")
    print("  Handles mixed-language text automatically")
    print("  Enhanced for Indian languages (Hindi, Marathi, Kannada, etc.)")
    print("=" * 80)
    
    # Show available commands
    print("\nCommands:")
    print("  'q' or 'quit'   - Exit the translator")
    print("  'list'          - Show all supported languages")
    print("  'examples'      - Show usage examples")
    print("  'mode'          - Toggle translation mode (sentence/whole)")
    print("  Type any text in any language(s) to translate")
    
    # Translation mode
    split_mode = False  # Default: Whole text mode for better quality
    
    while True:
        print("\n" + "-" * 80)
        mode_indicator = "[Sentence Mode]" if split_mode else "[Whole Text Mode]"
        print(f"Current mode: {mode_indicator}")
        
        text = input("Enter text to translate: ").strip()
        
        if text.lower() in ['q', 'quit']:
            print("\nThank you for using Neural Translator!")
            break
        
        if text.lower() == 'mode':
            split_mode = not split_mode
            mode_name = "Sentence Mode" if split_mode else "Whole Text Mode"
            print(f"\nSwitched to: {mode_name}")
            if not split_mode:
                print("Better for: Long paragraphs, Indian languages, better context")
            else:
                print("Better for: Mixed languages, multiple separate sentences")
            continue
        
        if text.lower() == 'examples':
            print("\n" + "=" * 80)
            print("EXAMPLES:")
            print("=" * 80)
            print("\n1. Single language:")
            print("   Input:  Hello, how are you?")
            print("   Target: hi (Hindi)")
            print("   Output: नमस्ते, आप कैसे हैं?")
            print("\n2. For Indian languages - Whole Text Mode (default):")
            print("   Input:  Good morning. Have a wonderful day.")
            print("   Target: hi (Hindi)")
            print("   Output: शुभ प्रभात। एक अद्भुत दिन हो।")
            print("\n3. Mixed languages (use Sentence Mode):")
            print("   Command: mode")
            print("   Input:  Hello friend. Bonjour mon ami.")
            print("   Target: de (German)")
            print("   Output: Hallo Freund. Hallo mein Freund.")
            print("\nTip: Type 'mode' to switch between modes")
            print("=" * 80)
            continue
        
        if text.lower() == 'list':
            supported_langs = translator.get_supported_languages()
            print(f"\nSupported Languages ({len(supported_langs)} total):")
            print("-" * 80)
            
            # Highlight Indian languages
            indian_langs = {
                'hi': 'Hindi', 'mr': 'Marathi', 'kn': 'Kannada', 
                'ta': 'Tamil', 'te': 'Telugu', 'gu': 'Gujarati',
                'bn': 'Bengali', 'pa': 'Punjabi', 'ml': 'Malayalam',
                'or': 'Odia (Oriya)', 'as': 'Assamese'
            }
            
            print("\nIndian Languages:")
            for code, name in indian_langs.items():
                print(f"  {code:6s} - {name}")
            
            print("\nOther Popular Languages:")
            popular = ['en', 'es', 'fr', 'de', 'ja', 'zh-cn', 'ar', 'ru', 'pt', 'ko']
            for code in popular:
                name = supported_langs.get(code, "Unknown")
                print(f"  {code:6s} - {name}")
            
            print("\nType 'python show_languages.py' to see all 245 languages")
            continue
        
        if not text:
            print("Please enter some text to translate.")
            continue
            
        dest_lang = input("Enter target language code (e.g., 'hi', 'mr', 'kn', 'es'): ").strip().lower()
        
        # Validate language code
        supported_langs = translator.get_supported_languages()
        if dest_lang not in supported_langs:
            print(f"Warning: '{dest_lang}' might not be a valid language code.")
            print("Type 'list' to see supported languages.")
            continue
        
        print(f"\nAnalyzing input text...")
        
        # Detect mixed languages
        lang_detection = translator.detect_mixed_languages(text)
        
        if 'error' not in lang_detection and lang_detection['count'] > 0:
            print(f"\n{'='*80}")
            print("LANGUAGE DETECTION:")
            print(f"{'='*80}")
            
            if lang_detection['is_mixed']:
                print(f"🌍 MIXED LANGUAGES DETECTED ({lang_detection['count']} languages found):")
                for i, lang in enumerate(lang_detection['languages'], 1):
                    print(f"   {i}. {lang['name'].title()} ({lang['code']})")
                print(f"\n✨ All languages will be translated to: {supported_langs[dest_lang]}")
            else:
                lang = lang_detection['languages'][0]
                print(f"📝 Single language detected: {lang['name'].title()} ({lang['code']})")
            print(f"{'='*80}")
        
        print(f"\nTranslating to {supported_langs[dest_lang]}...")
        
        # Automatically use sentence mode for mixed languages
        use_split_mode = split_mode
        if lang_detection.get('is_mixed', False) and lang_detection.get('count', 0) > 1:
            use_split_mode = True
            if not split_mode:
                print("(Automatically using Sentence Mode for mixed languages)")
        
        # Recommend mode for Indian languages
        indian_lang_codes = ['hi', 'mr', 'kn', 'ta', 'te', 'gu', 'bn', 'pa', 'ml', 'or', 'as']
        if dest_lang in indian_lang_codes and use_split_mode and not lang_detection.get('is_mixed', False):
            print("Tip: Using Whole Text Mode gives better results for Indian languages")
        
        try:
            # Check if text is romanized (Latin characters only)
            is_romanized = all(ord(c) < 128 or c.isspace() or c in ',.!?;-' for c in text)
            
            # Detected languages from analysis
            detected_langs = [lang['code'] for lang in lang_detection.get('languages', [])]
            
            # Indian languages that support transliteration
            indian_langs = ['hi', 'mr', 'bn', 'gu', 'pa', 'or', 'ta', 'te', 'kn', 'ml', 'ne', 'sa']
            has_indian_lang = any(lang in indian_langs for lang in detected_langs)
            
            # Use transliteration if:
            # 1. Text is romanized (Latin only) AND
            # 2. Detected language is an Indian language
            use_transliteration = is_romanized and has_indian_lang
            
            # Aggressively use Smart Mode for:
            # 1. Romanized Indian languages
            # 2. Mixed languages
            # 3. Any long romanized text (likely to be mixed/code-switched)
            word_count = len(text.split())
            use_smart_mode = use_transliteration or \
                             (lang_detection.get('is_mixed', False) and lang_detection.get('count', 0) > 1) or \
                             (is_romanized and word_count > 4)

            if use_smart_mode:
                # Show which Indian language was detected
                if use_transliteration:
                    detected_indian_langs = [lang for lang in detected_langs if lang in indian_langs]
                    lang_names = [CODES_TO_LANGUAGES.get(code, code).title() for code in detected_indian_langs]
                    
                    if lang_names:
                        lang_str = ", ".join(lang_names)
                        print(f"✨ Romanized {lang_str} detected - using Smart Segmented Translation!")
                    else:
                        print("✨ Romanized Indian language detected - using Smart Segmented Translation!")
                else:
                    print("✨ Mixed languages detected - using Smart Segmented Translation!")
                
                # Use the new Smart Segmented Translation
                result = translator.translate_smart(text, dest=dest_lang)
                used_langs = detected_langs # Approximate for display
            else:
                # Standard translation
                result = translator.translate(text, dest=dest_lang, src='auto', split_sentences=use_split_mode)
                # Detect source language separately
                detection = translator.detect_language(text)
                used_langs = [detection] if detection and not detection.startswith("Error") else []
            
            if result.startswith("Error:"):
                print(f"\nERROR: {result}")
            else:
                print(f"\n{'='*80}")
                print(f"Original:    {text}")
                print(f"Translated:  {result}")
                print(f"Target:      {supported_langs.get(dest_lang, dest_lang)} ({dest_lang})")
                print(f"{'='*80}")
                
                # Show all detected languages
                if used_langs:
                    # Filter out 'auto' or None
                    valid_langs = [l for l in used_langs if l and l != 'auto']
                    if valid_langs:
                        lang_names = [f"{LANGUAGES.get(code, code).title()} ({code})" for code in valid_langs]
                        print(f"Detected source: {', '.join(lang_names)}")
                    else:
                        print(f"Detected source: Unknown")
                else:
                    print(f"Detected source: Unknown")
                    
        except Exception as e:
            print(f"\nERROR: An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
