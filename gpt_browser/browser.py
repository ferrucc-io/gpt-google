#!/usr/bin/env python3
#

from playwright.sync_api import sync_playwright

class Browser:
  def __init__(self):
    	self.browser = (
			sync_playwright()
			.start()
			.chromium.launch(
				headless=False,
			)
		)