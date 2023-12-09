import streamlit as st
import pandas as pd
import joblib

# Streamlit App
# df.head()
def main():
    # st.write(df)
    # Set background image using HTML and CSS
    background_image_style = """
    <style>
        body {
            background-image: url('https://www.creatrixcampus.com/sites/default/files/2022-11/The-ultimate-guide-to-Placement-Management-system.jpg');  /* Replace with your image URL or local path */
            background-size: cover;
        }
    </style>
"""
    st.markdown(background_image_style, unsafe_allow_html=True)
    # df = pd.DataFrame('Balanceddataset.csv')

    st.title('Student Placement and Recommendation System')

    # Add a text box with content
    st.markdown("""
    Welcome! This project helps the students in pre-final and final years of their B. Tech course to know their individual placement status that they are most likely to achieve. 
    With this information, students can put in more hard work to enhance their chances of getting placed in companies that belong to higher hierarchies.
    Enter the details below and click 'Predict Placement' to see the recommendation.
    """)

    # User Input Fields
    st.header('Student SkillSet')
   
    dataframe = pd.read_csv('colab_dataframe.csv')
    filtered_dataset = dataframe[0:4500]
    # st.write(df.head())

    cgpa = st.number_input('Enter CGPA', min_value=0.0, max_value=10.0, value=7.0)
    internships = st.number_input('Enter No of Internships', min_value=0, value=0)
    projects = st.number_input('Enter total Projects', min_value=0, value=0)
    workshops_certifications = st.number_input('Enter total Certifications', min_value=0, value=0)
    aptitude_test_score = st.number_input('Enter Aptitude Test Score', min_value=0, max_value=100, value=50)
    soft_skills_rating = st.number_input('Enter Soft Skills Rating', min_value=0, max_value=10, value=5)
    extracurricular_activities = st.number_input('Enter Extracurricular Activities(1 if Yes , else 0)', min_value=0, value=0)
    placement_training = st.number_input('Enter Placement Training(1 if Yes , else 0)', min_value=0, value=0)
    ssc_marks = st.number_input('Enter SSC Marks', min_value=0, value=0)
    hsc_marks = st.number_input('Enter HSC Marks', min_value=0, value=0)

    # Empty space for centering the button
    st.empty()

    # Centered 'Predict Placement' button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        prediction_button = st.button('Predict My Placement Results')

    if prediction_button:
        # Create a DataFrame with user input for prediction
        user_data = pd.DataFrame({
            'CGPA': [cgpa],
            'Internships': [internships],
            'Projects': [projects],
            'Workshops/Certifications': [workshops_certifications],
            'AptitudeTestScore': [aptitude_test_score],
            'SoftSkillsRating': [soft_skills_rating],
            'ExtracurricularActivities': [extracurricular_activities],
            'PlacementTraining': [placement_training],
            'SSC_Marks': [ssc_marks],
            'HSC_Marks': [hsc_marks]
        })
        placement= joblib.load('placement.joblib')
        company= joblib.load('company.joblib')
        # with col2:
        st.subheader('Student Placement Performance Result')
        # from sklearn.ensemble import DecisionTreeClassifier


        new_dict = {1: 'Nutanix', 2: 'Fivetran', 3: 'Amazon', 4: 'VMware', 5: 'Cisco', 6: 'Josh', 7: 'Darwinbox', 8: 'Amadeus', 9: 'Kickdrum', 10: 'Juspay', 11: 'Oracle', 12: 'Accolite', 13: 'Principal Global', 14: 'Aveva', 15: 'C&R Software', 16: 'Persistent', 17: 'Intellipaat', 18: 'Schneider', 19: 'Sahaj', 20: 'Eaton', 21: 'HCL', 22: 'TCS', 23: 'Accenture', 24: 'IBM', 25: 'Infosys', 26: 'Capgemini', 27: 'Cognizant', 28: 'Hyperscale', 29: 'Hexaware', 30: 'Wipro', 31: 'Tech Mahindra', 32: 'Birlasoft'}
        comparray = [9, 17,12,5,10,3,20,18,30,27,6,1,15,19, 4,2,23,32,22,7,24,16,14,11,8,31,28,26,13,25, 29,21,0]
        scorearray = [87, 84, 88, 86, 93, 90, 91, 92, 81, 75, 72, 82, 73, 89, 74, 95, 85, 79, 78, 77, 94, 83, 80, 76, 71, 70, 67, 66, 69, 68, 64, 65]
        def calculate_score(row):
            val = (row['CGPA'] / 10) + (row['AptitudeTestScore'] / 100) + (row['SoftSkillsRating'] / 5) + ((row['SSC_Marks'] + row['HSC_Marks']) / 200)
            val /= 4
            val *= 100
            val += row['Internships'] + row['Projects']
            return int(val)


        def companyprediction(newdata1):
            
            
            ypred = company.predict(newdata1)
            comp_array = comparray
            # comp_array = list(dataframe.company_offer.unique())
            comp_array.append(ypred)
            comp_array.sort()
            ind = comp_array.index(ypred)
            sc = calculate_score(newdata1)
            n = int(sc/10)
            for i in range(n):
                st.write((new_dict[int(comp_array[ind-i])]).upper())
        
        def recommendation(inpt):
            score_array = scorearray
            score_array.sort()
            sc = int(calculate_score(inpt))
            # st.write(sc)
            skillarray=[]
            string = ''
            for i in score_array:
                if i>=sc:
                    sc = i
                    break
            for i, r in filtered_dataset.iterrows():
                if r['Score'] == sc:
                    string = r['skills']
                    break
            recomm = string.split(',')
            temp=[]
            for i in recomm:
                if i not in temp:
                    temp.append(i)
                    st.write(i.upper(), end="  ")

        def prediction_Recommendation(df):
            # p =  prediction(df)
            sc = calculate_score(df)

            if sc>=65:
                st.write('The estimated score of  your skill set out of 100 is: ', sc)
                st.write('Your result of the Placement Prediction is: Yes')
                st.write('The predicted companies based on your skill set is:')
                companyprediction(df)
                st.write('To further improve your Placement preparation we Recommend you the following skills: ')
                recommendation(df)
            else:
                st.write('The estimated score of  your skill set out of 100 is: ', sc)
                st.write('Unfortunately Your result of the Placement Prediction is: No')
                st.write('To improve your Placement preparation we Recommend you the following skills')
                recommendation(df)
        
        # st.write(placement.predict(user_data), value='Placement Prediction')
        # st.write(company.predict(user_data))
        prediction_Recommendation(user_data)

if __name__ == '__main__':
    main()
