from Constants import MODES, current_mode, water_lines, break_lines, restart_lines, giyu_welcome_messages
from Launcher import command_input
from Notifier import notify_user, command_toast
import keyboard
import random
import asyncio
import time

REMINDER_INTERVAL = 1800

async def work_break_loop():
    global current_mode
    while True:
        work_time = MODES[current_mode]["work"]
        break_time = MODES[current_mode]["break"]

        await asyncio.sleep(work_time)
        notify_user(random.choice(break_lines))

        await asyncio.sleep(break_time)
        notify_user(random.choice(restart_lines))

def switch_mode():
    global current_mode
    current_mode = "alternate" if current_mode == "default" else "default"
    notify_user(f"Switched to {current_mode}")

async def hydration_reminder():

    try:
        notify_user(random.choice(water_lines))

    except Exception as e:
        notify_user("Solve your notification first.")
        return 
    
async def reminder_loop():

    while True:

        await asyncio.sleep(REMINDER_INTERVAL)
        
        await hydration_reminder()

def start_hotkey_listener(loop):

    def trigger():
        loop.call_soon_threadsafe(
            lambda: asyncio.create_task(command_toast())
        )

    keyboard.add_hotkey("ctrl+shift+space", trigger)

async def run_ETHO():

    notify_user(random.choice(giyu_welcome_messages))

    loop = asyncio.get_running_loop()

    start_hotkey_listener(loop)

    tasks = [

        asyncio.create_task(reminder_loop()),
        asyncio.create_task(work_break_loop())

    ]

    await asyncio.gather(*tasks)

if __name__ == "__main__":

    try:
        time.sleep(2)
        
        asyncio.run(run_ETHO())

    except KeyboardInterrupt:
        notify_user("I have work now.")