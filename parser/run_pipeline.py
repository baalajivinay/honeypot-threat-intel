import sys
sys.path.insert(0, '/home/vinay/honeypot-threat-intel/ai')

from db_setup import init_db
from log_parser import parse_logs
from webhook_trigger import send_to_make
from ollama_analyzer import analyze_attack, get_latest_attack

print("Starting pipeline...")
init_db()
parse_logs()

attack = get_latest_attack()
if attack:
    summary = analyze_attack(attack)
    attack['ai_summary'] = summary
    print(f"\n🤖 AI Summary:\n{summary}\n")

send_to_make()
print("Pipeline complete.")
