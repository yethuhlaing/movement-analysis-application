def checkFirstTime():
    dataframe = getDataframe()
    if len(dataframe["reference_df"]) == 0 :
        return True
    return False

def setUserData(userData):
    USER_DATA = userData

def setDataframe(dataframe):
    DATAFRAME = dataframe

def setEachUserData(primaryType, secondaryType, isArray, value):
    if isArray:
        USER_DATA[primaryType][secondaryType].append(value)
    else:
        USER_DATA[primaryType][secondaryType] = value

def setEachDataframe(primaryType, value):
    DATAFRAME[primaryType] = value


def getDataframe():
    return DATAFRAME

def getUserData():
    return USER_DATA


def getHeadingData():
    return USER_DATA["headingData"]

def getInformationData():
    return USER_DATA["informationData"]

def getVisualizationData():
    return USER_DATA["visualizationData"]

def getSummaryData():
    return USER_DATA["summaryData"]





def setSummaryData(category, value):
    USER_DATA["summaryData"][category].append(value)

def getSummaryData(category):
    return USER_DATA["summaryData"][category]

def getReference_df():
    return DATAFRAME["reference_df"]

def getStudent_df():
    return DATAFRAME["student_df"]

def getStatus_df():
    return DATAFRAME["status_df"]

def setReference_df(value):
    DATAFRAME["reference_df"].append(value)

def setStudent_df(value):
    DATAFRAME["student_df"].append(value)

def setStatus_df(value):
    DATAFRAME["status_df"].append(value)
    
USER_DATA = { 
    "headingData" : {
        "project_name": "Running",
        "project_creator": "Ye Thu"
    },
    "informationData": {
        "height": 14,
        "weight" : 23,
        "student_name": "Meteo"
    } ,
    "visualizationData": {
        "categories": ["Joint Angles XZY"],
        "movements": ["L5S1 Lateral Bending", "L5S1 Axial Bending" ], 
        "scenario": "200Metres",
        "duration": 50,
        "starting_time": 20,
        "Graph_type": "Single Graph" , 
        # Graph type options =>["Single Graph", "Double Graph"],
        "ref_name": "JohnSon",
        "ref_file": "C:/Users/yethu/Desktop/Movement Analysis Project/data/Reference downsampled data/Simulator riding/Reference Harjusimu-003 Extended walk.xlsx",
        "student_name": "Toni",
        "student_file": "C:/Users/yethu/Desktop/Movement Analysis Project/data/Student downsampled data/simulator riding/Sudent1-003Harju ext walk.xlsx"
    },
    "summaryData": {
        "category" : [],
        "movement" : [],
        "minimum_time" : [],
        "maximum_time": [] ,
        "minimum_duration": [] ,
        "optimal_duration": [],
        "maximum_duration":[],
    }
}

DATAFRAME = {
    ## Dictionary in array
    "reference_df": [],
    "student_df": [],
    "status_df": []
}

