import os
import pandas as pd
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
import yaml
import os
import re
import load_dotenv
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import ast

load_dotenv(".env",override=True)


# fetching environment variables for API base and key
api_base = os.getenv("EYQ_INCUBATOR_ENDPOINT") # incubator endpoint
api_key = os.getenv("EYQ_INCUBATOR_KEY") # incubator API key
model = os.getenv("LLM_MODEL")
temp = os.getenv("LLM_TEMPERATURE", 0.0)  # Default to 0.0 if not set
max_tokens = os.getenv("LLM_MAX_TOKENS", "10000")  # Default to 10000 if not set
api_version= os.getenv("LLM_API_VERSION", "2024-06-01")  # Default to 2024-06-01 if not set

# Uncomment below lines to print the API key and base for debugging
# print("API key ---- >  ", api_key)
# print("API base ---- >  ", api_base)




def read_yaml_config(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def save_code_to_file(code, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(code)
def extract_code(text: str) -> str | None:
    patterns = [
        # Standard markdown with python specified
        (r"```python\s*(.*?)\s*```", re.DOTALL),
        # Generic code block (any language or none)
        (r"```\s*(.*?)\s*```", re.DOTALL),
        # Non-standard single quote variants
        (r"'''python\s*(.*?)\s*'''", re.DOTALL),
        (r"'''\s*(.*?)\s*'''", re.DOTALL)
    ]
    
    for pattern, flags in patterns:
        match = re.search(pattern, text, flags)
        if match:
            code = match.group(1).strip()
            if code:
                return code
    return None



class DeveloperAgent:
    def __init__(self, data_path, guidance_path, llm_model=model): 
        self.data_path = data_path
        self.guidance_path = guidance_path
        self.llm = AzureChatOpenAI( azure_endpoint=api_base, api_key=api_key, azure_deployment=llm_model,
        api_version=api_version,temperature=temp, max_tokens=max_tokens)
        self.data = None
        self.generated_code = ""
        

    def load_data(self):
        self.data = pd.read_csv(self.data_path)
        print("✅ Data loaded successfully.")

    def read_human_guidance(self):
        return read_yaml_config(self.guidance_path)
        print("✅ Prompts read successfully.")

    def generate_cleaning_code(self):
        guidance = self.read_human_guidance()
        filename =guidance['step_1']['step_name']
        user_instructions = guidance['step_1']['human_guidance']
        # regulatory_guidance = self.governance_agent.extract_relevant_guidance("data cleaning")

        sample_columns = ", ".join(self.data.columns[:5])
        prompt = f"""
        You are a data engineer with strong python syntax knowledge and all latest changes. Clean the dataset based on the following guidance.

        Human Guidance:
        {user_instructions}

        Regulatory Guidance:
        

        Sample Columns: {sample_columns}

        Generate Python  code that performs the above cleaning on a DataFrame named `df`.
        Make sure the response generated can be directly copied in py file and executed. There should be no syntax error and initial comment, double check for syntax errors.  Only give python code in response, nothing else , no english text before the code.     """

        response = self.llm([HumanMessage(content=prompt)]).content.strip()
        self.generated_code = extract_code(response)
        save_code_to_file(self.generated_code, f"ai_generated_code/{filename}.py")
        print(f"✅ Code generation complete. Saved to ai_generated_code/{filename}.py")
        return self.generated_code

    def self_review_and_fix_generated_code(self, max_retries=5):
        """
        Check if generated code has syntax errors and attempt to regenerate if needed.
        """
        for attempt in range(max_retries + 1):
            try:
                ast.parse(self.generated_code)
                print("✅ Code passed syntax check.")
                return True
            except SyntaxError as e:
                print(f"❌ Syntax error in generated code: {e}")
                if attempt < max_retries:
                    print("🔁 Attempting to regenerate code...")
                    self.generate_cleaning_code()
                else:
                    print("🚫 Maximum retries reached. Fix the code manually.")
                    return False

        if not self.generated_code:
            print("⚠️ No code to execute.")
            return

        if not self.self_review_and_fix_generated_code():
            print("⚠️ Execution aborted due to persistent syntax issues.")
            return

        try:
            exec_env = {'df': self.data}
            exec(self.generated_code, exec_env)
            self.data = exec_env['df']
            self.data.to_csv("data/cleaned_credit_data.csv", index=False)
            print("✅ Code executed , data cleaned and saved successfully.")
        except Exception as e:
            print(f"❌ Error during execution: {e}")

    def explore_data_and_generate_notebook(self, notebook_path="ai_generated_code/data_exploration.ipynb"):
        self.load_data()
        guidance = self.read_human_guidance()
        filename =guidance['step_2']['step_name']
        user_instructions = guidance['step_2']['human_guidance']

        preview = self.data.head(3).to_markdown()

        prompt = f"""
            You are a credit risk modeling expert and data scientist.

            Your task is to explore a credit dataset and generate a visually rich exploratory data analysis (EDA) notebook based on the following human guidance:

            {user_instructions}

            Here is a preview of the dataset:

            {preview}

            Generate well-structured Jupyter notebook cells including:
            - Markdown with explanations and titles
            - Code for basic statistics, null counts, distributions
            - Visuals: histograms, box plots, correlation matrix, category distributions

            The notebook should be insightful, readable, and professionally formatted.
            Only return valid Python or Markdown content in cell-ready format.
            """

        response = self.llm([HumanMessage(content=prompt)]).content.strip()

        # Parse response into notebook cells (naively by Markdown/code separators)
        lines = response.splitlines()
        cells = []
        current_block = []
        is_code = False

        for line in lines:
            if line.strip().startswith("```python"):
                if current_block:
                    cells.append(new_markdown_cell("\n".join(current_block)))
                    current_block = []
                is_code = True
            elif line.strip().startswith("```"):
                if is_code:
                    cells.append(new_code_cell("\n".join(current_block)))
                    current_block = []
                    is_code = False
            else:
                current_block.append(line)

        if current_block:
            cells.append(new_code_cell("\n".join(current_block)) if is_code else new_markdown_cell("\n".join(current_block)))

        notebook = new_notebook(cells=cells)
        os.makedirs(os.path.dirname(notebook_path), exist_ok=True)

        with open(notebook_path, "w", encoding="utf-8") as f:
            nbformat.write(notebook, f)

        print(f"📒 Notebook saved to: {notebook_path}")


    def run(self):
        self.load_data()
        self.explore_data_and_generate_notebook()
        self.generate_cleaning_code()

