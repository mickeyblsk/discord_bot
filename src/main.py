import os
import sys
import logging
from typing import Final

import discord

MESSAGE_CONTENT: Final[str] = "大家晚安，這是本週三的自動提醒！"
REACTION_EMOJI: Final[str] = "✅"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class ReminderBot(discord.Client):
    async def on_ready(self) -> None:
        logger.info("Logged in as %s (ID: %s)", self.user, self.user.id)

        channel_id = os.environ.get("DISCORD_CHANNEL_ID")
        if not channel_id:
            logger.error("環境變數 DISCORD_CHANNEL_ID 未設定")
            await self.close()
            return

        try:
            channel_id_int = int(channel_id)
        except ValueError:
            logger.error("DISCORD_CHANNEL_ID 不是有效的整數: %s", channel_id)
            await self.close()
            return

        channel = self.get_channel(channel_id_int)
        if channel is None:
            logger.error("找不到頻道 (ID: %s)，請確認 Bot 已被邀請至該頻道", channel_id)
            await self.close()
            return

        try:
            message = await channel.send(MESSAGE_CONTENT)
            logger.info("訊息已成功發送至頻道 #%s (Message ID: %s)", channel.name, message.id)
        except discord.Forbidden:
            logger.error("Bot 沒有在頻道 %s 發送訊息的權限", channel_id)
            await self.close()
            return
        except Exception as e:
            logger.error("發送訊息時發生未預期錯誤: %s", e)
            await self.close()
            return

        try:
            await message.add_reaction(REACTION_EMOJI)
            logger.info("已成功在訊息上新增 Reaction: %s", REACTION_EMOJI)
        except discord.Forbidden:
            logger.warning("Bot 沒有新增 Reaction 的權限，已跳過此步驟")
        except Exception as e:
            logger.warning("新增 Reaction 時發生錯誤: %s，已跳過此步驟", e)

        await self.close()


def main() -> None:
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        logger.error("環境變數 DISCORD_TOKEN 未設定")
        sys.exit(1)

    intents = discord.Intents.default()
    intents.message_content = True

    client = ReminderBot(intents=intents)
    try:
        client.run(token)
    except discord.LoginFailure:
        logger.error("Discord Token 無效，請確認 Token 是否正確")
        sys.exit(1)
    except Exception as e:
        logger.error("執行 Bot 時發生未預期錯誤: %s", e)
        sys.exit(1)

    logger.info("Bot 已正常結束執行")


if __name__ == "__main__":
    main()
