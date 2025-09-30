import pickle
import json
import numpy as np
import os
os.environ['SSL_CERT_FILE']="/nfs/home/ritterd/miniconda3/lib/python3.11/site-packages/certifi/cacert.pem"
from collections import defaultdict
#import gradio as gr
import streamlit as st
from streamlit.runtime.media_file_storage import MediaFileStorageError
from infer_egtr import calculate_similarity, convert_scene_triplets_to_embedding, create_scene_graph
from plot_egtr import SceneGraphPredictorEGTR
from Evaluator import search
from transformers import BertModel, BertTokenizer
from PIL import Image
import io
import zipfile



def image_based_query_old(image, quantile):
    triplets = create_scene_graph(image, True)
    result = []
    if len(triplets) > 0:
        model = BertModel.from_pretrained('bert-base-uncased')
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        matching = []
        with open('knwoledge_graph_test.pkl', 'rb') as fp:
            arrays = pickle.load(fp)
        
        with open('/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/knwoledge_graph_lengths_test.pkl', 'rb') as fp:
            lengths = pickle.load(fp)

        
        for kg in arrays.keys():
            scene_graph = convert_scene_triplets_to_embedding(triplets, model, tokenizer, lengths[kg])
            wikidata_code = fetch_key_from_value(kg)
            if wikidata_code != -1:
                sim_trips, sim_score = calculate_similarity(scene_graph, arrays[kg]['embedding'], quantile)
                
                if len(sim_trips) > 0:
                    tup = (sim_trips[0], sim_trips[1], kg, sim_score)
                    result.append(tup)

    result = sorted(result, key=lambda x: x[3], reverse=True)
    reason = ''
    for r in result:
        matching.append(fetch_key_from_value(r[2]))
        reason += f"Artwork {r[2]}: Triplets: {r[0]} match with score: {r[3]}\n"

    corresponding_images = []
    for image_name in matching:
            corresponding_images.append(fr'/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/image_dataset/images/{image_name}.jpg')

    for a in result:
        print(f'Artwork: {r[2]}; Score: {r[3]}\n\t {r[0]}, {r[1]}\n')


    return corresponding_images, reason


def fetch_key_from_value(val):
    with open('triples_with_label.json', 'r', encoding='utf-8') as fp:
        triplets = json.load(fp)

    for key, value in triplets.items():
        for v in value:
            try:
                if v['label'] == val:
                    return key
            except KeyError:
                continue

    return -1


def image_based_query(image, knowledge_graph_dataset, quantile, image_name, calculate=False, checkpoint="egtr__pretrained_detr__SenseTime__deformable-detr__batch__32__epochs__150_50__lr__1e-05_0.0001__visual_genome__finetune__version_0/batch__64__epochs__50_25__lr__2e-07_2e-06_0.0002__visual_genome__finetune/version_0"):
    # list of tuples that have the picture in first position, list of ranked triplets in second and total rank in last position

    result = search(image, checkpoint_path=checkpoint, knowledge_graph_dataset_path=knowledge_graph_dataset, quantile=quantile, image_name=image_name, calculate=calculate, triplet_based=False)


    result = [a for a in result if a[0] + '.jpg' in os.listdir('/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/image_dataset/iconclass/iconclass/')]
    

    return result


st.set_page_config(layout='wide')
with st.container():
    row_cols = [col for col in st.columns(3)]
    with row_cols[0]:
        query_image = st.file_uploader('Query image', type='jpg')
        
        if query_image:
            st.image(query_image, use_container_width=False, width=300)
            image_name = query_image.name
            query_image = io.BytesIO(query_image.getvalue())
            egtr_input = Image.open(query_image)
    with row_cols[1]:
        qunatile = st.slider('Qunatile', min_value=0.0, max_value=1.0, step=0.1, value=0.5)
        calculate = st.checkbox('Please check this box if you want to re-calculate the dataset embeddings. Leave it unchecked if you want to load pre-calculated dataset embeddings!')
    with row_cols[2]:
        kg_dataset = st.file_uploader('KG dataset', type=['zip'])

if st.button(label='Query', use_container_width=True, type='primary'):
    try: 
        with zipfile.ZipFile(kg_dataset) as zipf:
            dataset = zipf.namelist()[0]

        resul_images = image_based_query(egtr_input, dataset, quantile=qunatile,  image_name=image_name, calculate=calculate,)
    except (AttributeError, NameError) as e:
        st.write('please provide all the necessary inputs!')
        st.write(e)
    else:
        n_cols = 6

        # experimental
        show_n_triplets = 5
        cut_off = 30

        cols = [col for col in st.columns(n_cols)]
        height = 500
        for i, image in enumerate(resul_images):
            if i == cut_off:
                break
            with cols[i % n_cols]:
                with st.container(height=height):
                    try:
                        # think about a way to make the image paths variable  
                        st.image(fr'/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/image_dataset/iconclass/iconclass/{image[0]}.jpg', use_container_width=True)
                        st.metric(label=f'metric{i}', value=image[2], label_visibility='hidden')
                                 
                    except (FileNotFoundError, MediaFileStorageError):
                        # das passiert noch, weil für die neuen Datensätze nicht immer alle Bilder zur verfügung stehen
                        continue
                    except Exception as e:
                        raise e

                    for j, trip in enumerate(image[1]):
                        st.write(trip)
                        if j == show_n_triplets:
                            break
