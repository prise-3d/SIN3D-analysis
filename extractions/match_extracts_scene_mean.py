# main imports
import argparse
import numpy as np
import sys

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
    parser.add_argument('--scene', type=str, help='Scene identifier to use', choices=cfg.scenes_indices)

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

    if p_scene:

        index = cfg.scenes_indices.index(p_scene.strip())
        scene_name = cfg.scenes_names[index]

        print("Scene used", scene_name)
        query['data.msg.sceneName'] = scene_name

    print(query)

    res = db.datas.find(query)

    zone_index = np.arange(16)
    threshold_img = (zone_index / 15) * 100

    for cursor in res:
        user_data = cursor['data']
        user_id = user_data['userId']

        experiment_user_thresholds = []
        experiment_error_thresholds = []
        for id, val in enumerate(user_data['msg']['extracts']):
            experiment_user_thresholds.append(val['quality'])

        print(user_id, experiment_user_thresholds)

if __name__== "__main__":
    main()