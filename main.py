from statistics import mean

import drawBoxPlot
import mapByLocation
import hi
import filterData
def chooseSpecificFeatures(featureName):
    if featureName=="location":
        #featureList=['membrane', 'cytoplasm','nucleus', 'lysosome', 'chromosome', 'mitochondrion','proteasome complex']
        featureList = ['nucleus', 'cytoplasm']
    if featureName=="function":
        featureList=['rRNA binding', 'rRNA binding', 'mRNA binding', 'translation initiation factor activity', 'DNA-binding transcription factor activity',
                     'translation factor activity, RNA binding', 'tRNA binding', 'nucleosomal DNA binding', 'growth factor activity',
                     'nuclease activity','nuclease activity', 'exonuclease activity', 'ribonuclease activity', 'tRNA binding'
                     ]

    if featureName=="pathway":
        featureList=["Meiosis", 'Gastric Cancer Network 1', 'Cell Cycle, Mitotic',
                   "Apoptosis",'DNA Damage Response', 'Chromatin Remodeling', 'DNA replication',
                     'Homologous recombination', 'DNA methylation', 'Activation of DNA fragmentation factor', 'Synthesis of DNA']
        #featureList=["disease","Parkinson disease","Huntington disease","Prostate cancer","Breast cancer","Melanoma","Small cell lung cancer",
         #             "Non-small cell lung cancer"]
    return featureList

def specificFeatures(featuresList,featureDict):
    specificFeaturesDict={}
    for protFeature in featureDict:
        if protFeature in featuresList:
            specificFeaturesDict[protFeature]= featureDict[protFeature]
    return specificFeaturesDict

def main():
    featureDict=mapByLocation.main()
    featuresList=chooseSpecificFeatures(featureName="function")
    specificFeaturesDict=specificFeatures(featuresList,featureDict)
    drawBoxPlot.draw(specificFeaturesDict,featuresList)

if __name__ == "__main__":
    main()