
#import libraries
import streamlit as st
st.write("This is our project of hardware and software for big data.")
import pandas as pd
import numpy as np

from pathlib import Path
import io
import sys
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from plotnine import *
import statsmodels.api as sm
import seaborn as sns
import plotly.figure_factory as ff
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from xgboost import XGBClassifier
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
import missingno as msno
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import silhouette_score
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# Load the dataset

@st.cache_data
def load_data():
    courses = pd.read_csv('C:/Users/kk928/Downloads/archive/courses.csv')
    assessments = pd.read_csv('C:/Users/kk928/Downloads/archive/assessments.csv')
    student_assessments = pd.read_csv('C:/Users/kk928/Downloads/archive/studentAssessment.csv')
    student_info = pd.read_csv('C:/Users/kk928/Downloads/archive/studentInfo.csv')
    student_registration = pd.read_csv('C:/Users/kk928/Downloads/archive/studentRegistration.csv')
    student_vle = pd.read_csv('C:/Users/kk928/Downloads/archive/studentVle.csv')
    vle = pd.read_csv('C:/Users/kk928/Downloads/archive/vle.csv')
    return courses, assessments, student_assessments, student_info, student_registration, student_vle, vle

# Load data
courses, assessments, student_assessments, student_info, student_registration, student_vle, vle = load_data()

# Streamlit app
st.title('Open University Learning Analytics Dataset')
st.write("Loading all the dataset")

         
        
st.sidebar.title('Dataset Overview')
dataset_option = st.sidebar.selectbox('Select a dataset', ('Courses', 'Assessments', 'Student Assessments', 'Student Info', 'Student Registration', 'Student VLE', 'VLE'))

if dataset_option == 'Courses':
    st.header('Courses')
    st.write(courses.head(5))
    st.write('SIZE',('Row, Coloumn' ,courses.shape))
    st.write("Data Types",(courses.dtypes))
    st.write(courses.describe())
elif dataset_option == 'Assessments':
    st.header('Assessments')
    st.write(assessments.head(5))
    st.write('SIZE',('Row, Coloumn' ,assessments.shape))
    st.write("Data Types",(assessments.dtypes))
    st.write(assessments.describe())
elif dataset_option == 'Student Assessments':
    st.header('Student Assessments')
    st.write(student_assessments.head(5))
    st.write('SIZE',('Row, Coloumn' ,student_assessments.shape))
    st.write("Data Types",(student_assessments.dtypes))
    st.write(student_assessments.describe())
elif dataset_option == 'Student Info':
    st.header('Student Info')
    st.write(student_info.head(5))
    st.write('SIZE',('Row, Coloumn' ,student_info.shape))
    st.write("Data Types",(student_info.dtypes))
    st.write(student_info.describe())
elif dataset_option == 'Student Registration':
    st.header('Student Registration')
    st.write(student_registration.head(5))
    st.write('SIZE',('Row, Coloumn' ,student_registration.shape))
    st.write("Data Types",(student_registration.dtypes))
    st.write(student_registration.describe())
elif dataset_option == 'Student VLE':
    st.header('Student VLE')
    st.write(student_vle.head(5))
    st.write('SIZE',('Row, Coloumn' ,student_vle.shape))
    st.write("Data Types",(student_vle.dtypes))
    st.write(student_vle.describe())
elif dataset_option == 'VLE':
    st.header('VLE')
    st.write(vle.head(5))
    st.write('SIZE',('Row, Coloumn' ,vle.shape))
    st.write("Data Types",(vle.dtypes))
    st.write(vle.describe())
# Example Analysis: Distribution of final results
st.sidebar.title('Analysis')
analysis_option = st.sidebar.selectbox('Select an analysis', ('Final Results Distribution', 'Assessment Scores', 'VLE Activity'))

if analysis_option == 'Final Results Distribution':
    st.header('Distribution of Final Results')
    plt.figure(figsize=(10, 6))
    sns.countplot(x='final_result', data=student_info)
    st.pyplot(plt)
elif analysis_option == 'Assessment Scores':
    st.header('Assessment Scores Distribution')
    plt.figure(figsize=(10, 6))
    sns.histplot(student_assessments['score'], bins=30)
    st.pyplot(plt)
