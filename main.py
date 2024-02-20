import discord
import os
import requests
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ping'):
        await message.channel.send('Pong!')

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN');

@client.event
async def on_github_event(payload):
    if payload["action"] == "opened" and payload["pull_request"]["state"] == "open":
        repo_name = payload["repository"]["name"]
        await send_pr_notification(repo_name)

async def send_pr_notification(repo_name):
    webhook_url = os.getenv("WEBHOOK_DISCORD");

    message = f"Se ha creado una nueva Pull Request en el repositorio {repo_name}"
    
    payload = {
        "content": message
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(webhook_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Notificación enviada con éxito.")
    else:
        print(f"Error al enviar la notificación: {response.status_code} - {response.text}")

TOKEN = os.getenv('DISCORD_BOT_TOKEN');
client.run(TOKEN)
