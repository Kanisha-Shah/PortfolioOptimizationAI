import yfinance as yf
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class DataCollector:
    def __init__(self):
        # Initialize an LLM instance for ticker resolution.
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI( 
            api_key=openai_api_key,
            model="gpt-4-turbo",
            temperature=0.2,
            max_tokens=12
        )

    def get_stock_data(self, symbol: str, period: str = "1d", interval: str = "1m"):
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval=interval)
        return data.reset_index().to_dict(orient="records")

    def get_current_price(self, symbol: str) -> float:
        ticker = yf.Ticker(symbol)
        try:
            info = ticker.info
        except Exception:
            info = {}
        price = info.get("regularMarketPrice")
        if price is None:
            try:
                data = ticker.history(period="1d")
                price = data["Close"].iloc[-1] if not data.empty else 0.0
            except Exception:
                price = 0.0
        return price

    def resolve_ticker(self, company_name: str) -> str:
        """
        Uses an LLM to resolve a company name into its ticker symbol on the US stock market.
        The prompt asks for an answer in uppercase letters.
        """
        prompt = (
            f"Given the company name '{company_name}', what is its ticker symbol on the US stock market? "
            "Answer only with the ticker symbol in uppercase letters."
        )
        ticker = self.llm.invoke(prompt)
        return ticker.strip()

# if __name__ == "__main__":
#     collector = DataCollector()
#     print(collector.get_stock_data("AAPL", period="1d", interval="1m")[:5])
#     print("Current Price:", collector.get_current_price("AAPL"))