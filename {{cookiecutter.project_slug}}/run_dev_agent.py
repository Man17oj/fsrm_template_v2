from src.utils.developer_agent import DeveloperAgent
from dotenv import load_dotenv
import os

load_dotenv(".env",override=True)

api_base = os.getenv("EYQ_INCUBATOR_ENDPOINT") # incubator endpoint
api_key = os.getenv("EYQ_INCUBATOR_KEY") # incubator API key

# print("API key ---- >  ", api_key)
# print("API base ---- >  ", api_base)


def main():


    #  Developer interprets YAML + governance and generates code
    agent = DeveloperAgent("data/credit_data.csv", "prompts/prompts.yaml")
    agent.run()

if __name__ == "__main__":
    main()