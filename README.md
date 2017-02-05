# ctengg-api
Unofficial REST API for ctengg.amu.ac.in

## Endpoints

*Attendance* -  
 /attendance/<faculty_number>?api_key={auth_key} 
 
*Result* -  
 /result/btech?fac=<faculty_number>&en=<enrolment_number>&api_key={auth_key}
  
*Complete Attendance List* -  
/complete_attendance?api_key={auth_key}  

*Subject from Complete Attendance* -  
/complete_attendance/<subject_id>?api_key={auth_key}  

## Disclaimer
Project is managed poorly. Caching is very premature and database and memcached are warmed every 20 minutes using a cron job.
