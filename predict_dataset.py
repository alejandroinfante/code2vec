from common import Config, VocabType
from argparse import ArgumentParser
from interactive_pharo_predict import InteractivePredictor
from predictor_server import PredictorServer
from model import Model
import sys

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-te", "--test", dest="test_path",
                        help="path to test file", metavar="FILE", required=True)
    parser.add_argument("-l", "--load", dest="load_path",
                        help="path to save file", metavar="FILE", required=True)
    parser.add_argument("-o", "--output", dest="output_file",
                        help="path to save file", metavar="FILE", required=True)
    args = parser.parse_args()

    config = Config.get_default_config(args)

    model = Model(config)
    print('Created model')
    model.predict_dataset()
    model.close_session()