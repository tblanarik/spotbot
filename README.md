# spotbot

## Description

Spotbot is a simple Azure Function App to convert [HamAlert](https://hamalert.org/) alerts from [POTA](https://pota.app) or [SOTA](https://www.sota.org.uk/) in to a message format that can be forwarded on to a Discord channel webhook.

## Requirements

- Python 3.x
- Azure Functions
- requests

## Config

The Azure Function App expects one environment variable: `TARGET_URL`, which should be the webhook URL from the target Discord channel.
