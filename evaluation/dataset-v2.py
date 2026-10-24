from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

DATASET_NAME = "agentic-rag-system-test-retrieval-metrics-v2"

rag_dataset = [
    {
        "inputs": {
            "question": (
                "How do human activities contribute to climate change, "
                "and what role do greenhouse gases play in this process?"
            )
        },
        "outputs": {
            "answer": (
                "Human activities such as burning fossil fuels and "
                "deforestation contribute to climate change by increasing "
                "greenhouse gas concentrations in the atmosphere. These "
                "gases trap heat, intensifying the greenhouse effect and "
                "raising Earth's average temperature."
            )
        }
    },
    {
        "inputs": {
            "question": (
                "How can climate change affect both natural ecosystems "
                "and human communities?"
            )
        },
        "outputs": {
            "answer": (
                "Climate change can disrupt ecosystems through changing "
                "temperatures, rainfall patterns, and habitats. It can also "
                "affect human communities through extreme weather, food "
                "and water insecurity, health risks, damage to infrastructure, "
                "and the displacement of people."
            )
        }
    },
    {
        "inputs": {
            "question": (
                "Why are developing countries and vulnerable communities "
                "often disproportionately affected by climate change?"
            )
        },
        "outputs": {
            "answer": (
                "Vulnerable communities may face greater exposure to climate "
                "hazards while having fewer financial resources, less resilient "
                "infrastructure, and limited access to services needed to "
                "prepare for and recover from climate impacts. Their ability "
                "to adapt can therefore be more constrained."
            )
        }
    },
    {
        "inputs": {
            "question": (
                "What is the difference between climate change mitigation "
                "and adaptation, and why are both necessary?"
            )
        },
        "outputs": {
            "answer": (
                "Mitigation addresses the causes of climate change by reducing "
                "greenhouse gas emissions or increasing carbon absorption. "
                "Adaptation reduces vulnerability to actual or expected "
                "climate impacts. Both are necessary because reducing future "
                "warming and managing existing or unavoidable impacts are "
                "complementary goals."
            )
        }
    },
    {
        "inputs": {
            "question": (
                "How does international cooperation help address climate "
                "change, and how does the Paris Agreement contribute "
                "to this effort?"
            )
        },
        "outputs": {
            "answer": (
                "International cooperation enables countries to coordinate "
                "climate action, establish shared goals, and work together "
                "to reduce emissions and address climate impacts. The Paris "
                "Agreement provides an international framework that aims "
                "to hold global warming well below 2°C above pre-industrial "
                "levels while pursuing efforts to limit it to 1.5°C."
            )
        }
    }
]

retrieval_metrics_dataset = [
    {
        "inputs": {
            "question": (
                "How do human activities contribute to climate change, "
                "and what role do greenhouse gases play in this process?"
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["f45c7437-0da3-4cbb-a203-60537a5c9f70", "8c7674d3-d1d3-4ec2-9747-58ef3d2b5e88", "1d589a9f-104b-4a34-9e7f-6dc71cb4af0a"]
        }
    },
    {
        "inputs": {
            "question": (
                "How can climate change affect both natural ecosystems "
                "and human communities?"
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["8c7674d3-d1d3-4ec2-9747-58ef3d2b5e88", "479c084e-0bac-436e-b595-b8620addf87a", "f45c7437-0da3-4cbb-a203-60537a5c9f70"]
        }
    },
    {
        "inputs": {
            "question": (
                "Why are developing countries and vulnerable communities "
                "often disproportionately affected by climate change?"
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["479c084e-0bac-436e-b595-b8620addf87a", "2922027d-d17f-47c1-aa46-beb9f79616a9", "8c7674d3-d1d3-4ec2-9747-58ef3d2b5e88"]
        }
    },
    {
        "inputs": {
            "question": (
                "What is the difference between climate change mitigation "
                "and adaptation, and why are both necessary?"
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["8c7674d3-d1d3-4ec2-9747-58ef3d2b5e88", "479c084e-0bac-436e-b595-b8620addf87a", "f45c7437-0da3-4cbb-a203-60537a5c9f70"]
        }
    },
    {
        "inputs": {
            "question": (
                "How does international cooperation help address climate "
                "change, and how does the Paris Agreement contribute "
                "to this effort?"
            )
        },
        "outputs": {
            "retrieved_doc_ids" : ["d8219c24-b45b-43ea-ac52-a7745b96b43d", "0b914df1-5587-449c-b7b2-023b92df67c8", "3f724b48-c55a-4e18-8406-5d3dcfc8c501"]
        }
    }
]

existing = list(
    client.list_datasets(dataset_name=DATASET_NAME)
)

if existing:
    dataset = existing[0]
    print(f"Dataset already exists : {dataset.name}\n\n")
else:
    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description=(
            "version-2 testing RAG dataset for my Agentic RAG System. "
            "Evaluating : https://www.un.org/en/global-issues/climate-change?utm_source=chatgpt.com"
        ),
    )

    client.create_examples(
        dataset_id=dataset.id,
        examples=retrieval_metrics_dataset,
    )

    print(f"Created dataset : {dataset.name}\n\n")