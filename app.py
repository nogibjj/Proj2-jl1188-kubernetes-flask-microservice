from flask import Flask
from flask import jsonify
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)


def sklearn_knn_predict(trainX, trainy, validX, distance_metric, k, validationy):
    # create KNeighborClassifier instance
    kNC = KNeighborsClassifier(n_neighbors=k, algorithm='brute', metric=distance_metric)
    kNC.fit(trainX, trainy)
    return [(distance_metric,k) , kNC.score(validX, validationy)]


def load(csv_file):
    """given a CSV file where each row is a data point,
    with the last column being the label and the rest being the vector,
    return a tuple consisting of two elements:
    (1) a matrix where each row is a vector, in the same order as they appear in the file
    (2) an array where the ith element is the label of the ith vector above.
    """

    DATA = np.loadtxt(csv_file, delimiter=',', skiprows=1) # Read data from comma delimited file
    y = DATA[:, -1] # last column is class
    X = DATA[:, :-1] # All columns except last column are features
    # print(y.shape)
    # print(X.shape)
    return (X, y)

def predictRainInCity(cityName):
    # load in CSV file and separate the returned object
    cityInfo = load("./weather/" + str(cityName) + ".csv")
    cityX = cityInfo[0]
    cityY = cityInfo[1]
    # split data into 70% and 30% training vs. testing data
    X_train, X_test, Y_train, Y_test = train_test_split(cityX, cityY, train_size=0.70, test_size=0.30)
    # scale features
    cityScaler = StandardScaler()
    cityScaler.fit(X_train)
    # cityScaler.mean_
    cityScaler.transform(X_train)
    cityScaler.transform(X_test)
    # calculate accuracy
    trainedCity = sklearn_knn_predict(cityScaler.transform(X_train), Y_train, cityScaler.transform(X_test), 'euclidean', 11, Y_test)
    res = {"name": str(cityName), "accuracy": str(trainedCity[1])}
    print(str(cityName))
    print("The accuracy is: " + str(trainedCity[1]))
    return res



@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    print("I am inside hello world")
    return 'Hello World! I can calculate my knn prediction accuracy at route: /accuracy/<cityname>. List of Cities: Canberra, GoldCoast, Hobart, Nuriootpa, Perth, Sydney, WaggaWagga, Wollongong'

@app.route('/accuracy/<cityname>')
def accuracyRoute(cityname):
    print(f"Calculating the accuracy of my trained knn model for {cityname}.")
    result = predictRainInCity(cityname)
    return jsonify(result)
    
    


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
