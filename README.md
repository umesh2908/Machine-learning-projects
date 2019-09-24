# Machine-learning-projects
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
df_train=pd.read_csv(r'D:\blackfriday_data\train_oSwQCTC\train.csv')
df_train.describe()
sns.set_style("whitegrid")
plt.figure(figsize=(10,5))
sns.countplot(df_train['Age'])
sns.countplot(df_train['Gender'])
sns.set_style("whitegrid")
plt.figure(figsize=(10,5))
sns.countplot(df_train['Age'],hue='Gender',data=df_train)
sns.set_style("whitegrid")
plt.figure(figsize=(10,5))
sns.countplot(df_train['Age'],hue=df_train['City_Category'])
sns.set_style("whitegrid")
plt.figure(figsize=(10,5))
sns.countplot(df_train['City_Category'])
sns.set_style("whitegrid")
plt.figure(figsize=(10,5))
sns.countplot(df_train['City_Category'],hue=df_train['Gender'])
sns.set_style("whitegrid")
plt.figure(figsize=(10,5))
sns.countplot(df_train['Gender'],hue=df_train['Marital_Status'])
df_train.isnull().sum()
#data_preprocessing
df_train['Age']=pd.get_dummies(df_train['Age'])
df_train['Gender']=pd.get_dummies(df_train['Gender'])
df_train['City_Category']=pd.get_dummies(df_train['City_Category'])
df_train['Product_Category_2']=df_train['Product_Category_2'].fillna(df_train['Product_Category_2'].mean())
df_train['Product_Category_3']=df_train['Product_Category_3'].fillna(df_train['Product_Category_3'].mean())
df_train['Stay_In_Current_City_Years']=df_train['Stay_In_Current_City_Years'].replace({'4+':4})
X=df_train.drop(['Purchase','Product_ID'],axis=1)
Y=df_train['Purchase']
X.isnull().sum(),Y.isnull().sum()
#split data into training and testing dataset 
from sklearn.model_selection import train_test_split
X_train , X_test , Y_train , Y_test = train_test_split (X,Y,test_size = 0.20 ,random_state=1)
#GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor
model = GradientBoostingRegressor(n_estimators=100,max_depth=4)
model.fit(X_train, Y_train)  
y_pred_GB = model.predict(X_test)
from sklearn import metrics
print('Mean Absolute Error:', metrics.mean_absolute_error(Y_test, y_pred_GB))  
print('Mean Squared Error:', metrics.mean_squared_error(Y_test, y_pred_GB))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(Y_test, y_pred_GB)))  
#Mean Absolute Error: 2195.1428007146806
#Mean Squared Error: 8497910.607736798
#Root Mean Squared Error: 2915.11759758278
#Randomforest_regression_model
from sklearn.ensemble import RandomForestRegressor

regressor = RandomForestRegressor(n_estimators = 150, oob_score='TRUE', n_jobs = -1,random_state =40,max_features = "auto", min_samples_leaf = 50) 
regressor.fit(X_train, Y_train)  
y_pred = regressor.predict(X_test)
from sklearn import metrics
print('Mean Absolute Error:', metrics.mean_absolute_error(Y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(Y_test, y_pred))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(Y_test, y_pred)))  
#Mean Absolute Error: 2131.943683167775
#Mean Squared Error: 8232608.7694961075
#Root Mean Squared Error: 2869.252301470909

 #testing of model on test data
df_test=pd.read_csv(r'D:\blackfriday_data\test_HujdGe7\test.csv')
df_test['Age']=pd.get_dummies(df_test['Age'])
df_test['Gender']=pd.get_dummies(df_test['Gender'])
df_test['City_Category']=pd.get_dummies(df_test['City_Category'])
df_test['Product_Category_2']=df_test['Product_Category_2'].fillna(df_test['Product_Category_2'].mean())
df_test['Product_Category_3']=df_test['Product_Category_3'].fillna(df_test['Product_Category_3'].mean())
df_test['Stay_In_Current_City_Years']=df_train['Stay_In_Current_City_Years'].replace({'4+':4})
x_test=df_test.drop('Product_ID',axis=1)
predictions = regressor.predict(x_test)
df = pd.DataFrame({'User_ID': df_test['User_ID'],'Product_ID':df_test['Product_ID'], 'Purchase':predictions.flatten()})
df.to_csv("submission_blackfriday3.csv")
