from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

DATASET_NAME = "agentic-rag-system-retrieval-metrics-v5"

rag_dataset = [
    {
        "inputs": {
            "question": (
                "Where is the Arctic Ocean located, and what makes "
                "it different from other oceans?"
            )
        },
        "outputs": {
            "answer": (
                "The Arctic Ocean surrounds the North Pole and is "
                "the smallest and shallowest of the world's oceans. "
                "It is characterized by extremely cold temperatures "
                "and extensive seasonal sea ice."
            )
        }
    },
    {
        "inputs": {
            "question": (
                "How does sea ice affect the Arctic Ocean's "
                "environment and climate?"
            )
        },
        "outputs": {
            "answer": (
                "Sea ice reflects sunlight back into space, helping "
                "regulate Earth's temperature. It also provides "
                "habitats for Arctic wildlife and influences ocean "
                "ecosystems and weather patterns."
            )
        }
    },
    {
        "inputs": {
            "question": (
                "What types of animals live in the Arctic Ocean?"
            )
        },
        "outputs": {
            "answer": (
                "The Arctic Ocean supports animals such as polar bears, "
                "seals, walruses, whales, and various fish and seabirds. "
                "Many of these species depend on sea ice and marine "
                "food webs for survival."
            )
        }
    },
    {
        "inputs": {
            "question": (
                "How does climate change affect the Arctic Ocean?"
            )
        },
        "outputs": {
            "answer": (
                "Climate change is warming the Arctic and reducing "
                "sea ice. These changes threaten ice-dependent wildlife, "
                "alter marine ecosystems, and reduce the ocean's ability "
                "to reflect sunlight."
            )
        }
    }
]

retrieval_metrics_dataset = [
    {
        "inputs": {
            "question": (
                "Where is the Arctic Ocean located, and what makes "
                "it different from other oceans?"
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["5317aea1-bb28-47c4-a976-c0131ccd707d", "23a63427-a623-422f-85d6-8254ec9ab392", "6fb4ad18-9424-4945-b14c-21f6b4a9fe9a"]
        }
    },
    {
        "inputs": {
            "question": (
                "How does sea ice affect the Arctic Ocean's "
                "environment and climate?"
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["5317aea1-bb28-47c4-a976-c0131ccd707d", "9b7898b1-2078-4f9c-8573-a512df8dc2fe", "daa05fad-8b02-4f95-9ff5-9c89b0f5dba3"]
        }
    },
    {
        "inputs": {
            "question": (
                "What types of animals live in the Arctic Ocean?"
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["832de71b-55ba-4ad6-a10a-4b48152cdd6d", "f7589885-cf89-4fa9-b5f1-e40bdd4b6150", "a2b21797-ca7b-471c-a8e5-ee017c241dd9"]
        }
    },
    {
        "inputs": {
            "question": (
                "How does climate change affect the Arctic Ocean?"
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["5317aea1-bb28-47c4-a976-c0131ccd707d", "1d66a060-665e-45c3-ad9d-cb01519ad6b5", "9b7898b1-2078-4f9c-8573-a512df8dc2fe"]
        }
    },
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
            "Testing dataset-v5 to test my Agentic RAG System. "
            "Evaluating : https://science.howstuffworks.com/environmental/earth/arctic-ocean.htm"
        ),
    )

    client.create_examples(
        dataset_id=dataset.id,
        examples=retrieval_metrics_dataset,
    )

    print(f"Dataset created : {dataset.name}")