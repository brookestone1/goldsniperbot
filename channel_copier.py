from telethon import TelegramClient, events
import asyncio
import re

# ==== CHANGE THESE TWO LINES ====
api_id = 30386961                   
api_hash = 8d24b078c7f8167108e3ee01b0a48195      
# ================================

SOURCE_CHANNELS = [
    'goldsignalsvip',
    'cryptosignalspro',
    'fxpremiere',
    'xaupips',
    'btcsignalfree',
    'goldscalpingpro',
    'cryptovipclub',
    'signalstartgold',
]

DESTINATION_CHANNEL = '@GoldSniperBTC'

def format_signal(text):
    if not text:
        return text
    text = text.strip()
    text = re.sub(r'^Forwarded from.*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)

    if any(x in text.lower() for x in ['xau', 'gold', 'xauusd']):
        header = "GOLD SNIPER SIGNAL (XAUUSD) ⚡\n"
        tags = "\n#XAU #Gold #SniperSignal"
    elif any(x in text.lower() for x in ['btc', 'bitcoin', 'btcusd']):
        header = "BTC SNIPER SIGNAL ₿\n"
        tags = "\n#BTC #Bitcoin #SniperSignal"
    else:
        header = "SNIPER SIGNAL\n"
        tags = "\n#Signal"
    
    text = header + text + tags + f"\n\n@GoldSniperBTC"
    return text

client = TelegramClient('sniper_session', api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    try:
        if event.message.edit_date or not event.message.message:
            return
        new_text = format_signal(event.message.message)
        if event.message.media:
            await client.send_file(DESTINATION_CHANNEL, file=event.message.media, caption=new_text, silent=True)
        else:
            await client.send_message(DESTINATION_CHANNEL, new_text, silent=True)
        print(f"Sniped: {event.message.id}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    print("GoldSniperBTC bot STARTED")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
