#! python

import discord
import auth

client = discord.Client()

def activate():
    client.run(auth.discord)

def main():
    activate()
