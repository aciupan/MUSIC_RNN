import numpy as np
import random
import tensorflow as tf
from constants import MELODY_DIR, CHORDS_DIR, DATA_X_NAME, DATA_Y_NAME,\
TIMESTEP, CONTINUATION_CHORD, VELOCITY, DICT_ALLCHORDS, DICT_MELODY,\
DICT_CHORDS, DICT_SIZE, MELODYCHORDS_LEN
from functions import song_to_chorddurlist, chorddurlists_to_soundlist,\
soundlist_split,soundlist_to_segmentlist, tuplesegment_to_twohotsegment,\
encoded_sound_to_soundlist, soundlist_to_midi, lstm_cell,\
twohotlist_to_tuplelist

## Constants

#Related to the training model
N_LAYERS                = 2     
N_LSTM_CELLS            = 256
NUMSEGM_IN_BATCH        = 20
NUM_EPOCHS              = 200
N_MODELS                = 20
PCT_TEST                = 0.7
PCT_TRAIN               = 0.2
PCT_VALID               = 0.1

# Define our model
class Model(object):
    def __init__(self, session, x_data, y_data, n_lstm_cells, n_layers):
        self.session                    = session
        self.x                          = x_data
        self.y                          = y_data
        self.x_input                    = tf.placeholder(tf.float32, [None,None,\
        DICT_SIZE]) 
        self.y_input                    = tf.placeholder(tf.float32, [None,None,\
        DICT_SIZE])
        y_input_melody                  = self.y_input[:, :, 0:MELODYCHORDS_LEN]
        y_input_chord                   = self.y_input[:, :, MELODYCHORDS_LEN:]
        
        # Tensorflow weight variables
        self.outer_layer_weights        = tf.Variable(tf.random_normal([\
                            n_lstm_cells, DICT_SIZE], dtype=tf.float32))
        self.outer_layer_bias            = tf.Variable(tf.random_normal([\
                                            DICT_SIZE],dtype = tf.float32))
        
        # RNN model. We use LSTM cells
        batch_size                      = tf.shape(self.x_input)[0]
        stacked_lstm                    = tf.contrib.rnn.MultiRNNCell(
                        [lstm_cell(N_LSTM_CELLS) for _ in range(n_layers)])
        init_state                      = stacked_lstm.zero_state(batch_size,\
                                        tf.float32)
        self.output, self.final_state   = tf.nn.dynamic_rnn(stacked_lstm,\
        self.x_input,dtype=tf.float32, initial_state = init_state)
        
        # Prediction tensors
        reshaped_output         = tf.reshape(self.output, [-1, n_lstm_cells])
        logits                  = tf.nn.xw_plus_b(reshaped_output,\
                                self.outer_layer_weights,self.outer_layer_bias)
        logits_melody           = logits[:, 0:MELODYCHORDS_LEN]
        logits_chord            = logits[:, MELODYCHORDS_LEN:]
        softmax_loss_melody     = tf.nn.softmax_cross_entropy_with_logits(\
                                logits = logits_melody, labels =y_input_melody)
        softmax_loss_chord      = tf.nn.softmax_cross_entropy_with_logits(\
                                logits = logits_chord, labels =y_input_chord)
        loss_chord              = tf.reduce_mean(softmax_loss_chord)
        loss_melody             = tf.reduce_mean(softmax_loss_melody)

        # Our neat loss function
        self.avg_loss           = 0.5 * loss_chord + 0.5* loss_melody
        self.predict_melody     = tf.argmax(tf.nn.softmax(logits_melody), axis=1)
        self.predict_chord      = tf.argmax(tf.nn.softmax(logits_chord), axis=1)
        optimizer               = tf.train.AdamOptimizer()
        self.minimize           = optimizer.minimize(self.avg_loss)
        self.session.run(tf.global_variables_initializer())
        self.saver              = tf.train.Saver(max_to_keep=N_MODELS)
    def train_model(self,session):
        num_segments            = self.x.shape[0]
        n                       = NUMSEGM_IN_BATCH
        num_packages            = num_segments // n
        for package_id in range(num_packages):
            x_dat = self.x[package_id*n:(package_id+1) * n, :, :]
            y_dat = self.y[package_id*n:(package_id+1) * n, :, :]
            session.run(self.minimize, {self.x_input: x_dat, self.y_input: y_dat})
    def save_model(self, id, folder):
        self.saver.save(self.session, folder, global_step = id)
    def predict(self, session, initial, max_len, name):
        seq_list          = list(initial)[:]
        l                 = len(seq_list)
        while (l < max_len):
            current_vector      = np.asarray(seq_list)
            shape               = current_vector.shape
            current_input       = np.zeros((1, l, DICT_SIZE))
            current_input[0]    = current_vector
            melody_id           = sess.run(self.predict_melody[-1],\
                                    {self.x_input: current_input})
            chords_id           = sess.run(self.predict_chord[-1],\
                                    {self.x_input: current_input})
            new_elem            = np.zeros(DICT_SIZE)
            new_elem[melody_id] = 1
            new_elem[chords_id+MELODYCHORDS_LEN] = 1
            seq_list.append(new_elem)
            l+=1

        # seq_list now has the encoding of the new song
        # we transform it into midi
        song_tuplelist = twohotlist_to_tuplelist(seq_list)
        song_soundlist = encoded_sound_to_soundlist(song_tuplelist,\
                            DICT_ALLCHORDS, CONTINUATION_CHORD, TIMESTEP)
        soundlist_to_midi(song_soundlist, name, VELOCITY)

# Data inputs
DATA_X                  = np.load(DATA_X_NAME + '.npy')
DATA_Y                  = np.load(DATA_Y_NAME + '.npy')

## Data setup

# Split the data into test, training and validation observations
n_rows                  = DATA_X.shape[0]
train_cutoff            = int(n_rows * 0.7)
test_cutoff             = int(n_rows * 0.2)
valid_cutoff            = int(n_rows * 0.1)
train_x                 = DATA_X[0:train_cutoff, :, :]
train_y                 = DATA_Y[0:train_cutoff, :, :]
test_x                  = DATA_X[train_cutoff:(train_cutoff + test_cutoff), :, :]
test_y                  = DATA_Y[train_cutoff:(train_cutoff + test_cutoff), :, :]
valid_x                 = DATA_X[(train_cutoff + test_cutoff):, :, :]
valid_y                 = DATA_Y[(train_cutoff + test_cutoff):, :, :]

# Train the model
# save_every_t_iter   = NUM_EPOCHS // N_MODELS
#sess                = tf.Session()
#model               = Model(sess, train_x, train_y, N_LSTM_CELLS, N_LAYERS)
#for i in range(NUM_EPOCHS):
#    model.train_model(sess)
#    test_err        = sess.run(model.avg_loss, {model.x_input:train_x,\
#                                model.y_input:train_y})
#    train_err       = sess.run(model.avg_loss, {model.x_input:test_x,\
#                                model.y_input:test_y})
#    if i % save_every_t_iter == 0 and i!= 0:
#        model.save_model(i, 'saved_models_3/')
#        print("Saved at step",i)
#    print(i, test_err, train_err)

# Load an existing model
sess                    = tf.Session()
model                   = Model(sess, train_x, train_y, N_LSTM_CELLS, N_LAYERS)
saver                   = model.saver
saver.restore(model.session, "saved_models_3/-85")


# Compose music from an existing sequence
initial_song            = valid_x[1, 0:16, :]
model.predict(sess, initial_song, 64, 'thurs1.mid')

sess.close()

