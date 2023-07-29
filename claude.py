import os
from dotenv import load_dotenv
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import xml.etree.ElementTree as ET

load_dotenv()

anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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


def create_bug_prompt(code, context):
  return f"""
      {HUMAN_PROMPT}
      <prompt>
      You are a an AI model tasked with finding bugs in a codebase. 
      You will be given the details of the bug in <bug></bug> tags.
      You will be given the codebase in <code></code> tags.
      The context about what bug you are looking for will be in <context></context> tags.
      Do your best to find the bug!
      If you don't know, say you cannot find the bug and then create
      steps to maybe find the bug in <step></step> tags.
      Don't output a step tag if you have a solution.
      If you find the bug, add a <solution></solution> tag with the
      solution code.
      Give your explanation in <explanation></explanation> tags.
      Don't output anything without tags.
      </prompt>

      <context>
      {context}
      </context>
      
      <code>
      {code}
      </code>


      Okay go!
      {AI_PROMPT}
    """

def create_files_prompt():
  return f"""
    {HUMAN_PROMPT}
    <prompt>
    You are a an AI model tasked with determining which files,
    based on their name, are most likely to contain bugs.
    I will give you a list of files in <files></files> tags.
    You will output a list of files in <files></files> tags.
  """

def string_to_xml(string):
  return ET.fromstring(f'<root>{string}</root>')


def find_bug_in_code(code, bug_context):
  completion = anthropic.completions.create(
      model="claude-2",
      max_tokens_to_sample=100000, # will i need to change this?
      prompt=create_bug_prompt(code, bug_context),
  )
  return completion.completion

claude_output = find_bug_in_code("def add_numbers(a, b):\n  result = a + c\n  return result\n\nprint(add_numbers(5, 3))", "The bug is in the add_numbers function")
print(claude_output)
root = string_to_xml(claude_output)
bug = root.find('bug') != None if root.find('bug').text else None
solution = root.find('solution').text
explanation = root.find('explanation').text
steps = root.find('step') != None if root.find('step').text else None

print(f"Bug: {bug}\nSolution: {solution}\nExplanation: {explanation}")

