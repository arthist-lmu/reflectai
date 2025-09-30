import pickle
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
from transformers import CLIPModel, CLIPImageProcessor
os.environ['SSL_CERT_FILE']="/nfs/home/ritterd/miniconda3/lib/python3.11/site-packages/certifi/cacert.pem"
from collections import defaultdict

from infer_egtr import calculate_similarity, convert_scene_triplets_to_embedding, convert_kgtriplets_to_embedding, convert_image_to_iconclass_notation, build_triplets_dicted, convert_kgtriplets_to_list, calculate_iconclass_depth

#from plot_egtr import SceneGraphPredictorEGTR
from transformers import BertModel, BertTokenizer
import Levenshtein
from PIL import Image
import PIL
import argparse
from numpy.linalg import norm
import re
import pandas as pd
import random 
import iconclass as iclass
import statistics
try:
    from ollama import Client, _types
    client = Client(
        host='gpu5.research.tib.eu'
    )
except ModuleNotFoundError:
    pass
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer


def concept_recognition(mode='qwen'):
    if mode == 'qwen':
        llm_prompt = 'please show me all the concepts you can see in the image as a simple list. I expect the list to look like ' \
        'this: 1. "Jesus", 2. "Palm", 3. "sky", etc. The concepts are only the terms within the quotation marks. The valid concepts are of the classes: Person, animal, plant, landscape and object. ' \
        'The Persons can be known persons like Jesus or just some unknown person. They can also be mystical person like angels or demons.' \
        'similar to animals and plants. The same goes for objects as well. Finally, please include every concept only once in the list.'
        response = client.chat(model='qwen2.5vl:7b', messages=[
            {
                'role': 'user',
                'content': llm_prompt, 
                "images":  ['/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/image_dataset/iconclass/iconclass/Q1131476.jpg']
            }
            ])
        print(response)
        # from transformers import Qwen2_5_VLForConditionalGeneration, AutoTokenizer, AutoProcessor
        # from qwen_vl_utils import process_vision_info

        # # default: Load the model on the available device(s)
        # # model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        # #     "Qwen/Qwen2.5-VL-32B-Instruct", torch_dtype="auto", device_map="auto"
        # # )

        # # We recommend enabling flash_attention_2 for better acceleration and memory saving, especially in multi-image and video scenarios.
        # model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        #     "Qwen/Qwen2.5-VL-32B-Instruct",
        #     dtype='auto',
        #     attn_implementation="flash_attention_2",
        #     device_map="auto",
        # )

        # # default processer
        # processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-32B-Instruct")

        # # The default range for the number of visual tokens per image in the model is 4-16384.
        # # You can set min_pixels and max_pixels according to your needs, such as a token range of 256-1280, to balance performance and cost.
        # # min_pixels = 256*28*28
        # # max_pixels = 1280*28*28
        # # processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-32B-Instruct", min_pixels=min_pixels, max_pixels=max_pixels)

        # messages = [
        #     {
        #         "role": "user",
        #         "content": [
        #             {
        #                 "type": "image",
        #                 "image": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
        #             },
        #             {"type": "text", "text": "Describe this image."},
        #         ],
        #     }
        # ]

        # # Preparation for inference
        # text = processor.apply_chat_template(
        #     messages, tokenize=False, add_generation_prompt=True
        # )
        # image_inputs, video_inputs = process_vision_info(messages)
        # inputs = processor(
        #     text=[text],
        #     images=image_inputs,
        #     videos=video_inputs,
        #     padding=True,
        #     return_tensors="pt",
        # )
        # inputs = inputs.to("cuda")

        # # Inference: Generation of the output
        # generated_ids = model.generate(**inputs, max_new_tokens=128)
        # generated_ids_trimmed = [
        #     out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        # ]
        # output_text = processor.batch_decode(
        #     generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        # )
        # print(output_text)



