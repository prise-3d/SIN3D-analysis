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

    args = parser.parse_args()

    p_expe_id = args.expeId

    # connect to Mongo db and collect data
    client = MongoClient(cfg.default_host)
    db = client.sin3d

    query = {
        'data.msg.experimentName': "CalibrationMeasurement",
        'data.msgId': "EXPERIMENT_VALIDATED"
    }

    # add of expeid into query if exists
    if p_expe_id:
        print("Expe id used", p_expe_id)
        query['data.experimentId'] = p_expe_id

    print(query)

    res = db.datas.find(query)

    zone_index = np.arange(16)
    threshold_img = (zone_index / 15) * 100

    print(threshold_img)

    for cursor in res:
        user_data = cursor['data']
        user_id = user_data['userId']

        experiment_user_thresholds = []
        experiment_user_zone = []
        experiment_error_thresholds = []
        for val in user_data['msg']['extracts']:
            zone_id = int(val['zone']) - 1
            experiment_user_thresholds.append(val['quality'])
            error = (val['quality'] - threshold_img[zone_id])
            error_squared = error * error
            experiment_user_zone.append(zone_id)
            experiment_error_thresholds.append(error_squared)

        print('----------------------------------------------')
        print('User', user_id)
        print('zone id', experiment_user_zone)
        print('Estimated', experiment_user_thresholds)
        print('Squared error', list(map(lambda x: str('%.2f' % x), experiment_error_thresholds)))
        print('Mean squared error', np.mean(experiment_error_thresholds))

if __name__== "__main__":
    main()
