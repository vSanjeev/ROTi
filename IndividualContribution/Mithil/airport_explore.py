
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn import tree


airlines = pd.read_csv('airlines.csv')
airports = pd.read_csv('airports.csv')
flights = pd.read_csv('flights.csv')

df = flights

#print('Dataframe dimensions:', flights.shape)

tab_info=pd.DataFrame(df.dtypes).T.rename(index={0:'column type'})
tab_info=tab_info.append(pd.DataFrame(df.isnull().sum()).T.rename(index={0:'null values (nb)'}))
tab_info=tab_info.append(pd.DataFrame(df.isnull().sum()/df.shape[0]*100)
                         .T.rename(index={0:'null values (%)'}))
#print tab_info

#df = df.drop(['FLIGHT_NUMBER', 'TAIL_NUMBER', 'TAXI_OUT', 'WHEELS_OFF', 'SCHEDULED_TIME','ELAPSED_TIME','WHEELS_ON',
# 'TAXI_IN','SCHEDULED_ARRIVAL','DIVERTED', 'CANCELLED', 'CANCELLATION_REASON','DIVERTED', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY',
# 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY'])
df = df.iloc[:, [0,1,2, 3,4,7,8,10,11,16,17,21,22]]
#df = df.drop([''])

print list(df)
df = df.dropna(axis = 0, how = 'any')

#print df['DEPARTURE_DELAY'].head

df['Dep_Delay_bin'] = df['DEPARTURE_DELAY'].apply(lambda x: 1 if x >=15 else 0)

#print df['Dep_Delay_bin'].head

#print df.dtypes

clf = tree.DecisionTreeClassifier(criterion='entropy', min_samples_split=5)

le = preprocessing.LabelEncoder()
le.fit(df.iloc[:,4])
col_2_transformed =  le.transform(df.iloc[:,4])
#print col_2_transformed
df.iloc[:,4] = col_2_transformed

#print df.head



tr_data = df.iloc[:,[0,1,2,3,4,7,9,10,11,12]]
tr_target = df.iloc[:,13]


#print tr_data.head

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(tr_data, tr_target, test_size = 0.25, random_state = 0)

clf = clf.fit(X_train, y_train)

#Predicting the results
y_pred = clf.predict(X_test)

#making the confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print cm


tree.export_graphviz(clf, out_file='decision_tree.dat',
                     feature_names=list(tr_data)[0:10],
                     filled=True)


