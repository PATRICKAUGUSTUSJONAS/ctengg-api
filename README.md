# ctengg-api
[![Codacy grade](https://img.shields.io/codacy/grade/19e342e095b74db1a35f18d8ae6f34cc.svg)]()
[![Website](https://img.shields.io/website-up-down-green-red/http/ctengg.amu.ac.in.svg)]()
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

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
Project is managed poorly. Caching is very premature and database and memcached are warmed every Sunday using a cron job.
