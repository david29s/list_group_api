import pandas as pd

from telethon import TelegramClient

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import InputChannel, InputPeerEmpty, ChannelParticipantsSearch


api_id = 161374
api_hash = '8b2159e9334093765c6909e6ae0ecada'

client = TelegramClient('myGroups', api_id, api_hash, update_workers=1, spawn_read_thread=False)
client.start()

get_dialogs = GetDialogsRequest(
    offset_date=None,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=100,
)

def count_members(id, access_hash):
    offset = 0
    limit = 10000
    all_participants = []

    while True:
        participants = client(GetParticipantsRequest(
            InputChannel(id, access_hash), ChannelParticipantsSearch(''), offset, limit,
            hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)


    return len(all_participants)


dialogs = client(get_dialogs)

df = pd.DataFrame(columns=['Name', 'Type', 'Members'])

for chat in dialogs.chats:
    try:
        members = count_members(chat.id, chat.access_hash)
        df.loc[len(df)] = [chat.title, str(chat).split('(')[0], members]
    except Exception:
        df.loc[len(df)] = [chat.title, str(chat).split('(')[0], chat.participants_count]


print(df)
df.to_csv('myGroups.csv', sep=',')
