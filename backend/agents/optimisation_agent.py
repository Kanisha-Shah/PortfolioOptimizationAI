from langchain_core.prompts import PromptTemplate 
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class PortfolioOptimizer:
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4-turbo",
            temperature=0.7,
            max_tokens=400
        )

        self.prompt_template = PromptTemplate(
            input_variables=["analysis", "risk_tolerance"],
            template=(
                "Please analyze the following portfolio analysis data:\n\n{analysis}\n\n"
                "Given a risk tolerance of '{risk_tolerance}', provide a detailed, risk-adjusted portfolio "
                "optimization strategy with recommendations for improving diversification and returns. "
                "Highlight key suggestions in **bold** where applicable."
            )
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def optimize_with_llm(self, analysis: dict, risk_tolerance: str) -> dict:
        recommendation = self.chain.run({
            "analysis": str(analysis),
            "risk_tolerance": risk_tolerance
        })
        return {"recommendation": recommendation}

# if __name__ == "__main__":
#     # Example test using sample analysis
#     from agents.analysis_agent import PortfolioAnalysis
#     sample_holdings = [
#         {"symbol": "AAPL", "quantity": 10, "purchase_price": 120},
#         {"symbol": "GOOGL", "quantity": 5, "purchase_price": 1500},
#         {"symbol": "TSLA", "quantity": 8, "purchase_price": 600}
#     ]
#     analyzer = PortfolioAnalysis()
#     analysis_result = analyzer.analyze_portfolio(sample_holdings)
    
#     import os
#     openai_api_key = os.getenv("OPENAI_API_KEY")
#     optimizer = PortfolioOptimizer(openai_api_key=openai_api_key)
#     optimization_result = optimizer.optimize_with_llm(analysis_result, "medium")
#     print(optimization_result)