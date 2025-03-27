import io
import os
import re
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI 

load_dotenv()

def markdown_to_html(text: str) -> str:
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    return text

class ReportGenerator:
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4-turbo",
            temperature=0.6,
            max_tokens=700
        )

        self.prompt_template = PromptTemplate(
            input_variables=["analysis", "optimization"],
            template=(
                "Generate a concise one-page report summarizing the following portfolio analysis:\n\n{analysis}\n\n"
                "and the following optimization recommendations:\n\n{optimization}\n\n"
                "Include clear headings, bullet points for key metrics, and use **bold** for emphasis where appropriate."
            )
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def generate_report_text(self, analysis: dict, optimization: dict) -> str:
        report_text = self.chain.run({
            "analysis": str(analysis),
            "optimization": str(optimization)
        })
        return markdown_to_html(report_text)

    def generate_pdf(self, report_text: str) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=50,
            rightMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        # Define styles for the report
        styles = getSampleStyleSheet()
        custom_style = ParagraphStyle(
            'Custom',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            spaceAfter=12,
            alignment=0
        )
        story = []
        # Split report text into paragraphs and create a Paragraph object for each
        for paragraph in report_text.split('\n'):
            if paragraph.strip():
                story.append(Paragraph(paragraph, custom_style))
                story.append(Spacer(1, 12))
        doc.build(story)
        pdf_data = buffer.getvalue()
        buffer.close()
        return pdf_data

# if __name__ == "__main__":
#     sample_analysis = {
#         "total_invested": 5000,
#         "total_current_value": 6000,
#         "total_profit_loss": 1000,
#         "overall_return_percent": 20
#     }

#     sample_optimization = {
#         "recommendation": "Invest more in **AAPL** and **TSLA** to diversify your portfolio and reduce risk."
#     }

#     openai_api_key = os.getenv("OPENAI_API_KEY")
#     generator = ReportGenerator(openai_api_key=openai_api_key)
#     report_text = generator.generate_report_text(sample_analysis, sample_optimization)
#     pdf_bytes = generator.generate_pdf(report_text)

#     with open("report.pdf", "wb") as f:
#         f.write(pdf_bytes)

#     print("✅ PDF report generated as report.pdf")