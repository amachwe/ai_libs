import json
import pydantic 

class PromptMetadata(pydantic.BaseModel):
    name: str
    description: str
    prompt_file: str
    input_variables: list[str]


class Prompt(pydantic.BaseModel):
    metadata: PromptMetadata
    prompt_template: str

    def generate_prompt(self, **kwargs) -> str:
        return self.prompt_template.format(**kwargs)

class PromptRegistry:
    def __init__(self, registry_file: str):
        self.registry_file = registry_file
        self.prompts = self.load_registry()

    def load_registry(self) -> dict[str, Prompt]:
        with open(self.registry_file, 'r') as f:
            data = json.load(f)
            return {prompt_data['name']: Prompt(metadata=PromptMetadata(**prompt_data), prompt_template=open(prompt_data['prompt_file']).read()) for prompt_data in data}

    def get_prompt(self, name: str) -> Prompt:
        return self.prompts.get(name)

    def add_prompt(self, prompt: Prompt):
        self.prompts[prompt.metadata.name] = prompt
        self.save_registry()

    def save_registry(self):
        with open(self.registry_file, 'w') as f:
            json.dump({name: prompt.model_dump() for name, prompt in self.prompts.items()}, f, indent=4)