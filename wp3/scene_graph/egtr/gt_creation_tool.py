import os
from collections import defaultdict
import pickle
import time
import json
import numpy as np
import re
import pandas as pd
from numpy.linalg import norm
import streamlit as st
from streamlit.runtime.media_file_storage import MediaFileStorageError
import io
import PIL
import zipfile
import iconclass as iclass
from streamlit_tree_select import tree_select


def calculate_iconclass_depth(notation, with_key=False, with_addendum=False):
    cnt = 0
    bracket_open = False
    valid_key = False
    valid_addendum = False
    is_key = False
    for char in notation:
        if char == ')':
            bracket_open = False
            valid_key = False
            valid_addendum = False
        elif bracket_open:
            if with_key:
                if char == '+' or valid_key:
                    cnt += 1
                    valid_key = True
            if with_addendum:
                if (char != '+' or valid_addendum) and not is_key:
                    cnt += 1
                    valid_addendum = True
                else:
                    is_key = True

        elif char.isalnum():
            cnt += 1
        elif char == '(':
            bracket_open = True

    return cnt


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

#Q1057817
def close_range_calculation(query, corpus, abstract=2, detailed=2, with_key=False, with_addendum=False,
                            min_notation_depth=3):
    accepted_concepts = defaultdict(list)
    for concept in query:
        # this makes sure that every concept is stored as a key
        dummy = accepted_concepts[concept]
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


            taken_q.append((query_image, k, concepts, v, intersection_q, i_o_q, i_o_c, i_o_u_all))

            taken_c.append((query_image, k, concepts, v, intersection_c, i_o_q, i_o_c, i_o_u_all))


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


def traverse_helper(notation):
    "return True if the there is a '+' right before a '('"
    notation = reversed(list(notation))
    key = re.search('\(\+\d+\)', notation)
    if key is not None:
        span = key.span()
        key = notation[span[0]:span[1]]
        return span, key

    return '', key


def traverse_iconclass_tree(notation):
    level = []
    n = len(notation) - 1
    while notation:
        if re.search('\(\+\d+\)', notation):
            level.append(notation)

            if notation[n] == ')' and notation[n - 1] != '+':
                notation = notation[:-2] + notation[-1:]
                n -= 1
            else:
                notation = notation[:-1]
                n -= 1

            if notation and notation[n] == ')' and notation[n - 1] == '+' and notation[n - 2] == '(':
                notation = notation[:-3]
                n -= 3
        else:
            level.append(notation)

            if notation[n] == ')':
                while notation[n] != '(':
                    notation = notation[:-1]
                    n -= 1
                notation = notation[:-1]
                n -= 1
            else:
                notation = notation[:-1]
                n -= 1

    return level



def transform_into_dcts(level, ic_notation_class):
    # in the off chances that there are multiple keys in the notation --> implement it better than it is working now!
    # similar with additoinal information within the brackets
    """nodes = [
                {
                    "label": "Folder B",
                    "value": "folder_b",
                    "showCheckbox": False,
                    "children": [
                        {"label": "Sub-folder A", "value": "sub_a", "showCheckbox":False},
                        {"label": "Sub-folder B", "value": "sub_b", "showCheckbox":False},
                        {"label": "Sub-folder C", "value": "sub_c", "showCheckbox":False},
                    ],
                }
            ]"""
    try:
        label = f'{level[0]}  {ic_notation_class[level[0]]()}'
    except iclass.NotationNotFound:
        label = f'{level[0]}'

    if len(level) == 1:
        dct = {'label': label, 'value': level[0], 'showCheckbox': True}
        return dct
    else:
        dct = {'label': label, 'value': level[0], 'showCheckbox': True,
               'children': [transform_into_dcts(level[1:], ic_notation_class)]}
        return dct

