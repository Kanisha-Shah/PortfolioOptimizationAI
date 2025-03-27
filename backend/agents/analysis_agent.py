from agents.data_collector import DataCollector

class PortfolioAnalysis:
    def __init__(self):
        self.collector = DataCollector()

    def analyze_portfolio(self, holdings: list) -> dict:
        """
        Analyzes portfolio holdings.
        Each holding must include: symbol, quantity, purchase_price.
        Returns analysis with current price, profit/loss (absolute & %), and allocation percentages.
        """
        analysis_details = []
        total_current_value = 0.0
        total_invested = 0.0

        for holding in holdings:
            symbol = holding["symbol"]
            quantity = holding["quantity"]
            purchase_price = holding["purchase_price"]
            current_price = self.collector.get_current_price(symbol)
            invested = purchase_price * quantity
            current_value = current_price * quantity
            profit_loss = current_value - invested
            profit_loss_percent = ((current_price - purchase_price) / purchase_price) * 100 if purchase_price else 0.0

            analysis_details.append({
                "symbol": symbol,
                "quantity": quantity,
                "purchase_price": purchase_price,
                "current_price": current_price,
                "invested": invested,
                "current_value": current_value,
                "profit_loss": profit_loss,
                "profit_loss_percent": profit_loss_percent
            })

            total_current_value += current_value
            total_invested += invested

        for detail in analysis_details:
            detail["allocation_percentage"] = (detail["current_value"] / total_current_value) * 100 if total_current_value > 0 else 0.0

        total_profit_loss = total_current_value - total_invested
        overall_return_percent = ((total_current_value - total_invested) / total_invested) * 100 if total_invested > 0 else 0.0

        return {
            "total_invested": total_invested,
            "total_current_value": total_current_value,
            "total_profit_loss": total_profit_loss,
            "overall_return_percent": overall_return_percent,
            "details": analysis_details
        }

# if __name__ == "__main__":
#     sample_holdings = [
#         {"symbol": "AAPL", "quantity": 10, "purchase_price": 120},
#         {"symbol": "GOOGL", "quantity": 5, "purchase_price": 1500},
#         {"symbol": "TSLA", "quantity": 8, "purchase_price": 600}
#     ]
#     analyzer = PortfolioAnalysis()
#     result = analyzer.analyze_portfolio(sample_holdings)
#     print(result)