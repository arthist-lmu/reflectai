from typing import List, Dict, Generator
import json
import numpy as np
import pandas as pd
from kg_pipeline.manager import Manager
from difflib import SequenceMatcher
from kg_pipeline.plugin import Plugin
from ollama import Client, _types
import re
from collections import defaultdict


client = Client(
  host='devbox2.research.tib.eu'
)

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
    """
    key: either the class name or the predicate of a triplet
    """
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
    # if mode == 'single':
    #     for triplet in structure:
    #         if triplet[0] == remove:
    #             return structure.remove(triplet)
            
    # elif mode == 'multiple':
    #     for triplet in structure:
    #         found_flag = True
    #         for i, element in enumerate(triplet[:-2]):
    #             if element != remove[i]:
    #                 found_flag = False
    #                 break

    #         if found_flag:
    #             return structure.remove(triplet)


def calculate_metrics_detailed(pred_dict, pos_dict, mode='class', with_n=False):
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
            
            # todo: prediction has way more than ref and that needs to be addressed
            
            if with_n:
                scores = [s_f1_score, s_precision, s_recall, s_total_pre]
            else:
                scores = [s_f1_score, s_precision, s_recall]

            results.update({key: scores})
        
        # include all the classes that have not been found but could have been found
        for gt_key in pos_dict.keys():
            if gt_key not in results.keys():
                if with_n:
                    scores = [0, 0, 0, 0]
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

#-------------------------------------------------------------------------------#


#---------------- evaluates the metrics for the entire dataset -----------------#

def eval_subject_accuracy(text_entries, save_path, mode='word_distance', llm_log_path=None):
    # evaluates the correctly found subjects only one of the three modes can be True
    s_tp = s_total_pos = s_total_pre = 0

    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference = [(triplet['triplet']['subject'].lower(),) for triplet in reference]
            reference = list(set(reference))

            #------- count the counter variables up ---------#
            s_total_pos += len(reference)

            predictions_['content'] = [(triplet['subject']['label'].lower(),) for triplet in  predictions_['content']]

            # remove duplicates from the predictions 
            #predictions_['content'] = [i for n, i in enumerate(predictions_['content']) if i not in predictions_['content'][n + 1:]]
            predictions_['content'] = list(set(predictions_['content']))
            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                s_total_pre += 1
            
                #----------- Extract the RDF tuples ----------#
                s_pred = trips

                #---------- count the matches -------------#
                ##----------count in different ways-------#

                if mode == 'word_distance':
                    candidate = ('', 0)
                    for tup in reference:
                        ratio = SequenceMatcher(lambda x: x==' ', s_pred[0], tup[0]).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough
                            if candidate[1] < ratio:
                                candidate = (tup[0], ratio)
       
                    if candidate[0] != '':  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
                        remove_entry(remove=candidate[0], structure=reference)
                
                elif mode == 'perfect':
                    # count up with perfect matches
                    for tup in reference:
                        if tup[0] == s_pred[0]:
                            s_tp += 1
                            remove_entry(remove=s_pred[0], structure=reference)
                            break
                      
                elif mode == ('hard', 'soft'):
                    # count up with llm prompts (hard cut)
                    for tup in reference:
                        if 'y' in llm_query((s_pred[0], tup[0]), llm_log_path, mode): # '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt.json'
                            s_tp += 1
                            remove_entry(remove=s_pred[0], structure=reference)
                            break

                ## ---------- /count in different ways ----------- ##

    s_scores = calculate_metrics(s_tp, s_total_pre, s_total_pos)

    s_scores.to_csv(save_path) # '../test/gollie_testset/subjects/subject_eval.csv')


