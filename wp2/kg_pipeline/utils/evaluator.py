from typing import List, Dict, Generator
import json
import pandas as pd
from kg_pipeline.manager import Manager
from difflib import SequenceMatcher
from kg_pipeline.plugin import Plugin
from ollama import Client, _types
import re
from collections import defaultdict
import itertools


client = Client(
  host='devbox2.research.tib.eu'
)

#----------------------------------------------------------------#
# This is to count the predicates despite them beeing different but ought to mean the same 
equal_predicates = {'depicts': ['depicts', 'symbolizes', 'contains', 'has_characteristic'], 
                    'created_in': ['created_in', 'created_by'], 
                    'contains': ['contains', 'depicts'], 
                    'symbolizes': ['symbolizes', 'depicts'], 
                    'has_characteristic': ['has_characteristic', 'depicts'], 
                    'created_by': ['created_in', 'created_by', 'influenced_by']}
#-----------------------------------------------------------------#

# -------------------- utility functions --------------------------------------#

def convert_annotation_to_triplet(annotation):
    triplets = []
    for s, po in annotation.items():
        entry = {}
        s_class = annotation[s]['s_class_name']
        for p, o in po.items():
            oo = o[0]
            if type(o[0]) != list:
                oo = [o[0]]
            
            for i, obj in enumerate(oo):

                if p != 's_class_name':
                    if type(o[1]['o_class_name']) != list:
                        o_class = o[1]['o_class_name']
                    else:
                        o_class = o[1]['o_class_name'][i]
                    entry = {'triplet': {'subject':s, 'predicate': p, 'object': obj, 'o_class':o_class, 's_class': s_class}}
                    triplets.append(entry)
    
    return triplets


def detailed_storage(key, dct, s_tp_flag):
    if key in dct.keys():
        if s_tp_flag:
            dct[key]['tp'] += 1

        dct[key]['total_pre'] += 1

    else:
        if s_tp_flag:
            stp = 1
        else:
            stp = 0


        entry = dict(tp = stp,
                    total_pre = 1,
        )

        dct.update({key:entry})
    
    return dct


def remove_entry(remove, structure, mode='single'):
    structure.update({remove:1})
    return structure


def calculate_metrics_detailed(pred_dict, pos_dict, mode='class', with_n=True, full_dict=False):
    results = {}
    if mode == 'class':
        for key, values in pred_dict.items():
            s_tp = values['tp']
            s_total_pre = values['total_pre']

            if key in pos_dict.keys():
                s_total_pos = pos_dict[key]
            else:
                s_total_pos = 0
             
            s_precision = s_tp / s_total_pre if s_total_pre > 0.0 else 0.0
            s_recall = s_tp / s_total_pos if s_total_pos > 0.0 else 0.0
            s_f1_score = 2 * s_precision * s_recall / (s_precision + s_recall) if (s_precision + s_recall) > 0.0 else 0.0
    
            
            if with_n:
                scores = [s_f1_score, s_precision, s_recall, s_total_pre, s_total_pos]
            else:
                scores = [s_f1_score, s_precision, s_recall]

            results.update({key: scores})

        # include all the classes that have not been found but could have been found
        if full_dict:
            for gt_key in pos_dict.keys():
                if gt_key not in results.keys():
                    if with_n:
                        scores = [0, 0, 0, 0, pos_dict[gt_key]]
                    else:
                        scores = [0, 0, 0]

                    results.update({gt_key: scores})

    return results


def calculate_metrics(s_tp, s_total_pre, s_total_pos, printing=False):
    s_precision = s_tp / s_total_pre if s_total_pre > 0.0 else 0.0
    s_recall = s_tp / s_total_pos if s_total_pos > 0.0 else 0.0
    s_f1_score = 2 * s_precision * s_recall / (s_precision + s_recall) if (s_precision + s_recall) > 0.0 else 0.0

    if printing:
        print()
        print('Total results:')
        print('total subject F1 Score: ', s_f1_score,)
        print('total subject Precision: ', s_precision,)
        print('total subject Recall: ', s_recall,)
    
    col = ['Entire Testset']
    subject_scores = pd.DataFrame.from_dict(data={'F1': s_f1_score, 'Precicision': s_precision, 'Recall': s_recall}, orient='index', columns=col).T
    
    return subject_scores


