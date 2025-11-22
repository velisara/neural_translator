# Multilingual Neural Translator with Mixed Language Detection

A powerful Python-based translator that **automatically detects mixed languages** in your input and translates everything to your target language among 245+ supported languages.

##  NEW FEATURE: Mixed Language Detection

The translator now **automatically detects when you use multiple languages** in the same sentence!

### Example:
```
Input: "Hello friend. Bonjour mon ami. Hola amigo."

LANGUAGE DETECTION:
 MIXED LANGUAGES DETECTED (3 languages found):
   1. French (fr)
   2. English (en)
   3. Spanish (es)

 All languages will be translated to: german

1. Make sure you have Python installed (Python 3.7+)

2. Install required dependencies:
```bash
pip install googletrans==4.0.2
```

---

## Usage

### Run the Interactive Translator

```bash
python main.py
```

### Commands

- Type any text → Translates and shows detected languages
- `mode` - Switch between Sentence/Whole Text mode
- `list` - Show all 245 supported languages
- `examples` - See usage examples
- `q` or `quit` - Exit

---

## Example Sessions

### Example 1: Mixed English + French + Spanish → German
```
Enter text to translate: Hello friend. Bonjour mon ami. Hola amigo.
Enter target language code: de

Analyzing input text...

LANGUAGE DETECTION:
MIXED LANGUAGES DETECTED (3 languages found):
   1. French (fr)
   2. English (en)
   3. Spanish (es)

✨ All languages will be translated to: german

Original:    Hello friend. Bonjour mon ami. Hola amigo.
Translated:  Hallo Freund. Hallo mein Freund. Hallo Freund.
```

### Example 2: Mixed English + Hindi + Spanish → French
```
Enter text to translate: I love programming. मुझे कोडिंग पसंद है. Me gusta programar.
Enter target language code: fr

LANGUAGE DETECTION:
MIXED LANGUAGES DETECTED (3 languages found):
   1. Hindi (hi)
   2. English (en)
   3. Spanish (es)

Translated: J'aime programmer. J'aime coder. J'aime programmer.
```

---

## API Usage

You can also use the translator programmatically:

```python
from translator import NeuralTranslator

translator = NeuralTranslator()

# Detect mixed languages
text = "Hello. Bonjour. Hola."
detection = translator.detect_mixed_languages(text)

if detection['is_mixed']:
    print(f"Mixed languages found: {detection['count']}")
    for lang in detection['languages']:
        print(f"  - {lang['name']} ({lang['code']})")

# Translate to target language
result = translator.translate(text, dest='de')
print(f"Translation: {result}")
```

---

## Translation Modes

### Whole Text Mode (Default)
- Best for: Single language, Indian languages
- Better context and natural flow
- Recommended for Hindi, Marathi, Kannada, etc.

### Sentence Mode
- Best for: Mixed languages in separate sentences
- Translates each sentence independently
- Use `mode` command to switch

---

## Supported Languages

### Indian Languages:
- Hindi (hi), Marathi (mr), Kannada (kn)
- Tamil (ta), Telugu (te), Gujarati (gu)
- Bengali (bn), Punjabi (pa), Malayalam (ml)
- Odia (or), Assamese (as)

### Popular Languages:
- English (en), Spanish (es), French (fr)
- German (de), Japanese (ja), Chinese (zh-cn)
- Arabic (ar), Russian (ru), Portuguese (pt)
- Korean (ko), Italian (it), Dutch (nl)

**Total: 245 languages!**

Type `list` in the translator or run `python show_languages.py` to see all.

---

## Files

### Core Application:
- **`main.py`** - Main translator application  **RUN THIS**
- **`translator.py`** - Translation engine with mixed language detection

### Optional:
- `test_translator.py` - Unit tests
- `show_languages.py` - Display all 245 languages
- `compare_modes.py` - Compare translation modes
- `demo_mixed_detection.py` - Demo of mixed language detection
- `README.md` - This file
- `SUPPORTED_LANGUAGES.txt` - Complete language list

---

## How It Works

1. **Input Analysis**: When you enter text, it analyzes for multiple languages
2. **Language Detection**: Identifies all languages present in your input
3. **Display Detection**: Shows you which languages were found (e.g., "Detected source: Hindi (hi), Marathi (mr)")
4. **Translation**: Translates ALL detected languages to your target language
5. **Output**: Displays translation directly in terminal

The translator splits text by sentences (or keeps it whole in Whole Text Mode) and intelligently detects each language component.

---

## Mixed Language Detection Details

The `detect_mixed_languages()` function:
- Analyzes your input text word by word
- Detects the language of each segment
- Identifies all unique languages present
- Returns a detailed report with language codes and names

**Example:**
```python
Input: "Hello. Bonjour. Hola."

Returns:
{
    'is_mixed': True,
    'count': 3,
    'languages': [
        {'code': 'en', 'name': 'english'},
        {'code': 'fr', 'name': 'french'},
        {'code': 'es', 'name': 'spanish'}
    ]
}
```

---

## Tips for Best Results

Use complete sentences** with proper grammar  
Switch to Whole Text Mode** for Indian languages (type `mode`)  
Accept mixed output** for technical terms (normal behavior)  
Use Windows Terminal** for better Unicode support  

---

## Running Tests

```bash
python test_translator.py
```

---

## Requirements

- Python 3.7+
- googletrans==4.0.2
- Internet connection (uses Google Translate API)

---

## Notes

- The translator requires an internet connection
- Google Translate may rate-limit heavy usage
- Translation quality depends on Google Translate's algorithms
- Mixed language detection works best with meaningful text chunks (2+ words per language)

---

## License

Open source - feel free to use and modify!

---

**Start translating with mixed language detection:**
```bash
python main.py
```

Supports **245 languages** with automatic mixed language detection!
