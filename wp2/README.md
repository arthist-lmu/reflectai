# WP2: Creation of art-historical KGs

# Running KnowGL pipeline

```
poetry run pipeline -i /nfs/data/reflectai/redai-data/data/processed/rijksmuseum-20220107.jsonl -p '[{"plugin": "NLTKSentenceSplitter"}, {"plugin": "XLMRobertaLanguageDetection"},{"plugin": "SentenceMerger"}, {"plugin": "KnowGL"}]'
```
