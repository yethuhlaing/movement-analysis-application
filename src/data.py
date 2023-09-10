def checkFirstTimeDF():
    dataframe = getDataframe()
    if len(dataframe["reference_df"]) == 0 :
        return True
    return False

def checkFirstTimeHD():
    if USER_DATA["informationData"]["student_name"] == "" :
        print("TUre")
        return True
    return False

def checkFirstTimeID():
    if USER_DATA["headingData"]["project_name"] == "" :
        print("HeadingData", True)
        return True
    return False

def setHeadingData(project_name, project_creator,):
    global USER_DATA
    USER_DATA["headingData"]["project_name"] = project_name
    USER_DATA["headingData"]["project_creator"] = project_creator

def setInformationData( height, weight, student_name):
    global USER_DATA
    USER_DATA["headingData"]["height"] = height
    USER_DATA["headingData"]["weight"] = weight
    USER_DATA["headingData"]["student_name"] = student_name

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
    global USER_DATA
    return USER_DATA["headingData"]

def getInformationData():
    global USER_DATA
    return USER_DATA["informationData"]

def getVisualizationData():
    global USER_DATA
    return USER_DATA["visualizationData"]

def getSummaryData():
    global USER_DATA
    return USER_DATA["summaryData"]


def setLoadingContents(content):
    global LOADING_CONTENTS
    LOADING_CONTENTS.append(content)

def getLoadingContents():
    global LOADING_CONTENTS
    return LOADING_CONTENTS


def setSummaryData(category, value):
    global USER_DATA
    USER_DATA["summaryData"][category].append(value)

def getSummaryData(category):
    global USER_DATA
    return USER_DATA["summaryData"][category]

def getReference_df(): 
    global DATAFRAME
    return DATAFRAME["reference_df"]

def getStudent_df():
    global DATAFRAME
    return DATAFRAME["student_df"]

def getStatus_df():
    global DATAFRAME
    return DATAFRAME["status_df"]

def setReference_df(value):
    global DATAFRAME
    DATAFRAME["reference_df"] = value

def setStudent_df(value):
    global DATAFRAME
    DATAFRAME["student_df"] = value

def setStatus_df(value):
    global DATAFRAME
    DATAFRAME["status_df"] = value


    
def setOneReference_df(value):
    global DATAFRAME
    DATAFRAME["reference_df"].append(value)  

def setOneStudent_df(value):
    global DATAFRAME
    DATAFRAME["student_df"].append(value)

def setOneStatus_df(value):
    global DATAFRAME
    DATAFRAME["status_df"].append(value)




def resetReference_df():
    global DATAFRAME
    DATAFRAME["reference_df"] = []

def resetStudent_df():
    global DATAFRAME
    DATAFRAME["student_df"] = []

def resetStatus_df():
    global DATAFRAME
    DATAFRAME["status_df"] = []

USER_DATA = {}
    # "headingData" : {
    #     "project_name": "",
    #     "project_creator": ""
    #     # "project_name": "Running",
    #     # "project_creator": "Ye Thu"
    # },
    # "informationData": {
    #     "height": 0,
    #     "weight" : 0,
    #     "student_name": ""
    #     # "height": 14,
    #     # "weight" : 23,
    #     # "student_name": "Meteo"
    # } ,
    # "visualizationData": {
    #     "categories": {} ,         
    #     "scenario": "",
    #     "duration": 0,
    #     "starting_time": 0,
    #     "Graph_type": "" , 

    #     "ref_name": "",
    #     "ref_file": "",
    #     "student_name": "",
    #     "student_file": ""

    #     # "categories": {
    #     #     # 'Segment Velocity': ['Pelvis x', 'Pelvis y', 'L5 y', 'L3 x', 'L3 y', 'L3 z', 'T12 x'], 
    #     #     # 'Joint Angles XZY': ['L5S1 Axial Bending', 'L4L3 Lateral Bending', 'L4L3 Axial Rotation',  'L4L3 Flexion/Extension', 'L1T12 Lateral Bending', 'L1T12 Axial Rotation', 'L1T12 Flexion/Extension', 'T9T8 Lateral Bending'], 
    #     #     'Sensor Orientation - Quat': ['Pelvis q1', 'Pelvis q3', 'L5 q0', 'L5 q1', 'L5 q2', 'L5 q3', 'L3 q0']
    #     # } ,         
    #     # "scenario": "200Metres",
    #     # "duration": 50,
    #     # "starting_time": 20,
    #     # "Graph_type": "Single Graph" , 
    #     # # Graph type options =>["Single Graph", "Double Graph"],
    #     # "ref_name": "JohnSon",
    #     # "ref_file": "C:/Users/yethu/Desktop/Movement Analysis Project/data/Reference downsampled data/Simulator riding/Reference Harjusimu-003 Extended walk.xlsx",
    #     # "student_name": "Toni",
    #     # "student_file": "C:/Users/y
    # },
    # "summaryData": {
    #     "category" : [],
    #     "movement" : [],
    #     "minimum_time" : [],
    #     "maximum_time": [] ,
    #     "minimum_duration": [] ,
    #     "optimal_duration": [],
    #     "maximum_duration":[],
    # }


DATAFRAME = {
    ## Dictionary in array
    "reference_df": [],
    "student_df": [],
    "status_df": []
}

LOADING_CONTENTS = []

# "categories": ["Joint Angles XZY"],
# "movements": ["L5S1 Lateral Bending", "L5S1 Axial Bending" ],
    