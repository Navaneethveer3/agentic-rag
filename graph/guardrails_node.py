import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from langchain.agents.middleware import PIIMiddleware, PIIDetectionError
from langchain.messages import HumanMessage
from states.agent_state import AgentState
from langgraph.graph import END

pii_rules = [
    PIIMiddleware("email", strategy="redact"),
    PIIMiddleware("credit_card", strategy="mask"),
    PIIMiddleware("ip", strategy="redact"),
    PIIMiddleware("api_key", detector=r"sk-[a-zA-Z0-9]{32}", strategy="block"),
]

def guardrail_node(state : AgentState) -> dict:
    raw_query = state["question"]
    sanitized_query = raw_query

    try:
        for rule in pii_rules:
            sanitized_query, _ = rule._process_content(sanitized_query)
    except PIIDetectionError as e:
        return {
            "answer": "Security Alert: Your message contains sensitive personal information (PII) and cannot be processed.",
            "source_used": "guardrail_blocked",
        }
    
    print("---GUARDRAILS CHECKED---\n\n")
    print(f"Sanitized query : {sanitized_query}\n\n")
    
    return {
        "question" : sanitized_query,
        "current_query" : sanitized_query,
        "messages" : [HumanMessage(sanitized_query)],
    }

def check_guardrail(state : AgentState):
    if state.get("source_used")=="guardrail_blocked":
        return "blocked"
    return "proceed"