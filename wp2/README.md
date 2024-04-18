# WP2: Creation of art-historical KGs

Extracting the triplets from the raw text and transferring to a graph hosting software.

# KnowledgeGraph solutions

Possible approaches:
* Integration of ReflectAI triplets with 

# Running KnowGL pipeline

```
poetry run pipeline -i /nfs/data/reflectai/redai-data/data/processed/rijksmuseum-20220107.jsonl -p '[{"plugin": "NLTKSentenceSplitter"}, {"plugin": "XLMRobertaLanguageDetection"},{"plugin": "SentenceMerger"}, {"plugin": "KnowGL"}]'
```
