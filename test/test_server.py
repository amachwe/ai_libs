import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import prompt_registry as pr

if __name__ == "__main__":
    registry = pr.PromptRegistry('test/registry.json')
    prompt = registry.get_prompt('Prompt1')
    print(prompt)
    print(prompt.generate_prompt(name="Alice", age=30))