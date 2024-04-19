# WP3: Multimodal analysis of artworks using a hybrid AI approach

In WP 3, hybrid multimodal deep learning methods for the analysis of artworks based on domain-specific expert knowledge are researched. 
Due to the black box property of deep learning architectures, explainable AI methods and visualizations are developed to better understand and evaluate the obtained results with respect to the biases described (WP 4).

# Creation of scene graphs

Using models to extract triplets describing the composition of art pieces.
Approaches could be any set of these methods:

* Descriptive texts (e.g museums)
* Describing the object with a model and extracting triplets from the descriptions
* Segmenting the object first and using recognition and description capable LLMs

The resulting triplets could be integrated into the existing knowledge graph setup.
It could be sensible to split the scene graphs of to separate items, following the model of [Structured data on Commons (SDC)](https://commons.wikimedia.org/wiki/Commons:Structured_data).

# Model selection

* [BLIP-2](https://huggingface.co/docs/transformers/main/model_doc/blip-2): descriptions
* [SAM](https://github.com/facebookresearch/segment-anything): segmentation