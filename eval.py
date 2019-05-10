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
    parser.add_argument("-m", "--model", dest="model",
                        help="path to save file", metavar="FILE", required=True)
    parser.add_argument("-e", "--epochs", dest="epochs",
                        help="path to save file", type=int, required=True)
    parser.add_argument("-o", "--output", dest="output_file",
                        help="path to save file", metavar="FILE", required=False)
    args = parser.parse_args()

    config = Config.get_default_config(args)

    for epoch in range(args.epochs):
        config.LOAD_PATH = args.model + '_iter' + str(epoch + 1)
        model = Model(config)
        print('Created model for epoch ' + str(epoch + 1))
        eval_results = model.evaluate()
        if eval_results is not None:
            results, precision, recall, f1 = eval_results
            print(results)
            print('Precision: ' + str(precision) + ', recall: ' + str(recall) + ', F1: ' + str(f1))
        model.close_session()