def llm_query(predictions, save_path, mode='soft'):
    try:
        with open(save_path, 'r', encoding='utf-8') as fp:
            mitschrift = json.load(fp)
    except:
        mitschrift = {}
    
    if mode == 'soft':
        llm_prompt = 'In the context of paintings, do the terms "{}" and "{}"' \
        'semantically describe the same thing? Note that the terms can refer to artists, eras, materials, art styles, depictions, or other' \
        'art-related terms. Also note that subcategories are to be equated with the corresponding supercategories. The same is to be considered if one term is an instance of the other term. Furthermore,' \
        'plural forms and singular forms are to be equated. Terms are also to be equated if core terms such as “The Lady, A Hunter'\
        'or A House” are included in one term and further described in the other term. Answer with only yes and no.'
    elif mode == 'hard':
         llm_prompt = 'In the context of paintings, do the terms "{}" and "{}"' \
        'semantically describe the same thing? Note that both terms should only be equal if they are either exactly the same or '\
        'are in plural/singular form. Furthermore slight variations like one of the terms including information while the other does not. e.g. the first name of a person or the full name of a location.'\
        'This also includes cases in where one term uses punctuation marks like an apostrophe while the other does not or in cases where the one term is the abbreviation of the other. They are also equal,' \
        'when one term uses article and such.'\
        'It should not be equal e.g. if one of the terms includes more information than just stated or if one term is a subcategory or instance of the other term. Answer only with yes and no.'

    try:
        response = client.chat(model='qwen3:14b', messages=[
            {
                'role': 'user',
                'content': llm_prompt.format(predictions[0].lower(), predictions[1].lower()),
            },
            ])

    except _types.ResponseError as e: 
        print('Due to response Error "', e, '" the semantical filter LLM is not used!')
        return predictions

    resp = response['message']['content'].lower()
    mitschrift.update({f"{predictions[0].lower()}, {predictions[1].lower()}, {mode}" : resp})
    with open(save_path, 'a', encoding='utf-8') as fp:
       json.dump(mitschrift, fp, indent=4, ensure_ascii=False)

    end = re.search('</think>', resp).end()
    return resp[end:]


def calculate_metrics_df(pred_classes_dict, gt_classes_dict, save_path, save_types, type_prediction, amounts=True, save_gt=None, save_pred=None):

    class_eval = calculate_metrics_detailed(pred_classes_dict, gt_classes_dict, mode='class')
    class_df = pd.DataFrame.from_dict(data=class_eval, orient='index', columns=['F1', 'precision', 'recall', 'N_pred', 'N_gt'])
    class_df.to_csv(save_path)

    if len(type_prediction) != 0:
        type_prediction_df = pd.DataFrame.from_dict(data=type_prediction, orient='index')
        type_prediction_df["procentage"] = type_prediction_df['found'] / type_prediction_df['existing']
        type_prediction_df.to_csv(save_types)
    
    if amounts:
        gt_df = pd.DataFrame.from_dict(data=gt_classes_dict, orient='index', columns=['gt'])
        #gt_df.to_csv(save_gt)
        print(gt_df)

        pred_df = pd.DataFrame.from_dict(data=pred_classes_dict, orient='index')
        print(pred_df)
        pred_df = pred_df.merge(gt_df, how='right', left_index=True, right_index=True)
        pred_df.to_csv(save_pred)




def count_type_accuracy_block(tup, pred, type_prediction, a):
    if tup[a] == pred[1]:
        type_prediction[tup[a]]['found'] += 1
        type_prediction[tup[a]]['existing'] += 1
    else:
        type_prediction[tup[a]]['existing'] += 1
    
    return type_prediction


def count_type_accuracy(tup, pred, type_prediction, single):
    if single == '':
        pred = pred[0]
        type_prediction = count_type_accuracy_block(tup, pred, type_prediction, 1)
    else:
        s_pred = pred[0]
        o_pred = pred[1]
        type_prediction = count_type_accuracy_block(tup, s_pred, type_prediction, 2)
        type_prediction = count_type_accuracy_block(tup, o_pred, type_prediction, 3)
    
    return type_prediction


def determine_ollama_candidate(candidate1, candidate2):
    ratio = SequenceMatcher(lambda x: x==' ', candidate1, candidate2).ratio()
    if ratio >= 0.5:
        return True
    
    longer = candidate1
    shorter = candidate2
    if len(candidate1) < len(candidate2):
        longer = candidate2
        shorter = candidate1

    return shorter in longer


#-------------------------------------------------------------------------------#


#---------------- evaluates the metrics for the entire dataset -----------------#
def prepare_data_total(reference, eval, predictions):
    if eval == 'subject':
        reference = [(triplet['triplet']['subject'].lower(),) for triplet in reference]
        reference = list(set(reference))
        predictions = [(triplet['subject']['label'].lower(),) for triplet in  predictions]
        predictions = list(set(predictions))

    elif eval == 'object':
        reference = [(triplet['triplet']['object'].lower(), ) for triplet in reference]
        reference = list(set(reference))
        predictions = [(triplet['object']['label'].lower(),) for triplet in  predictions]
        predictions = list(set(predictions))
    
    elif eval == 'subject_object':
        reference = [(triplet['triplet']['subject'].lower(), triplet['triplet']['object'].lower(), triplet['triplet']['s_class'], triplet['triplet']['o_class']) for triplet in reference]
        seen = set()
        reference = [(a, b, c, d) for a, b, c, d in reference if not ((a, b) in seen or seen.add((a, b)))]
        predictions = [(triplet['subject']['label'].lower(), triplet['object']['label'].lower(), triplet['subject']['s_class'], triplet['class_name']) for triplet in predictions]
        predictions.sort()
        seen = set()
        predictions = [(a, b, c, d) for a, b, c, d in predictions if not ((a, b) in seen or seen.add((a, b)))]
    
    elif eval == 'subject_object_predicate':
        reference = [(triplet['triplet']['subject'].lower(), triplet['triplet']['predicate'], triplet['triplet']['object'].lower(), triplet['triplet']['s_class'], triplet['triplet']['o_class']) for triplet in reference]
        seen = set()
        reference = [(a, b, c, d, e) for a, b, c, d, e in reference if not ((a, b, c) in seen or seen.add((a, b, c)))]
        predictions = [(triplet['subject']['label'].lower(), triplet['relation']['label'], triplet['object']['label'].lower(), triplet['subject']['s_class'], triplet['class_name']) for triplet in  predictions]
        predictions.sort()
        seen = set()
        predictions = [(a, b, c, d, e) for a, b, c, d, e in predictions if not ((a, b, c) in seen or seen.add((a, b, c)))]

    return reference, predictions


