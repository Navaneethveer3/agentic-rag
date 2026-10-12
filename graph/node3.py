import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from states.agent_state import AgentState
from states.grade_decision import GradeEvidence
from agents.rag_agent import load_model

model = load_model()

decision_llm = model.with_structured_output(GradeEvidence, method="json_mode")

def grade_kb_evidence(state : AgentState):
    question = state["question"]

    context = "\n\n".join(
        f"Source: {doc.metadata.get("source")}\n{doc.page_content}"
        for doc in state["kb_docs"]
    )

    grade = decision_llm.invoke(f"""
    you are a evidence grader.

    question :
    {question}
    
    context :
    {context}

    is this information sufficient to answer?
    if yes, return "good"
    else, return "weak"

    return in the JSON format.

    Example :
    {{"grade" : "good"}}

    """)

    print("---KB EVIDENCE GRADED---\n\n")

    return {"kb_grade" : grade.grade}


def decide_after_kb_grade(state : AgentState):
    if state["kb_grade"]=="good":
        print("KB graded as GOOD\n\n")
        return "generate_from_kb"
    else:
        print("KB graded as WEAK\n\n")
        return "search_web"