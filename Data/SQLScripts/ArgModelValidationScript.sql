SELECT forumposts.Post, experiences.Experience, experienceS.Sentence, symptomcondition.SymptomCriticality, symptomCondition.Sentence, sideeffectspresent.SideEffectsStatus, sideeffectspresent.Sentence, forumposts.Rating
FROM forumposts
	INNER JOIN experiences ON experiences.Post = forumposts.Post
	INNER JOIN symptomcondition ON symptomcondition.Post = experiences.Post
    INNER JOIN sideeffectspresent ON sideeffectspresent.Post = symptomcondition.Post
    
    
SELECT forumposts.Post,
 (SELECT COUNT(*) FROM forumposts INNER JOIN experiences ON experiences.Post = forumposts.Post WHERE ) AS EXPERIENCES 
FROM forumposts


SELECT forumposts.Post
from forumposts
	INNER JOIN experiences ON experiences.Post = forumposts.Post
	INNER JOIN symptomcondition ON symptomcondition.Post = experiences.Post
    INNER JOIN sideeffectspresent ON sideeffectspresent.Post = symptomcondition.Post
    
    
SELECT * FROM forumposts INNER JOIN experiences ON experiences.Post = forumposts.Post WHERE 

SELECT *
FROM supplementarydrugs



SELECT * 
FROM forumposts