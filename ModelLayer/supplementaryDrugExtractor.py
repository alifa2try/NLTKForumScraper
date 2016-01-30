import logging 

logger = logging.getLogger(__name__)

class supplementaryDrugExtractor(object):

    def __init__(self):
        self.sentence = ''
        self.drug = ''
        self.suppDrug = ''
        self.reason = ''
        self.symptom = ''

    def findSupplementaryDrug(self, sentence, mainDrug, drugsFound, symptomsFound, dbobj):

        if len(drugsFound) == 0:
            return
    

        suppFound = False

        for drug in drugsFound:
            if drug != mainDrug:
                suppDrug = drug
                suppFound = True
    
        if(suppFound is False):
            return
       
        if len(symptomsFound) == 0:
            suppDrugReason = 'No symptom found for taking supplementary drug'
            symptom = ''
        else:
            suppDrugReason = 'Drug being taken for a symptom'
            symptom = symptomsFound[0]
        
        self.sentence = sentence
        self.drug = mainDrug
        self.suppDrug = suppDrug
        self.reason = suppDrugReason
        self.symptom = symptom

        #insertIntoDB(sentence, mainDrug, suppDrug, symptom, suppDrugReason, dbobj)



    def insertIntoDB(sentence, drug, suppDrug, symptom, suppDrugReason, dbobj):

        sqlSentence = (sentence.replace("'","\\'"))

        insertSql = "INSERT INTO SupplementaryDrugs (Sentence, MainTreatment, SuppDrug, Symptom, Reason) VALUES (%s, %s, %s, %s, %s);" % ("'"+ sqlSentence + "'", "'"+ drug + "'", "'"+ suppDrug + "'", "'" + symptom + "'", "'" + suppDrugReason + "'")

        dbobj.insert(insertSql)

    def insertIntoDB(self, post, dbobj):

        sqlSentence = (self.sentence.replace("'","\\'"))

        insertSql = "INSERT INTO SupplementaryDrugs (Post, Sentence, MainTreatment, SuppDrug, Symptom, Reason) VALUES (%s, %s, %s, %s, %s, %s);" 
        data = (post, sqlSentence, self.drug, self.suppDrug, self.symptom, self.reason)
        dbobj.insert(insertSql, data)
