prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:
calculate:
e.g. A functional website with multiple pages
Parses through all the pages before summarizing using the prompt given by the user.

uta.edu:
e.g. uta.edu: Application information
Returns a summary of application information in their website

sf.gov:
e.g. sf.gov: FAQs (Frequently Asked Questions)
Search sf.gov for that term

Example session:
Question: What is the capital of France?
Thought: I should look up France on Wikipedia
Action: wikipedia: France
PAUSE

You will be called again with this:
Observation: France is a country. The capital is Paris.

You then output:
Answer: The capital of France is Paris
""".strip()