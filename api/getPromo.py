
from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime, timedelta
import hashlib
import random

app = FastAPI()

promo_codes = [
    "JU75OLZ3", "TO38J351", "ZXTVL2ZA", "CDKPVF93", "OLWFH5SR", "8D9SZ6RN",
    "K0L45XUN", "ZGJC9H3M", "T2XFMB8K", "6Y4BJQGT", "MF3RZ1VU", "R5TJ6EPO",
    "N8AXCV9B", "UHZR5KQW", "XP2JKNDV", "9TYSFMW4", "EBGJKRUX", "7QMRDY4K",
    "FXO1CAJP", "WBZL9S7N", "PL6RVEGM", "Y1Q9KO2D", "C4M7GNJF", "VAZH0QIW",
    "DH82MKT3", "U9L3YFNE", "BJ6TVSZO", "NHK7F53A", "QRTZLM09", "MA8UKIV2",
    "XJZ6EYOL", "2QVMGXH5", "K9RBH7TJ", "WLPD9YMV", "TF0ROSKQ", "E2JB7C6U",
    "AYVHZGX9", "L8FRCXJ5", "NPTMQJLY", "G1X8UB3A", "HOM2YVK7", "JTEV5BWP",
    "CL3YDZ78", "B2PMR1UG", "S98KQH0C", "4JMFZCTY", "V0UXQPGI", "KMJ2RLF8",
    "Y3CNB65Z", "DAWFMPT6"
]

issued_codes = {}
user_timestamps = {}

class PromoRequest(BaseModel):
    fingerprint: str

@app.post("/api/getPromo")
async def get_promo(req: PromoRequest):
    fingerprint_hash = hashlib.sha256(req.fingerprint.encode()).hexdigest()
    now = datetime.utcnow()

    if fingerprint_hash in user_timestamps:
        last_time = user_timestamps[fingerprint_hash]
        if now - last_time < timedelta(minutes=60):
            return {"status": "wait", "message": "Попробуйте позже. Код можно получить раз в 60 минут."}

    available_codes = list(set(promo_codes) - set(issued_codes.values()))
    if not available_codes:
        return {"status": "wait", "message": "Промокоды закончились."}

    selected_code = random.choice(available_codes)
    issued_codes[fingerprint_hash] = selected_code
    user_timestamps[fingerprint_hash] = now

    return {"status": "success", "promo": selected_code}
