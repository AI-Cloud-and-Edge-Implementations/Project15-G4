import matplotlib.pyplot as plt
from sklearn import metrics
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras
import tensorflow as tf

from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths


class ElephantCounterResnet:
    def __init__(self, training_loc = '', epochs = 25, model_name='binaries/resnet_'):
        self.res_model = self._generate_res_model()
        self.epochs = epochs
        self.model_save_loc = model_name + str(epochs) + '_epoch'
        self.training_loc = training_loc
        self.datagen = ImageDataGenerator()

    @staticmethod
    def _generate_res_model():
        input_t = keras.Input(shape = (224, 224, 3))
        res_model = keras.applications.ResNet50(include_top = False, weights = "imagenet",
                                                input_tensor = input_t)

        return res_model

    def get_dataset_it(self, dir_path):
        return self.datagen.flow_from_directory(
            dir_path, target_size = (224, 224), class_mode = 'categorical'
        )

    def get_train_test_set(self, dir_path):
        # create generator
        # prepare an iterators for each dataset
        train_it = self.get_dataset_it(join_paths([dir_path, 'train']))
        val_it = self.get_dataset_it(join_paths([dir_path, 'val']))
        test_it = self.get_dataset_it(join_paths([dir_path, 'test']))
        return train_it, val_it, test_it

    def custom_sequential_model(self):
        for layer in self.res_model.layers[:143]:
            layer.trainable = False

        for i, layer in enumerate(self.res_model.layers):
            print(i, layer.name, "-", layer.trainable)

        to_res = (224, 224)
        
        model = keras.models.Sequential()
        model.add(keras.layers.Lambda(lambda image: tf.image.resize(image, to_res)))
        model.add(self.res_model)
        model.add(keras.layers.Flatten())
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Dense(256, activation = 'relu'))
        model.add(keras.layers.Dropout(0.5))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Dense(128, activation = 'relu'))
        model.add(keras.layers.Dropout(0.5))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Dense(64, activation = 'relu'))
        model.add(keras.layers.Dropout(0.5))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Dense(3, activation = 'softmax'))

        return model

    @staticmethod
    def load_model(model_save_loc):
        return keras.models.load_model(join_paths([get_project_root(), model_save_loc]))

    def build_model(self):
        train_it, val_it, test_it = self.get_train_test_set(
            self.training_loc
        )
        try:
            model = self.load_model(self.model_save_loc)
        except OSError:
            model = self.custom_sequential_model()

            model.compile(
                loss = 'categorical_crossentropy',
                #optimizer = keras.optimizers.RMSprop(lr = 2e-5),
                optimizer = keras.optimizers.Adam(learning_rate=0.001),
                metrics = ['accuracy']
            )

            history = model.fit(train_it, epochs = self.epochs, validation_data = val_it, batch_size=100)
            model.save(join_paths([get_project_root(), self.model_save_loc]))

            plt.plot(history.history['accuracy'], label = 'accuracy')
            plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
            plt.xlabel('Epoch')
            plt.ylabel('Accuracy')
            plt.ylim([0.5, 1])
            plt.legend(loc = 'lower right')
            #plt.savefig(join_paths([get_project_root(), 'graph.png']))
            plt.savefig(join_paths([get_project_root(), self.model_save_loc, 'graph.png']))

        pred = model.predict_classes(test_it)
        print(metrics.confusion_matrix(test_it.labels, pred))
        test_loss, test_acc = model.evaluate(test_it, verbose = 2)

        print(test_acc)

    def run_model(self, dir_path):
        data_it = self.get_dataset_it(join_paths(dir_path))
        try:
            model = self.load_model(self.model_save_loc)
        except OSError:
            print('model {} not loaded'.format(self.model_save_loc))
        else:
            return model.predict_classes(data_it)
