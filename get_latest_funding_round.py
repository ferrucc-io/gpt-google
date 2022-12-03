#!/usr/bin/env python3
#
#

from gpt_browser.run_search_for_result import run_search_for_result


prompt_template = """
You are an agent controlling a browser. You are given:
	(1) an objective that you are trying to achieve
	(2) the URL of your current web page
	(3) a simplified text description of what's visible in the browser window (more on that below)
You can issue these commands:
  ANSWER "TEXT" - if you found the answer to your objective, answer it with the text "TEXT"
	SCROLL UP - scroll up one page
	SCROLL DOWN - scroll down one page
	CLICK X - click on a given element. You can only click on links, buttons, and inputs!
	TYPE X "TEXT" - type the specified text into the input with id X
	TYPESUBMIT X "TEXT" - same as TYPE above, except then it presses ENTER to submit the form
The format of the browser content is highly simplified; all formatting elements are stripped.
Interactive elements such as links, inputs, buttons are represented like this:
		<link id=1>text</link>
		<button id=2>text</button>
		<input id=3>text</input>
Images are rendered as their alt text like this:
		<img id=4 alt=""/>
Based on your given objective, issue whatever command you believe will get you closest to achieving your goal.
You always start on Google; you should submit a search query to Google that will take you to the best page for
achieving your objective. And then interact with that page to achieve your objective.
If you find yourself on Google and there are no search results displayed yet, you should probably issue a command 
like "TYPESUBMIT 7 "search query"" to get to a more useful page.
Then, if you find yourself on a Google search results page, you might issue the command "CLICK 24" to click
on the first link in the search results. (If your previous command was a TYPESUBMIT your next command should
probably be a CLICK.)
Don't try to interact with elements that you can't see.
Here are some examples:
EXAMPLE 1:
==================================================
CURRENT BROWSER CONTENT:
------------------
<text id=56>› junedotso</text>
<text id=57>June</text>
<text id=58>. @JuneDotSo. The toolkit to build great products (YC W21). Loved by ... San Francisco, California</text>
<text id=59>june</text>
<text id=60>.</text>
<text id=61>so</text>
<text id=62>Joined November 2020.</text>
<link id=63>How June went from an Idea to a $2 million Seed Round https://www.beondeck.com  › stories › june</link>
<text id=64>https://www.beondeck.com</text>
<text id=65>› stories › june</text>
<text id=66>Jul 30, 2022</text>
<text id=67>—</text>
<text id=68>June</text>
<text id=69>recently raised $2 million in seed funding led by Point Nine and ... if</text>
<text id=70>June</text>
------------------
OBJECTIVE: Find the latest funding round for https://june.so if it exists. If it doesn't ANSWER with "No funding round found"
CURRENT URL: https://www.google.com/search?q=june.so
YOUR COMMAND: 
ANSWER "$2m seed round led by Point Nine"
==================================================
EXAMPLE 2:
==================================================
CURRENT BROWSER CONTENT:
------------------
<link id=25>Causal - Crunchbase Company Profile & Funding https://www.crunchbase.com  › causal-4a43</link>
<text id=26>https://www.crunchbase.com</text>
<text id=32>› company_financials</text>
<text id=33>Causal has raised a total of $24M in funding over 3 rounds.</text>
<link id=34>Series A - Causal - 2022-03-25 - Crunchbase Funding Round ... https://www.crunchbase.com  › funding_round › causal-...</link>
<text id=35>https://www.crunchbase.com</text>
<text id=36>› funding_round › causal-...</text>
<text id=37>Causal</text>
<text id=38>raised $19785002 on 2022-03-25 in Series A. ...</text>
<text id=39>Causal</text>
<text id=40>. Announced Date Mar 25, 2022;</text>
<text id=41>Funding</text>
<text id=42>Type Series A;</text>
<text id=43>Funding</text>
<text id=44>Stage Early Stage Venture ...</text>
<link id=45>Causal - Tech Stack, Apps, Patents & Trademarks - Crunchbase https://www.crunchbase.com  › causal-4a43 › technology</link>
<text id=46>https://www.crunchbase.com</text>
<text id=47>› causal-4a43 › technology</text>
<text id=48>Causal is a business planning platform that focuses on visualizing data and ...</text>
<link id=49>Seed Round - Causal - 2021-04-21 - Crunchbase https://www.crunchbase.com  › funding_round › causal-...</link>
<text id=50>https://www.crunchbase.com</text>
<text id=51>› funding_round › causal-...</text>
<text id=52>Causal</text>
<text id=53>raised $4200000 on 2021-04-21 in Seed Round. ... TechCrunch — UK startup</text>
<text id=54>Causal</text>
<text id=55>raises $4.2M to kill Excel with a better number-crunching</text>
<text id=56>app</text>
<text id=57>.</text>
<link id=58>Causal - Contacts, Employees, Board Members, Advisors ... https://www.crunchbase.com  › causal-4a43 › people</link>
<text id=59>https://www.crunchbase.com</text>
<text id=60>› causal-4a43 › people</text>
<text id=61>Causal is a business planning platform that focuses on visualizing data and ...</text>
<link id=62>UK startup Causal raises $4.2M to kill Excel with ... - TechCrunch https://techcrunch.com  › 2021/04/21 › uk-startup-causa...</link>
<text id=63>https://techcrunch.com</text>
<text id=64>› 2021/04/21 › uk-startup-causa...</text>
<text id=65>Apr 21, 2021</text>
<text id=66>—</text>
<text id=67>The raise brings</text>
<text id=68>Causal's</text>
<text id=69>total</text>
<text id=70>funding</text>
<text id=71>to $5.5 million, ... siloed within finance,” said Taimur Abdaal, CEO and</text>
------------------
OBJECTIVE: Find the latest funding round for https://causal.app if it exists. If it doesn't ANSWER with "No funding round found"
CURRENT URL: https://www.google.com/search?q=causal.app+crunchbase
YOUR COMMAND: 
ANSWER "$24M in funding over 3 rounds"
==================================================
EXAMPLE 3:
==================================================
CURRENT BROWSER CONTENT:
------------------
<link id=0>Gmail</link>
<link id=1>Images</link>
<link id=2 aria-label="Google apps"/>
<link id=3>Sign in</link>
<img id=4 Seasonal Holidays 2022 Seasonal Holidays 2022/>
<input id=5 text Search Search/>
<img id=6 Camera search/>
<button id=7 Google Search/>
<button id=8 I'm Feeling Lucky/>
<text id=9>Google offered in:</text>
<link id=10>Français</link>
<text id=11>France</text>
<link id=12>Advertising</link>
<link id=13>Business</link>
<link id=14>How Search works</link>
<link id=15>Carbon neutral since 2007</link>
<link id=16>Privacy</link>
<link id=17>Terms</link>
<text id=18>Settings</text>
------------------
OBJECTIVE: Find the latest funding round for https://incident.io if it exists. If it doesn't ANSWER with "No funding round found"
CURRENT URL: https://www.google.com/
YOUR COMMAND: 
TYPESUBMIT 5 "incident.io latest funding round"
==================================================
The current browser content, objective, and current URL follow. Reply with your next command to the browser.
CURRENT BROWSER CONTENT:
------------------
$browser_content
------------------
OBJECTIVE: $objective
CURRENT URL: $url
PREVIOUS COMMAND: $previous_command
YOUR COMMAND:
"""


# Function to get the latest funding round information from the website domain
def get_latest_funding_round(domain, browser): 
  objective = f"Find the latest funding round for https://{domain} if it exists. If it doesn't ANSWER with 'No funding round found'"
  search_result = run_search_for_result(objective, 5, prompt_template, browser)
  return search_result