def evaluate_total(reference, eval, mode, llm_log_path, trips, found, tp):
    if eval in ('subject', 'object'):
        pred = trips
        tp, found = mode_specific_counting_total(pred=(pred, ), reference=reference, llm_log_path=llm_log_path, mode=mode, found=found, single='', tp=tp)
    elif eval == 'subject_object':
        s_pred = (trips[0], trips[2])
        o_pred = (trips[1], trips[3])
        tp, found = mode_specific_counting_total(pred=(s_pred, o_pred), reference=reference, llm_log_path=llm_log_path, mode=mode, found=found, single='c', tp=tp)
    elif eval == 'subject_object_predicate':
        s_pred = (trips[0], trips[3])
        o_pred = (trips[2], trips[4])
        p_pred = trips[1]
        tp, found = mode_specific_counting_total(pred=(s_pred, o_pred, p_pred), reference=reference, llm_log_path=llm_log_path, mode=mode, found=found, single='p', tp=tp)         

    return tp, found


def calc_word_distance_total(reference, pred, found, tp, single):
    if single == '':
        pred = pred[0]
        candidate = ('', 0)
        for tup in reference:
            ratio = SequenceMatcher(lambda x: x==' ', pred[0], tup[0]).ratio() 
            if ratio > 0.75:  # assuming that the string are similar enough
                if candidate[1] < ratio:
                    candidate = (tup[0], ratio)
                    saved_tup = tup

        if candidate[0] != ''  and found.get(saved_tup) is None:  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
            tp += 1
            found = remove_entry(remove=saved_tup, structure=found)

    elif single == 'c':
        s_pred = pred[0]
        o_pred = pred[1]
        candidate = ('', 0)
        saved_tups = []
        for tup in reference:
            ratio = SequenceMatcher(lambda x: x==' ', s_pred[0], tup[0]).ratio() 
            if ratio > 0.75 and found.get(tup) is None:  # assuming that the string are similar enough
                saved_tups.append(tup)
    
        for saved_tup in saved_tups:  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
            ratio = SequenceMatcher(lambda x: x==' ', o_pred[0], saved_tup[1]).ratio() 

            if ratio > 0.75 and found.get(saved_tup) is None:  # assuming that the string are similar enough 
                tp += 1
                found = remove_entry(remove=saved_tup, structure=found, mode='multiple')
                break

    elif single == 'p':
        s_pred = pred[0]
        o_pred = pred[1]
        p_pred = pred[2]
        candidate = ('', 0)
        saved_tups = []
        for tup in reference:
            ratio = SequenceMatcher(lambda x: x==' ', s_pred[0], tup[0]).ratio() 
            if ratio > 0.75 and found.get(tup) is None:  # assuming that the string are similar enough
                saved_tups.append(tup)
        
        for saved_tup in saved_tups:  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
            ratio = SequenceMatcher(lambda x: x==' ', o_pred[0], saved_tup[1]).ratio() 
            if ratio > 0.75 and p_pred == saved_tup[1] and found.get(saved_tup) is None:  # assuming that the string are similar enough 
                p_tp += 1
                found = remove_entry(remove=saved_tup, structure=found, mode='multiple')
                break

    return tp, found


def calc_perfect_total(reference, pred, found, tp, single):
    if single == '':
        pred = pred[0]
        for tup in reference:
            if tup[0] == pred[0] and found.get(tup) is None:
                tp += 1
                found = remove_entry(remove=tup, structure=found)
                break

    elif single == 'c':
    # count up with perfect matches
        s_pred = pred[0]
        o_pred = pred[1]
        for tup in reference:
            if tup[0] == s_pred and found.get(tup) is None:
                if tup[1] == o_pred:
                    tp += 1
                    found = remove_entry(remove=tup, structure=found, mode='multiple')
                    break

    elif single == 'p':
        s_pred = pred[0]
        o_pred = pred[1]
        p_pred = pred[2]
        for tup in reference:
            if tup[0] == s_pred and found.get(tup) is None:
                if tup[2] == o_pred:
                    if tup[1] == p_pred:
                        tp += 1
                        found = remove_entry(remove=tup, structure=found, mode='multiple')
                        break

    return tp, found


