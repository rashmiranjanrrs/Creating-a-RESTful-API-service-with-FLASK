create a RESTful API service for To-Do list application having 5 end-point api with http method "GET" "POST".
----------------------------------------------------------------------------------------------------------------
I have import flash, flask_httpauth for Basic Http Authentication, flask_sqlachemy for SQLAlchemy and datetime and checked the full task
by POSTMAN.
I used SQLAchemy for Database Interaction.

content - here our todo list will save
id - this is a unique identifier
add_date - this is the date when the task was added
end_date - this is the date when the task was completed successfully.
done - this is the boolean which is False if task is incomplete and if task is completed the True.

pass_auth() is called by authentication module to match with the password that user has entered while making request. 
it will check in the given username in the querry if its find the username it will return the password .

sign up(): Here we created a user object having Username, password and email. then it will storeed in the database.

addtask(): It will first authentucate the username and password, then added to the content object.
 wchich will stored in the database, json object will create an id for it by which user can delete or add new task to it.
 
 markdone(): It will take the GET request with task id of which user want to mark as done then it checks the database if it found the 
 content with the id it will mark it as done(True).
 
 deleteask(): It will take the POST request with task id of which user want to delete then it checks the database if it found the 
 content with the id it will remove it.
 
 showtasks(): It will take the GET request then show user all his task with statuses.
 
