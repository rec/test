import sentence_transformers
import superduperdb as s
from pymongo import MongoClient
from superduperdb.container.document import Document
from superduperdb.container.listener import Listener
from superduperdb.container.model import Model
from superduperdb.container.vector_index import VectorIndex
from superduperdb.db.mongodb.query import Collection
from superduperdb.ext.numpy.array import array

# This fails, because of the model name
MODEL_NAME = "BAAI/bge-base-en"
VECTOR_SIZE = 768

# Below works
# MODEL_NAME = "all-MiniLM-L6-v2"
# VECTOR_SIZE = 384

IDENTIFIER_ID = "my-index"
COLLECTION_NAME = "docs"

client = MongoClient("localhost", 27017)
db = s.superduper(client.documents)
collection = Collection(name=COLLECTION_NAME)

data = [
    {
        "title": "Anarchism",
        "abstract": "Anarchism is a political philosophy and movement that is skeptical of all justifications for authority and seeks to abolish the institutions they claim maintain unnecessary coercion and hierarchy, typically including, though not necessarily limited to, the state and capitalism. Anarchism advocates for the replacement of the state with stateless societies or other forms of free associations.",
    },
    {
        "title": "Albedo",
        "abstract": "Albedo (; ) is the measure of the diffuse reflection of solar radiation out of the total solar radiation and measured on a scale from 0, corresponding to a black body that absorbs all incident radiation, to 1, corresponding to a body that reflects all incident radiation.",
    },
    {
        "title": "Achilles",
        "abstract": 'In Greek mythology, Achilles ( ) or Achilleus ( Accessed 5 May 2017. the latter being the dative of the former. The name grew more popular, even becoming common soon after the seventh century BCEpigraphical database gives 476 matches for Ἀχιλ-.The earliest ones: Corinth 7th c. BC, Delphi 530 BC, Attica and Elis 5th c. BC. and was also turned into the female form Ἀχιλλεία (Achilleía), attested in Attica in the fourth century BC (IG II² 1617) and, in the form Achillia, on a stele in Halicarnassus as the name of a female gladiator fighting an "Amazon".',
    },
]


model = Model(
    identifier=MODEL_NAME,
    object=sentence_transformers.SentenceTransformer(MODEL_NAME),
    encoder=array("float32", shape=(VECTOR_SIZE,)),
    predict_method="encode",
    batch_predict=True,
)


db.add(
    VectorIndex(
        identifier=IDENTIFIER_ID,
        indexing_listener=Listener(
            model=model,
            key="abstract",
            select=Collection(name=COLLECTION_NAME).find(),
        ),
    )
)


print(db.show("listener"))
print(db.show("model"))
print(db.show("vector_index"))

data = [Document(r) for r in data]
db.execute(collection.insert_many(data))
