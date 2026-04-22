from sklearn.ensemble import RandomForestClassifier

def train_model():
    model = RandomForestClassifier()

    X = [
        [5, 1],
        [200, 5],
        [3, 0],
        [300, 8]
    ]

    y = [0, 1, 0, 1]

    model.fit(X, y)
    return model