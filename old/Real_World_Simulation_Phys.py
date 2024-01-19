import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split

# Neural network model
def neural_net(X, layers):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(layers[0], activation='relu', input_shape=(X.shape[1],)))
    for layer in layers[1:]:
        model.add(tf.keras.layers.Dense(layer, activation='relu'))
    model.add(tf.keras.layers.Dense(1))
    return model

# Physics loss 
def physics_loss(y_true, y_pred):

    g = y_pred  
    T = y_true
    
    G = 6.67430e-11 # Gravitational constant
    c = 299792458 # Speed of light
    lambda_ = 1.0545718e-35 # Cosmological constant    
    k_b = 1.380649e-23 # Boltzmann constant
    h_bar = 1.0545718e-34 # Reduced Planck constant
    rho_vac = lambda_/(8*np.pi*G) # Vacuum energy density
    E = g - 8*np.pi*G*T + lambda_ # Modified Einstein field equations
    loss = tf.reduce_mean(tf.square(E)) 
    
    return loss

# Train as before
X = np.random.rand(100, 10) 
y = np.random.rand(100, 1) 

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the input data
X_train = (X_train - np.mean(X_train, axis=0)) / np.std(X_train, axis=0)
X_val = (X_val - np.mean(X_val, axis=0)) / np.std(X_val, axis=0)

layers = [64, 64, 64, 64]
model = neural_net(X_train, layers)
model.compile(optimizer='adam', loss=physics_loss)

# Add early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, verbose=1)

model.fit(X_train, y_train, epochs=500, validation_data=(X_val, y_val), callbacks=[early_stopping])

# Load the data for prediction
X_test = np.random.rand(50, 10) 

# Make predictions
y_pred = model.predict(X_test)

# Print predictions
for i in range(len(X_test)):
    print(f"Input: {X_test[i]}")
    print(f"Predicted output: {y_pred[i]}")
