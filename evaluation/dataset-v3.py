from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

DATASET_NAME = "agentic-rag-system-retrieval-metrics-v3"

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


retrieval_metrics_dataset = [
    {
        "inputs": {
            "question": (
                "Rhodium is a rare, silvery-white metal belonging "
                "to the platinum group. It is resistant to corrosion "
                "and is valued for its reflectivity and catalytic properties."
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["8522b888-7fee-4b9b-92cb-15bb2cbc518b", "0748963a-6aa5-469f-a1c5-b1ca627b9eb3", "47de2d59-f2bc-47c5-b2dc-b1c55383064e"]
        }
    },
    {
        "inputs": {
            "question": (
                "Rhodium is rare because it occurs in low concentrations "
                "and is usually obtained as a byproduct of mining other "
                "metals. Its limited supply and industrial demand "
                "contribute to its high price."
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["47de2d59-f2bc-47c5-b2dc-b1c55383064e", "1469067b-98a2-420c-aff4-532b5beaa76e"]
        }
    },
    {
        "inputs": {
            "question": (
                "Rhodium is used in catalytic converters to reduce "
                "harmful nitrogen oxide emissions from vehicle exhaust, "
                "helping to control air pollution."
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["61ec1f21-a43e-4939-87b1-74f7d101f0b0", "f2ddd34b-b78a-4671-b570-fee8132e22c7", "a2449274-476a-4a74-9893-76eeb4dc6c9a"]
        }
    },
    {
        "inputs": {
            "question": (
                "Rhodium prices are influenced by its limited supply, "
                "automotive industry demand, mining production, recycling, "
                "and emissions regulations. These factors can cause "
                "significant price fluctuations."
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["47de2d59-f2bc-47c5-b2dc-b1c55383064e"]
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
            "version-3 testing RAG dataset for my Agentic RAG System. "
            "Evaluating : https://science.howstuffworks.com/rhodium.htm"
        ),
    )

    client.create_examples(
        dataset_id=dataset.id,
        examples=retrieval_metrics_dataset,
    )

    print(f"Create dataset : {dataset.name}\n\n")