# WP2: Creation of art-historical KGs

(WP 1) serve the (semi-)automatic creation of art-historical knowledge graphs (WP 2).

# Extraction

Extracting the triplets from the raw text

Approaches:
* [KnowGL](https://huggingface.co/ibm/knowgl-large) as a specialized KG extractor, [Related Work](https://arxiv.org/pdf/2210.13952.pdf)
* [Mistral](https://huggingface.co/docs/transformers/main/model_doc/mistral) general LLM, with templating option
* [GoLLIE](https://huggingface.co/collections/HiTZ/gollie-651bf19ee315e8a224aacc4f) with annotation templates

## KnowGL

Requires additional pipeline steps before and after:

* Translator (Knowgl is english only) ->
* CoREF resolution ->
* Sentence Splitter (because it can't handle long paragraphs) ->
* KnowGL ->
* Output parser (to convert into machine readable format like JSON) ->
* Reconciler (Matching existing entities to Wikidata to reduce errors)

The output of the pipeline is not optimal, due to two errorprone operations:
* KnowGL delivers many hallucinated relations
* Reconciliation is better supported than in other models (due to provided entity type), but still contains a significant mismatch risk in some areas

Possible Mitigations:
* Optimizing KnowGL
* Reducing the set of accepted relationship types to a constraint set (e.g 25)

## Mistral

As a general LLM this approach could be replicated other models of the same class.

## GoLLIE

Provides an extensive templating engine to enhance extraction of predefined triplets

# KnowledgeGraph integration
Transferring the triplets to a graph hosting software.
Wikibase was chosen as the target platform, due to providing the most unrestricted object modeling.

Reconciliation is the process of matching the extracted triplets to existing data in other data repositories (in this case Wikidata). Considerations about its inclusion are:
* Reducing noise by detecting already existing entities
* Reducing duplication: a significant percentage of relevant extracted data is already available in Wikidata, ReflectAI should focus on newly found triplets
* Improving W4 goals: Including reconciliation would allow queries to rely on Wikidata as a baseline knowledge, that would drastically enhance the possible output. This baseline knowledge would be impossible to extract from ReflectAIs datasets and includes all relevant locations, institutions, people and their relationships.

Hosting options:
* TIB: Full control, self provisioning required
* [Wikibase.cloud](https://www.wikibase.cloud/): Full control over modeling, some rate-limiting may apply in parts
* [Factgrid](https://database.factgrid.de/wiki/Main_Page): Significant control over modeling, some rate limiting. 
* [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page): Only correct triplets allowed, rate limited queries and upload

Possible approaches:
* Upload reconciled ReflectAI triplets to a controlled Wikibase. Create all reconciled item with only the ReflectAI triplets (mostly empty), and link them to Wikidata, either via sitelink or property
* Upload only ReflectAI triplets without reconciliation
* Integrate correct triplets into Wikidata
* 

Improvements:
* Reducing noise via HITL (Human in the loop) before upload (required for upload in Wikidata, optional otherwise)
* Improving Reconciliation via HITL before upload (required for upload in Wikidata, optional otherwise)

# Setup

## Running KnowGL pipeline

```
poetry run pipeline -i /nfs/data/reflectai/redai-data/data/processed/rijksmuseum-20220107.jsonl -p '[{"plugin": "NLTKSentenceSplitter"}, {"plugin": "XLMRobertaLanguageDetection"},{"plugin": "SentenceMerger"}, {"plugin": "KnowGL"}]'
```

```
srun --mem 128G -N 1 --exclude gpu3,devbox5,devbox4,devbox3 -G 1  --pty apptainer exec --env PYTHONPATH=".." /nfs/data/env/huggingface_24_04_16.sif python main.py -i ~/projects/reflect_ai/reflectai/wp2/test/test_dataset/museums/testset_museum.jsonl -p '[{"plugin": "NLLB200", "config":{"src_lang":"de", "tgt_lang":"en"}}, {"plugin": "FCoref"}, {"plugin": "NLTKSentenceSplitter"}, {"plugin": "KnowGL"}, {"plugin":"SentenceMerger"},  {"plugin": "TripletsPrinter"}]'
```