def calc_ollama_total(reference, pred, llm_log_path, mode, found, tp, single):
    if single == '':
        for tup in reference:
            if 'y' in llm_query((pred[0], tup[0]), llm_log_path, mode) and found.get(tup) is None: # '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt.json'
                tp += 1
                found = remove_entry(remove=tup, structure=found)
                break

    elif single == 'c':
        # count up with llm prompts (soft cut)
        s_pred = pred[0]
        o_pred = pred[1]
        for tup in reference:
            if 'y' in llm_query((s_pred, tup[0]), llm_log_path, mode) and found.get(tup) is None: #'/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt.json'
                if 'y' in llm_query((o_pred, tup[1]), llm_log_path, mode):
                    tp += 1
                    found = remove_entry(remove=tup, structure=found)
                    break

    elif single == 'p':
        s_pred = pred[0]
        o_pred = pred[1]
        p_pred = pred[2]
        # count up with llm prompts (hard cut)
        for tup in reference:
            if found.get(tup) is None and determine_ollama_candidate(s_pred[0], tup[0]) and 'y' in llm_query((s_pred, tup[0]), llm_log_path, mode): #'/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt_prädikat.json'
                if determine_ollama_candidate(o_pred[0], tup[2]) and 'y' in llm_query((o_pred, tup[2]), llm_log_path, mode):
                    # since the predicates are hardcoded there is no need for the llm
                    if tup[1] == p_pred:  
                        tp += 1
                        found = remove_entry(remove=tup, structure=found, mode='multiple')
                        break

    return tp, found


def mode_specific_counting_total(pred, reference, llm_log_path, mode, found, single, tp):
    if mode == 'word_distance':
        tp, found = calc_word_distance_total(reference, pred, found, tp, single)
    
    elif mode == 'perfect':
        tp, found = calc_perfect_total(reference, pred, found, tp, single)
            
    elif mode == ('hard', 'soft'):
        tp, found = calc_ollama_total(reference, pred, llm_log_path, mode, found, tp, single)

    return tp, found


def eval_accuracy_total(text_entries, save_path, mode='word_distance', llm_log_path=None, eval='subject'):
    # evaluates the correctly found subjects only one of the three modes can be True
    tp = total_pos = total_pre = 0
    found = {}

    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference, predictions_['content'] = prepare_data_total(reference, eval, predictions_['content'])

            #------- count the counter variables up ---------#
            total_pos += len(reference)
            
            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                total_pre += 1
                tp, found = evaluate_total(reference=reference, eval=eval, mode=mode, llm_log_path=llm_log_path, found=found, trips=trips, tp=tp)

    # ------------- calculate metrics -------------#
    scores = calculate_metrics(tp, total_pre, total_pos)
    scores.to_csv(save_path) 


def eval_accuracy_total_triplets(text_entries, save_path, mode='perfect', eval='subject_object_predicate',
                                  llm_log_path=None, gt_s=[], gt_p=[], gt_o=[], pred_s=[], pred_o=[], pred_p=[], 
                                  with_subject=True, with_predicate=True):

    # TODO Erweiterung möglich?
    # pred_objects = "all"
    # requireObjectTrue

    # TODO Performance per Class
    # splitPerformanceFor = "object"

    # Beispielausgaben:
    # - GT: A dear sitting on a cat, depicts, dear
    # - Pred: cat, depicts, dear

    tp = 0
    found = {}
    total_pre = 0
    total_pos = 0
    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference, predictions_['content'] = prepare_data_total(reference, eval, predictions_['content'])

            if gt_s:
                reference = [a for a in reference if a[3] in gt_s]
            if gt_o:
                reference = [a for a in reference if a[4] in gt_o]
            if gt_p:
                reference = [a for a in reference if a[1] in gt_p]

            if pred_s:
                predictions_['content'] = [a for a in predictions_['content'] if a[3] in pred_s]
            if pred_o:
                predictions_['content'] = [a for a in predictions_['content'] if a[4] in pred_o]
            if pred_p:
                predictions_['content'] = [a for a in predictions_['content'] if a[1] in pred_p]

            total_pos += len(reference)
            for trips in predictions_['content']:
                total_pre += 1

                if mode == 'perfect':
                    #tp, found = calc_perfect_total(reference=reference, pred=trips, found=found, tp=tp, single='p')
                    s_pred = trips[0]
                    o_pred = trips[2]
                    p_pred = trips[1]
                    
                    for tup in reference:
                        if not with_subject:
                            s = True
                        else:
                            s = tup[0] == s_pred 
                        
                        if not with_predicate:
                            p = True
                        else:
                            p = tup[1] == p_pred

                        if s and found.get(tup) is None:
                            if tup[2] == o_pred:
                                if p:
                                    tp += 1
                                    found = remove_entry(remove=tup, structure=found, mode='multiple')
                                    break

                elif mode == 'word_distance':
                    #tp, found = calc_word_distance_total(reference=reference, pred=trips, found=found, tp=tp, single='p')
                    s_pred = trips[0]
                    o_pred = trips[2]
                    p_pred = trips[1]
                    saved_tups = []

                    if not with_subject:
                        saved_tups = reference
                    else:
                        for tup in reference:
                            ratio = SequenceMatcher(lambda x: x==' ', s_pred, tup[0]).ratio() 
                            if ratio > 0.75 and found.get(tup) is None:  # assuming that the string are similar enough
                                saved_tups.append(tup)

                    for saved_tup in saved_tups:  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
                       
                        if not with_predicate:
                            p = True
                        else:
                            p = p_pred == saved_tup[1]

                        ratio = SequenceMatcher(lambda x: x==' ', o_pred, saved_tup[2]).ratio() 
                        if ratio > 0.75 and p and found.get(saved_tup) is None:  # assuming that the string are similar enough 
                            tp += 1
                            found = remove_entry(remove=saved_tup, structure=found, mode='multiple')
                            break

                elif mode in ('hard', 'soft'):
                    #tp, found = calc_ollama_total(reference=reference, pred=trips, found=found, tp=tp, single='p', mode=mode, llm_log_path=llm_log_path)
                    s_pred = trips[0]
                    o_pred = trips[2]
                    p_pred = trips[1]
                    
                    for tup in reference:
                        if not with_subject:
                            s = True
                        else:
                            s = determine_ollama_candidate(s_pred, tup[0]) and 'y' in llm_query((s_pred, tup[0]), llm_log_path, mode)
                        
                        if not with_predicate:
                            p = True
                        else:
                            p = tup[1] == p_pred

                        if found.get(tup) is None and s: #'/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt_prädikat.json'
                            if determine_ollama_candidate(o_pred, tup[2]) and 'y' in llm_query((o_pred, tup[2]), llm_log_path, mode):
                                # since the predicates are hardcoded there is no need for the llm
                                if p:  
                                    tp += 1
                                    found = remove_entry(remove=tup, structure=found, mode='multiple')
                                    break
    # ------------- calculate metrics -------------#
    print(total_pos)
    scores = calculate_metrics(tp, total_pre, total_pos)
    scores.to_csv(save_path) 
            


