from ModelLayer.sideEffectsLevelExtractor import sideEffectsLevelExtractor
from ModelLayer.experienceExtractor import experienceExtractor
from ModelLayer.symptomConditionExtractor import symptomConditionExtractor
from ModelLayer.supplementaryDrugExtractor import supplementaryDrugExtractor
import logging 

logger = logging.getLogger(__name__)

def insertArgumentSetsIntoDB(post, sideEffectsLevelExtractorObj, experienceExtractorObj, symptomConditionExtractorObj, supplementaryDrugExtractorObj, dbObj):

    review = post.getReview()

    # Insert all argument sets into the DB
    if sideEffectsLevelExtractorObj.sentence:  sideEffectsLevelExtractorObj.insertIntoDB(review, dbObj)
    if experienceExtractorObj.sentence: experienceExtractorObj.insertIntoDB(review, dbObj)
    if symptomConditionExtractorObj.sentence: symptomConditionExtractorObj.insertIntoDB(review, dbObj)
    if supplementaryDrugExtractorObj.sentence: supplementaryDrugExtractorObj.insertIntoDB(review, dbObj)


