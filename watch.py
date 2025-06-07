import os
import time

while True:
    print("Launching josaa_bot...")
    exit_code = os.system("python bot.py")

    if exit_code != 0:
        print("Bot crashed or exited. Restarting in 5 seconds...")
        time.sleep(5)
    else:
        print("Bot exited normally.")
        break