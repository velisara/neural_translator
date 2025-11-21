import re
import sys
from deep_translator import GoogleTranslator, single_detection
from deep_translator import constants

# Apply patch to support all 245+ languages
try:
    import patch_languages
    patch_languages.patch_deep_translator()
except ImportError:
    print("Warning: patch_languages module not found. Using default language list.")
except Exception as e:
    print(f"Warning: Failed to patch languages: {e}")

# Define LANGUAGES alias after patching so it includes the new languages
LANGUAGES = constants.GOOGLE_LANGUAGES_TO_CODES

# Create reverse mapping (Code -> Name) for lookups
CODES_TO_LANGUAGES = {v: k for k, v in LANGUAGES.items()}

# Check if transliteration is available
try:
    from google.transliteration import transliterate_text
    TRANSLITERATION_AVAILABLE = True
except ImportError:
    TRANSLITERATION_AVAILABLE = False

class NeuralTranslator:
    def __init__(self):
        pass # No persistent translator needed for deep-translator

    def translate(self, text, dest='en', src='auto', split_sentences=True):
        """
        Translate text to the destination language.
        """
        try:
            translator = GoogleTranslator(source=src, target=dest)
            
            # Option to translate without splitting
            if not split_sentences:
                return translator.translate(text)
            
            # Split text by sentence terminators
            parts = re.split(r'([.!?。;]+)', text)
            
            translated_parts = []
            for part in parts:
                if not part.strip():
                    translated_parts.append(part)
                    continue
                
                leading_space = part[:len(part) - len(part.lstrip())]
                trailing_space = part[len(part.rstrip()):]
                stripped_part = part.strip()
                
                result = translator.translate(stripped_part)
                translated_parts.append(leading_space + result + trailing_space)
            
            return "".join(translated_parts)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def translate_mixed_text(self, text, dest='en'):
        """
        Special translation for mixed-language text.
        """
        try:
            translator = GoogleTranslator(source='auto', target=dest)
            parts = re.split(r'([,.!?;]+)', text)
            
            translated_parts = []
            for part in parts:
                if not part.strip() or part.strip() in ',.!?;':
                    translated_parts.append(part)
                    continue
                
                leading_space = part[:len(part) - len(part.lstrip())]
                trailing_space = part[len(part.rstrip()):]
                stripped_part = part.strip()
                
                try:
                    result = translator.translate(stripped_part)
                    translated_parts.append(leading_space + result + trailing_space)
                except:
                    translated_parts.append(part)
            
            return "".join(translated_parts)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def transliterate_to_native(self, text, target_script='hi'):
        if not TRANSLITERATION_AVAILABLE:
            return text
        try:
            return transliterate_text(text, lang_code=target_script)
        except:
            return text
    
    def translate_with_transliteration(self, text, dest='en', detected_lang=None):
        """
        Translate text with automatic transliteration.
        """
        try:
            indian_langs = ['hi', 'mr', 'bn', 'gu', 'pa', 'or', 'ta', 'te', 'kn', 'ml', 'ne', 'sa']
            false_positive_langs = ['vi', 'tl', 'id', 'ms', 'so', 'da', 'et', 'af', 'nl', 'fi', 'no', 'sw']
            
            parts = re.split(r'([,.!?;]+)', text)
            result_parts = []
            detected_langs_in_parts = []
            last_valid_indian_lang = None
            
            translator = GoogleTranslator(source='auto', target=dest)
            
            for part in parts:
                if not part.strip() or part.strip() in ',.!?;':
                    result_parts.append(part)
                    continue
                
                leading_space = part[:len(part) - len(part.lstrip())]
                trailing_space = part[len(part.rstrip()):]
                stripped_part = part.strip()
                
                try:
                    part_lang = self.detect_language(stripped_part)
                    part_is_latin = all(ord(c) < 128 or c.isspace() for c in stripped_part)
                    
                    use_translit = False
                    target_translit_lang = part_lang
                    
                    if part_is_latin and TRANSLITERATION_AVAILABLE:
                        if part_lang in indian_langs:
                            use_translit = True
                            last_valid_indian_lang = part_lang
                            detected_langs_in_parts.append(part_lang)
                        elif part_lang in false_positive_langs and last_valid_indian_lang:
                            use_translit = True
                            target_translit_lang = last_valid_indian_lang
                            detected_langs_in_parts.append(last_valid_indian_lang)
                    
                    if use_translit:
                        native_text = self.transliterate_to_native(stripped_part, target_translit_lang)
                        # Translate native text
                        t = GoogleTranslator(source=target_translit_lang, target=dest)
                        result = t.translate(native_text)
                        result_parts.append(leading_space + result + trailing_space)
                    else:
                        if part_lang not in false_positive_langs:
                            detected_langs_in_parts.append(part_lang)
                        result = translator.translate(stripped_part)
                        result_parts.append(leading_space + result + trailing_space)
                except:
                    result_parts.append(part)
            
            unique_langs = list(set(detected_langs_in_parts))
            return "".join(result_parts), unique_langs
        except Exception as e:
            return f"Error: {str(e)}", []

    def detect_mixed_languages(self, text):
        """
        Detect all languages present in a text using word-level analysis.
        """
        try:
            # Patterns for word-level detection
            patterns = {
                'hi': ['ek', 'hai', 'hain', 'ko', 'ka', 'ki', 'ke', 'se', 'me', 'par', 'aur', 'ya', 'jisme', 'karta', 'kaun', 
                       'bol', 'raha', 'rahe', 'rahi', 'andar', 'bahar', 'kya', 'kab', 'kaise', 'bhi', 'toh', 'magar', 'lekin',
                       'namaste', 'namaskar', 'aap', 'tum', 'mai', 'mera', 'tera', 'theek', 'hun'],
                'kn': ['idu', 'ide', 'tumba', 'ge', 'alli', 'illi', 'yava', 'yaake', 'hege', 'ella', 'nim', 'nanna', 'beku', 'maadi'],
                'en': ['speaker', 'diarization', 'process', 'system', 'different', 'speakers', 'separate', 'audio', 
                       'real-time', 'applications', 'meetings', 'useful', 'like', 'and', 'is', 'the', 'for', 'to', 'in', 'of',
                       'hello', 'world', 'how', 'what', 'where', 'when'],
                'gu': ['khem', 'cho', 'majama', 'su', 'chhe', 'tamara', 'mara'],
                'mr': ['kasa', 'kay', 'kuthe', 'kevha', 'tumcha', 'maza'],
                'pa': ['tuhada', 'ki', 'haal', 'hai', 'kiddan', 'sat', 'sri', 'akal'],
                'ta': ['idu', 'enna', 'epdi', 'enge', 'yaar', 'naan', 'nee', 'avan', 'aval'],
                'te': ['idi', 'emi', 'ela', 'ekkada', 'evaru', 'nenu', 'nuvvu', 'atanu', 'aame']
            }
            
            detected_langs_set = set()
            words = text.split()
            
            # 1. Word-level pattern matching
            for word in words:
                word_lower = word.lower().strip('.,!?-')
                if not word_lower: continue
                
                for lang, vocab in patterns.items():
                    if word_lower in vocab:
                        detected_langs_set.add(lang)
            
            # 2. Fallback to chunk-based detection for unknown words
            if not detected_langs_set:
                parts = re.split(r'([,.!?;]+)', text)
                for part in parts:
                    if not part.strip() or part.strip() in ',.!?;': continue
                    try:
                        lang = self.detect_language(part.strip())
                        if lang and lang != 'auto':
                            detected_langs_set.add(lang)
                    except:
                        pass

            # Convert to list
            unique_langs = list(detected_langs_set)
            
            # Format for return
            lang_objects = []
            for code in unique_langs:
                # Reverse lookup for name
                name = CODES_TO_LANGUAGES.get(code, code)
                lang_objects.append({'code': code, 'name': name})
            
            return {
                'is_mixed': len(unique_langs) > 1,
                'count': len(unique_langs),
                'languages': lang_objects
            }
        except Exception as e:
            return {'error': str(e), 'is_mixed': False, 'count': 0, 'languages': []}

    def detect_language(self, text):
        """
        Detect language using deep-translator + patterns.
        """
        try:
            # Strategy 1: Native script
            has_non_latin = any(ord(c) > 127 for c in text if c.isalpha())
            if has_non_latin:
                return single_detection(text, api_key='auto')
            
            # Strategy 2: Patterns
            text_lower = text.lower().strip()
            patterns = {
                'en': ['hello', 'world', 'the', 'is', 'are', 'how', 'what', 'where', 'when', 'you', 'your', 'good', 'morning', 
                       'and', 'like', 'this', 'that', 'have', 'has', 'with', 'from'],
                'es': ['hola', 'mundo', 'como', 'que', 'donde', 'cuando', 'el', 'la', 'los', 'las'],
                'fr': ['bonjour', 'monde', 'comment', 'que', 'où', 'quand', 'le', 'la', 'les'],
                'de': ['hallo', 'welt', 'wie', 'was', 'wo', 'wann', 'der', 'die', 'das'],
                'hi': ['namaste', 'namaskar', 'kaise', 'kya', 'kahan', 'kab', 'aap', 'tum', 'mai', 'mera', 'tera', 'theek', 'hun',
                       'ek', 'hai', 'hain', 'ko', 'ka', 'ki', 'ke', 'se', 'me', 'par', 'aur', 'ya', 'jisme', 'karta', 'kaun', 
                       'bol', 'raha', 'rahe', 'rahi', 'andar', 'bahar'],
                'gu': ['khem', 'cho', 'majama', 'su', 'chhe', 'tamara', 'mara'],
                'mr': ['kasa', 'kay', 'kuthe', 'kevha', 'tumcha', 'maza'],
                'pa': ['tuhada', 'ki', 'haal', 'hai', 'kiddan', 'sat', 'sri', 'akal'],
                'kn': ['idu', 'ide', 'tumba', 'ge', 'alli', 'illi', 'yava', 'yaake', 'hege', 'ella', 'nim', 'nanna'],
                'ta': ['idu', 'enna', 'epdi', 'enge', 'yaar', 'naan', 'nee', 'avan', 'aval'],
                'te': ['idi', 'emi', 'ela', 'ekkada', 'evaru', 'nenu', 'nuvvu', 'atanu', 'aame'],
            }
            
            max_matches = 0
            best_lang = None
            exact_match_lang = None
            
            for lang, words in patterns.items():
                matches = sum(1 for word in words if word in text_lower)
                if matches > max_matches:
                    max_matches = matches
                    best_lang = lang
                if text_lower in words:
                    exact_match_lang = lang
            
            if exact_match_lang and len(text_lower.split()) == 1:
                return exact_match_lang
            if max_matches >= 2:
                return best_lang
            
            hint_lang = best_lang if max_matches == 1 else None
            
            # Strategy 3: deep-translator detection
            try:
                detected = single_detection(text, api_key='auto')
                false_positive_langs = ['vi', 'tl', 'id', 'ms', 'so', 'da', 'et', 'nl', 'fi', 'no', 'af', 'sw']
                
                if detected in false_positive_langs and hint_lang:
                    return hint_lang
                if detected == 'en' and hint_lang in ['hi', 'gu', 'mr', 'pa', 'kn', 'ta', 'te']:
                    return hint_lang
                return detected
            except:
                return hint_lang if hint_lang else 'en'
        except:
            return 'auto'

    def translate_smart(self, text, dest='hi'):
        """
        Smart segmented translation using deep-translator.
        Strategy: Transliterate Romanized parts to Native Script first, 
        then translate the WHOLE sentence to preserve context and grammar.
        """
        # Patterns
        patterns = {
            'hi': ['ek', 'hai', 'hain', 'ko', 'ka', 'ki', 'ke', 'se', 'me', 'par', 'aur', 'ya', 'jisme', 'karta', 'kaun', 
                   'bol', 'raha', 'rahe', 'rahi', 'andar', 'bahar', 'kya', 'kab', 'kaise', 'bhi', 'toh', 'magar', 'lekin'],
            'kn': ['idu', 'ide', 'tumba', 'ge', 'alli', 'illi', 'yava', 'yaake', 'hege', 'ella', 'nim', 'nanna', 'beku', 'maadi'],
            'en': ['speaker', 'diarization', 'process', 'system', 'different', 'speakers', 'separate', 'audio', 
                   'real-time', 'applications', 'meetings', 'useful', 'like', 'and', 'is', 'the', 'for', 'to', 'in', 'of']
        }
        
        words = text.split()
        segments = []
        current_segment = []
        current_lang = 'en'
        
        # 1. Segment the text
        for word in words:
            word_lower = word.lower().strip('.,!?-')
            detected_word_lang = None
            for lang, vocab in patterns.items():
                if word_lower in vocab:
                    detected_word_lang = lang
                    break
            if not word_lower.isalpha():
                detected_word_lang = current_lang
            if not detected_word_lang:
                detected_word_lang = current_lang
            
            if detected_word_lang != current_lang:
                if current_segment:
                    segments.append({'text': " ".join(current_segment), 'lang': current_lang})
                current_segment = [word]
                current_lang = detected_word_lang
            else:
                current_segment.append(word)
                
        if current_segment:
            segments.append({'text': " ".join(current_segment), 'lang': current_lang})
            
        # 2. Pre-process: Transliterate Romanized parts to Native Script
        mixed_script_parts = []
        
        for seg in segments:
            text_seg = seg['text']
            lang = seg['lang']
            
            try:
                if lang in ['hi', 'kn', 'mr', 'gu', 'pa', 'ta', 'te', 'bn', 'ml']:
                    # Transliterate to Native Script (e.g. "ek" -> "एक")
                    native_text = self.transliterate_to_native(text_seg, target_script=lang)
                    mixed_script_parts.append(native_text)
                else:
                    # Keep English/Other as is
                    mixed_script_parts.append(text_seg)
            except:
                mixed_script_parts.append(text_seg)
        
        # Join to form the "Mixed Script" sentence
        # e.g. "Speaker diarization एक process है..."
        mixed_script_sentence = " ".join(mixed_script_parts)
        
        # 3. Translate the WHOLE sentence at once
        # This preserves grammar and context!
        try:
            # CRITICAL: For Indian target languages, we must treat the source as 'en' (English/Hinglish).
            # If we use 'auto', Google detects the native script and assumes the Latin parts 
            # are intentional code-switching, leaving them untranslated.
            # By forcing 'en', we tell Google to translate the Latin parts (English) to the target.
            
            # CRITICAL REFINEMENT:
            # 1. For Hindi Target ('hi'): Force source='en'. 
            #    Reason: Input is usually Hinglish. If we use 'auto'/'hi', Google preserves English words (Code-switching).
            #    Forcing 'en' makes it translate "process" -> "प्रक्रिया".
            #
            # 2. For Other Indian Targets ('mr', 'kn', etc.): Use source='auto'.
            #    Reason: If input is Hinglish ("ke andar"), 'auto' detects Hindi.
            #    Hindi -> Marathi translation is excellent ("ke andar" -> "madhil").
            #    If we forced 'en', it would treat "ke andar" as English words and fail to translate grammar correctly.
            
            if dest == 'hi':
                translator = GoogleTranslator(source='en', target=dest)
            else:
                translator = GoogleTranslator(source='auto', target=dest)
                
            final_translation = translator.translate(mixed_script_sentence)
            return final_translation
        except Exception as e:
            return f"Error: {str(e)}"

    def get_supported_languages(self):
        # deep-translator provides Name -> Code (e.g. {'hindi': 'hi'})
        # We need Code -> Name (e.g. {'hi': 'hindi'}) for compatibility
        return {v: k for k, v in LANGUAGES.items()}
