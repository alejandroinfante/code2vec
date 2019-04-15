from common import common
from pharo_extractor import Extractor
from flask import Flask, request, abort
import threading
import json
import tempfile
import werkzeug
import os

PHARO_IMAGE_PATH = 'PharoExtractor/extractor.image'
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
SHOW_TOP_CONTEXTS = 10

app = Flask(__name__)
app.use_reloader=False

SERVER = None

class PredictorServer:
    def __init__(self, config, model, port):
        model.predict([])
        self.model = model
        self.config = config
        self.port = port
        self.path_extractor = Extractor(config,
                                        pharo_image_path=PHARO_IMAGE_PATH,
                                        max_path_length=MAX_PATH_LENGTH,
                                        max_path_width=MAX_PATH_WIDTH)
    
    @app.route("/predict", methods=["POST"])
    def predict_route():
        if request.content_length > 100000:
            abort(400)
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(request.get_data(as_text=True))
            predict_lines, hash_to_string_dict = SERVER.path_extractor.extract_paths(path)
        finally:
            os.remove(path)
        results = SERVER.model.predict(predict_lines)
        method_prediction = common.parse_results(results, hash_to_string_dict, topk=SHOW_TOP_CONTEXTS)[0]
        ans = { 
            'predictions': method_prediction.predictions,
            'attention_paths': method_prediction.attention_paths
        }
        # for method_prediction in prediction_results:
        #     print('Original name:\t' + method_prediction.original_name)
        #     for name_prob_pair in method_prediction.predictions:
        #         print('\t(%f) predicted: %s' % (name_prob_pair['probability'], name_prob_pair['name']))
        #     print('Attention:')
        #     for attention_obj in method_prediction.attention_paths:
        #         print('%f\tcontext: %s,%s,%s' % (
        #         attention_obj['score'], attention_obj['token1'], attention_obj['path'], attention_obj['token2']))
        return json.dumps(ans)

    def start(self):
        global SERVER
        SERVER = self
        app.run(port=self.port)