def pre_filter_corpus(kg, min_depth, min_concepts_at_depth):
    filtered = defaultdict(list)

    for corpus_image in kg.items():
        cnt = 0
        for values in corpus_image[1]:
            for relation, subject in values.items():
                if relation == 'P1257':
                    depth = calculate_iconclass_depth(subject)
                    if depth >= min_depth:
                        cnt += 1

        if cnt >= min_concepts_at_depth:
            filtered[corpus_image[0]] = corpus_image[1]

    return filtered

st.set_page_config(layout='wide')
st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    list-style-position: inside;
}
</style>
''', unsafe_allow_html=True)
row_cols = [col for col in st.columns(3)]
with row_cols[0]:
    kg_dataset = st.file_uploader('KG dataset', type=['zip'])
    if kg_dataset:
        with zipfile.ZipFile(kg_dataset) as zipf:
            dataset = zipf.namelist()[0]
            with open(dataset, 'rb') as fp:
                kg_triplets = pickle.load(fp)
        corpus_size = len(kg_triplets)
        pre_select_rows = [col for col in st.columns(2)]
        with pre_select_rows[0]:
            min_notation_depth = st.number_input(value=3, min_value=0, max_value=100, label='All concept minimum depths')
            min_primary_concepts_depth = st.number_input(value=3, min_value=0, max_value=100, label='Primary concept depths')
        with pre_select_rows[1]:
            min_notations = st.number_input(value=3, min_value=0, max_value=100, label=f'Minimum amount of concepts at depth')
            min_primary_concepts = st.number_input(value=3, min_value=0, max_value=100, label=f'Minimum amount of primary concepts at depth')

button_pressed = st.button(label='Filter', use_container_width=True, type='primary')
if 'filter' not in st.session_state:
    st.session_state['filter'] = False

if button_pressed:
    st.session_state['filter'] = button_pressed

if st.session_state['filter']:
    #st.session_state.page = 0
    filtered_corpus = pre_filter_corpus(kg_triplets, min_notation_depth, min_notations)
    with row_cols[1]:
        # filtering should be next to image upload
        st.write(f'The overall size of the dataset is: {corpus_size}')
        st.write(f'The filtered size of the dataset is: {len(filtered_corpus)}')
        # todo: Statistiken (wie viele notationen gibt es pro Level Tiefe im gefiltertem Datensatz)

    meta_rows = [col for col in st.columns(3)]
    with meta_rows[0]:
        query_image = st.multiselect(label='Query Selector', options=filtered_corpus)
        if query_image:
            #todo: den Pfad anpassbar machen
            query_image_path = rf'/nfs/data/reflectai/wikidata_image_dataset/full_wikidata_iconclass/{query_image[0]}.jpg'
            st.image(query_image_path, use_container_width=False, width=500)

            image_name = query_image[0]
            with meta_rows[1]:
                st.page_link(f'https://www.wikidata.org/wiki/{image_name}', label=f'Wikidata id: {image_name}')

                iconclass_concepts = []
                depicts_concepts = []
                multi_selects = []
                for c in kg_triplets[image_name]:
                    if c.get('label'):
                        st.write('Name:', c['label'])
                    if c.get('P1257'):
                        if ':' in c['P1257']:
                            concepts = c['P1257'].split(':')  # some cases need to be split into two
                            for concept in concepts:
                                iconclass_concepts.append(concept)
                        iconclass_concepts.append(c['P1257'])

                    if c.get('P180'):
                        depicts_concepts.append(c['P180'])

                ic = iclass.init()

                iconclass_concepts = list(set(iconclass_concepts))
                for level in iconclass_concepts:
                    icon_root = tree_select([transform_into_dcts(traverse_iconclass_tree(level), ic)],
                                            no_cascade=True)
                    multi_selects.extend(icon_root['checked'])

            
            
            with meta_rows[2]:
                # todo: the gt needs to be selected automatically with the query selector
                filtered_gt = st.file_uploader('Filtered Ground-Truth', type=['zip'])
                if filtered_gt:
                    with zipfile.ZipFile(filtered_gt) as zipf:
                        dataset = zipf.namelist()[0]
                        with open(dataset, 'rb') as fp:
                            gt = pickle.load(fp)

                    with_key = st.checkbox(label='with keys')
                    with_additional = st.checkbox(label= 'with additional')

                    #-------- for each level -------------
                    include = st.multiselect(label='concepts to include', options=multi_selects)
                    num_inputs = st.columns(3)
                    with num_inputs[0]:
                        abstract_primary = st.number_input(
                            label='How many steps more abstract', value=0)
                    with num_inputs[1]:
                        detailed_primary = st.number_input(
                            label='How many steps more detailed', value=0)
                    with num_inputs[2]:
                        min_primary = st.number_input(
                            label='Minimum level for each notation', value=3)

                    exclude = st.text_input(label='concepts to exclude')
                    exclude = exclude.split(', ')
                    num_inputs2 = st.columns(3)
                    with num_inputs2[0]:
                        abstract_excluded = st.number_input(
                            label='How many steps more abstract ', value=0)
                    with num_inputs2[1]:
                        detailed_excluded = st.number_input(
                            label='How many steps more detailed ', value=0)
                    with num_inputs2[2]:
                        min_exclued = st.number_input(
                            label='Minimum level for each notation ', value=3)

                    optional = st.multiselect(label='optional concepts to include', options=multi_selects)
                    num_inputs3 = st.columns(3)
                    with num_inputs3[0]:
                        abstract_optional = st.number_input(
                            label='How many steps more abstract  ', value=0)
                    with num_inputs3[1]:
                        detailed_optional = st.number_input(
                            label='How many steps more detailed  ', value=0)
                    with num_inputs3[2]:
                        min_optional = st.number_input(
                            label='Minimum level for each notation  ', value=3)
                    #-------------------------------------

                    ioq = st.slider('minimum intersect over the query image', max_value=1.0, step=0.1, min_value=0.0)
                    ioc = st.slider('minimum intersect over the corpus image', max_value=1.0, step=0.1, min_value=0.0)
                    iou = st.slider('minimum intersect over the union', max_value=1.0, step=0.1, min_value=0.0)
                    sort_by = st.pills(label="select a sort scheme", options= ['over the query image', 'over the corpus image'],
                        default='over the query image',
                    )


if 'queried' not in st.session_state:
    st.session_state['queried'] = False


if 'page' not in st.session_state:
    st.session_state.page = 0

if st.button(label='previous page', disabled=st.session_state.page <= 0):
    st.session_state.page -= 1
    st.session_state['queried'] = True
if st.button(label='next page'):
    st.session_state.page += 1
    st.session_state['queried'] = True
if st.button(label='reset page counter'):
    st.session_state.page = 0
    st.session_state['queried'] = False

st.write(f'page {st.session_state["page"]}')
if st.button(label='Query', use_container_width=True, type='primary') or st.session_state['queried']:

    maximum_length = max(len(include), len(exclude), len(optional))
    padding_size_include = maximum_length - len(include)
    padding_size_exclude = maximum_length - len(exclude)
    padding_size_optional = maximum_length - len(optional)

    configuration = dict(with_key=with_key, 
                                 with_additional=with_additional,
                                 primary_concepts=include + [''] * padding_size_include,
                                 primary_abstract=abstract_primary,
                                 primary_detailed=detailed_primary,
                                 min_primary_depth=min_primary,
                                 optional_concepts=optional + [''] * padding_size_optional,
                                 optional_abstract=abstract_optional,
                                 optional_detailed=detailed_optional,
                                 min_optional_depth=min_optional,
                                 excluded_concepts=exclude + [''] * padding_size_exclude,
                                 excluded_abstract=abstract_excluded,
                                 excluded_detailed=detailed_excluded,
                                 min_excluded_depth=min_exclued, 
                                 intersect_over_query=ioq, 
                                 intersect_over_corpus=ioc, 
                                 intersect_over_union=iou)
    n_cols = 6
    cols = [col for col in st.columns(n_cols)]

    height = 500
    # todo secondary and teritary needs to be included, however I do not know how
    full_include = include + optional

    resul_images_q, resul_images_c = display_filter_gt(gt, full_include, with_key, with_additional, ioq, ioc, iou, sort_by=sort_by,
                                    abstract=abstract_primary, detailed=detailed_primary, min_notation_depth=min_primary)
    i = 0
    all_results = resul_images_q
    if not resul_images_q:
        st.markdown('## No images found!')
    else:
        st.markdown(f'#### {len(all_results)} images found!')

    resul_images_q = resul_images_q[st.session_state.page * 30:(st.session_state.page + 1) * 30]
    resul_images_c = resul_images_c[st.session_state.page * 30:(st.session_state.page + 1) * 30]

    for image_q, image_c in zip(resul_images_q, resul_images_c):
        # primary check for valid corpus image
        cc = image_c[4].keys()
        exclude_set = set(exclude) & cc
        if set(include).issubset(cc) and not exclude_set:
            with cols[i % n_cols]:
                pop = st.popover(label=f'Open Comparison view of {image_q[1]}')
                with st.container(height=height):
                    try:
                        st.page_link(f'https://www.wikidata.org/wiki/{image_q[1]}', label=f'{image_q[1]}')
                        # think about a way to make the image paths variable
                        st.image(
                            fr'/nfs/data/reflectai/wikidata_image_dataset/full_wikidata_iconclass/{image_q[1]}.jpg',
                            use_container_width=True)

                        st.markdown(
                            f'Intersection over Query: {len([k for k, l in image_q[4].items() if l])} / {len(image_q[4].keys())}')
                        st.markdown(
                            f'Intersection over Corpus: {len([k for k, l in image_c[4].items() if l])} / {len(image_c[4].keys())}')
                        st.markdown(
                            f'Intersection over Union: {len(image_q[7][1])} / {len(set(image_q[4].keys()) | set(image_c[4].keys()))}')

                    except (FileNotFoundError, MediaFileStorageError) as e:
                        # das passiert noch, weil für die neuen Datensätze nicht immer alle Bilder zur verfügung stehen!
                        st.write(image_q[1])
                    except Exception as e:
                        continue
            with pop:
                with st.container(height=750):
                    # todo only the one that I opened
                    images_cols = st.columns(2)
                    with images_cols[0]:
                        st.header('Query image')
                        st.page_link(f'https://www.wikidata.org/wiki/{image_name}', label=f'{image_name}')
                        st.image(query_image_path, use_container_width=False, width=500)
                    with images_cols[1]:
                        st.header('Corpus image')
                        st.page_link(f'https://www.wikidata.org/wiki/{image_q[1]}', label=f'{image_q[1]}')
                        st.image(
                            fr'/nfs/data/reflectai/wikidata_image_dataset/full_wikidata_iconclass/{image_q[1]}.jpg',
                            use_container_width=False, width=500)

                tabs = st.tabs(['Query Concepts', 'Corpus Concepts'])
                with tabs[0]:
                    header_cols = st.columns(2)
                    with header_cols[0]:
                        st.header('Query Concepts')
                    with header_cols[1]:
                        st.header('Matching Concepts')

                    with st.container(height=1000):
                        for match_q, match_c in image_q[4].items():
                            try:
                                kw = ic[match_q]('en')
                            except iclass.NotationNotFound:
                                kw = []

                            with st.container(height=125):
                                q_cols = st.columns(2, gap='large')
                                with q_cols[0]:
                                    st.markdown(
                                        f'[{match_q}](https://iconclass.org/{match_q.replace(" ", "")})' + '&emsp;' * 1 + f'{kw} {calculate_iconclass_depth(match_q, with_key=with_key, with_addendum=with_additional)}')

                                with q_cols[1]:
                                    if match_c:
                                        for matches in match_c:
                                            try:
                                                kw = ((ic[matches])())
                                            except iclass.NotationNotFound:
                                                kw = []
                                                # pass
                                            st.markdown(
                                                f'- [{matches}](https://iconclass.org/{matches.replace(" ", "")})' + '&emsp;' * 1 + f'{kw} {calculate_iconclass_depth(matches, with_key=with_key, with_addendum=with_additional)}')
                                    else:
                                        st.markdown(' - No Matches!')

                        with st.container(height=150):
                            result_cols = st.columns(2)
                            with result_cols[0]:
                                st.markdown(
                                    f'Intersection over Query: {len([k for k, l in image_q[4].items() if l])} / {len(image_q[4].keys())}')
                                st.markdown(
                                    f'Intersection over Corpus: {len([k for k, l in image_c[4].items() if l])} / {len(image_c[4].keys())}')
                                st.markdown(
                                    f'Intersection over Union: {len(image_q[7][1])} / {len(set(image_q[4].keys()) | set(image_c[4].keys()))}')
                            with result_cols[1]:
                                st.write(f'Intersection over query: {image_q[5]}')
                                st.write(f'Intersection over corpus: {image_q[6]}')
                                st.write(f'Intersection over union: {image_q[7][0]}')

                with tabs[1]:
                    header_cols = st.columns(2)
                    with header_cols[0]:
                        st.header('Corpus Concepts')
                    with header_cols[1]:
                        st.header('Matching Concepts')

                    with st.container(height=1000):
                        for match_q, match_c in image_c[4].items():
                            try:
                                kw = ic[match_q]('en')
                            except iclass.NotationNotFound:
                                kw = []

                            with st.container(height=125):
                                q_cols = st.columns(2, gap='large')
                                with q_cols[0]:
                                    st.markdown(
                                        f'[{match_q}](https://iconclass.org/{match_q.replace(" ", "")})' + '&emsp;' * 1 + f'{kw} {calculate_iconclass_depth(match_q, with_key=with_key, with_addendum=with_additional)}')

                                with q_cols[1]:
                                    if match_c:
                                        for matches in match_c:
                                            try:
                                                kw = ((ic[matches])())
                                            except iclass.NotationNotFound:
                                                kw = []
                                            st.markdown(
                                                f'- [{matches}](https://iconclass.org/{matches.replace(" ", "")})' + '&emsp;' * 1 + f'{kw} {calculate_iconclass_depth(matches, with_key=with_key, with_addendum=with_additional)}')
                                    else:
                                        st.markdown(' - No Matches!')

                        with st.container(height=150):
                            result_cols = st.columns(2)
                            with result_cols[0]:
                                st.markdown(
                                    f'Intersection over Query: {len([k for k, l in image_q[4].items() if l])} / {len(image_q[4].keys())}')
                                st.markdown(
                                    f'Intersection over Corpus: {len([k for k, l in image_c[4].items() if l])} / {len(image_c[4].keys())}')
                                st.markdown(
                                    f'Intersection over Union: {len(image_q[7][1])} / {len(set(image_q[4].keys()) | set(image_c[4].keys()))}')
                            with result_cols[1]:
                                st.write(f'Intersection over query: {image_q[5]}')
                                st.write(f'Intersection over corpus: {image_q[6]}')
                                st.write(f'Intersection over union: {image_q[7][0]}')

            i += 1
            print(i)
try:
    relevant_gt = [gt[1] for gt in all_results]
    relevant_gt = all_results[0][0] + relevant_gt

    df = pd.DataFrame.from_dict(configuration, orient='index')
    relevant = pd.Series(relevant_gt, index=['query'] + list(range(len(relevant_gt) - 1)))

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        relevant.to_excel(writer, sheet_name='relevant paintings')
        df.to_excel(writer, sheet_name='configuration')
        writer.close()

    st.download_button(
        label='Download Ground-Truth images',
        data=buffer,
        file_name='Filtered_GT.xlsx',
        icon=":material/download:",
        type='secondary'
    )
    print('done')
except (NameError, IndexError):
    pass