#-------------------------------------------------------------------------------#

############################### these functions are part of the trick like approach and will therefore not last ##########################################
#----------------------------------------- evaluates the metrics for the entire dataset ----------------------------------#


def prepare_data(reference, eval, predictions, gt_classes_dict):
    f = 1
    if eval == 'subject':
        reference = [(triplet['triplet']['subject'].lower(), triplet['triplet']['s_class']) for triplet in reference]
        reference = ([next(b) for a, b in itertools.groupby(reference, lambda y: y[0])])
        predictions = [(triplet['subject']['label'].lower(), triplet['subject']['s_class']) for triplet in predictions]
        predictions.sort()
        predictions = ([next(b) for a, b in itertools.groupby(predictions, lambda y: y[0])]) 

    elif eval == 'object':
        reference = [(triplet['triplet']['object'].lower(), triplet['triplet']['o_class']) for triplet in reference]
        reference = ([next(b) for a, b in itertools.groupby(reference, lambda y: y[0])])
        predictions = [(triplet['object']['label'].lower(), triplet['class_name']) for triplet in  predictions]
        predictions.sort()
        predictions  = ([next(b) for a, b in itertools.groupby(predictions, lambda y: y[0])]) 

    elif eval == 'subject_object':
        reference = [(triplet['triplet']['subject'].lower(), triplet['triplet']['object'].lower(), triplet['triplet']['s_class'], triplet['triplet']['o_class']) for triplet in reference]
        seen = set()
        reference = [(a, b, c, d) for a, b, c, d in reference if not ((a, b) in seen or seen.add((a, b)))]
        predictions = [(triplet['subject']['label'].lower(), triplet['object']['label'].lower(), triplet['subject']['s_class'], triplet['class_name']) for triplet in  predictions]
        predictions.sort()
        seen = set()
        predictions = [(a, b, c, d) for a, b, c, d in predictions if not ((a, b) in seen or seen.add((a, b)))]
        f = 2

    elif eval == 'subject_object_predicate':
        reference = [(triplet['triplet']['subject'].lower(), triplet['triplet']['predicate'], triplet['triplet']['object'].lower(), triplet['triplet']['s_class'], triplet['triplet']['o_class']) for triplet in reference]
        seen = set()
        reference = [(a, b, c, d, e) for a, b, c, d, e in reference if not ((a, b, c) in seen or seen.add((a, b, c)))]
        predictions = [(triplet['subject']['label'].lower(), triplet['relation']['label'], triplet['object']['label'].lower(), triplet['subject']['s_class'], triplet['class_name']) for triplet in  predictions]
        predictions.sort()            
        seen = set()
        predictions = [(a, b, c, d, e) for a, b, c, d, e in predictions if not ((a, b, c) in seen or seen.add((a, b, c)))]

    #------- count the ground truth up for each class ---------#
    for tup in reference:         
        # count the occurences of all classes within the reference
        gt_classes_dict[tup[f]] += 1

    return reference, predictions, gt_classes_dict


def evaluate_tricks(trips, eval, reference, type_prediction, llm_log_path, mode, found, entity_storage=None):
    #---------- count the matches detailed in differnt ways -------------#
    if eval in ('subject', 'object'):
        pred = trips
        tp_flag, class_name, found, type_prediction = \
                mode_specific_counting((pred, ), reference, type_prediction, llm_log_path, mode, found, single='', entity_storage=entity_storage)

    elif eval == 'subject_object':
        s_pred = (trips[0], trips[2])
        o_pred = (trips[1], trips[3])
        tp_flag, class_name, found, type_prediction = \
                mode_specific_counting((s_pred, o_pred), reference, type_prediction, llm_log_path, mode, found, single='c')

    elif eval == 'subject_object_predicate':
        s_pred = (trips[0], trips[3])
        o_pred = (trips[2], trips[4])
        p_pred = trips[1]
        tp_flag, class_name, found, type_prediction = \
                mode_specific_counting((s_pred, o_pred, p_pred), reference, type_prediction, llm_log_path, mode, found, single='p')

    return tp_flag, class_name, found, type_prediction


