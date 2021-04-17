import json
import copy

def get_mapping(json_content):
    curr_idx = 0

    mapping = {}

    for idx, k in enumerate(cat_json):
        if k['isthing'] == 0:
            mapping[curr_idx] = idx
            curr_idx+=1

    for idx, k in enumerate(cat_json):
        if k['isthing'] == 1:
            mapping[curr_idx] = idx
            curr_idx+=1

    return mapping

def invert_mapping(mapping):
    return {v: k for k, v in mapping.items()}

if __name__ == "__main__":

    #idx_mapping = {**{idx1: idx2 for idx1, idx2 in zip(range(53), range(80, 133))}, **{idx1: idx2 for idx1, idx2 in zip(range(53, 133), range(80))}}
    #inv_idx_mapping = {**{idx1: idx2 for idx1, idx2 in zip(range(80), range(53, 133))}, **{idx1: idx2 for idx1, idx2 in zip(range(80, 133), range(53))}}

    #idx_mapping = {**{idx1: idx2 for idx1, idx2 in zip(range(53), range(80, 133))}, **{idx1: idx2 for idx1, idx2 in zip(range(53, 133), range(80))}}
    #inv_idx_mapping = {**{idx1: idx2 for idx1, idx2 in zip(range(80), range(53, 133))}, **{idx1: idx2 for idx1, idx2 in zip(range(80, 133), range(53))}}
    
    cat_json = json.load(open('data/coco/annotations/panoptic_coco_categories.json'))
    cat_json_stff = copy.deepcopy(cat_json)

    idx_mapping = get_mapping(cat_json)
    inv_idx_mapping = invert_mapping(idx_mapping)
    
    cat_idx_mapping = {}
    for idx, k in enumerate(cat_json):
        cat_idx_mapping[k['id']] = idx
    
    for k, v in idx_mapping.items():      
        cat_json_stff[k] = cat_json[v]
        cat_json_stff[k]['id'] = k
    
    json.dump(cat_json_stff, open('data/coco/annotations/panoptic_coco_categories_stff.json', 'w'))

    for s in ['train', 'val']:

        pano_json = json.load(open('data/coco/annotations/panoptic_{}2017.json'.format(s)))

        pano_json_stff = copy.deepcopy(pano_json)

        pano_json_stff['categories'] = cat_json_stff

        for anno in pano_json_stff['annotations']:
            for segments_info in anno['segments_info']:
                segments_info['category_id'] = inv_idx_mapping[cat_idx_mapping[segments_info['category_id']]]

        for img in pano_json_stff['images']:
             img['file_name'] = img['file_name'].replace('jpg', 'png')
        if s == 'val':
            pano_json_stff['images'] = sorted(pano_json_stff['images'], key=lambda x: x['id'])
        
        json.dump(pano_json_stff, open('data/coco/annotations/panoptic_{}2017_stff.json'.format(s), 'w'))