def parse_args():
    parser = argparse.ArgumentParser(description="Evaluator module")

    parser.add_argument('-m', '--image', help='The query image')
    parser.add_argument("-d", "--iconclass_depth", help='The minimum depth of the ICONCLASS Tree')
    parser.add_argument("-p", "--property_map", help='The path to the mapping dictionary that maps Wikidata property IDs into the description of it.')
    parser.add_argument("-e", "--entity_map", help='The path to the mapping dictionary that maps Wikidata entity IDs into the description of it.')
    parser.add_argument("--iconclass", action='store_true', help='Whether to evaluate on the ICONCLASS Dataset')
    parser.add_argument("--concepts_only", action='store_true', help='Whether to evaluate only on concepts instead of the whole triplets')
    parser.add_argument("-a", "--allowed_relations", help='List of the allowed relations. NOTE: if you want to use iconclass you have to include the relation like this ["P1257"]', type=list)
    parser.add_argument("-q", "--allowed_qualifiers", help='List of the allowed qualifiers (additional infromation of concepts). Provide a list', type=list)


    parser.add_argument("-t", "--calculate", help="Whether to calculate the embeddings of the KG anew", action='store_true', default=False)
    parser.add_argument("-c", "--checkpoint_path", help="path to checkpoint dir", required=True)
    parser.add_argument("-o", "--output_path", help="path to the output file")
    parser.add_argument("-k", "--kg_dataset_path", help="path to the knowledge graph dataset path", required=True)
    parser.add_argument("-i", "--image_dataset_path", help="path to the image files")
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--data_path", type=str, default="dataset/visual_genome")
    parser.add_argument("-g", "--create_gt", help='Whether to create new Ground-Truths for all queries', action='store_true', default=False)
    parser.add_argument("--created_gt_path", help='Path to the Ground-Truths')
    parser.add_argument('-b', "--baseline", help='The baseline methode', required=True)


    parser.add_argument("--ioq", help='intersect over query')
    parser.add_argument("--ioc", help='intersect over corpus')
    parser.add_argument("--iou", help='intersect over union')
    parser.add_argument("--key", help='whether or not to use keys')
    parser.add_argument("--addendum", help='whether or not to use the additional information')
    parser.add_argument("--abstract", help='How much hihger in the ICONCLASS tree to still count it as a match')
    parser.add_argument("--detailed", help='How much deeper in the ICONCLASS tree to still count it as a match')

    args = parser.parse_args()

    return args


def filter_gt(image, knowledge_graph_dataset_path, triplet_based=False, calculate=True, min_notation_depth=3, ioq=0.0, ioc=0.0, iou=0.0, key=True, addendum=True, abstract=0, detailed=0):
    allowed_qualifiers = ['P518', 'P462']
    allowed_relations = ['P1257'] # iconclass
    iconclass = True
    
    # get the information of the query image
    lst = build_triplets_dicted(knowledge_graph_dataset_path, filter_for_allowed_qualifiers=allowed_qualifiers, allowed_relations=allowed_relations)
    query_image = lst[re.findall('Q\d+\.jpg', image)[0][:-4]]

    concepts = []
    kw = []
    for concept in query_image: 
        if calculate_iconclass_depth(notation=concept[2], with_addendum=True, with_key=True) >= min_notation_depth:
            kw = concept[2]
        if kw:
            concepts.append(kw)
            if ':' in kw:
                kws = kw.split(':')
                concepts.extend(kws)


    # ---------- loading the knowledge graphs from the dataset --------- #

    kg_triplets = convert_kgtriplets_to_list(triplets=lst, iconclass=iconclass, triplet_based=triplet_based, allowed_relations=allowed_relations)
    # with open('/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/filtered_gt.pkl',
    #             'wb') as fp:
    #     pickle.dump(kg_triplets, fp, protocol=pickle.HIGHEST_PROTOCOL)

    taken_q, _ = display_filter_gt(kg_triplets, concepts, with_addendum=addendum, with_key=key, ioc=ioc, ioq=ioq, iou=iou, abstract=abstract, detailed=detailed, min_notation_depth=min_notation_depth)
    corpus_images = [k[1] for k in taken_q]

    return corpus_images
    

