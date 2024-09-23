# spotbot

## Description

Spotbot is an Azure Function App to convert [HamAlert](https://hamalert.org/) alerts from [POTA](https://pota.app) or [SOTA](https://www.sota.org.uk/) in to a message format that can be forwarded on to a Discord channel webhook.

| HamAlert Configuration |
| -- |
| ![image](https://github.com/user-attachments/assets/c25f8966-e107-4e67-838c-11ada7c5309d) |

| Discord Message |
| -- |
| ![image](https://github.com/user-attachments/assets/f664d60f-2042-4b2d-9c88-4ce4051f17c7) |


The function uses a Table in an Azure Storage Account to store the `messageId` of the last message posted for each callsign. If that message was posted recently (as defined by `LOOKBACK_SECONDS`), it will _update_ the message instead of posting a new one to reduce the chatter of the bot.

You can find a live, working version of this bot in the [Cascadia Radio](https://www.cascadiaradio.org/) Discord server, in the `#spots` channel. Join us!

## Config

The Azure Function App expects three environment variables: 
- `TARGET_URL` - the webhook URL from the target Discord channel.
- `LOOKBACK_SECONDS` - the number of seconds to look backwards for previous messages to update instead of posting a new one
- `TABLE_NAME` - the name of the table in the Azure Storage Account where the last messageIds will be stored for each callsign

## Deploy Notes

- Some basic tests run in `tests.py` on the creation of a new PR
- To deploy, manually run `main_hamalertspotbot.yml`
    - This will deploy to the staging slot for testing. 
    - The staging `TARGET_URL` points to my private Discord server
    - `LOOKBACK_SECONDS` is set to only 300 (instead of 7200) for easier testing.