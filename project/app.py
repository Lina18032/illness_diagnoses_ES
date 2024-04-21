from flask import Flask, render_template, request, jsonify
from aima.utils import expr
from aima.logic import FolKB, fol_fc_ask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

kb = FolKB()


kb.tell(expr('Fever(x) & Cough(x) ==> CommonCold(x)'))
kb.tell(expr('Fever(x) & Cough(x) & Headache(x) ==> Flu(x)'))
kb.tell(expr('SoreThroat(x) & Fever(x) ==> StrepThroat(x)'))
kb.tell(expr('RunnyNose(x) ==> Allergies(x)'))
kb.tell(expr('Fever(x) & Cough(x) & Fatigue(x) & MuscleAches(x) ==> COVID19(x)'))
kb.tell(expr('Fever(x) & Cough(x) & ShortnessOfBreath(x) ==> Pneumonia(x)'))
kb.tell(expr('cough(x) & ChestPain(x) & ShortnessOfBreath(x) ==> Asthma(x)'))
kb.tell(expr('Fever(x) & Cough(x) & Wheezing(x) ==> Bronchitis(x) '))
kb.tell(expr('Fever(x) & Nausea(x) & Diarrhea(x) ==> Gastroenteritis(x)'))
kb.tell(expr('Fever(x) & RunnyNose(x) ==> Sinusitis(x)'))
kb.tell(expr('Headache(x) & Nausea(x) ==> Migraine(x)'))
kb.tell(expr('Fever(x) & JointPain(x) & SkinRash(x) ==> LymeDisease(x)'))
kb.tell(expr('Fever(x) & Headache(x) & SwollenLymphNodes(x) ==> Mononucleosis(x)'))
kb.tell(expr('Fatigue(x) & Headache(x) & Hypertension(x) ==> Hypertension(x)'))
kb.tell(expr('AbdominalPain(x) & Nausea(x) ==> GERD(x)'))
kb.tell(expr('Fever(x) & PainDuringUrination(x) ==> UTI(x)'))
kb.tell(expr('EarPain(x) & Fever(x) ==> OtisMedia(x)'))


def calculate_certainty(symptoms, total_symptoms):
    base_certainty = len(symptoms) / total_symptoms
    adjustment_factor = 1 - (len(symptoms) / (len(symptoms) + 10))
    certainty = base_certainty * adjustment_factor

    return certainty

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    selected_symptoms = request.json.get('symptoms', [])
    print(selected_symptoms)
    total_symptoms = len(selected_symptoms)
    patient = expr('John')
    agenda = [expr(symptom + '(John)') for symptom in selected_symptoms]
    memory = {}
    seen = set()
    while agenda:
        p = agenda.pop(0)
        if p in seen:
            continue
        seen.add(p)
        if fol_fc_ask(kb, p):
            memory[p] = True
        else:
            memory[p] = False
        if memory.get(expr('Fever(John)'), False) and memory.get(expr('Cough(John)'), False):
            agenda.append(expr('CommonCold(John)'))
        if memory.get(expr('Fever(John)'), False) and memory.get(expr('Cough(John)'), False) and memory.get(expr('Headache(John)'), False):
            agenda.append(expr('Flu(John)'))
        if memory.get(expr('SoreThroat(John)'), False) and memory.get(expr('Fever(John)'), False) and memory.get(expr('StrepThroat(John)'), False):
            agenda.append(expr('Cold(John)'))
        if memory.get(expr('RunnyNose(John)'), False):
            agenda.append(expr('Allergies(John)'))
        if memory.get(expr('Fever(John)'), False) and memory.get(expr('Cough(John)'), False) and memory.get(expr('Fatigue(John)'), False) and memory.get(expr('MuscleAches(John)'), False):
            agenda.append(expr('COVID19(John)'))
        if memory.get(expr('Fever(John)'), False) and memory.get(expr('Cough(John)'), False) and memory.get(expr('ShortnessOfBreath(John)'), False):
            agenda.append(expr('Pneumonia(John)'))
        if memory.get(expr('Cough(John)'), False) and memory.get(expr('ChestPain(John)'), False) and memory.get(expr('ShortnessOfBreath(John)'), False):
            agenda.append(expr('Asthma(John)'))
        if memory.get(expr('Fever(John)'), False) and memory.get(expr('Cough(John)'), False) and memory.get(expr('Wheezing(John)'), False):
            agenda.append(expr('Branchitis(John)'))
        if memory.get(expr('Nausea(John)'), False) and memory.get(expr('Diarrhea(John)'), False):
            agenda.append(expr('Gastroenteritis(John)'))
        if memory.get(expr('Fever(John)'), False) and memory.get(expr('RunnyNose(John)'), False):
            agenda.append(expr('Sinusitis(John)'))
        if memory.get(expr('Headache(John)'),False) and memory.get(expr('Nausea(John)'), False):
            agenda.append(expr('Migraine(John)'))
        if memory.get(expr('Fever(John)'),False) and memory.get(expr('JointPain(John)'), False)and memory.get(expr('SkinRash(John)'), False):
            agenda.append(expr('LymeDisease(John)'))
        if memory.get(expr('Fver(John)'),False) and memory.get(expr('Headache(John)'), False)and memory.get(expr('SwollenLymphNodes(John)'), False):
            agenda.append(expr('Mononucleosis(John)'))
        if memory.get(expr('Fatigue(John)'),False) and memory.get(expr('Headache(John)'), False)and memory.get(expr('Hypertension(John)'), False):
            agenda.append(expr('Hypertension(John)'))
        if memory.get(expr('AbdominalPain(John)'),False) and memory.get(expr('Nausea(John)'), False):
            agenda.append(expr('GERD(John)'))
        if memory.get(expr('Fever(John)'),False) and memory.get(expr('PainDuringUrination(John)'), False):
            agenda.append(expr('UTI(John)'))
        if memory.get(expr('EarPain(John)'),False) and memory.get(expr('Fever(John)'), False):
            agenda.append(expr('OtisMedia(John)'))
    
    result = []
    for p, value in memory.items():
        if value and str(p).startswith(('Flu', 'Cold','CommonCold' ,'Allergies','COVID19','Pneumonia','Asthma','Branchitis','Gastroenteritis','Sinusitis')):
            disease = str(p).split('(')[0]
            certainty = calculate_certainty([disease], total_symptoms)
            #result.append({'message': f' Based on your symtoms ,you most likely have {round(certainty * 100)}% chance of:', 'diseases': [disease]})
            result.append({'disease': disease, 'certainty': round(certainty, 2)})
            print(result)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
