"""
Rights Agent for RentAgent.

Answers tenancy questions using retrieval-augmented generation over the
Renters' Rights Act 2025. Retrieved sections carry their commencement status,
so a provision that is enacted but not yet in force is identified as such
rather than presented as current law.

Abstains when no retrieved section is sufficiently similar to the question,
rather than generating an answer from model memory.
"""

from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
import json
import urllib.request

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_PATH = PROJECT_ROOT / 'data' / 'processed' / 'chroma'

EMBEDDER = SentenceTransformer('all-MiniLM-L6-v2')
CLIENT = chromadb.PersistentClient(path=str(CHROMA_PATH))
COLLECTION = CLIENT.get_collection('renters_rights_act')

# Distance above which no retrieved section is considered relevant.
# Calibrated against a test set; see notebooks/08_rights_evaluation.ipynb
ABSTENTION_THRESHOLD = 1.25


def retrieve(question, k=3):
    """Return the k closest sections with their metadata and distances."""
    q_emb = EMBEDDER.encode([question])
    res = COLLECTION.query(query_embeddings=q_emb.tolist(), n_results=k)

    return [
        {
            'section': m['section'],
            'heading': m['heading'],
            'in_force': m['in_force_now'],
            'partial': m['partial'],
            'commencement': m['commencement'],
            'text': d,
            'distance': dist,
        }
        for d, m, dist in zip(res['documents'][0],
                              res['metadatas'][0],
                              res['distances'][0])
    ]


OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL = 'llama3.1:8b'


def ask_model(prompt, temperature=0.0):
    """
    Send a prompt to the locally served model.

    Temperature is fixed at zero for reproducibility, as required by the
    experimental protocol in Section 3.7.
    """
    payload = json.dumps({
        'model': MODEL,
        'prompt': prompt,
        'stream': False,
        'options': {'temperature': temperature},
    }).encode('utf-8')

    req = urllib.request.Request(
        OLLAMA_URL, data=payload,
        headers={'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())['response']

def answer(question, k=3):
    """
    Answer a tenancy question from the Act.

    Abstains when no retrieved section falls below the distance threshold,
    rather than answering from model memory. Commencement status is passed
    to the model so that provisions not yet in force are identified as such.
    """
    hits = retrieve(question, k)

    if not hits or hits[0]['distance'] > ABSTENTION_THRESHOLD:
        return {
            'answered': False,
            'reason': 'No sufficiently relevant provision found',
            'best_distance': round(hits[0]['distance'], 3) if hits else None,
            'sections': [],
        }

    context = "\n\n---\n\n".join(
        f"Section {h['section']}: {h['heading']}\n"
        f"Status: {'IN FORCE' if h['in_force'] else 'ENACTED BUT NOT YET COMMENCED'}\n"
        f"{' (partial commencement)' if h['partial'] else ''}\n"
        f"Commencement: {h['commencement'][:200]}\n\n"
        f"{h['text'][:3000]}"
        for h in hits
    )

    prompt = f"""You are answering a question about the Renters' Rights Act 2025 \
for a tenant in England.

Answer ONLY from the provisions below. Do not use any other knowledge.
If a provision is marked as NOT YET COMMENCED, you must say so explicitly.
Do not speculate about when it might come into force.
Cite the section number for every statement you make.
If the provisions do not answer the question, say so.

PROVISIONS:
{context}

QUESTION: {question}

ANSWER:"""

    return {
        'answered': True,
        'answer': ask_model(prompt),
        'sections': [
            {'section': h['section'], 'heading': h['heading'],
             'in_force': h['in_force'], 'distance': round(h['distance'], 3)}
            for h in hits
        ],
    }


if __name__ == '__main__':
    import time

    q = "Can my landlord refuse to rent to me because I have children?"
    t0 = time.perf_counter()
    r = answer(q, k=3)
    print(f"{MODEL}: {time.perf_counter() - t0:.1f}s\n")
    print(r['answer'])