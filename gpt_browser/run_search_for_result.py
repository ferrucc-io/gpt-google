#!/usr/bin/env python3
#

from gpt_browser.crawler import Crawler
from gpt_browser.prompter import generate_gpt_command
import time
from sys import exit


def run_search_for_result(objective, max_depth_of_search, prompt_template, browser):
  _crawler = Crawler(browser=browser)
  depth_of_search = 0
  gpt_cmd = ""
  prev_cmd = ""
  _crawler.go_to_page("google.com")
  time.sleep(1)
  content = "\n".join(_crawler.crawl())
  search_result = False

  # Accept Google cookies policy
  _crawler.click(42)

  def run_cmd(cmd):
    cmd = cmd.split("\n")[0]

    if cmd.startswith("SCROLL UP"):
      _crawler.scroll("up")
    elif cmd.startswith("SCROLL DOWN"):
      _crawler.scroll("down")
    elif cmd.startswith("CLICK"):
      commasplit = cmd.split(",")
      id = commasplit[0].split(" ")[1]
      _crawler.click(id)
    elif cmd.startswith("ANSWER"):
      spacesplit = cmd.split(" ")
      id = spacesplit[1]
      search_result = spacesplit[1:]
      search_result = " ".join(search_result)
      search_result = search_result[1:-1]
      return search_result
    elif cmd.startswith("TYPE"):
      spacesplit = cmd.split(" ")
      id = spacesplit[1]
      text = spacesplit[2:]
      text = " ".join(text)
      # Strip leading and trailing double quotes
      text = text[1:-1]

      if cmd.startswith("TYPESUBMIT"):
        text += '\n'
      _crawler.type(id, text)

    time.sleep(2)
    return False
  
  try:
    while not search_result:
      depth_of_search += 1
      if depth_of_search > max_depth_of_search:
        print("Max depth of search reached")
        exit(1)
      browser_content = "\n".join(_crawler.crawl())
      prev_cmd = gpt_cmd
      gpt_cmd = generate_gpt_command(objective, _crawler.page.url, prev_cmd, browser_content, prompt_template)
      gpt_cmd = gpt_cmd.strip()

      
      print("URL: " + _crawler.page.url)
      print("Objective: " + objective)
      print("----------------\n" + browser_content + "\n----------------\n")
      
      if len(gpt_cmd) > 0:
        print("Suggested command: " + gpt_cmd)      
      
      search_result = run_cmd(gpt_cmd)

  except KeyboardInterrupt:
    print("\n[!] Ctrl+C detected, exiting gracefully.")
    return

  return search_result


  


