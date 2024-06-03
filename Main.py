import re
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.')
bot.remove_command("help")

sofi_msg = None
nori_msg = None

@bot.event
async def on_ready():
    print("----------- AutoClaimer Bot -----------")
    print("----- User : {0.user}".format(bot))
    print("--------------------------------------")

@bot.event
async def on_message(message):
    global sofi_msg, nori_msg

    if message.author.id == bot.user.id:
        return

    if message.author.id == 853629533855809596:
        sofi_msg = message

    elif message.author.id == 742070928111960155:
        nori_msg = message

    else:
        await bot.process_commands(message)
        return

    if nori_msg and ":heart:" in nori_msg.content.lower():

        if sofi_msg:

            data = []

            msg = sofi_msg.content.split("\n")

            for line in msg:
                parts = line.split(" • ")

                serial_number_match = re.search(r"(\d+)\]", parts[0])
                if serial_number_match:
                    serial_number = int(serial_number_match.group(1))

                heart_count_match = re.search(r"(\d+)\s*•", parts[1])
                if heart_count_match:
                    heart_count = int(heart_count_match.group(1))

                g_number_match = re.search(r"ɢ(\d+)\s*", parts[2])
                if g_number_match:
                    g_number = int(g_number_match.group(1))

                data.append({"sn": serial_number, "hc": heart_count, "g": g_number})

            final = sorted(data, key=lambda x: (x["hc"], x["g"]))

            number_to_select = final[0]["sn"]

            if 0 <= number_to_select - 1 < len(sofi_msg.components[0].children):
                await sofi_msg.components[0].children[number_to_select - 1].click()
            else:
                print("Oopsie! Something Went Off!")

    await bot.process_commands(message)


bot.run("")
