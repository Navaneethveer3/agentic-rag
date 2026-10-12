import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from states.grade_decision import GradeEvidence
from states.agent_state import AgentState
from agents.rag_agent import load_model

model = load_model()

grader_llm = model.with_structured_output(GradeEvidence, method="json_mode")

def grade_web_evidence(state : AgentState):
    question = state["question"]

    web_results = state["web_results"]

    grade = grader_llm.invoke(f"""
    you are an evidence grader.

    question :
    {question}

    web result evidence :
    {web_results}

    is this evidence good enough to answer the question?
    if yes, return "good"
    else return "weak"

    return in the JSON format.
    Example :
    {{"grade" : "good"}}

    """)

    print("---WEB EVIDENCE GRADED---\n\n")

    return {"web_grade" : grade.grade}


MAX_RETRIES = 1

def decide_after_web_grade(state : AgentState):
    if state["web_grade"]=="good":
        print("Decided to generate from web\n\n")
        return "generate_from_web"
    
    if state["retry_count"]<MAX_RETRIES:
        print("---INITIALIZING RETRY---\n\n")
        return "rewrite_query"
    else:
        print("Decided to rewrite the query\n\n")
        return "answer_insufficient"