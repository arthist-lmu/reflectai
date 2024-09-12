import json
from pathlib import Path

import numpy as np
from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline


def create_transe_embedding(in_path: Path, out_path: Path, model: str='TransE',
                            epochs: int=5, embedding_dim: int=128):
    tf = TriplesFactory.from_path(in_path)
    train, test = tf.split(0.95)
    result = pipeline(
        training=train,
        testing=test,
        model=model,
        model_kwargs={'embedding_dim': embedding_dim},
        epochs=epochs,
    )
    out_path.mkdir(exist_ok=True)
    np.save(
        out_path / 'node_embeddings.npy',
        result.model.entity_representations[0]().cpu().detach().numpy()
    )
    np.save(
        out_path / 'relation_embeddings.npy',
        result.model.relation_representations[0]().cpu().detach().numpy()
    )
    with (out_path / 'entity_id_to_label.json').open('w') as f:
        json.dump(result.training.entity_id_to_label ,f)
    with (out_path / 'relation_id_to_label.json').open('w') as f:
        json.dump(result.training.relation_id_to_label ,f)
