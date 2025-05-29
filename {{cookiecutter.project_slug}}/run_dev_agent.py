from src.utils.developer_agent import DeveloperAgent




def main():


    #  Developer interprets YAML + governance and generates code
    agent = DeveloperAgent("data/credit_data.csv", "prompts/prompts.yaml")
    agent.run()

if __name__ == "__main__":
    main()