def eval_object_accuracy(text_entries, save_path, mode='word_distance', llm_log_path=None):
    # evaluates the correctly found subjects only one of the three modes can be True
    o_tp = o_total_pos = o_total_pre = 0

    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference = [(triplet['triplet']['object'].lower(), ) for triplet in reference]
            reference = list(set(reference))

            #------- count the counter variables up ---------#
            o_total_pos += len(reference)

            # maybe I could also use the objects from the reference as a metric
            predictions_['content'] = [(triplet['object']['label'].lower(),) for triplet in  predictions_['content']]

            # remove duplicates from the predictions 
            predictions_['content'] = list(set(predictions_['content']))
            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                o_total_pre += 1
            
                #----------- Extract the RDF tuples ----------#
                o_pred = trips[0]

                #---------- count the matches -------------#
                ##----------count in different ways-------##
                
                if mode == 'word_distance':
                    candidate = ('', 0, None)
                    for tup in reference:
                        ratio = SequenceMatcher(lambda x: x==' ', o_pred, tup[0]).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough
                            if candidate[1] < ratio:
                                candidate = (tup[0], ratio)
                    
                    if candidate[0] != '':  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
                        o_tp += 1

                        remove_entry(remove=candidate[0], structure=reference)

                elif mode == 'perfect':
                    # count up with perfect matches
                    for tup in reference:
                        if tup[0] == o_pred:
                            o_tp += 1
                            remove_entry(remove=o_pred, structure=reference)
                            break
                        
                elif mode in ('hard', 'soft'):
                    # count up with llm prompts (hard cut)
                    for tup in reference:
                        if 'y' in llm_query((o_pred, tup[0]), llm_log_path, mode):
                            o_tp += 1
                            remove_entry(remove=o_pred, structure=reference)
                            break

                ## ---------- /count in different ways ----------- ##

    o_scores = calculate_metrics(o_tp, o_total_pre, o_total_pos)
    o_scores.to_csv(save_path) #'../test/gollie_testset/objects/object_eval.csv')


def eval_subject_object_accuracy(text_entries, save_path, mode='word_distance', llm_log_path=None):
    # evaluates the correctly found subjects only one of the three modes can be True
    os_tp = os_total_pos = os_total_pre = 0

    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference = [(triplet['triplet']['subject'].lower(), triplet['triplet']['object'].lower(), triplet['triplet']['s_class'], triplet['triplet']['o_class']) for triplet in reference]
            reference = list(set(reference))

            #------- count the counter variables up ---------#
            os_total_pos += len(reference)

            # maybe I could also use the objects from the reference as a metric
            predictions_['content'] = [(triplet['subject']['label'].lower(), triplet['object']['label'].lower(), triplet['subject']['s_class'], triplet['class_name']) for triplet in predictions_['content']]

            # remove duplicates from the predictions 
            predictions_['content'] = list(set(predictions_['content']))
            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                os_total_pre += 1
            
                #----------- Extract the RDF tuples ----------#
                s_pred = trips[0]
                o_pred = trips[1]

                #---------- count the matches -------------#
                ##----------count in different ways-------##
                
                if mode == 'word_distance':
                    candidate = ('', 0)
                    saved_tup = ()
                    for tup in reference:
                        ratio = SequenceMatcher(lambda x: x==' ', s_pred, tup[0]).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough
                            if candidate[1] < ratio:
                                candidate = (tup[0], ratio)
                                saved_tup = tup
                    
                    if candidate[0] != '':  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
                        ratio = SequenceMatcher(lambda x: x==' ', o_pred, saved_tup[1]).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough 
                            os_tp += 1
                            remove_entry(remove=(saved_tup[0], saved_tup[1]), structure=reference, mode='multiple')

                elif mode == 'perfect':
                    # count up with perfect matches
                    for tup in reference:
                        if tup[0] == s_pred:
                            if tup[1] == o_pred:
                                os_tp += 1
                                remove_entry(remove=(s_pred, o_pred), structure=reference, mode='multiple')
                                break
                            
                elif mode in  ('hard', 'soft'):
                    # count up with llm prompts (soft cut)
                    for tup in reference:
                        if 'y' in llm_query((s_pred, tup[0]), llm_log_path, mode): #'/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt.json'
                            if 'y' in llm_query((o_pred, tup[1]), llm_log_path, mode):
                                os_tp += 1
                                remove_entry(remove=(s_pred, o_pred), structure=reference, mode='multiple')
                                break

                ## ---------- /count in different ways ----------- ##

    s_scores = calculate_metrics(os_tp, os_total_pre, os_total_pos)
    s_scores.to_csv(save_path) #'../test/gollie_testset/subject_object/subject_object_eval.csv'


