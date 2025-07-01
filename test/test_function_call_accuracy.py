import re
import pytest

ollama = pytest.importorskip("ollama")

system_instructions = """
    Your name is ADA (Advanced Design Assistant) you are a helpful AI assistant. You are an expert in All STEM Fields providing concise and accurate information. When asked to perform a task, respond with the code to perform that task wrapped in ```tool_code```.  If the task does not require a function call, provide a direct answer without using ```tool_code```.  Always respond in a helpful and informative manner.

    You speak with a british accent and address people as Sir.
"""

instruction_prompt_with_function_calling = '''At each turn, if you decide to invoke any of the function(s), it should be wrapped with ```tool_code```. If you decide to call a function the response should only have the function wrapped in tool code nothing more. The python methods described below are imported and available, you can only use defined methods also only call methods when you are sure they need to be called. The generated code should be readable and efficient. The response to a method will be wrapped in ```tool_output``` use it generate a helpful, friendly response. For example if the tool output says ```tool_output camera on```. You should say something like "The Camera is on".

For regular prompts do not call any functions or wrap the response in ```tool_code```.

The following Python methods are available:

```python
def camera.open() -> None:
    """Open the camera"""

def system.info() -> None:
    """ Gathers and prints system information including CPU, RAM, and GPU details. """

def timer.set(time_str):
    """
    Counts down from a specified time in HH:MM:SS format.

    Args:
        time_str (str): The time to count down from in HH:MM:SS format.
    """
def project.create_folder(folder_name):
    """
    Creates a project folder and a text file to store chat history.

    Args:
        folder_name (str): The name of the project folder to create.
    """

```

User: {user_message}
'''

def extract_tool_call(text: str, function_name: str | None):
    pattern = r"```tool_code\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        code = match.group(1).strip()
        if function_name is None:
            return False
        return function_name in code
    return None

prompts_and_expectations = [
    ("Hello, how are you?", False, None),
    ("set 10 second timer", True, "timer.set"),
    ("Difference between DC and AC", False, None),
    ("Show me System Info", True, "system.info"),
    ("Briefly explain gravity", False, None),
    ("can you open the camera", True, "camera.open"),
    ("Give me a short explanation of the internet", False, None),
    ("set me a timer for 1 minute", True, "timer.set"),
    ("What is the chemical symbol for water?", False, None),
    ("open the camera", True, "camera.open"),
    ("What is a synonym for happy?", False, None),
    ("set me 33 second timer", True, "timer.set"),
    ("What is the largest planet in our solar system?", False, None),
    ("open camera", True, "camera.open"),
    ("How many continents are there?", False, None),
    ("Start a 10 hour timer", True, "timer.set"),
    ("What is the opposite of up?", False, None),
    ("Turn on the Camera", True, "camera.open"),
    ("What is the speed of light in a vacuum?", False, None),
    ("Timer for 10 minutes and 10 seconds", True, "timer.set"),
    ("Who painted the Mona Lisa?", False, None),
    ("Start the Camera", True, "camera.open"),
    ("Thank you very much.", False, None),
    ("Create new web shooter project", True, "project.create_folder"),
    ("Please and thank you.", False, None),
    ("Give me system info", True, "system.info"),
    ("No, thank you.", False, None),
    ("Create new project called Iron Man", True, "project.create_folder"),
    ("Where do Lions live", False, None),
    ("Show me GPU information", True, "system.info"),
    ("What ocean is larger the atlantic or pacific", False, None),
    ("Make a new project folder name robot arm", True, "project.create_folder"),
    ("What is the largest country in the world", False, None),
    ("How much RAM am I using", True, "system.info"),
    ("Briefly explain AI", False, None),
    ("Start a new project called robot car", True, "project.create_folder"),
    ("Give me CPU Info", True, "system.info"),
    ("What is a brushless motor?", False, None),
    ("Make me a new project folder called AI assistant", True, "project.create_folder"),
    ("Goodnight!", False, None),
]

@pytest.mark.parametrize("prompt, should_call, function_name", prompts_and_expectations)
def test_function_call_accuracy(prompt, should_call, function_name):
    messages = [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": instruction_prompt_with_function_calling.format(user_message=prompt)},
    ]
    response = ollama.chat(model="gemma3:4b-it-q4_K_M", messages=messages)
    result = extract_tool_call(response["message"]["content"], function_name)
    if should_call:
        assert result is True, f"Expected call to {function_name}"
    else:
        assert result is None, "Did not expect a function call"
