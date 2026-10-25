from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

DATASET_NAME = "agentic-rag-system-retrieval-metrics-v4"

rag_dataset = [
    {
        "inputs": {
            "question": (
                "Why is deep-ocean exploration difficult, "
                "and what challenges do explorers face?"
            )
        },
        "outputs": {
            "answer": (
                "Deep-ocean exploration is difficult because of "
                "extreme water pressure, low temperatures, and "
                "the absence of sunlight. These conditions require "
                "specialized equipment and underwater technology."
            )
        }
    },
    {
        "inputs": {
            "question": (
                "What technologies are used to explore the deep ocean?"
            )
        },
        "outputs": {
            "answer": (
                "Deep-ocean exploration uses submersibles, remotely "
                "operated vehicles, autonomous underwater vehicles, "
                "sonar systems, and specialized cameras to study "
                "the seafloor and marine life."
            )
        }
    },
    {
        "inputs": {
            "question": (
                "Why is exploring the deep ocean important "
                "for scientific research?"
            )
        },
        "outputs": {
            "answer": (
                "Deep-ocean exploration helps scientists discover "
                "unknown marine species, study underwater ecosystems, "
                "understand geological processes, and learn more "
                "about Earth's oceans."
            )
        }
    },
    {
        "inputs": {
            "question": (
                "How does extreme pressure affect deep-ocean "
                "exploration equipment?"
            )
        },
        "outputs": {
            "answer": (
                "Water pressure increases with depth and can crush "
                "equipment that is not designed to withstand it. "
                "Deep-sea vehicles and instruments therefore require "
                "strong pressure-resistant structures and specialized "
                "engineering."
            )
        }
    }
]


retrieval_metrics_dataset = [
    {
        "inputs": {
            "question": (
                "Why is deep-ocean exploration difficult, "
                "and what challenges do explorers face?"
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["6fb4ad18-9424-4945-b14c-21f6b4a9fe9a", "3fc14c9e-3a2b-4e61-82b7-fdfe4c4f81ff", "e1581b77-370e-492a-8a48-62c703ba3623"]
        }
    },
    {
        "inputs": {
            "question": (
                "Deep-ocean exploration is difficult because of "
                "extreme water pressure, low temperatures, and "
                "the absence of sunlight. These conditions require "
                "specialized equipment and underwater technology."
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["6fb4ad18-9424-4945-b14c-21f6b4a9fe9a", "3fc14c9e-3a2b-4e61-82b7-fdfe4c4f81ff", "e1581b77-370e-492a-8a48-62c703ba3623"]
        }
    },
    {
        "inputs": {
            "question": (
                "Deep-ocean exploration helps scientists discover "
                "unknown marine species, study underwater ecosystems, "
                "understand geological processes, and learn more "
                "about Earth's oceans."
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["6fb4ad18-9424-4945-b14c-21f6b4a9fe9a", "e1581b77-370e-492a-8a48-62c703ba3623", "6596eff6-98bf-420f-a079-6934f1479dea"]
        }
    },
    {
        "inputs": {
            "question": (
                "How does extreme pressure affect deep-ocean "
                "exploration equipment?"
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
            "Testing dataset-v4 to test my Agentic RAG System. "
            "Evaluating : https://science.howstuffworks.com/environmental/earth/oceanography/deep-ocean-exploration.htm"
        ),
    )

    client.create_examples(
        dataset_id=dataset.id,
        examples=retrieval_metrics_dataset,
    )

    print(f"Dataset created : {dataset.name}")