def eval_subject_object_predicate(text_entries, save_path, mode='word_distance', llm_log_path=None):
    # evaluates the correctly found subjects only one of the three modes can be True
    p_tp = p_total_pos = p_total_pre = 0
    
    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference = [(triplet['triplet']['subject'].lower(), triplet['triplet']['predicate'], triplet['triplet']['object'].lower(), triplet['triplet']['s_class'], triplet['triplet']['o_class']) for triplet in reference]
            reference = list(set(reference))

            #------- count the counter variables up ---------#
            p_total_pos += len(reference)
            # maybe I could also use the objects from the reference as a metric
            predictions_['content'] = [(triplet['subject']['label'].lower(), triplet['relation']['label'], triplet['object']['label'].lower(), triplet['subject']['s_class'], triplet['class_name']) for triplet in  predictions_['content']]

            # remove duplicates from the predictions 
            predictions_['content'] = list(set(predictions_['content']))
            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                p_total_pre += 1
            
                #----------- Extract the RDF tuples ----------#
                s_pred = trips[0]
                p_pred = trips[1]
                o_pred = trips[2]

                #---------- count the matches -------------#
                ##----------count in different ways-------##
                if mode == 'word_distance':
                    candidate = ('', 0)
                    saved_tup = ()
                    for tup in reference:
                        ratio = SequenceMatcher(lambda x: x==' ', s_pred, tup[0]).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough
                            if candidate[1] < ratio:
                                candidate = (tup[0], ratio)
                                saved_tup = tup
                    
                    if candidate[0] != '':  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
                        ratio = SequenceMatcher(lambda x: x==' ', o_pred, saved_tup[2]).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough
                            ratio = SequenceMatcher(lambda x: x==' ', p_pred, saved_tup[1]).ratio() 
                            if ratio > 0.75:  # assuming that the string are similar enough
                                p_tp += 1
                                remove_entry(remove=(saved_tup[0], saved_tup[1], saved_tup[2]), structure=reference, mode='multiple')

                elif mode == 'perfect':
                    # count up with perfect matches
                    for tup in reference:
                        if tup[0] == s_pred:
                            if tup[2] == o_pred:
                                if tup[1] == p_pred:
                                    p_tp += 1
                                    remove_entry(remove=(s_pred, p_pred, o_pred), structure=reference, mode='multiple')
                                    break
                        
                elif mode in ('hard', 'soft'):
                    # count up with llm prompts (hard cut)
                    for tup in reference:
                        if 'y' in llm_query((s_pred, tup[0]), llm_log_path, mode): #'/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt_prädikat.json'
                            if 'y' in llm_query((o_pred, tup[2]), llm_log_path, mode):
                                # since the predicates are hardcoded there is no need for the llm
                                if tup[1] == p_pred:  
                                    p_tp += 1
                                    remove_entry(remove=(tup[0], tup[1], tup[2]), structure=reference, mode='multiple')
                                    break

                ## ---------- /count in different ways ----------- ##
    #------------- calculate and print total metrics -------------#
    s_scores = calculate_metrics(p_tp, p_total_pre, p_total_pos)
    s_scores.to_csv(save_path)

#-------------------------------------------------------------------------------#

############################### these functions are part of the trick like approach and will therefore not last ##########################################
#----------------------------------------- evaluates the metrics for the entire dataset ----------------------------------#