def evaluate_search_mrr(results):
    rank = 0 
    for i, result in enumerate(results):
        if result[-1] == 1:
            rank = 1 / (i + 1)

    return rank


def evaluate_search_ap(precision, recall):
    ap = 0
    for i in range(len(precision)):
        delta = recall[i + 1] - recall[i]
        ap += delta * precision[i]
        
    return ap


def evaluate_search_at_k(results, k):
    # p@k - how many of the elements that are ranked within k are actually relevant ? 
    # r@k - how many of the relevant elements are actually within k ?
    assert k > 0

    precision = []
    # start recall with a zero, so that calculateing average precision afterwards is way easier!
    recall = [0]
    tp = 0
    n = len([a for a in results if a[-1] == 1])
    for i, painting in enumerate(results):
        if painting[-1]:
            tp += 1
        r = tp / n if n > 0 else 0.0
        precision.append(tp / (i + 1))
        recall.append(r)
        if i == k:
            break

    return precision, recall


def search(image, checkpoint_path, knowledge_graph_dataset_path,  path_to_created_gt, quantile=0.5, triplet_based=True, image_name=None, calculate=True, baseline='BERT'):
    """
    Evaluation function that calculates the similarity of every scene graph triplet to every knwoledge graph triplet
    """

    # ------- creating SGG -------- #
    ic = iclass.init()
    try:
        if image_name is not None:
            img = image
            img = img.convert("RGB")
            image = image_name
        else:
            img = Image.open(image)
            img = img.convert("RGB")
    except (PIL.Image.DecompressionBombError, PIL.UnidentifiedImageError):
        return list()
    
    # ---------- loading the knowledge graphs from the dataset --------- #
    
    # ---------- create sentance embedding using BERT for SG and KG. Caluclating the similarity using cosine similarity ------- # 

    if calculate:
        # ---------- loading the knowledge graphs from the dataset --------- #
        allowed_qualifiers = ['P518', 'P462']
        allowed_relations = ['P1257']  # iconclass
        iconclass = True
        lst = build_triplets_dicted(knowledge_graph_dataset_path, filter_for_allowed_qualifiers=allowed_qualifiers)

        kg_triplets = convert_kgtriplets_to_list(triplets=lst, iconclass=iconclass, triplet_based=triplet_based,
                                                    allowed_relations=allowed_relations)

        if baseline == 'BERT':
            # ----- load all the necessary models for SGG and Sentence embedding --------- #
            #egtr = SceneGraphPredictorEGTR(config={"device": 'cuda', "artifact_path": checkpoint_path})
            #
            concept_recognition()

            model = BertModel.from_pretrained('bert-base-uncased').to('cuda')
            tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            for corpus_image in kg_triplets.keys():
                notations = kg_triplets[corpus_image]
                notations_final = []
                for notation in notations:
                    try:
                        if ':' in notation:
                            tmp = notation.split(':')
                            notations_final.append(ic[tmp[0]]())
                            notations_final.append(ic[tmp[1]]())
                        else:
                            notations_final.append(ic[notation]())
                    except:
                        pass
                
                kg_triplets[corpus_image] = notations_final

            kg_embeddings, kg_len = convert_kgtriplets_to_embedding(kg_triplets, tokenizer=tokenizer, model=model)
            with open('/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/knwoledge_graph_test_iconclass.pkl',
                        'wb') as fp:
                pickle.dump(kg_embeddings, fp, protocol=pickle.HIGHEST_PROTOCOL)

            with open(
                    '/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/knwoledge_graph_lengths_test_iconclass.pkl',
                    'wb') as f:
                pickle.dump(kg_len, f, protocol=pickle.HIGHEST_PROTOCOL)

        elif baseline == 'vlm':
            # todo: this is fine, since vlm and iconclass classifier take images in and return notations. if iconclass is True
            # kg_triplets is already as needed
            pass 
        elif baseline == 'CLIP':
            pass

    else:
        if baseline == 'BERT':
            with open('knwoledge_graph_test_iconclass.pkl', 'rb') as fp:
                kg_embeddings = pickle.load(fp)

            with open('knwoledge_graph_lengths_test_iconclass.pkl', 'rb') as fp:
                kg_len = pickle.load(fp)

        elif baseline == 'CLIP':
            with open('/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/clip_embeddings.pkl', 'rb') as fp:
                kg_embeddings = pickle.load(fp)

    # at this point: the correct gt needs to be loaded
    with open(path_to_created_gt, 'rb') as fp:
        filtered_gt = pickle.load(fp)

    #print(filtered_gt[0] == re.search('Q\d+\.jpg', image).group()[:-4])
    results = []
    if baseline == 'BERT':
        # todo: this will be changed to a object detector later
        output = egtr(img)
        triplets = []
        for a in output['triplets']:
            triplets.append((a['subject'], a['predicate'], a['object']))

        for kg in kg_embeddings:
            scene_embeddings = convert_scene_triplets_to_embedding(model=model, tokenizer=tokenizer, triplets=triplets, padding=kg_len[kg], triplet_based=triplet_based)
            if scene_embeddings and kg_embeddings[kg]['embedding']:
                trip_sims, total_sim = calculate_similarity(scene_embeddings, kg_embeddings[kg]['embedding'], quantile=quantile)
                y = 0 
                if kg in filtered_gt[re.findall('Q\d+\.jpg', image)[0][:-4]]:
                    y = 1

                results.append((kg, trip_sims, total_sim, y))
                results = sorted(results, key=lambda x: x[-2], reverse=True)
    elif baseline == 'vlm':
        q_notations = convert_image_to_iconclass_notation(img, model=baseline)
        for corpus_image, c_notations in kg_triplets.items():

            dct = close_range_calculation(query=q_notations, corpus=c_notations)
            for query_concept, corpus_concepts in dct.items():
                most_fitting_score = 0
                most_fitting_concept = ''
                trip_sims = []
                for c_concept in corpus_concepts:
                    if most_fitting_score <= Levenshtein.ratio(query_concept, c_concept):
                        most_fitting_concept = c_concept
                        most_fitting_score = Levenshtein.ratio(query_concept, c_concept)
                    
                trip_sims.append((most_fitting_score, query_concept, most_fitting_concept))
            # --------------------------------for now this is the very easy method ---------------------------------
            total_sim = statistics.mean([similarity[0] for similarity in trip_sims])
            #-------------------------------------------------------------------------------------------------------
            y = 0 
            if corpus_image in filtered_gt[re.findall('Q\d+\.jpg', image)[0][:-4]]:
                y = 1
            results.append((corpus_image, trip_sims, total_sim, y))
            results = sorted(results, key=lambda x: x[-2], reverse=True)   
    elif baseline == 'CLIP':
        #if os.path.getsize(args.image_dataset_path + '/' + painting) >= 50000000:
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to('cuda')
        processor = CLIPImageProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        inputs = processor(images=image, return_tensors='pt')
        clip_embedding = model.get_image_features(**inputs.to('cuda'))
        i = 0
        print(image)
        print(os.path.dirname(image))
        for corpus_image in os.listdir(os.path.dirname(image)):     
            print(i)
            try:
                inputs = processor(images=f'{os.path.dirname(image)}/{corpus_image}', return_tensors='pt')
                corpus_embedding = model.get_image_features(**inputs.to('cuda'))

                sim = cosine_similarity(clip_embedding.cpu().detach().numpy(), corpus_embedding.cpu().detach().numpy())
                y = 0 
                if re.findall('Q\d+\.jpg', corpus_image)[0][:-4] in filtered_gt[re.findall('Q\d+\.jpg', image)[0][:-4]]:
                    y = 1
                results.append((corpus_image[:-4], sim, y))
                i+=1
            except (PIL.Image.DecompressionBombError, PIL.UnidentifiedImageError):
                continue
        results = sorted(results, key=lambda x: x[-2], reverse=True)

    # sanity check: since there is no possible way that the artwork itself can be regarded as irrelevant (y=0) you could only check for its position (and sim-value) in this list
    for i, result in enumerate(results):
        if result[0] == re.search('Q\d+\.jpg', image).group()[:-4]:
            print(i, result)

    return results


