from flask import Flask, request
import requests

app = Flask(__name__)

# Remplace par ton vrai token ici :
PAGE_ACCESS_TOKEN = "EAALUhjIDi8sBPrwXpfWlNNpOpzm4JEZAZBTL4ZCq7BPzi9yG3H4hgwDKIZBw68j0zafu7dEvRp02UgZCMzeTbtoIbIA5hbCBKPMD5o4z1UpG3s9bV33ZCugGZCgCyPbD27jD4XOtfHfRxDOtpqbwXIYEwavmV7YYbGIAFmM6qvJQhEfIGKoU5RigfaEer1Qz8xyeP3M2TXBugZDZD"

VERIFY_TOKEN = "ny_secret"  # mot secret pour vérifier ton webhook

@app.route('/')
def home():
    return "Bot Messenger de LOSER est en ligne ✅"

@app.route('/webhook', methods=['GET'])
def verify():
    # Facebook envoie ce GET pour vérifier ton webhook
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge
    return "Erreur de vérification", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)

    if "entry" in data:
        for entry in data["entry"]:
            for messaging_event in entry.get("messaging", []):
                if "message" in messaging_event:
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"].get("text", "")
                    envoyer_message(sender_id, f"Tu as dit : {message_text}")

    return "ok", 200

def envoyer_message(user_id, text):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    data = {
        "recipient": {"id": user_id},
        "message": {"text": text}
    }
    requests.post(url, json=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
