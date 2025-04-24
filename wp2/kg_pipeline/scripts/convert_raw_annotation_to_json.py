import os
import jsonl


def create_jsonl_file():
    collection = []
    i = 0

    for annotations_groups in os.listdir('/nfs/data/reflectai/data/annotation/'):
        if annotations_groups != 'auctions':
            continue
        for annotation_text in os.listdir(f'/nfs/data/reflectai/data/annotation/{annotations_groups}'):
            with open(f'/nfs/data/reflectai/data/annotation/{annotations_groups}/{annotation_text}', encoding='utf-8') as fp: 
                read = fp.read()
                n = len(read) 
                if n > 20000:
                    while n > 20000:
                        k = 0
                        text = {'text': [{'content': read[k * 20000: (k+1) * 20000]}], 'id': annotation_text}
                        collection.append(text)  
                        k += 1
                        n -= 20000     
                else: 
                    text = {'text': [{'content': read}], 'id': annotation_text}
                    collection.append(text)



    jsonl.dump(collection, "/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/gollietestset.jsonl")
            
            


if __name__ == '__main__':
    create_jsonl_file()
