"""
MedPal Voice & Accessibility Helper Engine
Generates Text-to-Speech (TTS) audio using gTTS and HTML5 Web Speech API
for elderly and low-literacy users who prefer listening over reading.
"""

import io
import re
from typing import Optional

try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False

class VoiceHelper:
    def __init__(self):
        pass

    def clean_text_for_speech(self, text: str) -> str:
        """Removes markdown formatting and emojis for smooth audio reading."""
        clean = re.sub(r'[*_#`~]', '', text)
        clean = re.sub(r'https?://\S+', '', clean)
        clean = re.sub(r'[^\w\s.,?!;:()\-/]', '', clean)
        return clean.strip()

    def generate_audio_bytes(self, text: str, lang: str = "en") -> Optional[io.BytesIO]:
        """
        Synthesizes speech audio using gTTS.
        Returns BytesIO buffer for st.audio.
        """
        if not HAS_GTTS:
            return None
        clean_text = self.clean_text_for_speech(text)
        if not clean_text:
            return None
        
        # Map languages
        lang_code = "en"
        if lang.lower() in ["hi", "hindi"]:
            lang_code = "hi"
        elif lang.lower() in ["es", "spanish"]:
            lang_code = "es"
        elif lang.lower() in ["fr", "french"]:
            lang_code = "fr"

        try:
            tts = gTTS(text=clean_text[:500], lang=lang_code, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp
        except Exception:
            return None

    def render_browser_speak_button(self, text: str, button_label: str = "🔊 Read Aloud") -> str:
        """
        Creates an accessible HTML/JS Web Speech API button that speaks
        directly in the user's browser with natural client-side voice synthesis.
        """
        safe_text = self.clean_text_for_speech(text).replace('"', '\\"').replace("'", "\\'")
        html = f"""
        <div style="margin: 8px 0;">
            <button onclick="
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{safe_text}');
                msg.rate = 0.9;
                msg.pitch = 1.0;
                window.speechSynthesis.speak(msg);
            " style="
                background: linear-gradient(135deg, #2563EB, #1D4ED8);
                color: white;
                border: none;
                padding: 8px 18px;
                font-size: 15px;
                font-weight: 600;
                border-radius: 8px;
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0,0,0,0.15);
                display: inline-flex;
                align-items: center;
                gap: 6px;
            ">
                {button_label}
            </button>
            <button onclick="window.speechSynthesis.cancel();" style="
                background: #E5E7EB;
                color: #374151;
                border: none;
                padding: 8px 14px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 8px;
                cursor: pointer;
                margin-left: 6px;
            ">
                ⏹️ Stop Audio
            </button>
        </div>
        """
        return html
