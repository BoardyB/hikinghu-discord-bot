import discord
import os
from datetime import datetime, timedelta, timezone
import asyncio

# === CONFIG ===
BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])
INACTIVE_DAYS = int(os.environ.get("INACTIVE_DAYS", "14"))  # Default to 14 days (2 weeks)
DRY_RUN = os.environ.get("DRY_RUN", "true").lower() in ("true", "1")  # does not actually delete threads

async def cleanup_inactive_threads():
    """
    Clean up threads in the specified channel that:
    1. Are older than INACTIVE_DAYS
    2. Have no messages other than the initial post
    """
    intents = discord.Intents.default()
    intents.message_content = True  # Required to read message history
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}")

        if DRY_RUN:
            print("DRY RUN MODE ENABLED - No threads will be deleted")

        channel = client.get_channel(CHANNEL_ID)
        if not channel:
            print(f"Channel {CHANNEL_ID} not found")
            await client.close()
            return

        print(f"Found channel: {channel.name}")

        cutoff_date = datetime.now(timezone.utc) - timedelta(days=INACTIVE_DAYS)
        print(f"Looking for threads older than {cutoff_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")

        deleted_count = 0
        checked_count = 0

        # Check active threads
        print("\n=== Checking active threads ===")
        for thread in channel.threads:
            checked_count += 1
            deleted = await check_and_delete_thread(thread, cutoff_date)
            if deleted:
                deleted_count += 1

        # Check archived threads
        print("\n=== Checking archived threads ===")
        async for thread in channel.archived_threads(limit=None):
            checked_count += 1
            if thread.archived and thread.created_at < cutoff_date:
                deleted = await check_and_delete_thread(thread, cutoff_date)
                if deleted:
                    deleted_count += 1

        print(f"\n=== Summary ===")
        print(f"Threads checked: {checked_count}")
        print(f"Threads deleted: {deleted_count}")

        await client.close()

    async def check_and_delete_thread(thread, cutoff_date):
        """Check if a thread should be deleted and delete it if necessary

        Returns:
            bool: True if the thread was deleted, False otherwise
        """
        if thread.created_at >= cutoff_date:
            print(f"Skipping '{thread.name}' (too recent: {thread.created_at.strftime('%Y-%m-%d')})")
            return False

        try:
            # Count messages in the thread
            if thread.message_count <= 1:
                # Only the initial message exists, delete the thread
                if DRY_RUN:
                    print(f"[DRY RUN] Would delete inactive thread: '{thread.name}' (created {thread.created_at.strftime('%Y-%m-%d')}, {thread.message_count} message(s))")
                    return True
                else:
                    print(f"Deleting inactive thread: '{thread.name}' (created {thread.created_at.strftime('%Y-%m-%d')}, {thread.message_count} message(s))")
                    await thread.delete()
                    return True
            else:
                print(f"Keeping active thread: '{thread.name}' ({thread.message_count} messages)")
                return False

        except discord.Forbidden:
            print(f"Permission denied to access thread: '{thread.name}'")
            return False
        except discord.NotFound:
            print(f"Thread not found (may have been deleted): '{thread.name}'")
            return False
        except Exception as ex:
            print(f"Error processing thread '{thread.name}': {ex}")
            return False

    try:
        await client.start(BOT_TOKEN)
    except Exception as e:
        print(f"Error starting bot: {e}")
        raise


if __name__ == "__main__":
    print("Starting thread cleanup job...")
    asyncio.run(cleanup_inactive_threads())