def calc_word_distance(pred, reference, type_prediction, found, single):
    tp_flag = False
    if single == '':   
        pred = pred[0] 
        candidate = ('', 0)
        class_name = pred[1]

        for tup in reference:
            ratio = SequenceMatcher(lambda x: x==' ', pred[0], tup[0]).ratio() 
            if ratio > 0.75:  # assuming that the strings are similar enough
                if candidate[1] < ratio:
                    candidate = (tup[0], ratio)
                    saved_tup = tup

        if candidate[0] != '' and found.get(pred) is None:  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
            type_prediction = count_type_accuracy(tup, (pred, ), type_prediction, single)
            class_name = saved_tup[1]
            tp_flag = True
            found = remove_entry(remove=saved_tup, structure=found)
  
    elif single == 'c':
        s_pred = pred[0]
        o_pred = pred[1]
        class_name = s_pred[1]
        saved_tups = []

        for tup in reference:
            ratio = SequenceMatcher(lambda x: x==' ', s_pred[0], tup[0]).ratio() 
            if ratio > 0.75 and found.get(tup) is None:  # assuming that the string are similar enough
                saved_tups.append(tup)
    
        for saved_tup in saved_tups:  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
            ratio = SequenceMatcher(lambda x: x==' ', o_pred[0], saved_tup[1]).ratio() 

            if ratio > 0.75 and found.get(tup) is None:  # assuming that the string are similar enough 
                type_prediction = count_type_accuracy(tup, pred, type_prediction, single)
                tp_flag = True
                class_name = saved_tup[2]
                found = remove_entry(remove=saved_tup, structure=found, mode='multiple')
                break
    else:
        s_pred = pred[0]
        o_pred = pred[1]
        p_pred = pred[2]
        class_name = p_pred
        saved_tups = []
        class_name = p_pred
        for tup in reference:
            ratio = SequenceMatcher(lambda x: x==' ', s_pred[0], tup[0]).ratio() 
            if ratio > 0.75 and found.get(tup) is None:  # assuming that the string are similar enough
                saved_tups.append(tup)
        
        for saved_tup in saved_tups:  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
            ratio = SequenceMatcher(lambda x: x==' ', o_pred[0], saved_tup[1]).ratio() 
            if ratio > 0.75 and p_pred == saved_tup[1] and found.get(tup) is None:  # assuming that the string are similar enough 
                tp_flag = True
                class_name = saved_tup[1]
                found = remove_entry(remove=saved_tup, structure=found, mode='multiple')
                break

    return class_name, tp_flag, found


def calc_perfect(pred=None, reference=None, type_prediction=None, found=None, single=None):
    # count up with perfect matches
    tp_flag = False
    if single == '':
        pred = pred[0]
        class_name = pred[1]
        for tup in reference:
            if tup[0] == pred[0] and found.get(tup) is None:
                tp_flag = True
                class_name = tup[1]
                found = remove_entry(remove=tup, structure=found)
                type_prediction = count_type_accuracy(tup, (pred, ), type_prediction, single)

                break

    elif single == 'c':
        # count up with perfect matches
        s_pred = pred[0]
        o_pred = pred[1]
        class_name = s_pred[1]
        for tup in reference:
            if tup[0] == s_pred[0] and found.get(tup) is None:
                if tup[1] == o_pred[0] and found.get(tup) is None: 
                    type_prediction = count_type_accuracy(tup, pred, type_prediction, single) 
                    tp_flag = True
                    class_name = tup[2]
                    found = remove_entry(remove=tup, structure=found, mode='multiple')
                    break
    else:
        # count up with perfect matches
        s_pred = pred[0]
        o_pred = pred[1]
        p_pred = pred[2]
        class_name = p_pred
        for tup in reference:
            if tup[0] == s_pred[0] and found.get(tup) is None:
                if tup[1] == o_pred[0] and found.get(tup) is None:
                    if p_pred == tup[1] and found.get(tup) is None:
                        tp_flag = True
                        class_name = tup[1]
                        found = remove_entry(remove=tup, structure=found, mode='multiple')
                        break
        
    return class_name, tp_flag, found


def calc_ollama(pred, reference, type_prediction, found, llm_log_path, mode, single=True):
    # count up with llm prompts (hard/soft cut)
    tp_flag = False
    if single == '':
        pred = pred[0]  
        class_name = pred[1]
        for tup in reference:
            if found.get(tup) is None and determine_ollama_candidate(pred[0], tup[0]) and 'y' in llm_query((pred[0], tup[0]), llm_log_path, mode):
                type_prediction = count_type_accuracy(tup, (pred,), type_prediction, single)
                class_name = tup[1]
                tp_flag = True
                found = remove_entry(remove=tup, structure=found)
                break

    elif single == 'c':
        s_pred = pred[0]
        o_pred = pred[1]
        class_name = s_pred[1]

        for tup in reference:
            if found.get(tup) is None and determine_ollama_candidate(s_pred[0], tup[0]) and 'y' in llm_query((s_pred[0], tup[0]), llm_log_path, mode):
                if found.get(tup) is None and determine_ollama_candidate(o_pred[0], tup[1]) and 'y' in llm_query((o_pred[0], tup[1]), llm_log_path, mode):
                    type_prediction = count_type_accuracy(tup, pred, type_prediction, single)
                    tp_flag = True
                    class_name = tup[2]
                    found = remove_entry(remove=tup, structure=found, mode='multiple')
                    break
    else:
        s_pred = pred[0]
        o_pred = pred[1]
        p_pred = pred[2]
        class_name = p_pred
        class_name = p_pred
        for tup in reference:
            if  found.get(tup) is None and determine_ollama_candidate(s_pred[0], tup[0]) and 'y' in llm_query((s_pred[0], tup[0]), llm_log_path, mode):
                if found.get(tup) is None and determine_ollama_candidate(o_pred[0], tup[2]) and 'y' in llm_query((o_pred[0], tup[2]), llm_log_path, mode):
                    if p_pred == tup[1]  and found.get(tup) is None:
                        tp_flag = True
                        class_name = tup[1]
                        found = remove_entry(remove=tup, structure=found, mode='multiple')
                        break

    return class_name, tp_flag, found


