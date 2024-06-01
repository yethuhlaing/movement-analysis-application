# Movement analyze visualization tool for ergonomic and sport purposes

## Tables of Content
- [Description](#description)
- [Objectives](#objectives)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [License](#license)
- [Feedback and Support](#feedback-and-support)
  

## Description
The AIRIDE project develops new learning methods and technologies based on riding simulators, student biosignal measurements and artificial intelligence, which can be used in training in the riding industry and in various research and educational institutions. In this project, Excel Software acts as a medium to analyze the simulation data. Due to the massive volume of the data, it is essentially time-consuming to extract and compare even the two columns of the excel file in which almost 720 columns exist. The efficient tool needs to be implemented to compare easily different simulation data in sport and work, pick up and visualize the critical key points and give fast feedback to an athlete or worker based on those threshold values. The solution to tackle this problem is to implement analysis algorithms with the scripting language – python and produce the visualization graphs via appropriate User Interface.
  
![image](https://github.com/yethuhlaing/movement-analysis-application/assets/112906488/f4aa1824-83bb-4e20-8466-00ab0ba8e581)

![image](https://github.com/yethuhlaing/movement-analysis-application/assets/112906488/44a91cd3-ea49-454f-a8d0-bbcf0b3ba3b4)

## Objectives 
- Find out the tool to compare easily different tasks in sport and work
  - Task to task
  - Task to larger group average values
- Pick up and visualize the critical keypoints
- Give fast feedback to an athlete or worker based on threshold values

## Prerequisites
- Python 3.7 or higher
- Tkinter library
  
## Installation
To install this version, follow these steps:

Download the Installer: Go to the [Releases](https://github.com/yethuhlaing/movement-analysis-application/releases)

Run the Installer: Double-click the downloaded installer and follow the on-screen instructions.

Complete Installation: Finish the installation process and launch the application via the desktop shortcut.

## Analysis Algorithm

The dataset should be the same format to analyze in this app!

- When Selecting the starting time, the selected time is multiplied by 240, (eg. 2second = 480 frame)
- If the duration time is 2 seconds , it means 480 frames duration analysis.
- When the starting time is at 2seconds (480th frame) and the duration is 2seconds(480frames), the ending time is at 4 seconds (960th frames)
- When the duration is equal 0, it will analyze from the starting frame to the ending frame.

![image](https://github.com/yethuhlaing/movement-analysis-application/assets/112906488/3f4560c4-f618-4cf4-98d4-67b177632030)

- Only the same kind of data can be analyzed. ( Downsampled vs Downsampled )
- Downsampled data and Actual data cannot be analyzed together.

  ![image](https://github.com/yethuhlaing/movement-analysis-application/assets/112906488/d7516ac0-2b50-4e54-ac59-9a9b78ae5a6c)

- Lowest time means the time at which the value is lowest.
- Highest time means the time at which the value is highest.
- Too low means the total duration of being low value compared to the reference.
- Too High means the total duration of being high value compared to the reference.
- Optimal means the total duration of being between maximum and minimum value compared to the reference.

## Generated Analysis Report

![image](https://github.com/yethuhlaing/movement-analysis-application/assets/112906488/4a49aaea-c257-4ecc-8561-43be5452e00d)
![image](https://github.com/yethuhlaing/movement-analysis-application/assets/112906488/b530c6d4-cab5-47ac-8114-104ae489fa26)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Feedback and Support
We welcome feedback, bug reports, and feature requests. Please follow these guidelines when submitting your feedback or reporting issues:

- **Bug Reports**: If you encounter a bug or unexpected behavior, please [create a new issue](https://github.com/yethuhlaing/movement-analysis-application/issues/new) on our GitHub repository. Include detailed information about the issue, steps to reproduce it, and your environment (OS, Python version, etc.).

- **Feature Requests**: If you have an idea for a new feature or improvement, please [create a new issue](https://github.com/yethuhlaing/movement-analysis-application/issues/new) on our GitHub repository. Describe the feature you'd like to see and why it would be valuable.

- **Feedback**: If you have general feedback or questions about the project, feel free to [contact us](mailto:yethusteve217@gmail,com) or open a discussion on our [GitHub Discussions](https://github.com/yethuhlaing/movement-analysis-application/discussions) page.

Your feedback is essential to improving this project, and we appreciate your contributions!



