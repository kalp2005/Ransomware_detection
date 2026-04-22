def predict(model, features):
    prob = model.predict_proba([features])[0][1]  # probability of threat
    return prob