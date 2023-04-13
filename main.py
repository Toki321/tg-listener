import os
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

client = TelegramClient('anon', api_id, api_hash)
client.start(phone_number)

async def get_last_10_messages_from_group(group_name):
    groups = await client.get_dialogs()
    target_group = None

    for group in groups:
        if group.title == group_name:
            target_group = group
            break

    if target_group is None:
        print(f'No group found with the name "{group_name}".')
        return

    messages = await client(GetHistoryRequest(
        peer=target_group.entity,
        limit=10,
        offset_id=0,
        offset_date=None,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))
    for message in messages.messages[::-1]:
        sender = await client.get_entity(message.sender_id)
        print(f"{sender.username or sender.first_name}: {message.message}")



client.loop.run_until_complete(get_last_10_messages_from_group('arcadia - Trading Pit TG Scrape'))

