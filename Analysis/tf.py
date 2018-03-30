import tensorflow as tf
import numpy as np
from sklearn.datasets import make_classification
from Processing import config
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, KFold
from sklearn import metrics, ensemble
import glob
import os

# Concatenate all the files from each person into one dataframe
configs = config.Config()
path = configs.localPathAverage
df = pd.concat((pd.read_csv(f) for f in glob.glob(os.path.join(path, '*.csv'))))
df.to_csv("concat.csv", sep=',', index=False)

# Binary classification
df['Stimulus'] = df['Stimulus'].replace([2, 3, 4, 5, 6], 1)
anti_stim = df['Stimulus'].replace(1, -1)
anti_stim = anti_stim.replace(0, 1)
anti_stim = anti_stim.replace(-1, 0)
df['Anti.Stim'] = anti_stim

# Create X - features and y - labels
X = df[['Palm.EDA', 'Heart.Rate', 'Breathing.Rate', 'Perinasal.Perspiration', 'Speed', 'Acceleration', 'Brake',
        'Steering', 'LaneOffset', 'Lane.Position', 'Distance', 'Gaze.X.Pos', 'Gaze.Y.Pos', 'Lft.Pupil.Diameter',
        'Rt.Pupil.Diameter']]
Y = df[['Stimulus', 'Anti.Stim']]

print(df['Stimulus'].shape)
print(anti_stim.shape)
print(len(Y.shape))

# Split features and labels into training and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=42)

# Parameters
learning_rate = 0.001
training_epochs = 100
batch_size = 100
display_step = 10


# Network Parameters
n_hidden_1 = 10 # 1st layer number of features
n_hidden_2 = 10 # 2nd layer number of features
n_input = 15 # Number of feature
n_classes = 2 # Number of classes to predict


# tf Graph input
x = tf.placeholder("float", [None, n_input])
y = tf.placeholder("float", [None, n_classes])

# Create model
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}

biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

# Construct model
pred = multilayer_perceptron(x, weights, biases)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Initializing the variables
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(len(X)/batch_size)
        X_batches = np.array_split(X, total_batch)
        Y_batches = np.array_split(Y, total_batch)
        # Loop over all batches
        for i in range(total_batch):
            batch_x, batch_y = X_batches[i], Y_batches[i]
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_x,
                                                          y: batch_y})
            # Compute average loss
            avg_cost += c / total_batch
        # Display logs per epoch step
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))
    print("Optimization Finished!")

    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy:", accuracy.eval({x: X_test, y: Y_test}))
    global result
    result = tf.argmax(pred, 1).eval({x: X_test, y: Y_test})