elif analysis_option == 'VLE Activity':
    st.header('VLE Activity Analysis')
    vle_activity = student_vle.merge(vle, on='id_site')
    vle_activity_summary = vle_activity.groupby('activity_type')['sum_click'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(x='activity_type', y='sum_click', data=vle_activity_summary)
    plt.xticks(rotation=45)
    st.pyplot(plt)


vle_null_values = vle.isnull().sum()



st.write("NULL VALUES DETECTION",vle_null_values)
st.write("Find unregistered students according to registration table. \
        Then check whether they are consistent with the final results at StudentInfo table. \
        #If a student is unregistered, final result must be recorded as 'Withdrawn'.")


st.write("Select unregistered students according to registration table")
temp = student_registration.loc[student_registration.date_unregistration.notna(),['id_student','code_presentation','date_unregistration']]

# Join to see matching rows
temp =pd.merge(student_info, temp, on=['id_student','code_presentation'])

st.write("Unregistered students without a 'Withdrawn' in final result column \
        # Semantic Error -- If a student unregistered, have to have 'Withdrawn' as final result! ")
wrong_final_results=temp.loc[temp.final_result!='Withdrawn']
incorrect_final_results=wrong_final_results.index
st.write(wrong_final_results.head())

st.write("8 of these 9 students unregistered at the first day of the module presentation or earlier (by looking date_unregistration column), this may be a cause for that inconsistency.\
This also makes a 'Fail' impossible as a final result. The above 9 records' final_result entry will be changed into Withdrawn in the next step.")

st.write("Correction info_stu table's final_result entries")
for i in wrong_final_results[['id_student','code_module','code_presentation']].values:
    student_info.loc[(student_info.id_student==i[0])&(student_info.code_module==i[1])&\
                 (student_info.code_presentation==i[2]),'final_result'] = 'Withdrawn'


st.write('Consistency of Weights of Assesments')
st.write('As mentioned under Assessments table explanation, weights of the exams should sum up to %100 and other assessments should sum up to %100. Hence, total weight for each module_presentation should be 200.')

st.write(assessments.groupby(['code_module','code_presentation']).agg(total_weight = ('weight',sum)))

st.write("Module CCC adds up to 300 and module GGG adds up to 100 -- these 2 will be investigated.")
st.write(assessments[assessments.code_module.isin(["CCC","GGG"])]\
.groupby(['code_module','code_presentation',"assessment_type"]).agg(type_weights = ('weight',sum)))

st.write('Module CCC has an inconsistency. Total exam weight is 200%. Module CCC has 2 exams in every presentation so It is very likely to be entered as 2 times 100"%" instead of 50"%" and 50%. This will be fixed in the upcoming step.\
"Also Module GGG is incompatible. There is no weight assigned neither to TMA type nor to CMA type. For convenience TMA type assignments" weight will be imputed as to add up to 100.')

# Weights of exams are halved for module CCC
assessments.loc[(assessments.code_module=='CCC') &(assessments.assessment_type=='Exam'),'weight'] = \
assessments.loc[(assessments.code_module=='CCC') &(assessments.assessment_type=='Exam'),'weight']/2

# Weights of TMA type assessments arranged to be %100.
assessments.loc[(assessments.code_module=='GGG') & (assessments.assessment_type=='TMA'),'weight']=(100/3)

# Calculation of the marks by merging 2 tables to have assignment scores and weights together in one table.

# Join Assessment and StudentAssessment tables
joined=pd.merge(student_assessments,assessments,on='id_assessment',how='left')
# Calculate weighted scores for all assessments of all students
joined['score*weight']=(joined['score']*joined['weight'])

# Sum up score*weights and divide by total weights (There are some students has total weight higher or much lower than %100)
# for all students of all modules to calculate final mark.
marks=joined.groupby(['id_student','code_module','code_presentation'],as_index=False)[['score*weight','weight']].sum()

marks['adjusted_mark'] = marks['score*weight']/marks['weight']
marks["mark"]  = marks['score*weight']/200
marks.rename(columns = {'score*weight': 'total_score*weight', 'weight': 'attempted_weight'}, inplace=True)
marks = marks.round(1)


# Merging the marks table with info_stu to have a bigger table 
# containing all the relevant information about success, student characteristics and demographics.
joined = pd.merge(marks,student_info,on=['id_student','code_module','code_presentation'],how='left')

# There can be students who attempt some of the assignments but then withdraw the course,
# mark variable may have a value for these students.
# These marks shouldn't be used in analysis so will be replaced with NaN as follows.
joined.loc[joined.final_result=='Withdrawn','mark']= np.nan
joined.loc[joined.final_result=='Withdrawn','adjusted_mark']= np.nan



plt.figure(figsize=(10,6))
ggplot(joined) + geom_boxplot(aes(x="final_result", y="attempted_weight"))
plot_filename="plot boxplot and final score.png"
plt.savefig(plot_filename)
st.image(plot_filename, caption="boxplot and final score", use_column_width=True)


plt.figure(figsize=(10,8))
ggplot(joined[joined.final_result=="Distinction"]) + geom_point(aes(x="mark", y="adjusted_mark", color="attempted_weight"))\
+ggtitle("Students with Distinction Final Result")
plot_filename="students_pass with distinction.png"
plt.savefig(plot_filename)
st.image(plot_filename, caption="students Final result with distinction", use_column_width=True)

plt.figure(figsize=(10,8))
ggplot(joined[joined.final_result=="Pass"]) + geom_point(aes(x="mark", y="adjusted_mark", color="attempted_weight"))\
+ggtitle("Students with Pass Final Result")
plot_filename="students_pass with final result.png"
plt.savefig(plot_filename)
st.image(plot_filename, caption="students pass with final result", use_column_width=True)

plt.figure(figsize=(10,8))
ggplot(joined[joined.final_result=="Fail"]) + geom_point(aes(x="mark", y="adjusted_mark", color="attempted_weight"))\
+ggtitle("Students with Fail Final Result")
plot_filename="Students with Fail Final Result.png"
plt.savefig(plot_filename)
st.image(plot_filename, caption="Students with Fail Final Result", use_column_width=True)

st.write('By comparing the above 3 graphs-')

st.write('Difference between adjusted_mark and mark is much higher for "Fail" students.\
Suggesting that these students probably didn''t attempted these missing assessments indeed. Issue is not about being included in the dataset.\
For the attempted weight of 200 (attempting all assessments);\
Almost all Distinction results are higher than 70.\
Almost all Pass marks are higher than 40\
Therefore, 0-40 band will be accapted as "Fail", 40-70 band will be accapted as "Pass" and 70-100 as "Distinction".')

################
st.write("Most of the entries of 'week_from' and 'week_to' attributes are missing so the analysis will not be focusing on the datesIn order to get ride of the extra load on memory, these columns will be dropped in the next step.")
vle.drop(columns=['week_from','week_to'],inplace=True)

# Find the null values in the dataset student_registraion
studentRegistration_null_values = student_registration.isnull().sum()
st.write("Null values in student registration data")
# Displaying the null values
st.write(studentRegistration_null_values)

st.write("70'%' of the rows are missing date_unregistration. This means that 70'%' of the students don't withdraw the modules.")

####





# Fill null values in 'date_registration' with the mode of the column
date_registration_mode = student_registration['date_registration'].mode()[0]
student_registration['date_registration'].fillna(date_registration_mode, inplace=True)

# Fill null values in 'date_unregistration' with the mode of the column
date_unregistration_mode = student_registration['date_unregistration'].mode()[0]
student_registration['date_unregistration'].fillna(date_unregistration_mode, inplace=True)


# Find the null values in the dataset
studentRegistration_null_values = student_registration.isnull().sum()

# Displaying the null values
st.write(studentRegistration_null_values)


# Fill null values in 'imd_band' with the mode of the column
imd_band_mode = student_info['imd_band'].mode()[0]
student_info['imd_band'].fillna(imd_band_mode, inplace=True)


# Find the null values in the dataset
studentInfo_null_values = student_info.isnull().sum()

# Displaying the null values
st.write(studentInfo_null_values)

st.write(student_info.shape)

# Fill null values in 'score' with the mean of the column
score_mean = student_assessments['score'].mean()
student_assessments['score'].fillna(score_mean, inplace=True)

# Find the null values in the dataset
studentAssessment_null_values = student_assessments.isnull().sum()

# Displaying the null values
st.write(studentAssessment_null_values)

# Fill null values in 'date' with the mean of the column
date_mean = assessments['date'].mean()
assessments['date'].fillna(date_mean, inplace=True)

# Find the null values in the dataset
assessments_null_values = assessments.isnull().sum()

# Displaying the null values
st.write(assessments_null_values)

st.write("Exploratory data analysis")
#Checking gender distribution
plt.figure(figsize=(8, 6))
sns.countplot(x='gender', data=student_info)

# Save the plot as a file
plt.savefig('gender_count_plot.png')

# Optionally, display the plot
st.image('gender_count_plot.png', caption='Gender Distribution', use_column_width=True)

#Now let's try the same on age
#student_info[['id_student', 'age_band']].groupby(by='age_band').count().plot.bar();
#this shows majority of students fall in age band of 0-35


# Sample DataFrame (replace this with your actual data)


# Grouping by age_band and counting the number of students in each band
age_band_counts = student_info[['id_student', 'age_band']].groupby(by='age_band').count()

# Plotting the bar chart
plt.figure(figsize=(8, 6))
age_band_counts.plot(kind='bar', legend=False)
plt.xlabel('Age Band')
plt.ylabel('Number of Students')
plt.title('Number of Students by Age Band')

# Save the plot as an image file
plot_filename = 'age_band_count_plot.png'
plt.savefig(plot_filename)

# Display the image in the Streamlit app
st.image(plot_filename, caption='Number of Students by Age Band', use_column_width=True)

st.write("Students by regions")
region_counts = student_info[['id_student', 'region']].groupby(by='region').count()

# Plotting the bar chart
plt.figure(figsize=(10, 6))
region_counts.plot(kind='bar', legend=False)
plt.xlabel('Region')
plt.ylabel('Number of Students')
plt.title('Number of Students by Region')

plt.xticks(rotation=45, ha='right')

# Adjust layout to make room for rotated labels
plt.tight_layout()

# Save the plot as an image file
plot_filename = 'region_count_plot.png'
plt.savefig(plot_filename)

# Display the image in the Streamlit app
st.image(plot_filename, caption='Number of Students by Region', use_column_width=True)

data_to_plot = student_info.drop(['id_student', 'num_of_prev_attempts'], axis=1)

# Creating the box plot grouped by 'region'
plt.figure(figsize=(12, 8))
data_to_plot.boxplot(by='region')
plt.xticks(rotation=90)
plt.title('Box Plot by Region')
plt.suptitle('')  # Suppress the default title to avoid overlapping
plt.xlabel('Region')
plt.ylabel('Values')  # Adjust this as per your actual data columns

plt.xticks(rotation=45, ha='right')

# Adjust layout to make room for rotated labels
plt.tight_layout()

# Save the plot as an image file
plot_filename = 'box_plot_by_region.png'
plt.savefig(plot_filename)

# Display the image in the Streamlit app
st.image(plot_filename, caption='Box Plot by Region', use_column_width=True)


region_age_crosstab = pd.crosstab(student_info.region, student_info.age_band)

# Plotting the horizontal stacked bar chart
plt.figure(figsize=(10, 6))
region_age_crosstab.plot(kind='barh', stacked=True, ax=plt.gca())
plt.xlabel('Number of Students')
plt.ylabel('Region')
plt.title('Number of Students by Region and Age Band')

# Adjust layout
plt.tight_layout()

# Save the plot as an image file
plot_filename = 'region_age_distribution_plot.png'
plt.savefig(plot_filename)

# Display the image in the Streamlit app
st.image(plot_filename, caption='Number of Students by Region and Age Band', use_column_width=True)


plt.figure(figsize=(10, 6))
sns.boxplot(x = 'region', y = 'studied_credits', data=student_info)
plt.xticks(rotation = 90)
plt.tight_layout()

plt.savefig('box_plot_students credit by region.png')

# Optionally, display the plot
st.image('box_plot_students credit by region.png', caption='students credit by region', use_column_width=True)

st.write("selecting a subset of cols which are of importance to us and grouping them by student id and aggregating them using median")
# selecting a subset of cols which are of importance to us and grouping them by student id and aggregating them using median
studentPerformance_df = student_info[['id_student', 'num_of_prev_attempts', 'studied_credits']].groupby('id_student').median()
studentPerformance_df = studentPerformance_df.reset_index()
st.write(studentPerformance_df.head())

st.write("new dataframe for students information with his education, region and age deatils. dropped duplicate values")
studentProfile_df = student_info[['id_student', 'gender', 'region','highest_education', 'imd_band', 'age_band']].drop_duplicates()
st.write(studentProfile_df.head())
st.write(studentProfile_df.shape)
st.write(studentProfile_df.dtypes)
st.write(studentProfile_df.describe())



st.write("students enrolled in different courese wise")
plt.figure(figsize=(10,6))
sns.countplot(student_info.code_module)

plot_filename="students in different courses.png"
plt.savefig(plot_filename)
#course BBB and FFF are very famous
st.image(plot_filename,caption='students in different courses', use_column_width=True)

st.write("BBB and FFF is most popular courses in between students.")



plt.figure(figsize=(12,8))
pd.crosstab(student_info.code_module, student_info.code_presentation).plot.barh(stacked = True);
plot_filename="courses offer in different intakes and enrolled number of students.png"

plt.savefig(plot_filename)
st.image(plot_filename, caption="courses offer in different intakes and enrolled number of students", use_column_width=True )

st.write("'B' is for courses offered in Feb and 'J' is for courses offered in Oct.")
st.write("course 'CCC' is something introduced in 2014 only.")
st.write("course 'AAA' has a very low student count as compared to other courses")



student_vle = student_vle.merge(vle, on = 'id_site', how = 'left')




studentInteractivity_df = student_vle[['id_student',
                                     'activity_type', 'sum_click']].groupby(['id_student', 'activity_type']).mean()
studentInteractivity_df = studentInteractivity_df.reset_index()
st.write(studentInteractivity_df.head())
#pivoting will help us reduce multiple rows per student to one single row with multiple columns
#After this we can visualize the columns with missing data


studentInteractivity_df = studentInteractivity_df.pivot(index='id_student',
                                                    columns='activity_type', values='sum_click')
studentInteractivity_df = studentInteractivity_df.reset_index()

studentInteractivity_df = studentInteractivity_df[['id_student', 'forumng', 'homepage', 'oucollaborate',
       'oucontent', 'page', 'questionnaire', 'quiz',
       'resource', 'subpage', 'url']]


merged_data = student_info.merge(student_registration, on=['id_student', 'code_module', 'code_presentation'], how='left')\
                          .merge(student_assessments, on='id_student', how='left')\
                          .merge(assessments, on=['id_assessment', 'code_module', 'code_presentation'], how='left')\
                          .merge(courses, on=['code_module', 'code_presentation'], how='left')


# Scaling the data to bring into one range
sc = RobustScaler()

st.title(" Merging Data")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
import joblib



# Display basic info to check for missing values
st.write("\nBasic info of the dataset:")
st.write(merged_data.shape)
st.write(merged_data.describe())

# Label Encoding for categorical variables
label_encoders = {}
categorical_columns = ['code_module', 'code_presentation', 'gender', 'region', 'highest_education', 'imd_band', 'age_band', 'disability', 'final_result', 'assessment_type']

for column in categorical_columns:
    le = LabelEncoder()
    merged_data[column] = le.fit_transform(merged_data[column])
    label_encoders[column] = le



# Define features and target
X = merged_data.drop(columns=['final_result'])
y = merged_data['final_result']

# Impute missing values
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)



# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numerical features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# Initialize and train the model
clf = RandomForestClassifier(random_state=42)
st.write(clf.fit(X_train, y_train))

# Predict and evaluate
y_pred = clf.predict(X_test)
st.write("Confusion Matrix:")
st.write(confusion_matrix(y_test, y_pred))
st.write("Classification Report:")
st.write(classification_report(y_test, y_pred))



# Convert 'date_registration' to datetime
merged_data['date_registration'] = pd.to_datetime(merged_data['date_registration'], errors='coerce')

# Handle missing values
imputer = SimpleImputer(strategy='mean')
merged_data[['score']] = imputer.fit_transform(merged_data[['score']])

# Ensure data is sorted by date
st.write(merged_data.sort_values(by='date_registration', inplace=True))

# Set the index to date_registration
st.write(merged_data.set_index('date_registration', inplace=True))

# Display the first few rows to verify the changes
st.write("First few rows of the dataset after preparation:")
st.write(merged_data.head())

# Split the data into training and testing sets
train_data = merged_data.loc[:'2022-12-31']
test_data = merged_data.loc['2023-01-01':]

# Separate target variable
y_train = train_data['score']
y_test = test_data['score']


arima_model = sm.tsa.ARIMA(y_train, order=(1, 1, 1))
arima_result = arima_model.fit()

