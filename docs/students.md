# Student Module

The Student module manages admissions and the student enrollment profile. An
administrator first creates or assigns a user to the `student` role, then
creates its student record.

| Method | Endpoint | Access |
| --- | --- | --- |
| POST | `/api/v1/students` | Admin |
| GET | `/api/v1/students/me` | Student |
| GET | `/api/v1/students` | Faculty, Admin |
| GET | `/api/v1/students/{student_id}` | Faculty, Admin |
| PATCH | `/api/v1/students/{student_id}` | Admin |

The initial admission record stores the department, course, and semester as
enrollment fields so the module remains usable before the academic catalog is
introduced. Module 9 will add the normalized Department, Course, and Semester
foreign-key relationships and migrate these values.
