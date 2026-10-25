from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

DATASET_NAME = "agentic-rag-system-test-v3"

rag_dataset = [
    {
        "inputs": {
            "question": "What is rhodium, and what are its main properties?"
        },
        "outputs": {
            "answer": (
                "Rhodium is a rare, silvery-white metal belonging "
                "to the platinum group. It is resistant to corrosion "
                "and is valued for its reflectivity and catalytic properties."
            )
        }
    },
    {
        "inputs": {
            "question": "Why is rhodium so rare and expensive?"
        },
        "outputs": {
            "answer": (
                "Rhodium is rare because it occurs in low concentrations "
                "and is usually obtained as a byproduct of mining other "
                "metals. Its limited supply and industrial demand "
                "contribute to its high price."
            )
        }
    },
    {
        "inputs": {
            "question": "What is rhodium used for in automobiles?"
        },
        "outputs": {
            "answer": (
                "Rhodium is used in catalytic converters to reduce "
                "harmful nitrogen oxide emissions from vehicle exhaust, "
                "helping to control air pollution."
            )
        }
    },
    {
        "inputs": {
            "question": "What factors affect the price of rhodium?"
        },
        "outputs": {
            "answer": (
                "Rhodium prices are influenced by its limited supply, "
                "automotive industry demand, mining production, recycling, "
                "and emissions regulations. These factors can cause "
                "significant price fluctuations."
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
            "version-3 testing RAG dataset for my Agentic RAG System. "
            "Evaluating : https://science.howstuffworks.com/rhodium.htm"
        ),
    )

    client.create_examples(
        dataset_id=dataset.id,
        examples=rag_dataset,
    )

    print(f"Create dataset : {dataset.name}\n\n")