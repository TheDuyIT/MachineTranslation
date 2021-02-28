import sys
import os
sys.path.append(os.getcwd())
# import time
# from tqdm import tqdm

from src.dictionary import Dictionary
from src.utils import *
MAX_LENGTH = 250
class Test:
    def __init__(self, checkpoint_path = r"C:\Workplaces\NLP\Project\test\MachineTranslation\outputs\train1", dictionary_path = 'datasets/vi_zh') -> None:
        loader = DataLoader()
        content_cn = loader.np_load('lst_cn_all_with6k_except_1001')
        content_vn = loader.np_load('lst_vi_all_with6k_except_1001')
        for i in range(len(content_vn)):
            content_vn[i] = content_vn[i].lower()
        for i in range(len(content_cn)):
            content_cn[i] = self.preproces_cn(content_cn[i])

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(content_cn, content_vn, test_size=0.2, random_state=1)
        X_val, y_val = [X_train[0]], [y_train[0]]

        full_dataset = self.create_dataset(content_cn, content_vn)
        train_examples = self.create_dataset(X_train, y_train)
        test_dataset = self.create_dataset(X_test, y_test)
        val_dataset = self.create_dataset(X_val, y_val)

        self.tokenizer_cn = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(
            (en.numpy() for en, _ in full_dataset), target_vocab_size=2**13)

        self.tokenizer_vn = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(
            (vn.numpy() for _, vn in full_dataset), target_vocab_size=2**13)

        BUFFER_SIZE = 2000
        BATCH_SIZE = 64
        train_dataset = train_examples.map(self.tf_encode)
        train_dataset = train_dataset.filter(self.filter_max_length)
        train_dataset = train_dataset.cache()
        train_dataset = train_dataset.shuffle(BUFFER_SIZE)
        train_dataset = train_dataset.prefetch(tf.data.experimental.AUTOTUNE)
        val_dataset = val_dataset.map(self.tf_encode)
        val_dataset = val_dataset.filter(self.filter_max_length)
        test_dataset = test_dataset.map(self.tf_encode)
        test_dataset = test_dataset.filter(self.filter_max_length)

        num_layers = 6
        d_model = 256 # model dim
        dff = 512 # feed forward dim
        num_heads = 8 # number of multi head attention d_model%num_heads == 0

        input_vocab_size = self.tokenizer_cn.vocab_size + 2
        target_vocab_size = self.tokenizer_vn.vocab_size + 2
        dropout_rate = 0.1
        learning_rate = CustomSchedule(d_model)
        optimizer = tf.keras.optimizers.Adam(learning_rate, beta_1=0.9, beta_2=0.98, 
                                     epsilon=1e-9)
        self.dic = Dictionary().create_dict(dictionary_path)    
        self.transformer = Transformer(num_layers, d_model, num_heads, dff,
                          input_vocab_size, target_vocab_size, 
                          pe_input=input_vocab_size, 
                          pe_target=target_vocab_size,
                          rate=dropout_rate)   

        ckpt = tf.train.Checkpoint(transformer=self.transformer,
                                optimizer=optimizer)

        ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=5)
        if ckpt_manager.latest_checkpoint:
            ckpt.restore(ckpt_manager.latest_checkpoint).expect_partial()
            print ('Latest checkpoint restored!!')
        else:
            raise 'Checkpoint not found!'
    
    def preproces_cn(self, s):
        return re.sub('\s+', ' ', ' '.join(s))
        seg_list = jieba.cut(s)
        return " ".join(seg_list)
    def create_dataset(self, x, y):
        a = tf.data.Dataset.from_tensor_slices(x)  # ==> [ 1, 2, 3 ]
        b = tf.data.Dataset.from_tensor_slices(y)
        ds = tf.data.Dataset.zip((a, b))
        ds = ds.shuffle(buffer_size = 1000)
        return ds
    def encode(self, lang1, lang2):
        lang1 = [self.tokenizer_cn.vocab_size] + self.tokenizer_cn.encode(
            lang1.numpy()) + [self.tokenizer_cn.vocab_size+1]

        lang2 = [self.tokenizer_vn.vocab_size] + self.tokenizer_vn.encode(
            lang2.numpy()) + [self.tokenizer_vn.vocab_size+1]

        return lang1, lang2

    def tf_encode(self, en, vn):
        result_en, result_vn = tf.py_function(self.encode, [en, vn], [tf.int64, tf.int64])
        result_en.set_shape([None])
        result_vn.set_shape([None])

        return result_en, result_vn
    def filter_max_length(self, x, y, max_length=MAX_LENGTH):
        return tf.logical_and(tf.size(x) <= max_length,
                                tf.size(y) <= max_length)
    def evaluate(self, inp_sentence):
        start_token = [self.tokenizer_cn.vocab_size]
        end_token = [self.tokenizer_cn.vocab_size + 1]

        # inp sentence is eng, hence adding the start and end token
        inp_sentence = start_token + self.tokenizer_cn.encode(inp_sentence) + end_token
        encoder_input = tf.expand_dims(inp_sentence, 0)

        # as the target is vn, the first word to the transformer should be the
        # english start token.
        decoder_input = [self.tokenizer_vn.vocab_size]
        output = tf.expand_dims(decoder_input, 0)


        enc_padding_mask, combined_mask, dec_padding_mask = create_masks(
            encoder_input, output)
        enc_output = self.transformer.encoder(encoder_input, False, enc_padding_mask)
        
        for i in range(MAX_LENGTH):
            enc_padding_mask, combined_mask, dec_padding_mask = create_masks(
                encoder_input, output)
            dec_output, attention_weights = self.transformer.decoder(
                output, enc_output, False, combined_mask, dec_padding_mask)
            predictions = self.transformer.final_layer(dec_output)
            predictions = predictions[: ,-1:, :]  # (batch_size, 1, vocab_size)
            predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)
            if predicted_id == self.tokenizer_vn.vocab_size+1:
                return tf.squeeze(output, axis=0), attention_weights
            output = tf.concat([output, predicted_id], axis=-1)
        return tf.squeeze(output, axis=0), attention_weights
    def translate(self, sentence, plot=''):
        if self.dic.get(sentence):
            return self.dic[sentence]
        else:
            sentence = self.preproces_cn(sentence)
            result, attention_weights = self.evaluate(sentence)
            predicted_sentence = self.tokenizer_vn.decode([i for i in result 
                                                        if i < self.tokenizer_vn.vocab_size])  
            return predicted_sentence

if __name__ == "__main__":
    test = Test()
    s = time.time()
    print(test.translate('你好！'))
    
    print(time.time() -s)
    s = time.time()
    print(test.translate('汕'))
    print(time.time() -s)