def compare_iconclass_depths(concept, c_concept, with_key=False, with_addendum=False):
    i = 0
    j = 0
    bracket_open = False
    valid_key = False
    valid_addendum = False
    is_key = False
    # if size of c_concept exceeds: keep counting while j is in range
    #case: with key and with addendum
    while len(concept) > i and len(c_concept) > i and concept[i] == c_concept[i]:
        if concept[i] == ')':
            bracket_open = False
            valid_key = False
            valid_addendum = False
        elif bracket_open:
            if with_key:
                if concept[i] == '+' or valid_key:
                    j += 1
                    valid_key = True
            if with_addendum:
                if (concept[i] != '+' or valid_addendum) and not is_key:
                    j += 1
                    valid_addendum = True
                else:
                    is_key = True

        elif concept[i].isalnum():
            j += 1
        elif concept[i] == '(':
            bracket_open = True

        i += 1

    return j


def close_range_calculation(query, corpus, abstract=2, detailed=2, with_key=False, with_addendum=False,
                            min_notation_depth=3):
    accepted_concepts = defaultdict(list)
    for concept in query:
        # this makes sure that every concept is stored as a key
        accepted_concepts[concept]
        for c_concept in corpus:
            j = compare_iconclass_depths(concept, c_concept, with_key, with_addendum)
            # 1. is not too detailed; or 2. simply not too abstract;
            if ((calculate_iconclass_depth(concept) == j and calculate_iconclass_depth(c_concept) <= j + detailed
                    or calculate_iconclass_depth(concept) - abstract <= j and calculate_iconclass_depth(c_concept) == j)
                    and calculate_iconclass_depth(c_concept, with_key, with_addendum) >= min_notation_depth):
                accepted_concepts[concept].append(c_concept)

    return accepted_concepts


