import autogen
from utils import get_code, load_requirements
from config import config_list
from jinja2 import Environment, FileSystemLoader

# Create a Jinja2 environment with the template directory
env = Environment(loader=FileSystemLoader('./'))
# create an AssistantAgent named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "request_timeout": 600,
        "seed": 42,  # seed for caching and reproducibility
        "config_list": config_list,  # a list of OpenAI API configurations
        "temperature": 0,  # temperature for sampling
    },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=2,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "generated_code",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
)

GAME = 'Asteroids'
requirements = load_requirements('asteroids.txt')
code = get_code('.\generated_code')

def reset_agents():
    user_proxy.reset()
    assistant.reset()
    
def batch_list(input_list, batch_size):
    for i in range(0, len(input_list), batch_size):
        yield input_list[i:i + batch_size]

def build_message_from_template(game, requirements, code):
    data = {
        'game' : game,
        'requirements': requirements,
        'code': code,
    }

    # Load the template from the file
    template = env.get_template('template.jinja2')

    # Render the template with the data
    return template.render(data)

def batch_list(input_list, batch_size):
    for i in range(0, len(input_list), batch_size):
        yield input_list[i:i + batch_size]
        

for batch in batch_list(requirements, 3):
    reset_agents()
    code = get_code('.\generated_code')
    
    user_proxy.initiate_chat(
        assistant,
        message = build_message_from_template(game=GAME, requirements=batch, code=code)
    
)





