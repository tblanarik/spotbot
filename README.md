# spotbot

## Description

Spotbot is an application to convert [HamAlert](https://hamalert.org/) alerts from [POTA](https://pota.app) or [SOTA](https://www.sota.org.uk/) in to a message format that can be forwarded on to a Discord channel webhook.

| HamAlert Configuration |
| -- |
| ![image](https://github.com/user-attachments/assets/c25f8966-e107-4e67-838c-11ada7c5309d) |

| Discord Message |
| -- |
| ![image](https://github.com/user-attachments/assets/f664d60f-2042-4b2d-9c88-4ce4051f17c7) |


Spotbot stores the `messageId` of the last message posted for each callsign. If that message was posted recently (as defined by `LOOKBACK_SECONDS`), it will _update_ the message instead of posting a new one to reduce the chatter of the bot.

You can find a live, working version of this bot in the [Cascadia Radio](https://www.cascadiaradio.org/) Discord server, in the `#spots` channel. Join us!

## Config

The app expects four environment variables: 
- `TARGET_URL` - the webhook URL from the target Discord channel.
- `LOOKBACK_SECONDS` - the number of seconds to look backwards for previous messages to update instead of posting a new one
- `SECRET_ENDPOINT` - the name of the endpoint, kept secret to prevent abuse / unwanted messages
- `MYSQL_HOST`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`

## Deploy Notes

- Some basic tests run in `tests.py` on the creation of a new PR
- To deploy, login to PythonAnywhere and pull the latst from main