
import openai
import numpy as np
import re
from flask import Flask, render_template, request
import os
import speech_recognition as sr
from os import path
from pydub import AudioSegment

app = Flask(__name__)
app= Flask(__name__,template_folder='templates')
# Configure OpenAI API
openai.api_type = "azure"
#openai.api_base = "https://parsingdata.openai.azure.com/"
#openai.api_version = "2023-05-15"
#openai.api_key = "6d169e06f2644552aa93778092edadb1"

openai.api_base = "https://panther-jd-resume-parsing.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = "4fa70bb215a346bda1bb7bd3ef45fc29"


class PatientAnalysis:
    @staticmethod
    def patient_notes_analysis(patient_note):
        try:

            patient_note_input = {"patient_note": patient_note}
            patient_notes_analysis_ICD10 = [
               {"role": "system", "content": "You are a medical coder. User will provide patients notes, give response as an ICD10 and CPT billable code and health clinical assessment with chief complaint and history of present US based on the provided patient note."}
            
            ]
            patient_notes_analysis_ICD10.append({"role": "user", "content": str(patient_note_input)})

            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",
                messages=patient_notes_analysis_ICD10,
                temperature=0,
                max_tokens=500,
            )
            
            # patient_notes_analysis_ICD10.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

            patient_notes_analysis_ICD10 = response['choices'][0]['message']['content']        
                      
            print("\n LLM process: ", patient_notes_analysis_ICD10)
            # print("\n LLM process: ", response)
        
            pattern1 = r'(?<=ICD-10 code: ).*'
            pattern2 = r'(?<=CPT Code: ).*'  
            pattern3 = r'(?<=Chief Complaint:).*'               
            pattern4 = r'(?<=History of Present Illness:\n).*'           
            pattern5 = r'(?<=Health clinical assessment:\n).*'
            
            match1 = re.search(pattern1, patient_notes_analysis_ICD10, re.IGNORECASE)
            match2 = re.search(pattern2, patient_notes_analysis_ICD10, re.IGNORECASE)
            match3 = re.search(pattern3, patient_notes_analysis_ICD10, re.IGNORECASE)
            match4 = re.search(pattern4, patient_notes_analysis_ICD10, re.IGNORECASE)         
            match5 = re.search(pattern5, patient_notes_analysis_ICD10, re.IGNORECASE)   
            

            if match1:
                data_after_word1 = match1.group(0)
            else:
                data_after_word1 = patient_notes_analysis_ICD10

            if match2:
                data_after_word2 = match2.group(0)
            else:
                data_after_word2 = patient_notes_analysis_ICD10
                
            if match3:
                data_after_word3 = match3.group(0)
            else:
                data_after_word3 = patient_notes_analysis_ICD10
                
            if match4:
                data_after_word4 = match4.group(0)
            else:
                data_after_word4 = patient_notes_analysis_ICD10   
                
            if match5:
                data_after_word5 = match5.group(0)
            else:
                data_after_word5 = patient_notes_analysis_ICD10            
                

            return data_after_word1, data_after_word2, data_after_word3, data_after_word4, data_after_word5, patient_notes_analysis_ICD10

        except Exception as e:
            # print(e)
            return "except section", "failed", " "," ", " ",patient_notes_analysis_ICD10

@app.route("/", methods=["GET", "POST"])
def index1():
    if request.method == "POST":
        filename = request.form["patient_note"]
        AUDIO_FILE = filename                                     
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)               
        patient_note =  r.recognize_google(audio)
        output1, output2, output3, output4, output5,output6 = PatientAnalysis.patient_notes_analysis(patient_note)
        return render_template("index1.html", patient_note=patient_note, output1=output1, output2=output2, output3=output3, output4=output4, output5=output5, output6=output6)
    return render_template("index.html", patient_note="", output1="", output2="", output3="", output4="", output5="", output6="")


if __name__ == "__main__":
    app.run(debug=True)