def mode_specific_counting(pred, reference, type_prediction, llm_log_path, mode, found, single, entity_storage=None):
    if mode == 'word_distance':
        
        class_name, tp_flag, found = calc_word_distance(pred, reference, type_prediction, found, single)
        #store_entity(pred, entity_storage)  # if the ground truth class_name is needed replace pred[0][1] with class_name

    elif mode == 'perfect':
        class_name, tp_flag, found = calc_perfect(pred, reference, type_prediction, found, single)
            
    elif mode in ('hard', 'soft'):
        class_name, tp_flag, found = calc_ollama(pred, reference, type_prediction, found, llm_log_path, mode, single)

    return tp_flag, class_name, found, type_prediction


def eval_accuracy_classes_tricks(text_entries, save_path, save_types, mode='word_distance', llm_log_path=None, eval='subject', save_entity=None, save_gt=None, save_pred=None):
    # evaluates the correctly found subjects only one of the three modes can be True
    pred_classes_dict = {}
    gt_classes_dict = defaultdict(int)
    type_prediction = defaultdict(lambda: {'found':0, 'existing': 0})
    found = {}
    cnt_ob = defaultdict(int)
    cnt_sub = defaultdict(int)
    cnt_pred_sub = defaultdict(int)
    cnt_pred_ob = defaultdict(int)
    cnt = defaultdict(int)
    with open(save_entity, 'w', encoding='utf-8') as fp:
              
        for entry in text_entries:
            for predictions_ in entry['triplets']:
                reference = entry['annotations']
                reference = convert_annotation_to_triplet(reference)
                reference, predictions_['content'], gt_classes_dict = prepare_data(reference, eval, predictions_['content'], gt_classes_dict)
                
                ##############THIS PART REMOVES ALL THE SUBJECTS WHERE SUBJECT != ARTWORK FROM THE LIST ################# 
                
                # print(len(reference))
                # print(len(predictions_['content']))
                # try:
                #     end = re.search('^.*\n\n', entry['text']).end()
                #     match = entry['text'][:end-2]
                # except (TypeError, AttributeError):
                #     match = entry["id"]

                # reference_copy = reference.copy()
                # reference = [x for x in reference_copy if x[0].lower() != match.lower()]
                
                # for a in reference:
                #     cnt_sub[a[3]] += 1
                #     cnt_sub['total'] += 1
                #     cnt_ob[a[4]] += 1
                #     cnt_ob['total'] += 1
                #     cnt[a[1]] += 1
                #     cnt['total'] += 1

                # for a in predictions_['content']:
                #     cnt_pred_sub[a[3]] += 1
                #     cnt_pred_sub['total'] += 1
                #     cnt_pred_ob[a[4]] += 1
                #     cnt_pred_ob['total'] += 1

                # predictions_copy = predictions_['content'].copy()
                # predictions_['content'] = [x for x in predictions_copy if x[0].lower() == match.lower()]

                # reference_copy = reference.copy()
                # predictions_copy = predictions_['content'].copy()
                # reference = [x for x in reference_copy if x[1].lower() == 'depicts']
                # predictions_['content'] = [x for x in predictions_copy if x[1].lower() == 'depicts']

                # for a in reference:
                #     if a[-1] == 'Person':
                #         print(a)
                
                # ref_person = [a for a in reference if a[-1] == 'Occupation']
                # pred_person = [a for a in predictions_['content'] if a[-1] == 'Occupation']

                # print(entry['id'])
                # print(ref_person)
                
                # if len(ref_person) and len(pred_person) > 0:
                #     print('ref:', ref_person)
                #     print('pred:', pred_person)



                ##########################################################################################################
                
                # -------- main evaluation process ----------#
                for trips in predictions_['content']:
                    tp_flag, class_name, found, type_prediction = evaluate_tricks(trips, eval, reference, type_prediction, llm_log_path, mode, found, entity_storage=save_entity)
                    pred_classes_dict = detailed_storage(class_name, pred_classes_dict, tp_flag)
                    print(f'entity: {trips[0]}   class: {trips[1]}\n')
                    fp.write(f'entity: {trips[0]}   class: {trips[1]}\n')

    #------------- calculate metrics -------------#
    calculate_metrics_df(pred_classes_dict, gt_classes_dict, save_path=save_path, save_types=save_types, 
                         type_prediction=type_prediction, amounts=True, save_gt=save_gt, save_pred=save_pred)
    ################################
    #print(pred_classes_dict)

    # pd.DataFrame.from_dict(cnt_sub, orient='index').to_csv('/nfs/home/ritterd/reflect/reflectai/wp2/test/experiments/subjectequalsnameannotationfiltered.jsonl/subject_object_predicate/gt_sub_classes.csv')
    # pd.DataFrame.from_dict(cnt_ob, orient='index').to_csv('/nfs/home/ritterd/reflect/reflectai/wp2/test/experiments/subjectequalsnameannotationfiltered.jsonl/subject_object_predicate/gt_ob_classes.csv')
    # pd.DataFrame.from_dict(cnt, orient='index').to_csv('/nfs/home/ritterd/reflect/reflectai/wp2/test/experiments/subjectequalsnameannotationfiltered.jsonl/subject_object_predicate/gt_pred.csv')

    # pd.DataFrame.from_dict(cnt_pred_sub, orient='index').to_csv('/nfs/home/ritterd/reflect/reflectai/wp2/test/experiments/subjectequalsnameannotationfiltered.jsonl/subject_object_predicate/pred_sub_classes.csv')
    # pd.DataFrame.from_dict(cnt_pred_ob, orient='index').to_csv('/nfs/home/ritterd/reflect/reflectai/wp2/test/experiments/subjectequalsnameannotationfiltered.jsonl/subject_object_predicate/pred_ob_classes.csv')
    ################################


