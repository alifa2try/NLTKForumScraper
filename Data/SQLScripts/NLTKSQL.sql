DELETE FROM ForumPostFeatures
WHERE NounPhrase = 'full comment'

#----------------------#
#----------------------#
#--------DELETE STATEMENT---#

DELETE FROM ForumPosts;
DELETE FROM ForumPostFeatures;
DELETE FROM ConnectingVerbs;
DELETE FROM SideEffectsPresent;
DELETE FROM SymptomCondition;
DELETE FROM Experiences;
DELETE FROM SupplementaryDrugs

#----------------------#
#----------------------#
#--------SELECT STATEMENT---#


SELECT COUNT(*)
FROM ForumPosts

SELECT *
FROM ForumPosts

SELECT *
FROM SupplementaryDrugs

CREATE TABLE ForumPostFeatures
(
Post text,
Sentence text,
NounPhrase varchar(255)
);

CREATE TABLE SupplementaryDrugs
(
Post text, 
Sentence text,
MainTreatment varchar(255),
SuppDrug varchar(255),
Symptom varchar(255),
Reason varchar(255)
);

Create TABLE ConnectingVerbs
(
Sentence text,
ConnectingVerb varchar(255),
Symptoms varchar(255),
Drugs varchar(255),
DrugsFirst varchar(255)
);

Create Table SideEffectsPresent
(
Post text,
Sentence text,
SideEffectsStatus varchar(255),
Drug varchar(255)
);

CREATE TABLE SymptomCondition
(
Post text,
Sentence text,
SymptomCriticality varchar(255),
Symptom varchar(255),
Drug varchar(255)
);

CREATE TABLE Experiences
(
Post text,
Sentence text,
Experience varchar(255),
Drug varchar(255)
);

Create TABLE ForumPosts
(
ForumName text,
URL varchar(255),
Symptoms varchar(255),
Post text,
Drug varchar(255),
Rating varchar(255)
);

SELECT *
FROM ForumPosts

SELECT *
FROM Experiences
WHERE 

GROUP BY Sentence

SELECT *
FROM SymptomCondition
WHERE Sentence = "i have noticed that for extended use (2-5 days) the pain symptoms slowly come back, but at least this is something i can buy otc."

GROUP BY Sentence
WHERE drug = 'effexor'

SELECT *
FROM ConnectingVerbs

SELECT *
FROM SideEffectsPresent
WHERE DRUG = 'effexor'

SELECT NounPhrase
FROM ForumPostFeatures 

SELECT NounPhrase, COUNT(NounPhrase) AS Frequency
FROM ForumPostFeatures
GROUP BY NounPhrase
ORDER BY Frequency DESC

#---------------------------#
#---------------------------#
-- Drop all the tables here--
DROP TABLE ConnectingVerbs
DROP TABLE ForumPostFeatures
DROP TABLE ForumPosts
DROP TABLE SymptomCondition
DROP TABLE SupplementaryDrugs
DROP TABLE Experiences
DROP TABLE SideEffectsPresent


