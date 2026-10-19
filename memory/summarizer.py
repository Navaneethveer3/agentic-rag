import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from langmem.short_term import SummarizationNode, RunningSummary
from langchain_core.messages.utils import count_tokens_approximately
from agents.rag_agent import load_model

model = load_model()
summarization_model = model.bind(max_output_tokens=512)

summarization_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=summarization_model,
    max_tokens=600,
    max_tokens_before_summary=350,
    max_summary_tokens=150,
    input_messages_key="messages",
    output_messages_key="summarized_messages",
)

def load_summarizer():
    return summarization_node