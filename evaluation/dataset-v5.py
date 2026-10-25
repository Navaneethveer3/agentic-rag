from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

DATASET_NAME = "agentic-rag-system-test-v5"

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
        examples=rag_dataset,
    )

    print(f"Dataset created : {dataset.name}")