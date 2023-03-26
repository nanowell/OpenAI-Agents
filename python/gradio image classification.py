# use gradio to create a UI for image classification
import gradio as gr
import tensorflow as tf


def classify(image):
    image = tf.cast(image, tf.float32)
    image = tf.image.resize(image, (224, 224))
    image /= 255
    image = image.numpy()
    model = tf.keras.models.load_model('flower.h5')
    prediction = model.predict(image[None, ...])
    return {
        'daisy': prediction[0][0],
        'dandelion': prediction[0][1],
        'rose': prediction[0][2],
        'sunflower': prediction[0][3],
        'tulip': prediction[0][4]
    }


iface = gr.Interface(classify,
                     [gr.inputs.Image(shape=(224, 224, 3))],
                     'label',
                     examples=[
                         ['images/daisy.jpg'],
                         ['images/dandelion.jpg'],
                         ['images/rose.jpg'],
                         ['images/sunflower.jpg'],
                         ['images/tulip.jpg']
                     ])


if __name__ == '__main__':
    iface.launch()