def mode_specific_counting(pred, reference, type_prediction, llm_log_path, mode, found):
    tp_flag = False
    if mode == 'word_distance':
        candidate = ('', 0)
        class_name = pred[1]
        for tup in reference:
            ratio = SequenceMatcher(lambda x: x==' ', pred[0], tup[0]).ratio() 
            if ratio > 0.75:  # assuming that the strings are similar enough
                if candidate[1] < ratio:
                    candidate = (tup[0], ratio)
                    saved_tup = tup

        if candidate[0] != '' and found.get(pred) is None:  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
            if saved_tup[1] == pred[1]:
                if saved_tup[1] in type_prediction.keys():
                    type_prediction[saved_tup[1]]['found'] += 1
                    type_prediction[saved_tup[1]]['existing'] += 1
                else:
                    type_prediction.update({saved_tup[1]: {'existing': 1, 'found':1}}) 
            else:
                if saved_tup[1] in type_prediction.keys():
                    type_prediction[saved_tup[1]]['existing'] += 1
                else:
                    type_prediction.update({saved_tup[1]: {'existing': 1, 'found':0}})

            class_name = saved_tup[1]
            tp_flag = True
            found = remove_entry(remove=saved_tup, structure=found)
            # rather than removing items from the list, we have to save it in a dict and ignore if found 

    elif mode == 'perfect':
        class_name = pred[1]
        #print(s_pred)
        # count up with perfect matches
        for tup in reference:
            if tup[0] == pred[0] and found.get(pred) is None:
                #print('gefunden!')
                tp_flag = True
                class_name = tup[1]
                # what about the case where s_pred is actually part of the class just not in gt
                found = remove_entry(remove=tup, structure=found)

                if tup[1] == pred[1]:
                    if tup[1] in type_prediction.keys():
                        type_prediction[tup[1]]['found'] += 1
                        type_prediction[tup[1]]['existing'] += 1
                    else:
                        type_prediction.update({tup[1]: {'existing': 1, 'found':1}}) 
                else:
                    if tup[1] in type_prediction.keys():
                        type_prediction[tup[1]]['existing'] += 1
                    else:
                        type_prediction.update({tup[1]: {'existing': 1, 'found':0}}) 

                break
            
    elif mode in ('hard', 'soft'):
        # count up with llm prompts (hard cut)
        class_name = pred[1]
        for tup in reference:
            if found.get(pred) is None and 'y' in llm_query((pred[0], tup[0]), llm_log_path, mode):
                if tup[1] == pred[1]:
                    if tup[1] in type_prediction.keys():
                        type_prediction[tup[1]]['found'] += 1
                        type_prediction[tup[1]]['existing'] += 1
                    else:
                        type_prediction.update({tup[1]: {'existing': 1, 'found':1}}) 
                else:
                    if tup[1] in type_prediction.keys():
                        type_prediction[tup[1]]['existing'] += 1
                    else:
                        type_prediction.update({tup[1]: {'existing': 1, 'found':0}})

                class_name = tup[1]
                tp_flag = True
                found = remove_entry(remove=tup, structure=found)
                break

    return tp_flag, class_name, found, type_prediction



def eval_subject_accuracy_classes_tricks(text_entries, save_path, save_types, mode='word_distance', llm_log_path=None):
    # evaluates the correctly found subjects only one of the three modes can be True
    pred_classes_dict = {}
    gt_classes_dict = {}
    type_prediction = {}
    found = {}

    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference = [(triplet['triplet']['subject'].lower(), triplet['triplet']['s_class']) for triplet in reference]
            reference = list(set(reference))
 
            #------- count the counter variables up ---------#
            for tup in reference:            
                # count the occurences of all classes within the reference
                if tup[1] not in gt_classes_dict.keys():
                    gt_classes_dict.update({tup[1]: 1})
                else:
                    gt_classes_dict[tup[1]] += 1

            # the class_name is directed towards the object and not the subject! 
            predictions_['content'] = [(triplet['subject']['label'].lower(), triplet['subject']['s_class']) for triplet in  predictions_['content']]

            # remove duplicates from the predictions 
            predictions_['content'] = list(set(predictions_['content']))    

            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                #----------- Extract the RDF tuples ----------#
                s_pred = trips

                #---------- count the matches detailed -------------#
                ##----------count in different ways-------##
                tp_flag, class_name, found, type_prediction = \
                        mode_specific_counting(s_pred, reference, type_prediction, llm_log_path, mode, found)

                pred_classes_dict = detailed_storage(class_name, pred_classes_dict, tp_flag)
    #------------- calculate and print total metrics -------------#
    class_eval = calculate_metrics_detailed(pred_classes_dict, gt_classes_dict, mode='class')
    class_df = pd.DataFrame.from_dict(data=class_eval, orient='index', columns=['F1', 'precision', 'recall'])
    class_df.to_csv(save_path)

    type_prediction_df = pd.DataFrame.from_dict(data=type_prediction, orient='index')
    type_prediction_df["procentage"] = type_prediction_df['found'] / type_prediction_df['existing']
    type_prediction_df.to_csv(save_types)