######################################################################################################################################################################

default_config = {}
default_parameters = {}


@Manager.export("Evaluator")
class EvaluatorPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, text_entries: List[Dict]) -> Generator:      
        ####################### for now we will use this kind of metric scheme, however, it will not last ##############################
        try:
            tricks = self._config['tricks']
        except KeyError:
            tricks = False

        if not tricks:
            try:
                conf = self._config['conf']
            except KeyError:
                conf = False
        ################################################################################################################################

        try:
            mode = self._config['mode']
            eval = self._config['eval']
            save_path = self._config['save_path']
        except KeyError:
            # maybe not raise and only tell about the issue and that no evaluation took place
            raise KeyError('An evaluation scheme (eval) = (subject, object, subject_object, subject_object_predciates),' + 
                           'a (mode) = (word_distance, perfect, soft, hard), a path to the directory in where to save the results (save_path) needs to be given!')
        else:
            
            ###################################### this part is only for the beginning and is not planned to be used in the end #############################################################
            # ---------------------------------- Evaluate all four schemes with a classes focus -------------------------------------
            save_types = save_path + f'/{eval}/types_{mode}.csv'
            save_results = save_path + f'/{eval}/classes_{mode}.csv'
            llm_log_path = save_path + f'/{eval}/llm_mitschrift_{mode}_classes.json'
            save_entity = save_path + f'/{eval}/entities{mode}.txt'
            save_gt = save_path + f'/{eval}/GTs_{mode}.csv'
            save_pred = save_path + f'/{eval}/Preds_{mode}.csv'
            


            if tricks:
                eval_accuracy_classes_tricks(text_entries, save_path=save_results, save_types=save_types, mode=mode, llm_log_path=llm_log_path,
                                              eval=eval, save_entity=save_entity, save_gt=save_gt, save_pred=save_pred)
                print(f'\n{eval} done')
            #####################################################################################################################################################################################

            # --------------------------------- Evaluate all four schemes for the dataset in total ---------------------------------------------------- #
            
            
            elif conf:
                save_results = save_path + f'/{eval}/total_{mode}.csv'
                llm_log_path = save_path + f'/{eval}/llm_mitschrift_{mode}_total.json'
                
                try:
                    gt_s = self._config['gt_subjects']
                except KeyError:
                    gt_s = []

                try:
                    gt_o = self._config['gt_objects']
                except KeyError:
                    gt_o = []

                try:
                    gt_p = self._config['gt_predicates']
                except KeyError:
                    gt_p = []


                try:
                    pred_s = self._config['pred_subjects']
                except KeyError:
                    pred_s = []

                try:
                    pred_o = self._config['pred_objects']
                except KeyError:
                    pred_o = []

                try:
                    pred_p = self._config['pred_predicates']
                except KeyError:
                    pred_p = [] 

                try:
                    with_subject = self._config['with_subject']
                except KeyError:
                    with_subject = False 

                try:
                    with_predicate = self._config['with_predicate']
                except KeyError:
                    with_predicate = False 
                    
                eval_accuracy_total_triplets(text_entries, save_path=save_results, llm_log_path=llm_log_path, mode=mode, 
                                             gt_s=gt_s, gt_o=gt_o, gt_p=gt_p, pred_o=pred_o, pred_p=pred_p, pred_s=pred_s,
                                             with_predicate=with_predicate, with_subject=with_subject)
                
            else:
                eval_accuracy_total(text_entries, save_path=f'../test/gollie_testset/{eval}/eval_{mode}.csv', mode=mode, llm_log_path=f'../test/gollie_testset/{eval}/llm_mitschrift_{mode}_eval.json', eval=eval)
                print(f'\n{eval} done')
        
        yield text_entries
