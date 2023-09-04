def checkFirstTime():
    dataframe = getDataframe()
    if len(dataframe["reference_df"]) == 0 :
        return True
    return False

def setUserData(userData):
    global USER_DATA
    USER_DATA = userData

def setDataframe(dataframe):
    global DATAFRAME
    DATAFRAME = dataframe

def setEachUserData(primaryType, secondaryType, isArray, value):
    global USER_DATA
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


def setLoadingContents(content):
    global LOADING_CONTENTS
    LOADING_CONTENTS.append(content)

def getLoadingContents():
    return LOADING_CONTENTS


def setSummaryData(category, value):
    global USER_DATA
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
    DATAFRAME["reference_df"] = value

def setStudent_df(value):
    DATAFRAME["student_df"] = value

def setStatus_df(value):
    DATAFRAME["status_df"] = value


    
def setOneReference_df(value):
    DATAFRAME["reference_df"].append(value)  

def setOneStudent_df(value):
    DATAFRAME["student_df"].append(value)

def setOneStatus_df(value):
    DATAFRAME["status_df"].append(value)




def resetReference_df():
    DATAFRAME["reference_df"] = []

def resetStudent_df():
    DATAFRAME["student_df"] = []

def resetStatus_df():
    DATAFRAME["status_df"] = []

USER_DATA = { 
    "headingData" : {
        # "project_name": "Running",
        # "project_creator": "Ye Thu"
    },
    "informationData": {
        # "height": 14,
        # "weight" : 23,
        # "student_name": "Meteo"
    } ,
    "visualizationData": {
        "categories": {
            # 'Segment Velocity': ['Pelvis x', 'Pelvis y', 'L5 y', 'L3 x', 'L3 y', 'L3 z', 'T12 x'], 
            'Joint Angles XZY': ['L5S1 Axial Bending', 'L4L3 Lateral Bending', 'L4L3 Axial Rotation',  'L4L3 Flexion/Extension', 'L1T12 Lateral Bending', 'L1T12 Axial Rotation', 'L1T12 Flexion/Extension', 'T9T8 Lateral Bending'], 
            'Sensor Orientation - Quat': ['Pelvis q1', 'Pelvis q3', 'L5 q0', 'L5 q1', 'L5 q2', 'L5 q3', 'L3 q0']
        } ,         
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

LOADING_CONTENTS = []

# "categories": ["Joint Angles XZY"],
# "movements": ["L5S1 Lateral Bending", "L5S1 Axial Bending" ],
    