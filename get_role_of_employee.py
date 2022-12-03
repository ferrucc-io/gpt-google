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
<text id=0>Accessibility links</text>
<link id=1>Skip to main content</link>
<link id=2>Accessibility help</link>
<link id=3>Accessibility feedback</link>
<link id=4 alt="Seasonal Holidays 2022" title="Seasonal Holidays 2022"/>
<input id=5 text Search>enzo@june.so</input>
<button id=6 Clear/>
<button id=7 Search by voice/>
<button id=8 Search by image/>
<img id=9 Camera search/>
<button id=10 aria-label="Search"/>
<text id=11>Settings</text>
<link id=12 aria-label="Google apps"/>
<link id=13>Sign in</link>
<text id=14>Search modes</text>
<text id=15>All</text>
<text id=24>Search Results</text>
<link id=25>Enzo Avigo - Co-Founder & CEO - Junedotso - LinkedIn https://fr.linkedin.com  › enzoa</link>
<text id=26>https://fr.linkedin.com</text>
<text id=27>› enzoa</text>
<text id=28>France</text>
<text id=29>·</text>
<text id=30>Co-Founder & CEO</text>
<text id=31>·</text>
<text id=32>Junedotso</text>
<text id=33>Enzo</text>
<text id=34>Avigo · CEO @</text>
------------------
OBJECTIVE: Find the role of the employee with email address enzo@june.so
CURRENT URL: https://www.google.com/search?q=enzo%40june.so
YOUR COMMAND: 
ANSWER "Founder & CEO"
==================================================
EXAMPLE 2:
==================================================
CURRENT BROWSER CONTENT:
------------------
<link id=1>Skip to main content</link>
<link id=2>Accessibility help</link>
<link id=3>Accessibility feedback</link>
<link id=4 alt="Seasonal Holidays 2022" title="Seasonal Holidays 2022"/>
<input id=5 text Search>ferruccio@june.so role</input>
<link id=25>Ferruccio Balestreri - CTO & Co-Founder - Junedotso | LinkedIn https://fr.linkedin.com  › ferruccio-bal...</link>
<text id=26>https://fr.linkedin.com</text>
<text id=27>› ferruccio-bal...</text>
<text id=28>·</text>
<link id=29>Translate this page</link>
<text id=30>Paris, Île-de-France, France</text>
<text id=31>·</text>
<text id=32>CTO & Co-Founder</text>
<text id=33>·</text>
<text id=34>Junedotso</text>
<text id=35>Ferruccio Balestreri · CTO @ June.so -</text>
<text id=36>Next-gen product analytics for B2B SaaS</text>
<text id=37>· Signaler · Signaler · Activité · Expérience · Formation · Prix et distinctions · Plus d ...</text>
<link id=38>How June went from an Idea to a $2 million Seed Round https://www.beondeck.com  › stories › june</link>
<text id=39>https://www.beondeck.com</text>
<text id=40>› stories › june</text>
<text id=41>Jul 30, 2022</text>
<text id=42>—</text>
<text id=43>June recently</text>
<text id=44>raised $2 million in seed funding led by Point Nine</text>
<text id=45>and with participation from Y Combinator, Speedinvest, Kima Ventures, ...</text>
<link id=46>Ferruccio Balestreri - Co-Founder at June | The Org https://theorg.com  › org › june-so › org-chart › ferrucc...</link>
<text id=47>https://theorg.com</text>
------------------
OBJECTIVE: Find the role of the employee with email address ferruccio@june.so
CURRENT URL: https://www.google.com/search?q=ferruccio%40june.so+role
YOUR COMMAND: 
ANSWER "CTO & Co-Founder"
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
OBJECTIVE: Find the role of the employee with email address vinayak@june.so
CURRENT URL: https://www.google.com/
YOUR COMMAND: 
TYPESUBMIT 5 "Vinayak june.so linkedin"
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


# Function to get the role of the employee from the email address
def get_role_of_employee(email, browser):  
  objective = "Find the role of the employee with the email address " + email
  search_result = run_search_for_result(objective, 5, prompt_template, browser)
  return search_result

