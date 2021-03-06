# -*- coding: utf-8 -*-
"""CreditCardFraud2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AFp-1VngiYWTqU-uXWjhvd82RXOknjj2
"""

import warnings
warnings.filterwarnings("ignore")

"""Importing libraries"""

import pandas as pd
import numpy as np
import seaborn as sb

df_trn = pd.read_csv("train_transaction.csv",low_memory=False)
df_idn = pd.read_csv("train_identity.csv",low_memory=False)
df = pd.merge(df_trn, df_idn,on='TransactionID', how='left')

pd.set_option('display.max_columns', 400)
pd.set_option('display.max_rows', 20)

df_trn.shape

df.isnull().sum()
df.shape
df[df.isnull().any(1)]

print(df_trn.shape) 
print(df_idn.shape)
print(df.shape)

mylist= list(df.isnull().sum().values)

len(mylist)

"""Separating the columns which contain null values more than 100000"""

rel_list = []
irr_list = []
for index,val in enumerate(mylist):
    if val<100000:
        rel_list.append(index)
    else :
        irr_list.append(index)

len(rel_list)

columnname =[]
for index, column in enumerate(df.columns):
    if index in rel_list:
        columnname.append(column)

df[columnname].isnull().sum().values

latestdf = df[columnname]

latestdf.dtypes

imputemedian=latestdf.select_dtypes(exclude=['object']).columns
len(imputemedian)

imputemode=latestdf.select_dtypes(include=['object']).columns
len(imputemode)

len(latestdf.columns)

for index,colval in enumerate(imputemedian):
    latestdf[colval].fillna(latestdf[colval].median(),inplace=True)

for index,colval in enumerate(imputemode):
    latestdf[colval].fillna(latestdf[colval].mode()[0],inplace=True)

latestdf.isnull().sum().values

latestdf.sort_values(by='TransactionID')

latestdf.isFraud.value_counts()

sb.countplot(data=latestdf,x='isFraud')

len(latestdf.P_emaildomain.value_counts())

"""Dropping the P_emaildomain column as encoding this will include 58 more columns"""

y_train = latestdf.isFraud
x_train = latestdf.drop(['isFraud','P_emaildomain'], axis =1)

latestdf.select_dtypes('object')
latestdf.ProductCD.value_counts()
latestdf.card4.value_counts()
latestdf.card6.value_counts()

del df
del latestdf
del df_trn 
del df_idn
import gc
gc.collect()

from imblearn.over_sampling import RandomOverSampler
over_sampler = RandomOverSampler(random_state=42)
x_res, y_res = over_sampler.fit_resample(x_train, y_train)

# pip install imblearn
print(y_res.value_counts())
print(x_res.shape)
print(y_res.shape)

"""x_res.drop_duplicates(inplace=False).shape"""

sb.countplot(x=y_res)

from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(drop='first',sparse=False)

print(x_res.ProductCD.value_counts())
print(x_res.card4.value_counts())
print(x_res.card6.value_counts())

ohe.fit(x_res[['ProductCD', 'card4', 'card6']])
x_encoded=ohe.transform(x_res[['ProductCD', 'card4', 'card6']])
import joblib
joblib.dump(ohe,'ohe.save')

x_enc=pd.DataFrame(data=x_encoded,columns=['ProductCD_W','ProductCD_C','ProductCD_R','ProductCD_H','card40','card41','card42','card60','card61','card62'])
x_enc

x_res.drop(['ProductCD', 'card4', 'card6'],inplace=True,axis=1)
print(x_enc.shape)
print(x_res.shape)

newres= pd.concat([x_res,x_enc],axis=1)
print(newres.shape)

del x_res
del x_enc
gc.collect()

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report,accuracy_score,precision_score,confusion_matrix,f1_score,recall_score
import pickle

x_train_, x_test_, y_train_, y_test_ = train_test_split(newres,y_res,stratify=y_res, test_size=0.20, random_state=42)

def model_evaluation(modelname,model_):
  print("Training model :"+modelname+"\n\n")
  model = model_
  model.fit(x_train_,y_train_)
  predict = model.predict(x_test_)
  #print("Classification report for model "+modelname+ " is:" +str(classification_report(y_test_,predict)))
  print("Accuracy score for model "+modelname+" is:   "+str(accuracy_score(y_test_,predict)))
  print("Precision score for model "+modelname+" is : "+str(precision_score(y_test_,predict)))   
  print("F1 score for model "+modelname+" is : "+str(f1_score(y_test_,predict))) 
  print("Confusion matrix for model "+modelname+" is : "+str(confusion_matrix(y_test_,predict))) 
  print("Recall score for model "+modelname+" is : "+str(recall_score(y_test_,predict))) 
  print(model.get_params())
    
  pickle.dump(model,open('model_'+modelname+'.pkl','wb'))

models = {
          'RandomForestClassifier':RandomForestClassifier(),
          'DecisionTreeClassifier':DecisionTreeClassifier(),
          'LogisticRegression':LogisticRegression(),
          'AdaBoostClassifier':AdaBoostClassifier()
}
for modelname,model in models.items() : 
      model_evaluation(modelname,model)

from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import cross_val_score

random_search = {'max_depth': [5,10,20,40],               
               'min_samples_leaf': [4, 8, 12],
               'max_depth': [int(val) for val in np.linspace(10, 50, num = 5,dtype=int)],
               'min_samples_split': [5, 10, 15],
               'n_estimators': [int(val) for val in np.linspace(start = 200, stop = 2000, num = 10,dtype=int)]}

model = RandomizedSearchCV(estimator = RandomForestClassifier(), param_distributions = random_search, 
                               cv = 5, verbose= 5, random_state= 42, n_jobs = -1)
model_evaluation('hyperparametrised_rf',model)



