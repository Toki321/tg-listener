from collections import Counter
import os
import re
import time
from telethon import TelegramClient
import logging
from telethon.tl.functions.messages import GetHistoryRequest

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

from dotenv import load_dotenv

load_dotenv()

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
phone_number = os.environ.get('PHONE_NUMBER')
group_name = os.environ.get('GROUP_NAME')

client = TelegramClient('anon', api_id, api_hash)
client.start(phone_number)

async def get_tickers_from_last_30_minutes(group_name):
    groups = await client.get_dialogs()
    target_group = None

    for group in groups:
        if group.title == group_name:
            target_group = group
            break

    if target_group is None:
        print(f'No group found with the name "{group_name}".')
        return

    now = time.time()
    half_an_hour_ago = now - 30 * 60
    messages = await client(GetHistoryRequest(
        peer=target_group.entity,
        limit=1000,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    ticker_pattern = re.compile(r'/i\s+([a-zA-Z]+)')
    tickers = []

    for message in messages.messages:
        if message.date.timestamp() > half_an_hour_ago:
            matches = re.findall(ticker_pattern, message.message)
            tickers.extend(matches)

    ticker_counts = Counter(tickers)
    for ticker, count in ticker_counts.items():
        print(f'{ticker}: {count} times')


client.loop.run_until_complete(get_tickers_from_last_30_minutes(group_name))