def eval_object_accuracy_classes_tricks(text_entries, save_path, save_types, mode='word_distance', llm_log_path=None):
    # evaluates the correctly found subjects only one of the three modes can be True
    pred_classes_dict = {}
    gt_classes_dict = {}
    type_prediction = {}
    found = {}

    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference = [(triplet['triplet']['object'].lower(), triplet['triplet']['o_class']) for triplet in reference]
            reference = list(set(reference))
            #------- count the counter variables up ---------#
            for tup in reference:            
                # count the occurences of all classes within the reference
                if tup[1] not in gt_classes_dict.keys():
                    gt_classes_dict.update({tup[1]: 1})
                else:
                    gt_classes_dict[tup[1]] += 1

            # the class_name is directed towards the object and not the subject! 
            predictions_['content'] = [(triplet['object']['label'].lower(), triplet['class_name']) for triplet in  predictions_['content']]

            # remove duplicates from the predictions 
            predictions_['content'] = list(set(predictions_['content']))        
            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                #----------- Extract the RDF tuples ----------#
                o_pred = trips
                #---------- count the matches detailed -------------#
                ##----------count in different ways-------##
                tp_flag, class_name, found, type_prediction = \
                        mode_specific_counting(o_pred, reference, type_prediction, llm_log_path, mode, found)
 
                pred_classes_dict = detailed_storage(class_name, pred_classes_dict, tp_flag)
    
    #------------- calculate and print total metrics -------------#
    class_eval = calculate_metrics_detailed(pred_classes_dict, gt_classes_dict, mode='class')
    class_df = pd.DataFrame.from_dict(data=class_eval, orient='index', columns=['F1', 'precision', 'recall'])
    class_df.to_csv(save_path)

    type_prediction_df = pd.DataFrame.from_dict(data=type_prediction, orient='index')
    type_prediction_df["procentage"] = type_prediction_df['found'] / type_prediction_df['existing']
    type_prediction_df.to_csv(save_types)


