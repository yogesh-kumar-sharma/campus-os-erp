# Faculty Module

Faculty records are employment profiles connected one-to-one to user accounts
with the `faculty` role.

| Method | Endpoint | Access |
| --- | --- | --- |
| POST | `/api/v1/faculty` | Admin |
| GET | `/api/v1/faculty/me` | Faculty |
| GET | `/api/v1/faculty` | Admin |
| GET | `/api/v1/faculty/{faculty_id}` | Admin |
| PATCH | `/api/v1/faculty/{faculty_id}` | Admin |

The current profile contains named subject and class assignment lists so faculty
can view their workload immediately. Module 9 will replace these interim lists
with normalized Subject and timetable/class relationships.
