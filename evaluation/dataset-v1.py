from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

DATASET_NAME = "agentic-rag-system-test-retrieval-metrics-v1"

rag_dataset = [
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


trajectory_dataset = [
    {
        "inputs" : {
            "question" : (
                "How does LangGraph implement short-term memory across multiple interactions, "
                "and what role do a checkpointer "
                "and thread_id play in preserving conversation state?"
            )
        },
        "outputs" :{
            "route" : "private_kb"
        }
    },
    {
        "inputs" : {
            "question" : (
                "what are the types of architectures in multi-agents?"
            )
        },
        "outputs" : {
            "route" : "web_search"
        }
    },
    {
        "inputs" : {
            "question" : (
                "Hi, my name is shiva."
            )
        },
        "outputs" : {
            "route" : "direct"
        }
    }
]

retrieval_metrics_dataset = [
    {
        "inputs" : {
            "question" : (
                "How does LangGraph manage short-term memory across multiple interactions in a conversation, "
                "and what role do checkpoints and threads play in preserving conversation state?"
            )
        },
        "outputs" : {
            "retrieved_doc_ids" : ["5e7db127-01cd-42c4-85a5-ce039c507d82", "6d3c97bb-1fa6-4af9-9348-080cf24586a2", "604f209c-f4b5-4ed0-91e8-6ad4c9011a7d"]
        }
    },
    {
        "inputs" : {
            "question" : (
                "How does LangGraph store and retrieve long-term memories across different conversations, "
                "and how are namespaces and keys used to organize memories in a store?"
            )
        },
        "outputs" : {
            "retrieved_doc_ids" : ["c07a654c-234c-4bad-b775-08ea5e05a788", "cea822be-12aa-4d25-9418-94d1c4d17d0f", "5e7db127-01cd-42c4-85a5-ce039c507d82"]
        }
    },
    {
        "inputs" : {
            "question" : (
                "How can semantic search be used to retrieve relevant memories from a LangGraph store, "
                "and what role do embeddings and similarity search play in finding those memories?"
            )
        },
        "outputs" : {
            "retrieved_doc_ids" : ["cea822be-12aa-4d25-9418-94d1c4d17d0f", "c07a654c-234c-4bad-b775-08ea5e05a788", "edfbb932-352c-470f-9b29-e401075e860f"]
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
        examples=retrieval_metrics_dataset,
    )

    print(f"Created dataset : {dataset.name}")