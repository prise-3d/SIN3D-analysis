# main imports
import argparse
import numpy as np
import sys, os

# mongo import
from pymongo import MongoClient

# modules imports
sys.path.insert(0, '') # trick to enable import of main folder module

# config imports
import custom_config  as cfg

def main():

    parser = argparse.ArgumentParser(description="Get error during calibration experiment for each user")

    parser.add_argument('--expeId', type=str, help='Experiment identifier')
    parser.add_argument('--experiment', type=str, help='Experiment name', choices=cfg.experiment_list, required=True)
    parser.add_argument('--scene', type=str, help='Scene identifier to use', choices=cfg.scenes_indices, required=True)

    args = parser.parse_args()

    p_expe_id    = args.expeId
    p_experiment = args.experiment
    p_scene      = args.scene

    # connect to Mongo db and collect data
    client = MongoClient(cfg.default_host)
    db = client.sin3d

    query = {
        'data.msg.experimentName': p_experiment, 
        'data.msgId': "EXPERIMENT_VALIDATED"
    }

    # add of expeid into query if exists
    if p_expe_id:
        print("Expe id used", p_expe_id)
        query['data.experimentId'] = p_expe_id

    index = cfg.scenes_indices.index(p_scene.strip())
    scene_name = cfg.scenes_names[index]

    # from dataset retrieve human thresholds for each zone  
    zone_thresholds = []
    scene_folder = os.path.join(cfg.dataset_path, scene_name)
    zone_folders = sorted([zone for zone in os.listdir(scene_folder) if 'zone' in zone])
    
    for zone in zone_folders:
        threshold_file_path = os.path.join(scene_folder, zone, cfg.seuil_expe_filename)

        with open(threshold_file_path, 'r') as f:
            current_threshold = int(f.readline())
            zone_thresholds.append(current_threshold)
    
    print(zone_thresholds)

    print("Scene used", scene_name)
    query['data.msg.sceneName'] = scene_name

    print(query)


    for cursor in res:
        user_data = cursor['data']
        user_id = user_data['userId']

        experiment_user_thresholds = []
        for id, val in enumerate(user_data['msg']['extracts']):
            experiment_user_thresholds.append(val['quality'])

        print(user_id, experiment_user_thresholds)

if __name__== "__main__":
    main()