st.write("ARIMA Model Summary:")
st.write(arima_result.summary())




# Identify potential date columns
date_columns = [col for col in merged_data.columns if 'date' in col.lower()]
st.write("Potential date columns:")
st.write(date_columns)

# Ensure the correct column name is used
date_column = 'date_registration'  # Change this if the column name is different

if date_column in merged_data.columns:
    # Convert the date column to datetime
    merged_data[date_column] = pd.to_datetime(merged_data[date_column], errors='coerce')

    # Handle missing values
    imputer = SimpleImputer(strategy='mean')
    merged_data[['score']] = imputer.fit_transform(merged_data[['score']])

    # Ensure data is sorted by date
    st.write(merged_data.sort_values(by=date_column, inplace=True))

    # Set the index to the date column and set frequency
    st.write(merged_data.set_index(date_column, inplace=True))
    merged_data = merged_data.asfreq('D')

    

    # Split the data into training and testing sets
    train_data = merged_data.loc[:'2022-12-31']
    test_data = merged_data.loc['2023-01-01':]

    # Separate target variable
    y_train = train_data['score']
    y_test = test_data['score']

    # Fit the ARIMA model
    arima_model = sm.tsa.ARIMA(y_train, order=(1, 1, 1))
    arima_result = arima_model.fit()

    # Display the model summary
    st.write("ARIMA Model Summary:")
    st.write(arima_result.summary())

    # Forecast future values
    forecast = arima_result.get_forecast(steps=len(y_test))
    forecast_mean = forecast.predicted_mean
    forecast_conf_int = forecast.conf_int()

    # Plot the forecast
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(y_train.index, y_train, label='Training Data')
    ax.plot(y_test.index, y_test, label='Actual Data')
    ax.plot(forecast_mean.index, forecast_mean, label='Forecast')
    ax.fill_between(forecast_conf_int.index, forecast_conf_int.iloc[:, 0], forecast_conf_int.iloc[:, 1], color='pink', alpha=0.3)
    ax.legend()
    ax.set_title('ARIMA Forecast')
    ax.set_xlabel('Date')
    ax.set_ylabel('Score')

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Evaluate the model
    mse = mean_squared_error(y_test, forecast_mean)
    st.write(f"Mean Squared Error: {mse}")

