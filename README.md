# UIB_Week_Planner

This is just a small application which gets the schedule for a subjects at the university of Bergen.
It can then take those subjects store them locally and give you all possibly schedules in which all subjects fit. 
The application is in Beta and has a basic GUI. The application is not tested with all different kinds of subjects.  
When using the application remember that it makes no guarantee of accuracy. Before signing up to a combination of groups
suggested by this application always double check them yourself to make sure they are correct. 

The structure of the plans.json file, which is generated when you save a subject, is as follows.
The subject code which contains all the different groups and lectures. Each group or lecture contains all the different weeks the group/lecture meets represented by their week number. Each week contains the different events/occurences of that group aka when the group has a session. 

The search function is simple and searches for all partial matches. If you want to search only in one of the column/subjects.
Search like this: Subjectcode: group
For example if you are looking for group 6 in INFO135 you search for this like so: INFO135: group 6
