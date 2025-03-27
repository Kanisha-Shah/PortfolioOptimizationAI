import os
from agents.data_collector import DataCollector
from agents.analysis_agent import PortfolioAnalysis
from agents.optimisation_agent import PortfolioOptimizer
from agents.report_generation_agent import ReportGenerator

class PipelineOrchestrator:
    def __init__(self, openai_api_key: str):
        self.collector = DataCollector()
        self.analyzer = PortfolioAnalysis()
        self.optimizer = PortfolioOptimizer(openai_api_key=openai_api_key)
        self.report_generator = ReportGenerator(openai_api_key=openai_api_key)

    def run_pipeline(self, holdings: list, risk_tolerance: str) -> bytes:
        """
        Executes the full portfolio pipeline:
          1. Updates each holding with the current market price.
          2. Runs portfolio analysis (calculating profit/loss, risk metrics, etc.).
          3. Runs portfolio optimization via an LLM.
          4. Generates a PDF report.
        :param holdings: List of dictionaries with holding details.
        :param risk_tolerance: The user's risk tolerance.
        :return: PDF bytes of the generated report.
        """
        # Update holdings with current market price
        updated_holdings = []
        for holding in holdings:
            current_price = self.collector.get_current_price(holding["symbol"])
            updated_holdings.append({
                **holding,
                "current_price": current_price
            })
        
        # Analyze the portfolio
        analysis_result = self.analyzer.analyze_portfolio(updated_holdings)
        
        # Optimize the portfolio via the LLM
        optimization_result = self.optimizer.optimize_with_llm(analysis_result, risk_tolerance)
        
        # Generate the report text and convert to PDF
        report_text = self.report_generator.generate_report_text(analysis_result, optimization_result)
        pdf_bytes = self.report_generator.generate_pdf(report_text)
        return pdf_bytes

# if __name__ == "__main__":
#     sample_holdings = [
#         {"symbol": "AAPL", "quantity": 10, "purchase_price": 120},
#         {"symbol": "GOOGL", "quantity": 5, "purchase_price": 1500},
#         {"symbol": "TSLA", "quantity": 8, "purchase_price": 600}
#     ]
#     import os
#     openai_api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
#     orchestrator = PipelineOrchestrator(openai_api_key=openai_api_key)
#     pdf_bytes = orchestrator.run_pipeline(sample_holdings, "medium")
#     with open("orchestrator_report.pdf", "wb") as f:
#         f.write(pdf_bytes)
#     print("Orchestrated PDF report generated as orchestrator_report.pdf")