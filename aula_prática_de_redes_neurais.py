# -*- coding: utf-8 -*-
"""Aula prática de Redes Neurais.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12i0A-aq36OAitregQgodEaevDgnAIQQO
"""

# Código de Milo Spencer-Harper
# https://gist.github.com/miloharper/62fe5dcc581131c96276
#
# Treino (função booleana OU):
# a b saída
# 0 0 0
# 0 1 1
# 1 0 1
# Teste:
# 1 1 1
from numpy import exp, array, random, dot
import numpy as np
entradas_treinamento = array([[0, 0], [0, 1], [1, 0]])
saidas_treinamento = array([[0, 1, 1]]).T
random.seed(1)
pesos_sinapticos = 2 * random.random((2, 1)) - 1 #pesos aleatórios entre -1 e 1
for epoca in range(100):
  saida = 1 / (1 + exp(-(dot(entradas_treinamento, pesos_sinapticos)))) #saídas do neurônio
  mudanca_pesos = dot(entradas_treinamento.T, (saidas_treinamento - saida) * saida * (1 - saida))
  pesos_sinapticos += mudanca_pesos
  print('Mudança nos pesos:', np.linalg.norm(mudanca_pesos))
#Testando com 1 e 1, esperando que dê 1 na saída
print (1 / (1 + exp(-(dot(array([1, 1]), pesos_sinapticos)))))

from sklearn.neural_network import MLPClassifier
X = [[0., 0.], [0., 1.], [1., 0.]]
y = [0., 1., 1.]
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(2), random_state=1)
clf.fit(X, y) #treino
clf.predict([[1.,1.]]) #aplicação/teste

import numpy as np
import pandas as pd
import seaborn as sns # visualization
from sklearn.neural_network import MLPClassifier # neural network
from sklearn.datasets import load_iris
iris = load_iris()
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.25)
#transformando a base em um dataframe def sklearn_to_df(sklearn_dataset):
df_iris = pd.DataFrame(iris.data, columns=iris.feature_names)
df_iris['target'] = pd.Series([iris['target_names'][iris['target'][i]] for i in range(150)])
sns.pairplot( data=df_iris, vars=('sepal length (cm)','sepal width (cm)','petal length (cm)','petal width (cm)'), hue='target')
df_iris.describe()
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(3, 3), random_state=1)
clf.fit(X_train, y_train)
prediction = clf.predict(X_test)
from sklearn.metrics import classification_report
print('Relatório:\n',classification_report(y_test,prediction))
print("\nMatriz de confusão detalhada:\n", pd.crosstab(y_test, prediction, rownames=['Real'], colnames=['Predito'],
  margins=True, margins_name='Todos'))

import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
#UPDATE:
from tensorflow.keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
# Carregamos os dados do conjunto de dados MNIST do pacote Keras
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_test_copy = X_test
y_test_copy = y_test
# Redimensionamos os dados e fazemos cast para float32
X_train = X_train.reshape(60000, 784).astype('float32')
X_test = X_test.reshape(10000, 784).astype('float32')
# Normalizamos os dados entre 0 e 1 (Dividimos pelo maximo)
X_train /= 255
X_test /= 255
# Convertemos de vetores de classes para matrizes binárias de classes.
Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)
model = Sequential()
model.add(Dense(units=512, input_shape=(784,)))
model.add(Activation('relu'))
model.add(Dense(units=512))
model.add(Activation('relu'))
model.add(Dense(units=10))
model.add(Activation('softmax'))
#Imprimimos o modelo no console
model.summary()
#Compilamos/Criamos o modelo
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])
#Executamos o treinamento
history = model.fit(X_train, Y_train, batch_size=128, verbose=1, validation_data=(X_test, Y_test))
#Testamos o modelo e imprimimos o resultado
score = model.evaluate(X_test, Y_test, verbose=0)
print('Score:', score[0])
print('Accuracy:', score[1])
# salve o modelo treinado e a arquitetura da rede para um único arquivo
model.save("model.h5")
print('Modelo salvo no disco')

from numpy import loadtxt
from keras.models import load_model
# carregue o modelo
model = load_model('model.h5')
# summarize model
model.summary()

predicao=np.argmax(model.predict(X_test),axis=1)
#UPDATE:  predicao = model.predict_classes(X_test)

# example of loading the mnist dataset
from matplotlib import pyplot
erros = 0
errosSumario=''
print('Previsões:')
# plot first few images
for i in range(100):
  # define subplot
  pyplot.subplot(10, 10, 1 + i)
  # plot raw pixel data
  pyplot.imshow(X_test_copy[i], cmap=pyplot.get_cmap('gray'))
  if(i%10 == 0): print('')
  print(predicao[i], end=' ')
  if predicao[i] != y_test[i]:
    erros += 1
    errosSumario += ('Errei na linha ' + str(i//10 + 1) + ' e coluna ' + str(i%10 + 1) +
      ': Real = ' + str(y_test[i]) + ', Predito = ' + str(predicao[i]) + '\n')
# show the figure
print('\n\nImagens:\n')
pyplot.show()
print('\nErros =', erros)
print(errosSumario)

"""**Exercício:** Testemos uma base nova (*breast_cancer*) com o uso da biblioteca *sklearn*."""

import numpy as np
import pandas as pd
import seaborn as sns # visualization
from sklearn.neural_network import MLPClassifier # neural network
from sklearn.datasets import load_breast_cancer
bc = load_breast_cancer()

print(bc.DESCR)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(bc.data, bc.target, test_size=0.25, random_state=1)
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(3, 3), random_state=1)
clf.fit(X_train, y_train)
prediction = clf.predict(X_test)
from sklearn.metrics import classification_report
print('Relatório:\n',classification_report(y_test,prediction))
print("\nMatriz de confusão detalhada:\n", pd.crosstab(y_test, prediction, rownames=['Real'], colnames=['Predito'],
  margins=True, margins_name='Todos'))

"""**Este é um problema de Regressão:**

**Exercício:** Testemos uma base nova (*diabetes*) com o uso da biblioteca *sklearn*.
"""

from sklearn.datasets import load_diabetes
d = load_diabetes()

print(d.DESCR)

df = pd.DataFrame(d.data, columns=d.feature_names)
df.describe()

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor # neural network
X_train, X_test, y_train, y_test = train_test_split(d.data, d.target, test_size=0.25, random_state=1)
clf = MLPRegressor(solver='lbfgs', max_iter=2000, hidden_layer_sizes=(10, 6, 6, 3), random_state=1)
clf.fit(X_train, y_train)
prediction = clf.predict(X_test)

"""**Avaliando nosso modelo:**

Aqui estão três métricas de avaliação comuns para problemas de regressão:

• Mean Absolute Error (MAE) é a média do valor absoluto dos erros

• Mean Squared Error (MSE) é a média dos erros quadráticos

• Root Mean Squared Error (RMSE) é a raiz quadrada da média dos erros ao quadrado

**Comparando estas métricas:**

• MAE é o mais fácil de entender, porque é o erro médio.

• MSE é mais popular que o MAE, porque o MSE "pune" erros maiores, o que tende a ser útil no mundo real.

• RMSE é ainda mais popular que o MSE, porque o RMSE é interpretável nas unidades do eixo "y".

Todas essas são funções de perda, porque queremos minimizá-las.
"""



from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(y_test, prediction))
print('MSE:', metrics.mean_squared_error(y_test, prediction))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, prediction)))