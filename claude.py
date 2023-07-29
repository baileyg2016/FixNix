import os
from dotenv import load_dotenv
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import xml.etree.ElementTree as ET

load_dotenv()

PROMPT = f"""
  {HUMAN_PROMPT}
  <prompt>
  You are a an AI model tasked with finding bugs in a codebase. 
  You will be given the details of the bug in <bug></bug> tags.
  You will be given the codebase in <code></code> tags.
  Do your best to find the bug!
  If you don't know, say you cannot find the bug and then create
  steps to maybe find the bug in <step></step> tags.
  Don't output a step tag if you have a solution.
  If you find the bug, add a <solution></solution> tag with the
  solution code.
  Give your explanation in <explanation></explanation> tags.
  Don't output anything without tags.
  </prompt>

  <code>
  def add_numbers(a, b):
    result = a + c
    return result

  print(add_numbers(5, 3))
  </code>


  Okay go!
  {AI_PROMPT}
"""


anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
completion = anthropic.completions.create(
    model="claude-2",
    max_tokens_to_sample=10000, # will i need to change this?
    prompt=PROMPT,
)

claude_output = f'<root>{completion.completion}</root>'

root = ET.fromstring(claude_output)
bug = root.find('bug').text
solution = root.find('solution').text
explanation = root.find('explanation').text
steps = root.find('step').text

print(f"Bug: {bug}\nSolution: {solution}\nExplanation: {explanation}")

