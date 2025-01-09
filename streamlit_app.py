import streamlit as st
import discord
import asyncio
import threading

# Replace with your bot's token
BOT_TOKEN = "MTMyNjc5ODU4NjY4MzU5Mjc1NQ.Gg1HZN.UCI0RAi-15dLaf_y99d1T0hgxG1y6bZIsB_OWw"

# Replace with your channel ID
CHANNEL_ID = 1269107769462755349

# Global event to track when the bot is ready
bot_ready_event = threading.Event()

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        super().__init__(intents=intents, *args, **kwargs)
        self.channel_id = CHANNEL_ID
        self.channel = None  # To store the channel once fetched

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        try:
            self.channel = await self.fetch_channel(self.channel_id)
            print(f"Connected to channel: {self.channel.name}")
            bot_ready_event.set()
        except discord.NotFound:
            print("Channel not found!")
        except discord.Forbidden:
            print("Bot doesn't have permission to access the channel!")
        except discord.HTTPException as e:
            print(f"HTTP error occurred: {e}")

    def send_message_sync(self, message):
        """Send a message synchronously (blocking)"""
        if self.channel:
            # Block the call and send the message
            self.loop.create_task(self.channel.send(message))
        else:
            print("Channel not found!")

# Create and run the bot in a separate thread
def run_bot():
    global client
    client = MyClient()
    client.run(BOT_TOKEN)  # This runs the bot and manages its event loop

def main():
        # Start the bot in a separate thread to avoid blocking Streamlit
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Streamlit UI
    st.title('Request title')

    # Get message input from the user
    message = st.text_input('Please input: <title> <hk/lk> <x> <y>')

    if st.button('Send Message') and message:
        # Wait for the bot to be ready before sending the message
        if bot_ready_event.wait(timeout=30):  # Wait up to 10 seconds for the bot to be ready
            # Now that the bot is ready, send the message synchronously
            # client = MyClient()  # This should already be running in the background
            client.send_message_sync(message)
            st.success("Message sent successfully!")
        else:
            st.warning("Bot is not ready yet. Try again after a moment.")

    elif message == "":
        st.warning("Message cannot be empty.")

if __name__ =="__main__":
    main()