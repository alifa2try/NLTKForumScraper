CREATE TABLE SupplementaryDrugs
(
Post text, 
Sentence text,
MainTreatment varchar(255),
SuppDrug varchar(255),
Symptom varchar(255),
Reason varchar(255),
Classified varchar(255)
);

Create Table SideEffectsPresent
(
Post text,
Sentence text,
SideEffectsStatus varchar(255),
Drug varchar(255),
Classified varchar(255)
);

CREATE TABLE SymptomCondition
(
Post text,
Sentence text,
SymptomCriticality varchar(255),
Symptom varchar(255),
Drug varchar(255),
Classified varchar(255)
);

CREATE TABLE Experiences
(
Post text,
Sentence text,
Experience varchar(255),
Drug varchar(255),
Classified varchar(255)
);

LOAD DATA LOCAL INFILE 'C://Users//Robie//Desktop//ExperiencesTagged.csv' 
INTO TABLE experiences 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT *
FROM experiences 
WHERE Drug = 'tamoxifen'
and Classified LIKE 'T%'


DELETE FROM experiences
WHERE experiences.Post = ''

DELETE FROM experiences;
DELETE FROM sideeffectspresent;
DELETE FROM symptomcondition;

#=====================================================================================================================
#==============================================Aggregated Per Rule====================================================
SELECT symptomcondition.Post,
SUM(CASE WHEN symptomcondition.SymptomCriticality LIKE '%are ok%' AND symptomcondition.Classified LIKE 'T%' then 1 else 0 end) AS SymtomsNotOK,
SUM(CASE WHEN symptomcondition.SymptomCriticality LIKE '%are bad%' OR '%are possibly bad%' AND symptomcondition.Classified LIKE 'T%' then 1 else 0 end) AS SymtomsOK
FROM symptomcondition
GROUP BY symptomcondition.Post

SELECT sideeffectspresent.Post,
SUM(CASE WHEN sideeffectspresent.SideEffectsStatus LIKE '%No Side Effects%' OR '%Possibly no side effects%' AND sideeffectspresent.Classified LIKE 'T%' then 1 else 0 end) AS NoSideEffectsPresent,
SUM(CASE WHEN sideeffectspresent.SideEffectsStatus LIKE '%Side effects present%' AND sideeffectspresent.Classified LIKE 'T%' then 1 else 0 end) AS SideEffectsPresent
FROM sideeffectspresent
GROUP BY sideeffectspresent.Post

SELECT experiences.Post,
SUM(CASE WHEN experiences.Experience LIKE 'Positive%' AND experiences.Classified LIKE 'T%' then 1 else 0 end) AS PosExp,
SUM(CASE WHEN experiences.Experience LIKE 'Negative%' AND experiences.Classified LIKE 'T%' then 1 else 0 end) AS NegExp
FROM experiences
GROUP BY experiences.Post

#=====================================================================================================================
#==============================================Create Views===========================================================
DROP VIEW SymptomConditionAggr;
DROP VIEW ExperiencesAggr;
DROP VIEW SideEffectPresentAggr;

CREATE VIEW SymptomConditionAggr AS
SELECT symptomcondition.Post,
SUM(CASE WHEN symptomcondition.SymptomCriticality LIKE '%are ok%' AND symptomcondition.Classified LIKE 'T%' then 1 else 0 end) AS SymtomsOK,
SUM(CASE WHEN (symptomcondition.SymptomCriticality LIKE '%are bad%' OR '%are possibly bad%') AND (symptomcondition.Classified LIKE 'T%') then 1 else 0 end) AS SymtomsNotOK
FROM symptomcondition
GROUP BY symptomcondition.Post;

CREATE VIEW SideEffectPresentAggr AS
SELECT sideeffectspresent.Post,
SUM(CASE WHEN (sideeffectspresent.SideEffectsStatus LIKE '%No Side Effects%' OR '%Possibly no side effects%') AND (sideeffectspresent.Classified LIKE 'T%') then 1 else 0 end) AS NoSideEffectsPresent,
SUM(CASE WHEN sideeffectspresent.SideEffectsStatus LIKE '%Side effects present%' AND sideeffectspresent.Classified LIKE 'T%' then 1 else 0 end) AS SideEffectsPresent
FROM sideeffectspresent
GROUP BY sideeffectspresent.Post;

CREATE VIEW ExperiencesAggr AS
SELECT experiences.Post,
SUM(CASE WHEN experiences.Experience LIKE 'Positive%' AND experiences.Classified LIKE 'T%' then 1 else 0 end) AS PosExp,
SUM(CASE WHEN experiences.Experience LIKE 'Negative%' AND experiences.Classified LIKE 'T%' then 1 else 0 end) AS NegExp
FROM experiences
GROUP BY experiences.Post;


#=====================================================================================================================
#==============================================Query the Views========================================================

SELECT forumposts.post, 
	IFNULL(experiencesaggr.PosExp, 0) AS PosExp, 
    IFNULL(experiencesaggr.NegExp, 0) AS NegExp, 
    IFNULL(symptomconditionaggr.SymtomsOK, 0) AS SymtomsOK, 
    IFNULL(symptomconditionaggr.SymtomsNotOK, 0) AS SymtomsNotOK,
    IFNULL(sideeffectpresentaggr.NoSideEffectsPresent, 0) AS NoSideEffectsPresent,
    IFNULL(sideeffectpresentaggr.SideEffectsPresent, 0) AS SideEffectsPresent,
    forumposts.Rating, 
    forumposts.url, 
    forumposts.drug

FROM forumposts
LEFT JOIN experiencesaggr
ON experiencesaggr.post = forumposts.post
LEFT JOIN symptomconditionaggr
ON symptomconditionaggr.post = forumposts.post
LEFT JOIN sideeffectpresentaggr
ON sideeffectpresentaggr.post = forumposts.post

 

 
#=====================================================================================================================
#========================================LOAF TAGGED DATA==============================================================

LOAD DATA LOCAL INFILE 'C://Users//Robie//Desktop//ExperiencesTagged.csv' 
INTO TABLE experiences 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C://Users//Robie//Desktop//SideEffectStatusTagged.csv' 
INTO TABLE sideeffectspresent 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C://Users//Robie//Desktop//SymptomSeverityTagged.csv' 
INTO TABLE symptomcondition 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

#=====================================================================================================================
#=====================================================================================================================


Create TABLE ForumPosts
(
ForumName text,
URL varchar(255),
Symptoms varchar(255),
Post text,
Drug varchar(255),
Rating varchar(255)
);


LOAD DATA LOCAL INFILE 'C://Users//Robie//Desktop//ExperiencesTagged.csv' 
INTO TABLE experiences 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT *
FROM forumposts
FULL OUTER JOIN sideeffectspresent ON sideeffectspresent.post = forumposts.post

SELECT *
FROM symptomcondition
WHERE Post LIKE '%"I was suffering from the common cold and had symptoms of dry cough, congested sinus, large headache, s%'


SELECT symptomcondition.Post,
SUM(CASE WHEN symptomcondition.SymptomCriticality LIKE '%are ok%' AND symptomcondition.Classified LIKE 'T%' then 1 else 0 end) AS SymtomsOK,
SUM(CASE WHEN (symptomcondition.SymptomCriticality LIKE '%are bad%' OR '%are possibly bad%') AND (symptomcondition.Classified LIKE 'T%') then 1 else 0 end) AS SymtomsNotOK
FROM symptomcondition
WHERE Post LIKE '%"I was suffering from the common cold and had symptoms of dry cough, congested sinus, large headache, s%'
GROUP BY symptomcondition.Post;