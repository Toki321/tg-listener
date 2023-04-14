import requests

class Tg_Operator:

    def __init__(self, tg_chat_id, tg_bot_token) -> None:
        self.TELEGRAM_CHAT_ID = tg_chat_id
        self.TELEGRAM_BOT_TOKEN = tg_bot_token

    def send_message(self, message_to_send):
        call = f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={self.TELEGRAM_CHAT_ID}&text={message_to_send}"
        requests.get(call).json()
        print(f"sending update to tg with the message: {message_to_send}")