from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import numpy as np
import pandas as pd

class PongAI:

    def __init__(self,mode):
        self.model = make_pipeline(StandardScaler(),(DecisionTreeClassifier() if mode == "d" else LogisticRegression()))
        self.X = []
        self.y = []
        self.isTrained = False
    
    def train(self):
        self.isTrained = True
        self.model.fit(self.X,self.y)
    
    def predict(self,X):
        return self.model.predict(X)