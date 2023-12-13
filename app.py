import streamlit as st
import pandas as pd
import joblib

def main():

    st.title('Student Placement Prediction and Recommendation System')
    content = 'Welcome! This project helps the students in pre-final and final years of their B. Tech course to know their individual placement status that they are most likely to achieve. With this information, students can put in more hard work to enhance their chances of getting placed in companies that belong to higher hierarchies.Enter the details below and click Predict My Placement Result to see the recommendation.'
    style= f"<span style='font-size: 20px;'>{content}</span>"
    st.write(style, unsafe_allow_html=True)
    mid = f"<span style='font-size: 40px;'><b>Fillout the Below SkillSet<b></span>"
    centered_word = f"<div style='text-align: center;'><h4>{mid}</h4></div>"
    st.markdown(centered_word, unsafe_allow_html=True)
    # st.write(mid, unsafe_allow_html=True)


    dataframe = pd.read_csv('colab_dataframe.csv')
    filtered_dataset = dataframe[0:4500]
    cgpa = st.number_input('Enter Your CGPA', min_value=0.0, max_value=10.0, step=0.1)
    internships = st.number_input('Enter No of Internships You have Done', min_value=0, max_value=10)
    projects = st.number_input('Enter Your total Projects', min_value=0, max_value=10)
    workshops_certifications = st.number_input('Enter total Certifications', min_value=0)
    aptitude_test_score = st.number_input('Enter Your Aptitude Test Score(out 0f 100)', min_value=0, max_value=100)
    soft_skills_rating = st.number_input('Enter Soft Skills Rating(out of 5)',  min_value=0.0, step=0.1, max_value=5.0)
    extracurricular_activities = st.number_input('Enter Extracurricular Activities(1 if Yes , else 0)', min_value=0,max_value=1)
    placement_training = st.number_input('Enter Placement Training(1 if Yes , else 0)', min_value=0,max_value=1)
    ssc_marks = st.number_input('Enter SSC Marks(out 0f 100)', min_value=0, max_value=100)
    hsc_marks = st.number_input('Enter HSC Marks(out 0f 100)', min_value=0, max_value=100)

  
    st.empty()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        prediction_button = st.button('Predict My Placement Results')

    if prediction_button:
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
        headersub = 'Student Placement Performance Result'
        header = f"<span style='font-size: 35px;'>{headersub}</span>"
        centered_word = f"<div style='text-align: center;'><h4>{header}</h4></div>"
        st.markdown(centered_word, unsafe_allow_html=True)
    
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
            comp_array.append(ypred)
            comp_array.sort()
            ind = comp_array.index(ypred)
            sc = calculate_score(newdata1)
            n = int(sc/10)
            for i in range(1,n):
                result = new_dict[int(comp_array[ind+i])].upper()
                centered_word = f"<div style='text-align: center;'><h4>{result}</h4></div>"
                st.markdown(centered_word, unsafe_allow_html=True)   

        
        def recommendation(inpt):
            score_array = scorearray
            score_array.sort()
            sc = int(calculate_score(inpt))
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
                    r = i.upper()
                    centered_word = f"<div style='text-align: center;'><h4>{r}</h4></div>"
                    st.markdown(centered_word, unsafe_allow_html=True)   
            
            if recomm[0] == '':
                arr = ['Salesforce', 'Amazon Web Services', 'Deep Learing', 'C#', '.NET', 'Devops']
                sen = f"<span style='font-size: 25px;'>Your SkillSet is Exceptionally Good. We Recommend you the following Extra set of skills to further Enhance your Preparation</span>"
                st.write(sen, unsafe_allow_html=True)
                for k in arr:
                    centered_word = f"<div style='text-align: center;'><h4>{k}</h4></div>"
                    st.markdown(centered_word, unsafe_allow_html=True)   

        def prediction_Recommendation(df):
            sc = calculate_score(df)
            s = 'Your result of the Placement Prediction is: No'
            s1 = 'The estimated score of  your skill set out of 100 is: '
            s2='Your result of the Placement Prediction is: Yes'
            s3 = 'The predicted companies based on your skill set is: '
            s4='To further improve your Placement preparation we Recommend you the following skills: '
            styled_sentence1 = f"<span style='font-size: 25px;'>{s1}</span>"
            styled_sentence = f"<span style='font-size: 25px;'>{s}</span>"
            styled_sentence2 = f"<span style='font-size: 25px;'>{s2}</span>"
            styled_sentence3 = f"<span style='font-size: 25px;'>{s3}</span>"
            styled_sentence4 = f"<span style='font-size: 25px;'>{s4}</span>"
            styled_sentence5 = f"<span style='font-size: 25px;'>{sc}</span>"


            if sc>=65:
               
                st.write(styled_sentence1, styled_sentence5,unsafe_allow_html=True)
                st.write(styled_sentence2, unsafe_allow_html=True)
                st.write(styled_sentence3, unsafe_allow_html=True)
                companyprediction(df)
                st.write(styled_sentence4, unsafe_allow_html=True)
                recommendation(df)

            else:
                st.write(styled_sentence, unsafe_allow_html=True)
                st.write(styled_sentence1,styled_sentence5, unsafe_allow_html=True)
                st.write(styled_sentence4, unsafe_allow_html=True)
                recommendation(df)

        prediction_Recommendation(user_data)


main()
