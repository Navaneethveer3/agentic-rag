from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

DATASET_NAME = "agentic-rag-system-test-v2"

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
        examples=rag_dataset,
    )

    print(f"Created dataset : {dataset.name}\n\n")