def eval_subject_object_accuracy_classes_tricks(text_entries, save_path, save_types, mode='word_distance', llm_log_path=None):
    # evaluates the correctly found subjects only one of the three modes can be True
    pred_classes_dict = {}
    pos_classes_dict = {}
    type_prediction = {}
    found = {}

    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference = [(triplet['triplet']['subject'].lower(), triplet['triplet']['object'].lower(), triplet['triplet']['s_class'], triplet['triplet']['o_class']) for triplet in reference]
            reference = list(set(reference))
            #------- count the counter variables up ---------#
            for tup in reference:            
                # count the occurences of all classes within the reference
                if tup[2] not in pos_classes_dict.keys():
                    pos_classes_dict.update({tup[2]: 1})
                else:
                    pos_classes_dict[tup[2]] += 1

            # maybe I could also use the objects from the reference as a metric
            predictions_['content'] = [(triplet['subject']['label'].lower(), triplet['object']['label'].lower(), triplet['subject']['s_class'], triplet['class_name']) for triplet in  predictions_['content']]

            # remove duplicates from the predictions 
            predictions_['content'] = list(set(predictions_['content']))
            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                #----------- Extract the RDF tuples ----------#
                 
                s_pred = (trips[0], trips[2])
                o_pred = (trips[1], trips[3])

                #---------- count the matches -------------#
                os_tp_flag = False
                ##----------count in different ways-------##
                
                if mode == 'word_distance': 
                    saved_tups = []

                    s_class_name = s_pred[1]
                    for tup in reference:
                        ratio = SequenceMatcher(lambda x: x==' ', s_pred[0], tup[0]).ratio() 
                        if ratio > 0.75 and found.get(tup) is None:  # assuming that the string are similar enough
                            saved_tups.append(tup)
                
                    for saved_tup in saved_tups:  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
                        ratio = SequenceMatcher(lambda x: x==' ', o_pred[0], saved_tup[1]).ratio() 

                        if ratio > 0.75 and found.get(tup) is None:  # assuming that the string are similar enough 
                            if saved_tup[2] == s_pred[1]:
                                if saved_tup[2] in type_prediction.keys():
                                    type_prediction[saved_tup[2]]['found'] += 1
                                    type_prediction[saved_tup[2]]['existing'] += 1
                                else:
                                    type_prediction.update({saved_tup[2]: {'existing': 1, 'found':1}}) 
                            else:
                                if saved_tup[2] in type_prediction.keys():
                                    type_prediction[saved_tup[2]]['existing'] += 1
                                else:
                                    type_prediction.update({saved_tup[2]: {'existing': 1, 'found':0}})

                            if saved_tup[3] == o_pred[1]:
                                if saved_tup[3] in type_prediction.keys():
                                    type_prediction[saved_tup[3]]['found'] += 1
                                    type_prediction[saved_tup[3]]['existing'] += 1
                                else:
                                    type_prediction.update({saved_tup[3]: {'existing': 1, 'found':1}}) 
                            else:
                                if saved_tup[3] in type_prediction.keys():
                                    type_prediction[saved_tup[3]]['existing'] += 1
                                else:
                                    type_prediction.update({saved_tup[3]: {'existing': 1, 'found':0}})
                            
                            os_tp_flag = True
                            s_class_name = saved_tup[2]
                            found = remove_entry(remove=saved_tup, structure=found, mode='multiple')
                            break
                       

                elif mode == 'perfect':
                    # count up with perfect matches
                    s_class_name = s_pred[1]
                    for tup in reference:
                        if tup[0] == s_pred[0] and found.get(tup) is None:
                            if tup[1] == o_pred[0] and found.get(tup) is None:  
                                if tup[2] == s_pred[1]:
                                    if tup[2] in type_prediction.keys():
                                        type_prediction[tup[2]]['found'] += 1
                                        type_prediction[tup[2]]['existing'] += 1
                                    else:
                                        type_prediction.update({tup[2]: {'existing': 1, 'found':1}}) 
                                else:
                                    if tup[2] in type_prediction.keys():
                                        type_prediction[tup[2]]['existing'] += 1
                                    else:
                                        type_prediction.update({tup[2]: {'existing': 1, 'found':0}})

                                if tup[3] == o_pred[1]:
                                    if tup[3] in type_prediction.keys():
                                        type_prediction[tup[3]]['found'] += 1
                                        type_prediction[tup[3]]['existing'] += 1
                                    else:
                                        type_prediction.update({tup[3]: {'existing': 1, 'found':1}}) 
                                else:
                                    if tup[3] in type_prediction.keys():
                                        type_prediction[tup[3]]['existing'] += 1
                                    else:
                                        type_prediction.update({tup[3]: {'existing': 1, 'found':0}})
                               
                                os_tp_flag = True
                                s_class_name = tup[2]
                                found = remove_entry(remove=tup, structure=found, mode='multiple')
                                break
                        
                elif mode in ('hard', 'soft'):
                    # count up with llm prompts (hard cut)
                    s_class_name = s_pred[1]
                    for tup in reference:
                        if found.get(tup) is None and 'y' in llm_query((s_pred[0], tup[0]), llm_log_path, mode):
                            if found.get(tup) is None and 'y' in llm_query((o_pred[0], tup[1]), llm_log_path, mode):
                                if tup[2] == s_pred[1]:
                                    if tup[2] in type_prediction.keys():
                                        type_prediction[tup[2]]['found'] += 1
                                        type_prediction[tup[2]]['existing'] += 1
                                    else:
                                        type_prediction.update({tup[2]: {'existing': 1, 'found':1}}) 
                                else:
                                    if tup[2] in type_prediction.keys():
                                        type_prediction[tup[2]]['existing'] += 1
                                    else:
                                        type_prediction.update({tup[2]: {'existing': 1, 'found':0}})

                                if tup[3] == o_pred[1]:
                                    if tup[3] in type_prediction.keys():
                                        type_prediction[tup[3]]['found'] += 1
                                        type_prediction[tup[3]]['existing'] += 1
                                    else:
                                        type_prediction.update({tup[3]: {'existing': 1, 'found':1}}) 
                                else:
                                    if tup[3] in type_prediction.keys():
                                        type_prediction[tup[3]]['existing'] += 1
                                    else:
                                        type_prediction.update({tup[3]: {'existing': 1, 'found':0}})

                                os_tp_flag = True
                                s_class_name = tup[2]
                                found = remove_entry(remove=tup, structure=found, mode='multiple')
                                break

                ## ---------- /count in different ways ----------- ##
                pred_classes_dict = detailed_storage(s_class_name, pred_classes_dict, os_tp_flag)

    #------------- calculate and print total metrics -------------#
    print(pred_classes_dict)
    class_eval = calculate_metrics_detailed(pred_classes_dict, pos_classes_dict, mode='class')
    class_df = pd.DataFrame.from_dict(data=class_eval, orient='index', columns=['F1', 'precision', 'recall'])
    class_df.to_csv(save_path)

    type_prediction_df = pd.DataFrame.from_dict(data=type_prediction, orient='index')
    type_prediction_df["procentage"] = type_prediction_df['found'] / type_prediction_df['existing']
    type_prediction_df.to_csv(save_types)