def intersection_over(intersection1, intersection2=None):
    if intersection2 is None:
        n = len(intersection1.keys())
        r = len([k for k, l in intersection1.items() if l]) / n if n > 0 else 0.0
        return r, -1
    else:
        #todo if there is no key: get rid of those to avoid having too many union entries
        all_concepts1 = set(intersection1.keys())
        all_concepts2 = set(intersection2.keys())
        found_concepts1 = set([k for k, l in intersection1.items() if l])
        found_concepts2 = set([k for k, l in intersection2.items() if l])

        found_union = found_concepts1 | found_concepts2
        all_union = all_concepts1 | all_concepts2

        found_intersect = found_concepts1 & found_concepts2
        all_intersect = all_concepts1 & all_concepts2

        n_all = len(all_union)
        n_found = len(found_union)
        r_all = len(all_intersect) / n_all if n_all > 0 else 0.0
        r_found = len(found_intersect) / n_found if n_found > 0 else 0.0

        return (r_all, all_intersect, all_union), (r_found, found_intersect, found_union)


def display_filter_gt(gt, concepts, with_key, with_addendum, ioq, ioc, iou, abstract, detailed, min_notation_depth, sort_by='query'):
    # This functions gets the concepts as input parameter instead of loading all of them itself
    concepts = set(concepts)
    taken_q = []
    taken_c = []

    for k, v in gt.items():
        #------- split ':' cases into three ---------#
        for concept in v:
            if ':' in concept:
                v.extend(concept.split(':'))
        #--------------------------------------------#
        v = set(v)
        if v and concepts:
            intersection_q = close_range_calculation(concepts, v, abstract=abstract, detailed=detailed,
                                                     with_key=with_key, with_addendum=with_addendum,
                                                     min_notation_depth=min_notation_depth)
            intersection_c = close_range_calculation(v, concepts, abstract=abstract, detailed=detailed,
                                                     with_key=with_key, with_addendum=with_addendum,
                                                     min_notation_depth=min_notation_depth)


            i_o_q, _ = intersection_over(intersection_q)
            i_o_c, _ = intersection_over(intersection_c)
            i_o_u_all, i_o_u_found = intersection_over(intersection_c, intersection_q)


            taken_q.append(('query_image', k, concepts, v, intersection_q, i_o_q, i_o_c, i_o_u_all))

            taken_c.append(('query_image', k, concepts, v, intersection_c, i_o_q, i_o_c, i_o_u_all))


    if 'query' in sort_by:
        by = 5
    elif 'corpus' in sort_by:
        by = 6
    else:
        by = 7


    # todo: nicht an dieser STelle, aber die Berechnung von IOU ist falsch, da sie keys und so weiter untescheidet, wodurch andere Zahlen zustande kommen
    taken_q = [pick for pick in taken_q if pick[5] >= ioq]
    taken_q = [pick for pick in taken_q if pick[6] >= ioc]
    #todo hier muss ich mal einen weg finden wie ich die iou speichere; brauche ich wirklich die einzelnen gefundenen notationen
    taken_q = [pick for pick in taken_q if pick[7][0] >= iou]

    taken_c = [pick for pick in taken_c if pick[5] >= ioq]
    taken_c = [pick for pick in taken_c if pick[6] >= ioc]

    taken_c = [pick for pick in taken_c if pick[7][0] >= iou]

    taken_q.sort(key=lambda x: x[by], reverse=True)
    taken_c.sort(key=lambda x: x[by], reverse=True)

    return taken_q, taken_c


