from common import common

class Logger:
    
    def __init__(self, basename, model, batch_log_loss = 5, batch_log_eval = 10):
        self.FILE_EXTENSION = '.log'
        self.basename = basename
        self.current_batch = 1
        self.sum_loss = 0
        self.model = model
        self.BATCH_LOSS_LOG = batch_log_loss
        self.BATCH_EVAL_LOG = batch_log_eval

    def loss_filename(self):
        return self.basename + '.loss' + self.FILE_EXTENSION
    
    def train_set_filename(self):
        return self.basename + '.train' + self.FILE_EXTENSION
    
    def eval_set_filename(self):
        return self.basename + '.eval' + self.FILE_EXTENSION

    def increment_batch(self):
        self.current_batch += 1

    def log_loss(self, batch_loss):
        self.sum_loss += batch_loss
        if (self.current_batch % self.BATCH_LOSS_LOG) == 0:
            self.loss_file.write("%s;%s\n" % (self.current_batch,self.sum_loss))
            sum_loss = 0
            return True
        return False
    
    def eval_and_log(self):
        if (self.current_batch % self.BATCH_EVAL_LOG) == 0:
            self._evaluate_train_set()
            self._evaluate_eval_set()
            return True
        return False

    def _eval_in_file(self, data_file_path, output_file):
        top_k, precision, recall, f1 = self.model.evaluate(common.load_file_lines(data_file_path))
        output_file.write("%s;%s;%s;%s" % (self.current_batch,precision, recall, f1))
        for topk_val in top_k:
            output_file.write(";%s" % (topk_val,))
        output_file.write("\n")
        output_file.flush()

    def _evaluate_train_set(self):
        self._eval_in_file(self.model.config.TRAIN_PATH+".val.c2v", self.train_set_file)
    
    def _evaluate_eval_set(self):
        self._eval_in_file(self.model.config.TEST_PATH, self.eval_set_file)

    def __enter__(self):
        self.loss_file = open(self.loss_filename(),"w+")
        self.loss_file.write("Batch;Loss")
        self.train_set_file = open(self.train_set_filename(),"w+")
        self.train_set_file.write("Batch;Precision;Recall;F1")
        self.eval_set_file = open(self.eval_set_filename(),"w+")
        self.eval_set_file.write("Batch;Precision;Recall;F1")
        print('Start logging')
        return self

    def __exit__(self, type, value, traceback):
        print('Finish logging')
        self.loss_file.close()
        self.train_set_file.close()
        self.eval_set_file.close()
        return False