else:
    st.write(f"Error: The column '{date_column}' does not exist in the dataset.")




df = merged_data




# Select the relevant column for time series analysis
ts = df['score'].dropna()

# Apply ARIMA model
model = ARIMA(ts, order=(1, 1, 1))
model_fit = model.fit()

# Print summary of the model


# Plot the residuals to check for any patterns
residuals = model_fit.resid.dropna()
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(residuals)
ax.set_title('Residuals')
st.pyplot(fig)

# Plot ACF of residuals
fig, ax = plt.subplots(figsize=(10, 6))
plot_acf(residuals, lags=30, ax=ax)
ax.set_title('ACF of Residuals')
st.pyplot(fig)

# Plot PACF of residuals
fig, ax = plt.subplots(figsize=(10, 6))
plot_pacf(residuals, lags=30, ax=ax)
ax.set_title('PACF of Residuals')
st.pyplot(fig)




from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet



# Select the relevant column for time series analysis


# Split the data into training and testing sets
train_size = int(len(df) * 0.8)
train, test = df[:train_size], df[train_size:]

# Apply Prophet model
model = Prophet()
model.fit(train)

# Forecast the next steps
future = model.make_future_dataframe(periods=len(test))
forecast = model.predict(future)

# Plot the forecast
fig1 = model.plot(forecast)
st.pyplot(fig1)

# Plot the forecast components
fig2 = model.plot_components(forecast)
st.pyplot(fig2)
