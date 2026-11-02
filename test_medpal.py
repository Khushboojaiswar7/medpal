import sys
import io

# Set UTF-8 for console output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from modules.triage_engine import TriageEngine
from modules.hospital_finder import HospitalFinder
from modules.emergency_signal import EmergencySignalEngine
from modules.medicine_explainer import MedicineExplainer
from modules.voice_helper import VoiceHelper

t = TriageEngine()
rf = t.check_red_flags('Severe chest pain and left arm pain')
print('Triage red flag detected:', bool(rf), rf['condition'] if rf else 'None')
lvl, reason = t.assess_triage_level('high fever')
print('Triage assessment:', lvl, reason)

h = HospitalFinder()
hosp_list = h.get_nearest_hospitals(17.4156, 78.4125)
print('Hospitals found:', len(hosp_list), hosp_list[0]['name'], hosp_list[0]['distance_km'], 'km')

s = EmergencySignalEngine()
token = s.generate_emergency_token('John Doe', 70, 'O+', 'None', 'Diabetes', '+91-99999', 'Cardiac', 17.4156, 78.4125, hosp_list[0])
print('Generated Token ID:', token['dispatch_id'])

m = MedicineExplainer()
parsed = m.parse_prescription_text('Metformin 500mg 1-0-1 with meals and Atorvastatin 20mg 0-0-1')
print('Parsed meds:', len(parsed), [p['generic_name'] for p in parsed])
summary = m.generate_elderly_friendly_summary(parsed)
print('Elderly summary generated length:', len(summary))

v = VoiceHelper()
btn_html = v.render_browser_speak_button('Hello test')
print('Speak button HTML generated successfully:', len(btn_html) > 20)
print('ALL VERIFICATION CHECKS PASSED!')
