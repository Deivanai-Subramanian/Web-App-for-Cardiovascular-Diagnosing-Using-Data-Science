import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
scal = MinMaxScaler()

# Load the saved model
heart_dataset = pd.read_csv('HeartDisease.csv')

# Initialize data and target
features_1 = heart_dataset.drop(['target'], axis = 1)
target_1 = heart_dataset['target']

# Split the data into training set and testing set
X_train, X_test, y_train, y_test = train_test_split(features_1, target_1, test_size = 0.3, random_state = 0)
rf = RandomForestClassifier(random_state = 1)
rf.fit(X_train, y_train)
model = rf

#front end
st.set_page_config(page_title="Cardiovascular Disease Diagnosis WebApp", page_icon="⚕️", layout="centered", initial_sidebar_state="expanded")

# front end elements of the web page
html_temp = """ 
    <div style ="background-color:DodgerBlue;padding:13px"> 
    <h1 style ="color:white;text-align:center;">CARDIOVASCULAR DISEASE DIAGNOSIS WEB APP</h1> 
    </div> 
    """
# display the front end aspect
st.markdown(html_temp, unsafe_allow_html=True)
st.image('heart-disease-treatment-in-baner-800x400.png')
st.subheader('Cardiovascular Disease Test Form')

def user_input_features():
    # following lines create boxes in which user can enter data required to make prediction
    age = st.selectbox("Age", range(1, 121, 1))
    sex = st.radio("Select Gender: ", ('Male', 'Female'))
    cp = st.selectbox('Chest Pain Type', ("Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"))
    trestbps = st.selectbox('Resting Blood Sugar', range(1, 500, 1))
    chol = st.selectbox('Serum Cholestoral in mg/dl', range(1, 1000, 1))
    fbs = st.radio("Fasting Blood Sugar higher than 120 mg/dl", ("Yes", "No"))
    restecg = st.selectbox('Resting Electrocardiographic Results', (
        "Normal", "ST-T Wave abnormality", "Possible or definite left ventricular hypertrophy"))
    thalach = st.selectbox('Maximum Heart Rate Achieved', range(1, 300, 1))
    exang = st.radio('Exercise Induced Angina', ("Yes", "No"))
    oldpeak = st.number_input('Oldpeak')
    slope = st.selectbox('Heart Rate Slope', (
        "Upsloping: better heart rate with excercise(uncommon)", "Flatsloping: minimal change(typical healthy heart)",
        "Downsloping: signs of unhealthy heart"))
    ca = st.selectbox('Number of Major Vessels Colored by Flourosopy', range(0, 4, 1))
    thal = st.selectbox('Thalium Stress Result', ("None","Normal", "Fixed defect", "Reversable defect"))

# Pre-processing user input
    if sex == "Male":
        sex = int(1)
    else:
        sex = int(0)

    if cp == "Typical angina":
        cp = int(0)
    elif cp == "Atypical angina":
        cp = int(1)
    elif cp == "Non-anginal pain":
        cp = int(2)
    elif cp == "Asymptomatic":
        cp = int(3)

    if exang == "Yes":
        exang = int(1)
    elif exang == "No":
        exang = int(0)

    if fbs == "Yes":
        fbs = int(1)
    elif fbs == "No":
        fbs = int(0)

    if slope == "Upsloping: better heart rate with excercise(uncommon)":
        slope = int(0)
    elif slope == "Flatsloping: minimal change(typical healthy heart)":
        slope = int(1)
    elif slope == "Downsloping: signs of unhealthy heart":
        slope = int(2)


    if thal == "Fixed defect":
        thal = int(3)
    elif thal == "Reversable defect":
        thal = int(2)
    elif thal == "Normal":
        thal = int(1)
    else :
        thal = int(0)

    if restecg == "Normal":
        restecg = int(0)
    elif restecg == "ST-T Wave abnormality":
        restecg = int(1)
    elif restecg == "Possible or definite left ventricular hypertrophy":
        restecg = int(2)
    data = {'age': age,
            'sex': sex,
            'cp': cp,
            'trestbps':trestbps,
            'chol': chol,
            'fbs': fbs,
            'restecg': restecg,
            'thalach':thalach,
            'exang':exang,
            'oldpeak':oldpeak,
            'slope':slope,
            'ca':ca,
            'thal':thal
                }
    features = pd.DataFrame(data, index=[0])
    return features
input_df = user_input_features()
prediction = rf.predict(input_df)
prediction_proba = rf.predict_proba(input_df)

if st.button("Predict"):
    if prediction[0] == 1:
        st.error('Warning! You have high risk of getting a Cardiovascular Disease!')
        st.write(prediction_proba[0][1]*100,"% You are in Danger!")

    else:
        st.success('You have lower risk of getting a Cardiovascular Disease!')
        st.write(prediction_proba[0][0]*100,"% You are Healthy!")

st.sidebar.subheader("About App")
st.sidebar.info("This web app is helps you to find out whether you are at a risk of developing a Cardiovascular Disease.")
st.sidebar.info("Enter the required fields and click on the 'Predict' button to check whether you have a healthy heart")
st.sidebar.image('new7_Steps_to_a_Healthier_Heart.jpg')
