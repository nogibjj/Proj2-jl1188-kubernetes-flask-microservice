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
    cityScaler.mean_
    cityScaler.transform(X_train)
    cityScaler.transform(X_test)
    # calculate accuracy
    trainedCity = sklearn_knn_predict(cityScaler.transform(X_train), Y_train, cityScaler.transform(X_test), 'euclidean', 11, Y_test)
    print(str(cityName))
    print("The accuracy is: " + str(trainedCity[1]))
    # result = "The accuracy is: " + str(trainedCity[1])
    return 0

def change(amount):
    # calculate the resultant change and store the result (res)
    res = []
    coins = [1,5,10,25] # value of pennies, nickels, dimes, quarters
    coin_lookup = {25: "quarters", 10: "dimes", 5: "nickels", 1: "pennies"}

    # divide the amount*100 (the amount in cents) by a coin value
    # record the number of coins that evenly divide and the remainder
    coin = coins.pop()
    num, rem  = divmod(int(amount*100), coin)
    # append the coin type and number of coins that had no remainder
    res.append({num:coin_lookup[coin]})

    # while there is still some remainder, continue adding coins to the result
    while rem > 0:
        coin = coins.pop()
        num, rem = divmod(rem, coin)
        if num:
            if coin in coin_lookup:
                res.append({num:coin_lookup[coin]})
    return res


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    print("I am inside hello world")
    return 'Hello World! I can make change at route: /change'

@app.route('/change/<dollar>/<cents>')
def changeroute(dollar, cents):
    print(f"Make Change for {dollar}.{cents}")
    amount = f"{dollar}.{cents}"
    result = change(float(amount))
    return jsonify(result)
    
    
@app.route('/100/change/<dollar>/<cents>')
def change100route(dollar, cents):
    print(f"Make Change for {dollar}.{cents}")
    amount = f"{dollar}.{cents}"
    amount100 = float(amount) * 100
    print(f"This is the {amount} X 100")
    result = change(amount100)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
