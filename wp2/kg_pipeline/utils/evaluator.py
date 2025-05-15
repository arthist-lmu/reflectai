from typing import List, Dict, Generator
import json
import numpy as np
import pandas as pd
from kg_pipeline.manager import Manager
#import Levenshtein as ls
from difflib import SequenceMatcher
from kg_pipeline.plugin import Plugin
from ollama import Client, _types
#import asyncio
import re


client = Client(
  host='devbox2.research.tib.eu'
)


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
    scores: lists the values {s_tp, s_total_pred, s_total_pos, po_tp, po_total_pred, po_total_pos}
    """
    if key in dct.keys():
        #values_keys = ['s_tp', 's_total_pre', 's_total_pos', 'po_tp', 'po_total_pre']
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
    if mode == 'single':
        for triplet in structure:
            if triplet[0] == remove:
                return structure.remove(triplet)
    elif mode == 'multiple':
        for triplet in structure:
            found_flag = True
            for i, element in enumerate(triplet[:-1]):
                if element != remove[i]:
                    found_flag = False
                    break

            if found_flag:
                return structure.remove(triplet)


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
            if s_total_pos < s_tp:
                s_recall = -1
                s_f1_score = -1
            
            if with_n:
                scores = [s_f1_score, s_precision, s_recall, s_total_pre]
            else:
                scores = [s_f1_score, s_precision, s_recall]

            results.update({key: scores})

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
        'semantically describe the same thing? Note that both terms should only be equal if it is either exactly the same or '\
        'is in plural/singular form. Furthermore slight variations like one of the terms including information while the other does not. e.g. the first name of a person or the full name of a location.'\
        'This also includes cases in where one term uses punctuation marks like an apostrophe while the other does not or in cases where the one term is the abbreviation of the other. They are also equal,' \
        'when one term uses article and such.'\
        'It should not be equal e.g. if one of the terms includes more information than just stated or if one term is a subcategory or instance of the other term. Answer with only yes and no.'
    flag = True  

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
    #print('y' in resp[end:])
    return resp[end:]



def distingush_subjects(entry):
    # distingushes between subjects that are the same as the name of the painting and all the orther ones
    name_trips = []
    other_trips = []

    ref_name_trips = []
    ref_non_name_trips = []
    try:
        names = re.search('[a-zA-Z„"][a-zA-Z0-9 äüöÄÖÜ()"“,-\.]+\n\n', entry['text']).group()[:-2]
        for predictions in entry['triplets']:
            for triplet in predictions['content']:
                if triplet['subject']['label'] == names:
                    name_trips.append(triplet)
                else:
                    other_trips.append(triplet)

            
        for s, po in entry['annotations'].items():
            if s == names:
                ref_name_trips.append({s:po})
            else:
                ref_non_name_trips.append({s:po})

    except AttributeError:
        print('No name found in: ', entry['text'][:20])

    

    return name_trips, other_trips, ref_name_trips, ref_non_name_trips



def eval_subject_equals_name(entry):

    #------------- initializing variables for this entry -----------------------#
    name_trips, non_name_trips, ref_name_trips, ref_non_name_trips = distingush_subjects(entry)

    name_s_total_pre = name_po_total_pre = len(name_trips)
    non_s_total_pre = non_po_total_pre = len(non_name_trips)

    name_s_total_pos = 0
    name_po_total_pos = 0
    
    
    non_s_total_pos = 0
    non_po_total_pos = 0

    # name_po_total_pre = 0
    # non_po_total_pre = 0
 
    for triplets in ref_name_trips:
        for po in triplets.values():
            for s, o in po.items():
                if s != 's_class_name':
                    if type(o[0]) == list:
                        name_s_total_pos += len(o[0])
                    else:
                        name_s_total_pos += 1


    for triplets in ref_non_name_trips:
        for po in triplets.values():
            for s, o in po.items():
                if s != 's_class_name':
                    if type(o[0]) == list:
                        non_s_total_pos += len(o[0])
                    else:
                        non_s_total_pos += 1


    for trips in ref_name_trips:
        for values in trips.values():
            for p, o in values.items():
                if p != 's_class_name':
                    if type(o[0]) == list:
                        name_po_total_pos += len(o[0])
                    else:
                        name_po_total_pos += 1


    for trips in ref_non_name_trips:
        for values in trips.values():
            for p, o in values.items():
                if p != 's_class_name':
                    if type(o[0]) == list:
                        non_po_total_pos += len(o[0])
                    else:
                        non_po_total_pos += 1
    
    s_name_tp = 0
    s_non_name_tp = 0

    s_po_name_tp = 0
    s_po_non_name_tp = 0
    
    #-------------- evaluation process for the trips with subject equals painting name -------------------#
    for name in name_trips:
        s_pred = name['subject']['label']
        p_pred = name['relation']['label']
        o_pred = name['object']['label']

        #---------- check for the most fitting refrence key subject from the prediction ----------------------# 
        candidate = ('', 0) 
        for ref_trip in ref_name_trips:
            ref_key = next(iter(ref_trip))
            ratio = SequenceMatcher(lambda x: x==' ', s_pred.lower(), ref_key.lower()).ratio() 

            # if ratio is big enough, the respective ref_key is to be taken instead of the acutal prediction
            if ratio > 0.75:  # assuming that the string are similar enough
                if candidate[1] < ratio:
                    candidate = (ref_key, ratio)
        

        ####
        #candidate = ('upper part', )
        ####
        if candidate[0] != '':  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
            s_name_tp += 1

            #---------------------- check for the most fitting refrence key predicate from the prediction -------------#
            predicate_candidate = ('', 0)
            # fetch the correct predicate
            for ref_trips in ref_name_trips:
                if candidate[0] in ref_trips:
                    correct_trip = ref_trips  # SAVE THIS TRIP SOMEWHERE EARLIER!

            for p in correct_trip[candidate[0]].keys():
                ratio = SequenceMatcher(lambda x: x==' ', p_pred.lower(), p.lower()).ratio() 
                if ratio > 0.75:  # assuming that the string are similar enough
                    if predicate_candidate[1] < ratio:
                        predicate_candidate = (p, ratio)

            ###
            #predicate_candidate = ('depicts',)
            ###
            
            if predicate_candidate[0] != '':
                # check whether the the predicated objects are wihtin the reference
                coond1 = type(correct_trip[candidate[0]][predicate_candidate[0]][0]) == list 

                #---------------------- check for the most fitting refrence key object from the prediction -------------#
                object_candidate = ('', 0)
                if coond1:
                    for o in correct_trip[candidate[0]][predicate_candidate[0]][0]:
                        ratio = SequenceMatcher(lambda x: x==' ', o_pred.lower(), o.lower()).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough
                            if object_candidate[1] < ratio:
                                object_candidate = (o, ratio)

                else:
                    o = correct_trip[candidate[0]][predicate_candidate[0]][0]
                    ratio = SequenceMatcher(lambda x: x==' ', o_pred.lower(), o.lower()).ratio() 
                    if ratio > 0.75:  # assuming that the string are similar enough
                        if object_candidate[1] < ratio:
                            object_candidate = (o, ratio)

                ####
                #object_candidate = ('cometary beam of light',)
                ####
                
                if object_candidate[0] != '':
                    s_po_name_tp += 1

                    # remove the triplet from refrence to avoid wrongfully counting found triplets
                    remove_entry(object_candidate[0], ref_name_trips, candidate[0], predicate_candidate[0], mode='split')

    
    #-------------- evaluation process for the trips with subject equals painting name -------------------#
    for name in non_name_trips:
        s_pred = name['subject']['label']
        p_pred = name['relation']['label']
        o_pred = name['object']['label']

        #---------- check for the most fitting refrence key subject from the prediction ----------------------# 
        candidate = ('', 0) 
        for ref_trip in ref_non_name_trips:
            ref_key = next(iter(ref_trip))
            ratio = SequenceMatcher(lambda x: x==' ', s_pred.lower(), ref_key.lower()).ratio() 

            # if ratio is big enough, the respective ref_key is to be taken instead of the acutal prediction
            if ratio > 0.75:  # assuming that the string are similar enough
                if candidate[1] < ratio:
                    candidate = (ref_key, ratio)
        

        ####
        #candidate = ('upper part', )
        ####
        if candidate[0] != '':  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
            s_non_name_tp += 1

            #---------------------- check for the most fitting refrence key predicate from the prediction -------------#
            predicate_candidate = ('', 0)
            # fetch the correct predicate
            for ref_trips in ref_non_name_trips:
                if candidate[0] in ref_trips:
                    correct_trip = ref_trips  # SAVE THIS TRIP SOMEWHERE EARLIER!

            for p in correct_trip[candidate[0]].keys():
                ratio = SequenceMatcher(lambda x: x==' ', p_pred.lower(), p.lower()).ratio() 
                if ratio > 0.75:  # assuming that the string are similar enough
                    if predicate_candidate[1] < ratio:
                        predicate_candidate = (p, ratio)

            ###
            #predicate_candidate = ('depicts',)
            ###
            
            if predicate_candidate[0] != '':
                # check whether the the predicated objects are wihtin the reference
                coond1 = type(correct_trip[candidate[0]][predicate_candidate[0]][0]) == list 

                #---------------------- check for the most fitting refrence key object from the prediction -------------#
                object_candidate = ('', 0)
                if coond1:
                    for o in correct_trip[candidate[0]][predicate_candidate[0]][0]:
                        ratio = SequenceMatcher(lambda x: x==' ', o_pred.lower(), o.lower()).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough
                            if object_candidate[1] < ratio:
                                object_candidate = (o, ratio)

                else:
                    o = correct_trip[candidate[0]][predicate_candidate[0]][0]
                    ratio = SequenceMatcher(lambda x: x==' ', o_pred.lower(), o.lower()).ratio() 
                    if ratio > 0.75:  # assuming that the string are similar enough
                        if object_candidate[1] < ratio:
                            object_candidate = (o, ratio)

                ####
                #object_candidate = ('cometary beam of light',)
                ####
                
                if object_candidate[0] != '':
                    s_po_non_name_tp += 1

                    # remove the triplet from refrence to avoid wrongfully counting found triplets
                    remove_entry(object_candidate[0], ref_non_name_trips, candidate[0], predicate_candidate[0], mode='split')

    #print('finished!')
    return name_s_total_pre, name_po_total_pre, name_s_total_pos, name_po_total_pos, non_s_total_pre,\
    non_po_total_pre, non_s_total_pos, non_po_total_pos, s_name_tp, s_non_name_tp, s_po_name_tp, s_po_non_name_tp



def eval_subject_predicate_object_pair(entry):
    # evaluates the correctly found subjects and predicate object pairs

    s_tp = s_total_pos = s_total_pre = 0
    po_tp = po_total_pos = po_total_pre = 0
    
    
    pred_predicates_dict = {}
    pred_classes_dict = {}
    pos_classes_dict = {}
    pos_predicates_dict = {}

    for predictions_ in entry['triplets']:
            # predictions_['content'] = filter_out_semantically_identicals(predictions=predictions_['content'])
            # predictions_['content'] = filter_out_semantically_identicals(predictions=predictions_['content'], mode=1)

            reference = entry['annotations']
            ref_keys = reference.keys()

            #--------- initialize / set the counter variables ------------#
            s_current_pos = len(ref_keys)
            s_total_pos += len(ref_keys)
            po_current_pos = 0

            s_current_pre = 0
            po_current_pre = 0

            s_tp_current = 0
            po_tp_current = 0
            
            #------- count the counter variables up ---------#
            for _ , ref_po_pairs in reference.items():
                # count the occurences of all classes within the refrence
                s_class = ref_po_pairs['s_class_name']
                if s_class not in pos_classes_dict.keys():
                    pos_classes_dict.update({s_class: 1})
                else:
                    pos_classes_dict[s_class] += 1
                    
                # count the number of objects for all the predicates, i.e. not diferentiating between them
                for p, ref_objects in ref_po_pairs.items():
                    if p != 's_class_name':
                        # PRÜFE HIER NOCHEINMAL NACH; OB DAS SO IST WIE ICH DAS DENKE
                        if p not in pos_predicates_dict.keys():
                            if type(ref_objects[0]) == list:
                                pos_predicates_dict.update({p:len(ref_objects[0])})
                                po_total_pos += len(ref_objects[0])
                                po_current_pos += len(ref_objects[0])
                            else:
                                pos_predicates_dict.update({p:1})
                                po_total_pos += 1
                                po_current_pos += 1
                        else:
                            if type(ref_objects[0]) == list:
                                pos_predicates_dict[p] += len(ref_objects[0])
                                po_total_pos += len(ref_objects[0])
                                po_current_pos += len(ref_objects[0])
                            else:
                                pos_predicates_dict[p] += 1
                                po_total_pos += 1
                                po_current_pos += 1

            # remove duplicates from the predictions 
            predictions_['content'] = [i for n, i in enumerate(predictions_['content']) if i not in predictions_['content'][n + 1:]]
            for trips in predictions_['content']:
                s_total_pre += 1
                po_total_pre += 1
                s_current_pre += 1
                po_current_pre += 1

            
                #----------- Extract the RDF tuples ----------#
                s_pred = trips['subject']['label']
                p_pred = trips['relation']['label']
                o_pred = trips['object']['label']
                if 'class_name' in trips.keys():
                    class_name = trips['class_name']

                pred_po_pairs = {p_pred: o_pred}

                #---------- count the matches -------------#
                s_tp_flag = False
                po_class_tp = 0

                candidate = ('', 0)
                for ref_key in ref_keys:
                    ratio = SequenceMatcher(lambda x: x==' ', s_pred.lower(), ref_key.lower()).ratio() 
                    # IF RATIO IS BIG ENOUGH; THE RESPECTIVE REF KEY IS TO BE TAKEN INSTEAD OF THE ACUTAL PREDICTION!
                    if ratio > 0.75:  # ssuming that the string are similar enough
                        if candidate[1] < ratio:
                            candidate = (ref_key, ratio)
                
                if candidate[0] != '':  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
                    s_tp_flag = True
                    s_tp += 1
                    s_tp_current += 1 
                    
                    for predicate, objects in pred_po_pairs.items():

                        # check whether the predicate is indeed within the refrence

                        #---------- since the focus for now lies within the 'depitcs' relations everything else is skipped -----------#
                        # if predicate != 'depicts':
                        #     continue 
                        #--------------------------------------------------------#
                        predicate_candidate = ('', 0)
                        for p in reference[candidate[0]].keys():
                            ratio = SequenceMatcher(lambda x: x==' ', predicate.lower(), p.lower()).ratio() 
                            # IF RATIO IS BIG ENOUGH; THE RESPECTIVE REF KEY IS TO BE TAKEN INSTEAD OF THE ACUTAL PREDICTION!
                            if ratio > 0.75:  # assuming that the string are similar enough
                                if predicate_candidate[1] < ratio:
                                    predicate_candidate = (p, ratio)

                        if predicate_candidate[0] != '':

                            po_class_tp = 0
                            # check whether the the predicated objects are wihtin the reference
                            coond1 = type(reference[candidate[0]][predicate_candidate[0]][0]) == list 
                            #coond2 = objects in reference[candidate[0]][predicate_candidate[0]]

                            object_candidate = ('', 0)
                            if coond1:
                                for o in reference[candidate[0]][predicate_candidate[0]][0]:
                                    ratio = SequenceMatcher(lambda x: x==' ', objects.lower(), o.lower()).ratio() 
                                    # IF RATIO IS BIG ENOUGH; THE RESPECTIVE REF KEY IS TO BE TAKEN INSTEAD OF THE ACUTAL PREDICTION!
                                    if ratio > 0.75:  # assuming that the string are similar enough
                                        if object_candidate[1] < ratio:
                                            object_candidate = (o, ratio)

                            else:
                                o = reference[candidate[0]][predicate_candidate[0]][0]
                                ratio = SequenceMatcher(lambda x: x==' ', objects.lower(), o.lower()).ratio() 
                                # IF RATIO IS BIG ENOUGH; THE RESPECTIVE REF KEY IS TO BE TAKEN INSTEAD OF THE ACUTAL PREDICTION!
                                if ratio > 0.75:  # assuming that the string are similar enough
                                    if object_candidate[1] < ratio:
                                        object_candidate = (o, ratio)

                            if object_candidate[0] != '':
                                po_tp += 1
                                po_tp_current += 1
                                po_class_tp += 1
                                # remove the triplet from refrence to avoid wrongfully counting found triplets

                                remove_entry(object_candidate[0], reference, candidate[0], predicate_candidate[0])
                    
                try:
                    pred_classes_dict = detailed_storage(class_name, pred_classes_dict, s_tp_flag, po_class_tp)
                    pred_predicates_dict = detailed_storage(p_pred, pred_predicates_dict, s_tp_flag, po_class_tp)
                    detailed = True
                except UnboundLocalError:
                    #print('Not in classes mode. Operating without taking classes into account!')
                    detailed = False
                
            #------------- calculate and print current metrics -------------#
            #calculate_metrics(s_tp_current, s_current_pre, s_current_pos, po_tp_current, po_current_pre, po_current_pos, i)
    #KONTROLIERE NOCHMLA WIESO ES SEIN KANN; DASS RECALL ÜBER 100 PROZENNT HAT:   

    #------------- calculate and print total metrics -------------#
    if detailed:
        #print('predicates')
        pred_eval = calculate_metrics_detailed(pred_predicates_dict, pred_classes_dict, pos_classes_dict, pos_predicates_dict, mode='predicates')
        pred_df = pd.DataFrame.from_dict(data=pred_eval, orient='index', columns=['F1', 'prediction', 'recall'])
        pred_df.to_csv('../test/gollie_testset/predicates_accuracy_alt.csv')
        
        #print('classes')
        class_eval = calculate_metrics_detailed(pred_predicates_dict, pred_classes_dict, pos_classes_dict, pos_predicates_dict, mode='class')
        class_df = pd.DataFrame.from_dict(data=class_eval, orient='index', columns=['F1', 'prediction', 'recall'])
        class_df.to_csv('../test/gollie_testset/classes_accuracy_alt.csv')

    s_scores, po_scores = calculate_metrics(s_tp, s_total_pre, s_total_pos, po_tp, po_total_pre, po_total_pos)

    s_scores.to_csv('../test/gollie_testset/subject_eval_alt.csv')
    po_scores.to_csv('../test/gollie_testset/predicate_object_eval_alt.csv')




def eval_subject_accuracy(text_entries, mode='word_distance'):
    
    # evaluates the correctly found subjects only one of the three modes can be True
    s_tp = s_total_pos = s_total_pre = 0
    
    pred_classes_dict = {}
    pos_classes_dict = {}

    detailed = False
    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference = [(triplet['triplet']['subject'], triplet['triplet']['s_class']) for triplet in reference]
            reference = list(set(reference))

            #------- count the counter variables up ---------#
            s_total_pos += len(reference)
            print(reference)
            for tup in reference:            
                # count the occurences of all classes within the reference
                if tup[1] not in pos_classes_dict.keys():
                    pos_classes_dict.update({tup[1]: 1})
                else:
                    pos_classes_dict[tup[1]] += 1


            predictions_['content'] = [(triplet['subject']['label'], triplet['class_name']) for triplet in  predictions_['content']]

            # remove duplicates from the predictions 
            #predictions_['content'] = [i for n, i in enumerate(predictions_['content']) if i not in predictions_['content'][n + 1:]]
            predictions_['content'] = list(set(predictions_['content']))
            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                s_total_pre += 1
            
                #----------- Extract the RDF tuples ----------#
                s_pred = trips[0]
                # p_pred = trips['relation']['label']
                # o_pred = trips['object']['label']
                #if 'class_name' in trips: maybe later I can see if it works without -k
                class_name = trips[1]

                #---------- count the matches -------------#
                s_tp_flag = False
                ##----------count in different ways-------##
                
                if mode == 'word_distance':
                    candidate = ('', 0, None)
                    for tup in reference:
                        ratio = SequenceMatcher(lambda x: x==' ', s_pred.lower(), tup[0].lower()).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough
                            if candidate[1] < ratio:
                                candidate = (tup[0], ratio)
                    
                    if candidate[0] != '':  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
                        s_tp_flag = True
                        s_tp += 1

                        remove_entry(remove=candidate[0], structure=reference)
                elif mode == 'perfect':
                    # count up with perfect matches
                    for tup in reference:
                        if tup[0].lower() == s_pred.lower():
                            s_tp_flag = True
                            s_tp += 1
                            remove_entry(remove=s_pred, structure=reference)
                            break
                        
                elif mode == 'hard':
                    # count up with llm prompts (hard cut)
                    
                    for tup in reference:
                        if 'y' in llm_query((s_pred, tup[0]), '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt.json', mode):
                            s_tp_flag = True
                            s_tp += 1
                            remove_entry(remove=s_pred, structure=reference)
                            break
                            
                elif mode == 'soft':
                    # count up with llm prompts (soft cut)
                    for tup in reference:
                        if 'y' in llm_query((s_pred, tup[0]), '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt.json', mode):
                            s_tp_flag = True
                            s_tp += 1
                            remove_entry(remove=s_pred, structure=reference)
                            break

                ## ---------- /count in different ways ----------- ##
                # ------------ count detailed ------------ #
                try:
                    pred_classes_dict = detailed_storage(class_name, pred_classes_dict, s_tp_flag)
                    #pred_predicates_dict = detailed_storage(p_pred, pred_predicates_dict, s_tp_flag)
                    detailed = True
                except UnboundLocalError:
                    #print('Not in classes mode. Operating without taking classes into account!')
                    detailed = False
                
    #KONTROLIERE NOCHMLA WIESO ES SEIN KANN; DASS RECALL ÜBER 100 PROZENNT HAT:   
    #------------- calculate and print total metrics -------------#
    if detailed:   
        class_eval = calculate_metrics_detailed(pred_classes_dict, pos_classes_dict, mode='class')
        class_df = pd.DataFrame.from_dict(data=class_eval, orient='index', columns=['F1', 'precision', 'recall'])
        class_df.to_csv('../test/gollie_testset/subjects/classes_accuracy.csv')

    s_scores = calculate_metrics(s_tp, s_total_pre, s_total_pos)

    s_scores.to_csv('../test/gollie_testset/subjects/subject_eval.csv')



def eval_object_accuracy(text_entries, mode='word_distance'):
    # evaluates the correctly found subjects only one of the three modes can be True
    o_tp = o_total_pos = o_total_pre = 0
    
    pred_classes_dict = {}
    pos_classes_dict = {}

    detailed = False
    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference = [(triplet['triplet']['object'], triplet['triplet']['s_class']) for triplet in reference]
            reference = list(set(reference))

            #------- count the counter variables up ---------#
            o_total_pos += len(reference)
            
            for tup in reference:            
                # count the occurences of all classes within the reference
                if tup[1] not in pos_classes_dict.keys():
                    pos_classes_dict.update({tup[1]: 1})
                else:
                    pos_classes_dict[tup[1]] += 1

            # maybe I could also use the objects from the reference as a metric
            predictions_['content'] = [(triplet['object']['label'], triplet['class_name']) for triplet in  predictions_['content']]

            # remove duplicates from the predictions 
            #predictions_['content'] = [i for n, i in enumerate(predictions_['content']) if i not in predictions_['content'][n + 1:]]
            predictions_['content'] = list(set(predictions_['content']))
            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                o_total_pre += 1
            
                #----------- Extract the RDF tuples ----------#
                #s_pred = trips[0]
                # p_pred = trips['relation']['label']
                o_pred = trips[0]
                #if 'class_name' in trips: maybe later I can see if it works without -k
                class_name = trips[1]

                #---------- count the matches -------------#
                o_tp_flag = False
                ##----------count in different ways-------##
                
                if mode == 'word_distance':
                    candidate = ('', 0, None)
                    for tup in reference:
                        ratio = SequenceMatcher(lambda x: x==' ', o_pred.lower(), tup[0].lower()).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough
                            if candidate[1] < ratio:
                                candidate = (tup[0], ratio)
                    
                    if candidate[0] != '':  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
                        o_tp_flag = True
                        o_tp += 1

                        remove_entry(remove=candidate[0], structure=reference)
                elif mode == 'perfect':
                    # count up with perfect matches
                    for tup in reference:
                        if tup[0].lower() == o_pred.lower():
                            o_tp_flag = True
                            o_tp += 1
                            remove_entry(remove=o_pred, structure=reference)
                            break
                        
                elif mode == 'hard':
                    # count up with llm prompts (hard cut)
                    for tup in reference:
                        if 'y' in llm_query((o_pred, tup[0]), '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_objekt.json', mode):
                            o_tp_flag = True
                            o_tp += 1
                            remove_entry(remove=o_pred, structure=reference)
                            break
                            
                elif mode == 'soft':
                    # count up with llm prompts (soft cut)
                    for tup in reference:
                        if 'y' in llm_query((o_pred, tup[0]), '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_objekt.json', mode):
                            o_tp_flag = True
                            o_tp += 1
                            remove_entry(remove=o_pred, structure=reference)
                            break

                ## ---------- /count in different ways ----------- ##
                # ------------ count detailed ------------ #
                try:
                    pred_classes_dict = detailed_storage(class_name, pred_classes_dict, o_tp_flag)
                    #pred_predicates_dict = detailed_storage(p_pred, pred_predicates_dict, s_tp_flag)
                    detailed = True
                except UnboundLocalError:
                    #print('Not in classes mode. Operating without taking classes into account!')
                    detailed = False
                
    #KONTROLIERE NOCHMLA WIESO ES SEIN KANN; DASS RECALL ÜBER 100 PROZENNT HAT:   
    #------------- calculate and print total metrics -------------#
    if detailed:   
        class_eval = calculate_metrics_detailed(pred_classes_dict, pos_classes_dict, mode='class')
        class_df = pd.DataFrame.from_dict(data=class_eval, orient='index', columns=['F1', 'precision', 'recall'])
        class_df.to_csv('../test/gollie_testset/objects/classes_accuracy.csv')

    o_scores = calculate_metrics(o_tp, o_total_pre, o_total_pos)

    o_scores.to_csv('../test/gollie_testset/objects/object_eval.csv')


def eval_subject_object_accuracy(text_entries, mode='word_distance'):
     # evaluates the correctly found subjects only one of the three modes can be True
    os_tp = os_total_pos = os_total_pre = 0
    
    pred_classes_dict = {}
    pos_classes_dict = {}

    detailed = False
    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference = [(triplet['triplet']['subject'], triplet['triplet']['object'], triplet['triplet']['s_class']) for triplet in reference]
            reference = list(set(reference))

            #------- count the counter variables up ---------#
            os_total_pos += len(reference)
            
            for tup in reference:            
                # count the occurences of all classes within the reference
                if tup[2] not in pos_classes_dict.keys():
                    pos_classes_dict.update({tup[2]: 1})
                else:
                    pos_classes_dict[tup[2]] += 1

            # maybe I could also use the objects from the reference as a metric
            predictions_['content'] = [(triplet['subject']['label'], triplet['object']['label'], triplet['class_name']) for triplet in  predictions_['content']]

            # remove duplicates from the predictions 
            #predictions_['content'] = [i for n, i in enumerate(predictions_['content']) if i not in predictions_['content'][n + 1:]]
            predictions_['content'] = list(set(predictions_['content']))
            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                os_total_pre += 1
            
                #----------- Extract the RDF tuples ----------#
                s_pred = trips[0]
                # p_pred = trips['relation']['label']
                o_pred = trips[1]
                #if 'class_name' in trips: maybe later I can see if it works without -k
                class_name = trips[2]

                #---------- count the matches -------------#
                os_tp_flag = False
                ##----------count in different ways-------##
                
                if mode == 'word_distance':
                    candidate = ('', 0)
                    saved_tup = ()
                    for tup in reference:
                        ratio = SequenceMatcher(lambda x: x==' ', s_pred.lower(), tup[0].lower()).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough
                            if candidate[1] < ratio:
                                candidate = (tup[0], ratio)
                                saved_tup = tup
                    
                    if candidate[0] != '':  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
                        ratio = SequenceMatcher(lambda x: x==' ', o_pred.lower(), saved_tup[1].lower()).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough 
                            os_tp_flag = True
                            os_tp += 1
                            remove_entry(remove=(saved_tup[0], saved_tup[1]), structure=reference, mode='multiple')

                elif mode == 'perfect':
                    # count up with perfect matches
                    for tup in reference:
                        if tup[0].lower() == s_pred.lower():
                            if tup[1].lower() == o_pred.lower():
                                os_tp_flag = True
                                os_tp += 1
                                remove_entry(remove=(s_pred, o_pred), structure=reference, mode='multiple')
                                break
                        
                elif mode == 'hard':
                    # count up with llm prompts (hard cut)
                    for tup in reference:
                        if 'y' in llm_query((s_pred, tup[0]), '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt.json',mode):
                            if 'y' in llm_query((o_pred, tup[1]), '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt.json', mode):
                                os_tp_flag = True
                                os_tp += 1
                                remove_entry(remove=(s_pred, o_pred), structure=reference, mode='multiple')
                                break
                            
                elif mode == 'soft':
                    # count up with llm prompts (soft cut)
                    for tup in reference:
                        if 'y' in llm_query((s_pred, tup[0]), '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt.json',mode):
                            if 'y' in llm_query((o_pred, tup[1]), '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt.json',mode):
                                os_tp_flag = True
                                os_tp += 1
                                remove_entry(remove=(s_pred, o_pred), structure=reference, mode='multiple')
                                break

                ## ---------- /count in different ways ----------- ##
                # ------------ count detailed ------------ #
                try:
                    pred_classes_dict = detailed_storage(class_name, pred_classes_dict, os_tp_flag)
                    #pred_predicates_dict = detailed_storage(p_pred, pred_predicates_dict, s_tp_flag)
                    detailed = True
                except UnboundLocalError:
                    #print('Not in classes mode. Operating without taking classes into account!')
                    detailed = False
                
    #KONTROLIERE NOCHMLA WIESO ES SEIN KANN; DASS RECALL ÜBER 100 PROZENNT HAT:   
    #------------- calculate and print total metrics -------------#
    if detailed:   
        class_eval = calculate_metrics_detailed(pred_classes_dict, pos_classes_dict, mode='class')
        class_df = pd.DataFrame.from_dict(data=class_eval, orient='index', columns=['F1', 'precision', 'recall'])
        class_df.to_csv('../test/gollie_testset/subject_object/classes_accuracy.csv')

    s_scores = calculate_metrics(os_tp, os_total_pre, os_total_pos)

    s_scores.to_csv('../test/gollie_testset/subject_object/subject_object_eval.csv')


def eval_subject_object_predicate(text_entries, mode='word_distance'):
    # evaluates the correctly found subjects only one of the three modes can be True
    p_tp = p_total_pos = p_total_pre = 0
    
    pred_classes_dict = {}
    pos_classes_dict = {}

    pred_predicates_dict = {}
    pos_predicates_dict = {}    

    detailed = False
    for entry in text_entries:
        for predictions_ in entry['triplets']:
            reference = entry['annotations']
            reference = convert_annotation_to_triplet(reference)
            reference = [(triplet['triplet']['subject'], triplet['triplet']['predicate'], triplet['triplet']['object'], triplet['triplet']['s_class']) for triplet in reference]
            reference = list(set(reference))

            #------- count the counter variables up ---------#
            p_total_pos += len(reference)
            
            for tup in reference:            
                # count the occurences of all classes within the reference
                if tup[3] not in pos_classes_dict.keys():
                    pos_classes_dict.update({tup[3]: 1})
                else:
                    pos_classes_dict[tup[3]] += 1

                if tup[1] not in pos_classes_dict.keys():
                    pos_predicates_dict.update({tup[1]: 1})
                else:
                    pos_predicates_dict[tup[1]] += 1
                

            # maybe I could also use the objects from the reference as a metric
            predictions_['content'] = [(triplet['subject']['label'], triplet['relation']['label'], triplet['object']['label'], triplet['class_name']) for triplet in  predictions_['content']]

            # remove duplicates from the predictions 
            #predictions_['content'] = [i for n, i in enumerate(predictions_['content']) if i not in predictions_['content'][n + 1:]]
            predictions_['content'] = list(set(predictions_['content']))
            # -------- main evaluation process ----------#
            for trips in predictions_['content']:
                p_total_pre += 1
            
                #----------- Extract the RDF tuples ----------#
                s_pred = trips[0]
                p_pred = trips[1]
                o_pred = trips[2]
                #if 'class_name' in trips: maybe later I can see if it works without -k
                class_name = trips[3]

                #---------- count the matches -------------#
                p_tp_flag = False
                ##----------count in different ways-------##
                
                if mode == 'word_distance':
                    candidate = ('', 0)
                    saved_tup = ()
                    for tup in reference:
                        ratio = SequenceMatcher(lambda x: x==' ', s_pred.lower(), tup[0].lower()).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough
                            if candidate[1] < ratio:
                                candidate = (tup[0], ratio)
                                saved_tup = tup
                    
                    if candidate[0] != '':  # IF needed and LLM wont work, maybe add a simple list count of valid entries might be useful  
                        ratio = SequenceMatcher(lambda x: x==' ', o_pred.lower(), saved_tup[2].lower()).ratio() 
                        if ratio > 0.75:  # assuming that the string are similar enough
                            ratio = SequenceMatcher(lambda x: x==' ', p_pred.lower(), saved_tup[1].lower()).ratio() 
                            if ratio > 0.75:  # assuming that the string are similar enough
                                p_tp_flag = True
                                p_tp += 1
                                remove_entry(remove=(saved_tup[0], saved_tup[1], saved_tup[2]), structure=reference, mode='multiple')

                elif mode == 'perfect':
                    # count up with perfect matches
                    for tup in reference:
                        if tup[0].lower() == s_pred.lower():
                            if tup[2].lower() == o_pred.lower():
                                if tup[1].lower() == p_pred.lower():
                                    p_tp_flag = True
                                    p_tp += 1
                                    remove_entry(remove=(s_pred, p_pred, o_pred), structure=reference, mode='multiple')
                                    break
                        
                elif mode == 'hard':
                    # count up with llm prompts (hard cut)
                    for tup in reference:
                        if 'y' in llm_query((s_pred, tup[0]), '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt_prädikat.json' ,mode):
                            if 'y' in llm_query((o_pred, tup[2]), '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt_prädikat.json',mode):
                                # since the predicates are hardcoded there is no need for the llm
                                if tup[1].lower() == p_pred.lower():  
                                    p_tp_flag = True
                                    p_tp += 1
                                    remove_entry(remove=(tup[0], tup[1], tup[2]), structure=reference, mode='multiple')
                                    break
                            
                elif mode == 'soft':
                    # count up with llm prompts (soft cut)
                    for tup in reference:
                        if 'y' in llm_query((s_pred, tup[0]), '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt_prädikat.json',mode):
                            if 'y' in llm_query((o_pred, tup[2]), '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_subjekt_objekt_prädikat.json',mode):
                                # since the predicates are hardcoded there is no need for the llm
                                if tup[1].lower() == p_pred.lower():
                                    p_tp_flag = True
                                    p_tp += 1
                                    remove_entry(remove=(tup[0], tup[1], tup[2]), structure=reference, mode='multiple')
                                    break

                ## ---------- /count in different ways ----------- ##
                # ------------ count detailed ------------ #
                try:
                    pred_classes_dict = detailed_storage(class_name, pred_classes_dict, p_tp_flag)
                    pred_predicates_dict = detailed_storage(p_pred, pred_predicates_dict, p_tp_flag)
                    detailed = True
                except UnboundLocalError:
                    #print('Not in classes mode. Operating without taking classes into account!')
                    detailed = False
                
    #KONTROLIERE NOCHMLA WIESO ES SEIN KANN; DASS RECALL ÜBER 100 PROZENNT HAT:   --> weil die predicteden Entitäten 
    # vermehrt einer bestimmten Klasse zugewiesen werden, während in der Annotation vermehrt verschiedene verwenden werden 

    #------------- calculate and print total metrics -------------#
    if detailed:   
        class_eval = calculate_metrics_detailed(pred_classes_dict, pos_classes_dict, mode='class', with_n=True)
        class_df = pd.DataFrame.from_dict(data=class_eval, orient='index', columns=['F1', 'precision', 'recall', 'N'])
        class_df.to_csv('../test/gollie_testset/subject_object_predicate/classes_accuracy.csv')

        predicate_eval = calculate_metrics_detailed(pred_predicates_dict, pos_predicates_dict, mode='class', with_n=True)
        predicate_df = pd.DataFrame.from_dict(data=predicate_eval, orient='index', columns=['F1', 'precision', 'recall', 'N'])
        predicate_df.to_csv('../test/gollie_testset/subject_object_predicate/predicates_accuracy.csv')

    s_scores = calculate_metrics(p_tp, p_total_pre, p_total_pos)

    s_scores.to_csv('../test/gollie_testset/subject_object_predicate/subject_object_eval.csv')



def eval_llm_acc(lst_a, lst_b, mode, labels=None, save_path=None, i=None):
    predicted_labels = []
    for subject in lst_a:
        for g_subject in lst_b:
            predicted_labels.append((subject, g_subject, mode, 
                                     'y' in llm_query([subject, g_subject], 
                                                      save_path=f'/nfs/home/ritterd/reflect/reflectai/wp2/test/ollama_mitschrift_{i}.json',
                                                        mode=mode)))
    return predicted_labels




default_config = {}
default_parameters = {}


@Manager.export("Evaluator")
class EvaluatorPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, text_entries: List[Dict]) -> Generator:
        #eval_subject_equals_name(entry) # possibly depricated
        #eval_subject_predicate_object_pair(entry) depricated

        # different evaluation schemes
        eval_subject_accuracy(text_entries, mode='hard')
        #eval_object_accuracy(text_entries, mode='hard')
        #eval_subject_object_accuracy(text_entries, mode='soft')

        #print(llm_query(['Der Schmadribachfall', 'Schmadribachfall'], '/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/mitschrift_test.json', mode='hard'))
        #eval_subject_object_predicate(text_entries)

        # print(llm_query(['Tiger', 'Tiger eating a boar']))
        #resp = llm_query(['hunter', 'hunter killing a tiger'], mode='soft')
        # print(resp)
        # end = re.search('</think>', resp).end()
        # print('y' in resp[end:])

        # subjects_1 = ['BRUNNENANLAGE MIT BADENDEN FRAUEN', 'In the foreground', 'lady', 'In the trees above the well', 'woman', 'cloak'] 
        # subjects_2 = ['bridge', 'The Little Bridge', 'over a canal', 'canal'] 
        # subjects_3 = ['Gropiusbau', 'sky', 'ohne Titel (Zeitgeist mit Springer)', 'In front of sand and debris', 'mountain of sand and debris']
        # subjects_4 = ['green', 'stream' ,'mountain', 'nature', 'landscape', 'Der Schmadribachfall', 'at the foot', 'pine forest', 'above' ]
        # subjects_5 = ['painting', 'sky', 'background', 'on the right', 'to the left' ]

        # g_subjects_1 = ['BRUNNENANLAGE','building', 'wells', 'well', 'water pool','pool','trees','tree']
        # g_subjects_2 = ['The Little Bridge', 'painting', 'bridge', 'canal', 'house']
        # g_subjects_3 = ['capital', 'metropolitan', 'Berlin', 'Potsdamer Platz', 'marshland', 'Gropiusbau', 'building', 'Gropius']
        # g_subjects_4 = ['gem', 'rock', 'forest', 'zone', 'Smadribachfall', 'mountain', 'waterfall', 'region', 'stream', 'wood']
        # g_subjects_5 = ['pavement', 'Via Appia', 'Tyrrhenian Sea', 'Ponza Islands', 'Ariccia', 'forest', 'town', 'Pontine marshes', 'Monte Circeo', 'contours']

        # i = 9
        # lst = eval_llm_acc(subjects_5, g_subjects_5, 'soft', i=i)
        # with open(f'../test/ollama_acc_{i}.txt', 'w') as fp:
        #     for a in lst:
        #         fp.write(str(a) + '\n')



        yield text_entries



# def llm_query(predictions, mode=0):
#     llm_prompt = 'In the context of paintings, do the terms "{}" and "{}"' \
#     'semantically describe the same thing? Note that the terms can refer to artists, eras, materials, art styles, or other' \
#     'art-related terms. Also note that subcategories are to be equated with the corresponding supercategories. Furthermore,' \
#     'plural forms and singular forms are to be equated. Terms are also to be equated if core terms such as “The Lady, A Hunter'\
#     'or A House” are included in one term and further described in the other term. Answer with only yes and no.'

#     # llm_prompt = 'im kontext von Gemälden, Beschreiben die Bezeichnungen "{}" und "{}" '\
#     # 'semantisch das gleiche? Beachte, dass es sich bei den Begriffen um Künstler, Zeitepochen, Materialien, Kunststile,'\
#     # 'oder andere Kunst nahe Begriffe handeln kann. Beachte weiterhin, dass Unterkategorien mit den entsprechenden Oberkategorien'\
#     # ' gleichzusetzen sind. Desweiteren sind pluralformen und singularformen gleichzusetzen. Ebenfalls gleichzusetzen sind Begriffe,'\
#     # ' wenn Kernbegriffe wie z.B. "The Lady, A Hunter or A House" in der einen Bezeichung steht, und in der anderen Bezeichnung weiter '\
#     # 'beschrieben wird. Antworte mit nur ja und nein.'
#     # # llm_prompt = 'im kontext von Gemälden, Beschreiben die Bezeichnungen {} und {} semantisch das gleiche? ' \
#     # #     'Beachte, dass es sich bei den Begriffen um Künstler, Zeitepochen, Materialien, Kunststile, ' \
#     # #     'oder andere Kunst nahe Begriffe handeln kann. Beachte weiterhin, dass Unterkategorien mit den ' \
#     # #     'entsprechenden Oberkategorien gleichzusetzen sind. Falls korrekt vorhanden, antworte mit ja oder nein.'
#     # llm_prompt = 'im kontext von Gemälden, Beschreiben die Bezeichnungen {} und {} ' \
#     # 'semantisch das gleiche? Beachte, dass es sich bei den Begriffen um Künstler, Zeitepochen, Materialien, Kunststile, ' \
#     # 'oder andere Kunst nahe Begriffe handeln kann. Beachte weiterhin, dass Unterkategorien mit den entsprechenden ' \
#     # 'Oberkategorien gleichzusetzen sind. Desweiteren sind pluralformen und singularformen gleichzusetzen und sofern ' \
#     # 'ein Kernbegriff wie z.B. The Lady in beiden Bezeichnungen auftaucht, sind auch diese gleichzusetzen. Antworte mit ja und nein.'

#     unique = []
#     modes = ['object', 'subject']
#     for prediction in predictions:
#         flag = True
#         for taken_prediction in unique:
#             try:
#                 response = client.chat(model='gemma3:1b', messages=[
#                     {
#                         'role': 'user',
#                         'content': llm_prompt.format(taken_prediction[modes[mode]]['label'].lower(), prediction[modes[mode]]['label'].lower()),
#                     },
#                     ])
#                 if 'j' in response['message']['content'].lower() and taken_prediction[modes[mode-1]]['label'] == prediction[modes[mode-1]]['label']\
#                         and taken_prediction['relation']['label'] == prediction['relation']['label']: 
#                     flag = False
#                     break
#             except _types.ResponseError as e: 
#                 print('Due to response Error "', e, '" the semantical filter LLM is not used!')
#                 return predictions

#         if flag:
#             unique.append(prediction)

#     return unique