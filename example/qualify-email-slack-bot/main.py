#!/usr/bin/env python3
#

#  Same script as main.py but better organized and running for a specific use case
#  This script is used to qualify new sign ups coming to June.so

# It takes an email address as input and returns a JSON object with the following fields:
# 1. email: the email address
# 2. is_valid: True if the email address is valid, False otherwise
# 3. company_domain: the company name associated with the email address
# 4. role_of_employee: the role of the employee associated with the email address
# 5. funding_stage: the funding stage of the company associated with the email address


# Importing libraries

import time
from sys import argv
import os
from email_validator import validate_email, EmailNotValidError
from get_role_of_employee import get_role_of_employee
from get_latest_funding_round import get_latest_funding_round
from gpt_browser.browser import Browser
from dotenv import load_dotenv
import requests

load_dotenv()

email = argv[1]


try:
  validation = validate_email(email, check_deliverability=True)
  email = validation.email
  is_valid = True
except EmailNotValidError as e:
  print(e)
  exit(0)



def get_company_domain(email):
  company_domain = email.split("@")[1]
  return company_domain

company_domain = get_company_domain(email)


browser = Browser().browser

role_of_employee = get_role_of_employee(email, browser)
latest_funding_round = get_latest_funding_round(company_domain, browser)



slack_channel_hook_url = os.getenv("SLACK_CHANNEL_HOOK")

slack_message_blocks = [
  {
    "type": "header",
    "text": {
      "type": "plain_text",
      "text": "🆕 New qualified sign up",
      "emoji": True
    }
  },
  {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "🕵️ *<mailto:" + email + "|" + email + ">*"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Valid email:*\n "+ "✅" if str(is_valid) else "❌"
        },
        {
          "type": "mrkdwn",
          "text": "*Company website:*\n<https://"+ company_domain + "|"+ company_domain + ">"
        },
        {
          "type": "mrkdwn",
          "text": "*Role of employee:*\n "+ role_of_employee
        },
        {
          "type": "mrkdwn",
          "text": "*Latest funding round:*\n "+ latest_funding_round
        }
      ]
  },
  {
			"type": "divider"
  }
]


requests.post(slack_channel_hook_url, json={'text': "Email: " + email, 'blocks': slack_message_blocks})