if __name__ == '__main__':
    args = parse_args()
    # checkpoint path
    "egtr__pretrained_detr__SenseTime__deformable-detr__batch__32__epochs__150_50__lr__1e-05_0.0001__visual_genome__finetune__version_0/batch__64__epochs__50_25__lr__2e-07_2e-06_0.0002__visual_genome__finetune/version_0"
    # image dataset path
    '/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/image_dataset/images'
    # knowledge graph dataset path
    '/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/triplets_with_qualities_on_experimental.pkl'
    '/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/triplets_with_iconclass.pkl '
    # 
    '/nfs/data/reflectai/wikidata_image_dataset/full_wikidata_iconclass'
    '/nfs/data/reflectai/wikidata_image_dataset/full_wikidata_iconclass/Q12418.jpg'
    # "--iconclass_depth", help='The minimum depth of the ICONCLASS Tree')
    # add_argument("-p", "--property_map", help='The path to the mapping dictionary that maps Wikidata property IDs into the description of it.')
    # add_argument("-e", "--entity_map", help='The path to the mapping dictionary that maps Wikidata entity IDs into the description of it.')
    # parser.add_argument("--iconclass", action='store_true', help='Whether to evaluate on the ICONCLASS Dataset')
    # parser.add_argument("--concepts_only", action='store_false', help='Whether to evaluate only on concepts instead of the whole triplets')
    # parser.add_argument("-a", "--allowed_relations", help='List of the allowed relations. NOTE: if you want to use iconclass you have to include the relation like this ["P1257"]', type=list)
    # parser.add_argument("-q", "--allowed_qualifiers", help='List of the allowed qualifiers (additional infromation of concepts). Provide a list', type=list)

    #print(len(os.listdir('/nfs/data/reflectai/wikidata_image_dataset/full_wikidata_iconclass')))

    if args.create_gt:
        taken = defaultdict(list)
        for image in os.listdir(args.image_dataset_path):
            taken[image[:-4]] = filter_gt(image, args.kg_dataset_path, calculate=True, triplet_based=False, ioq=args.ioq, ioc=args.ioc, iou=args.iou, key=args.key, addendum=args.addendum, abstract=args.abstract, detailed=args.detailed)

        #'/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/filtered_gt_for_each_query_1619_easyusecase_ioc0.5_ioq0.0_iou0.0.pkl'
        with open(args.created_gt_path, 'wb') as fp:
            pickle.dump(taken, fp, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open(args.created_gt_path, 'rb') as fp:
            taken = pickle.load(fp)


    if args.image:
        path_to_input_image = args.image
        results  = search(path_to_input_image, args.checkpoint_path, args.kg_dataset_path, args.created_gt_path, triplet_based=False, calculate=args.calculate)
        p, r = evaluate_search_at_k(results, 100) 
    else:
        dct = defaultdict(list)
        aps = [] 
        ranks = []
    
        with open('query_images.pkl', 'rb') as fp:
            query_images = pickle.load(fp)

        for i, painting in enumerate(query_images):
            path_to_input_image = f'{args.image_dataset_path}/{painting}.jpg'
            results = search(path_to_input_image, args.checkpoint_path, args.kg_dataset_path, args.created_gt_path, triplet_based=False, calculate=args.calculate, baseline=args.baseline)
            print(results)
            p, r = evaluate_search_at_k(results, 30) 
            if p: 
                ap = evaluate_search_ap(p, r)
                ranks.append(evaluate_search_mrr(results))
                aps.append(ap)
                dct[painting[:-4]].extend([statistics.mean(p), ap])
                mrr_update = statistics.mean(ranks)
                map_update = statistics.mean(aps)
                dct['mAP'] = [map_update]
                dct['MRR'] = [mrr_update]
                df = pd.DataFrame.from_dict(dct, orient='index')
                df.to_csv('./current_results.csv')


        if aps:
            mrr = statistics.mean(ranks)
            map = statistics.mean(aps)
            
            dct['mAP'] = [map]
            dct['MRR'] = [mrr]
            print(dct)
            df = pd.DataFrame.from_dict(dct, orient='index')
            df.to_csv(args.output_path)
    # elif False:

    #     with open(args.created_gt_path, 'rb') as fp:
    #         filtered_gt = pickle.load(fp)

    #     model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    #     processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")
    #     results = []
    #     for i, painting in enumerate(os.listdir(args.image_dataset_path)):
    #         try:
                
    #             if os.path.getsize(args.image_dataset_path + '/' + painting) >= 50000000:
                    
    #                 inputs = processor(images=args.image_dataset_path + '/' + painting, return_tensors='pt')
    #                 print(args.image_dataset_path + '/' + painting)
    #                 print(os.path.getsize(args.image_dataset_path + '/' + painting))
    #                 clip_embedding = model.get_image_features(**inputs)
    #                 i = 0
    #                 for corpus_image in os.listdir('/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/image_dataset/iconclass/iconclass'):     
    #                         inputs = processor(images=f'/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/image_dataset/iconclass/iconclass/{corpus_image}', return_tensors='pt')
    #                         corpus_embedding = model.get_image_features(**inputs)
    #                         sim = cosine_similarity(clip_embedding.detach().numpy(), corpus_embedding.detach().numpy())
    #                         y = 0 
    #                         if re.findall('Q\d+\.jpg', corpus_image)[0][:-4] in filtered_gt[re.findall('Q\d+\.jpg', args.image_dataset_path + '/' + painting)[0][:-4]]:
    #                             y = 1
    #                         results.append((corpus_image[:-4], sim, y))
    #                         #print(i)
    #                         i+=1
    #         except (PIL.Image.DecompressionBombError, PIL.UnidentifiedImageError):
    #             continue
    #         results = sorted(results, key=lambda x: x[-2], reverse=True)
    #         print(painting)
    #         print(results)
    #         results = []

    # cnt = 0
    # for image in os.listdir(args.image_dataset_path):
        
    #     try:
    #         if os.path.getsize(args.image_dataset_path + '/' + image) >= 50000000:
    #             cnt +=1
    #         #print(Image.open(args.image_dataset_path + '/' + image).size)
    #     except (PIL.Image.DecompressionBombError, PIL.UnidentifiedImageError):
    #         continue
    # print(cnt)
