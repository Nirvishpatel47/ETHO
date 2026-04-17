import winsound
import asyncio
from pathlib import Path
from desktop_notifier import DesktopNotifier, ReplyField, Button

notifier = DesktopNotifier(
    app_name="ETHO",
    app_icon=Path(r"your_logo_path")
)

def play_notification_sound():
    try:
        winsound.MessageBeep(winsound.MB_OK)
    except Exception:
        pass

def notify_user(message):
    """
    Send desktop notification safely from sync code
    """
    play_notification_sound()

    async def _send():
        await notifier.send(
            title="ETHO",
            message=str(message),
            timeout=5
        )

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(_send())
        else:
            loop.run_until_complete(_send())
    except RuntimeError:
        asyncio.run(_send())

async def command_toast():

    try:
        from Command_Executor import execute_command
        
        play_notification_sound()

        await notifier.send(
            title="Command",
            message="Type. Now!",
            reply_field=ReplyField(
                on_replied=lambda text: execute_command(text)
            )
        )

    except Exception as e:
        notify_user("Solve command toast.")

if __name__ == "__main__":
    notify_user("Hello")