def eval_subject_object_predicate_classes_tricks(text_entries, save_path, mode='word_distance', llm_log_path=None):
    # evaluates the correctly found subjects only one of the three modes can be True
    pred_classes_dict = {}
    gt_classes_dict = {}
    found = {}

    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference = [(triplet['triplet']['subject'].lower(), triplet['triplet']['predicate'], triplet['triplet']['object'].lower(), triplet['triplet']['s_class'], triplet['triplet']['o_class']) for triplet in reference]
            reference = list(set(reference))

            #------- count the counter variables up ---------#
            for tup in reference:            
                # count the occurences of all classes within the reference
                if tup[1] not in gt_classes_dict.keys():
                    gt_classes_dict.update({tup[1]: 1})
                else:
                    gt_classes_dict[tup[1]] += 1

            # maybe I could also use the objects from the reference as a metric
            predictions_['content'] = [(triplet['subject']['label'].lower(), triplet['relation']['label'], triplet['object']['label'].lower(), triplet['subject']['s_class'], triplet['class_name']) for triplet in  predictions_['content']]

            # remove duplicates from the predictions 
            predictions_['content'] = list(set(predictions_['content']))
            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                #----------- Extract the RDF tuples ----------#
                 
                s_pred = (trips[0], trips[3])
                o_pred = (trips[2], trips[4])
                p_pred = trips[1]
                #---------- count the matches -------------#
                os_tp_flag = False
                ##----------count in different ways-------##
                
                if mode == 'word_distance':
                    saved_tups = []
                    s_class_name = p_pred
                    for tup in reference:
                        ratio = SequenceMatcher(lambda x: x==' ', s_pred[0], tup[0]).ratio() 
                        if ratio > 0.75 and found.get(tup) is None:  # assuming that the string are similar enough
                            saved_tups.append(tup)
                    
                    for saved_tup in saved_tups:  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
                        ratio = SequenceMatcher(lambda x: x==' ', o_pred[0], saved_tup[1]).ratio() 
                        if ratio > 0.75 and p_pred == saved_tup[1] and found.get(tup) is None:  # assuming that the string are similar enough 
                            os_tp_flag = True
                            s_class_name = saved_tup[1]
                            found = remove_entry(remove=saved_tup, structure=found, mode='multiple')

                elif mode == 'perfect':
                    # count up with perfect matches
                    s_class_name = p_pred
                    for tup in reference:
                        if tup[0] == s_pred[0] and found.get(tup) is None:
                            if tup[1] == o_pred[0] and found.get(tup) is None:
                                if p_pred == tup[1] and found.get(tup) is None:
                                    os_tp_flag = True
                                    s_class_name = tup[1]
                                    found = remove_entry(remove=tup, structure=found, mode='multiple')
                                    break
                        
                elif mode in ('hard', 'soft'):
                    # count up with llm prompts (hard cut)
                    s_class_name = p_pred
                    for tup in reference:
                        if  found.get(tup) is None and 'y' in llm_query((s_pred[0], tup[0]), llm_log_path, mode):
                            if found.get(tup) is None and 'y' in llm_query((o_pred[0], tup[1]), llm_log_path, mode):
                                if p_pred == tup[1]  and found.get(tup) is None:
                                    os_tp_flag = True
                                    s_class_name = tup[1]
                                    found = remove_entry(remove=tup, structure=found, mode='multiple')
                                    break

                ## ---------- /count in different ways ----------- ##
                pred_classes_dict = detailed_storage(s_class_name, pred_classes_dict, os_tp_flag)

                  
    #------------- calculate and print total metrics -------------#
    print(pred_classes_dict)
    class_eval = calculate_metrics_detailed(pred_classes_dict, gt_classes_dict, mode='class', with_n=True)
    class_df = pd.DataFrame.from_dict(data=class_eval, orient='index', columns=['F1', 'precision', 'recall', 'N'])
    class_df.to_csv(save_path)



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
        ################################################################################################################################

        try:
            mode = self._config['mode']
            eval = self._config['eval']
        except KeyError:
            # maybe not raise and only tell about the issue and that no evaluation took place
            raise KeyError('An evaluation scheme (subject, object, subject_object, subject_object_predciates) and a mode (word_distance, perfect, soft, hard) needs to be given!')
        else:
            ###################################### this part is only for the beginning and is not planned to be used in the end #############################################################
            # ---------------------------------- Evaluate all four schemes with a classes focus -------------------------------------
            if tricks:
                if eval == 'subject':
                    eval_subject_accuracy_classes_tricks(text_entries, save_path=f'../test/gollie_testset/subjects/classes_{mode}_tricks.csv', save_types=f'../test/gollie_testset/subjects/types_{mode}_tricks.csv', mode=mode, llm_log_path=f'../test/gollie_testset/subjects/llm_mitschrift_{mode}_classes_tricks.json')
                    print('subjects done')
                elif eval == 'object':
                    eval_object_accuracy_classes_tricks(text_entries, save_path=f'../test/gollie_testset/objects/classes_{mode}_tricks.csv', save_types=f'../test/gollie_testset/objects/types_{mode}_tricks.csv', mode=mode, llm_log_path=f'../test/gollie_testset/objects/llm_mitschrift_{mode}_classes_tricks.json')
                    print('objects done')
                elif eval == 'subject_object':
                    eval_subject_object_accuracy_classes_tricks(text_entries, save_path=f'../test/gollie_testset/subject_object/classes_{mode}_tricks.csv', save_types=f'../test/gollie_testset/subject_object/types_{mode}_tricks.csv', mode=mode, llm_log_path=f'../test/gollie_testset/subject_object/llm_mitschrift_{mode}_classes_tricks.json')
                    print('subject_object_done')
                elif eval == 'subject_object_predicate':
                    eval_subject_object_predicate_classes_tricks(text_entries, save_path=f'../test/gollie_testset/subject_object_predicate/predicates_{mode}_tricks.csv', mode=mode, llm_log_path=f'../test/gollie_testset/subject_object_predicate/llm_mitschrift_{mode}_predicates_tricks.json')
                    print('Subject_object_predicate done')
            #####################################################################################################################################################################################

            # --------------------------------- Evaluate all four schemes without classes focus ---------------------------------------------------- #
            else:
                if eval == 'subject':
                    eval_subject_accuracy(text_entries, save_path=f'../test/gollie_testset/subjects/subject_eval_{mode}.csv', mode=mode, llm_log_path=f'../test/gollie_testset/subjects/llm_mitschrift_{mode}_eval.json')
                    print('subjects done')
                elif eval == 'object':
                    eval_object_accuracy(text_entries, save_path=f'../test/gollie_testset/objects/object_eval_{mode}.csv', mode=mode, llm_log_path=f'../test/gollie_testset/objects/llm_mitschrift_{mode}_eval.json')
                    print('objects done')
                elif eval == 'subject_object':
                    eval_subject_object_accuracy(text_entries, save_path=f'../test/gollie_testset/subject_object/subject_object_eval_{mode}.csv', mode=mode, llm_log_path=f'../test/gollie_testset/subject_object/llm_mitschrift_{mode}_eval.json')
                    print('subject_object_done')
                elif eval == 'subject_object_predicate':
                    eval_subject_object_predicate(text_entries, save_path=f'../test/gollie_testset/subject_object_predicate/subject_object_predicate_eval_{mode}.csv', mode=mode, llm_log_path=f'../test/gollie_testset/subject_object_predicate/llm_mitschrift_{mode}_eval.json')
                    print('Subject_object_predicate done')
        
        yield text_entries
