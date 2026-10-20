from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

DATASET_NAME = "agentic-rag-system-test-v1"

examples = [
    {
        "inputs" : {
            "question" : (
                "How do you implement short-term memory in LangGraph "
                "so an agent can remember information across multiple "
                "messages in the same conversation?"
            )
        },
        "outputs" : {
            "answer" : (
                "Short-term memory in LangGraph uses thread-level "
                "persistence. Create a checkpointer, such as InMemorySaver, "
                "compile the graph with checkpointer=checkpointer, and "
                "invoke it with a configurable thread_id. Reusing the same "
                "thread_id allows conversation state to persist across "
                "interactions. For production, use a database-backed "
                "checkpointer."
            )
        }
    },
    {
        "inputs" : {
            "question" : (
                "How can a LangGraph agent store and retrieve user-specific "
                "memories across separate conversation sessions?"
            )
        },
        "outputs" : {
            "answer" : (
                "Use LangGraph long-term memory with a store. Create an "
                "InMemoryStore for development and compile the graph with "
                "store=store. Access the store through the Runtime object "
                "inside node functions. Organize memories using namespaces, "
                "such as (user_id, 'memories'). Use search or asearch to "
                "retrieve relevant memories and put or aput to save them. "
                "Use a user-specific namespace to keep memories associated "
                "with the correct user across conversations."
            )
        }
    },
    {
        "inputs" : {
            "question" : (
                "What should you change when moving LangGraph memory from "
                "an in-memory setup to production, and what initialization "
                "step is required for PostgreSQL?"
            )
        },
        "outputs" : {
            "answer" : (
                "Use database-backed persistence instead of in-memory "
                "implementations. PostgresSaver provides a PostgreSQL-backed "
                "checkpointer for short-term memory, while PostgresStore "
                "supports long-term memory. During initial setup, call "
                "checkpointer.setup() for the checkpointer and "
                "store.setup() for the store, as applicable."
            )
        }
    }
]

existing = list(
    client.list_datasets(dataset_name=DATASET_NAME)
)

if existing:
    dataset = existing[0]
    print(f"Dataset already exists : {dataset.name}")
else:
    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description=(
            "Initial testing RAG dataset for my Agentic RAG System. "
            "Contains three evaluation questions based on LangGraph "
            "short-term memory, long-term memory, and production persistence."
        ),
    )

    client.create_examples(
        dataset_id=dataset.id,
        examples=examples,
    )

    print(f"Created dataset : {dataset.name}")