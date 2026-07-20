# Academic Module

The academic catalog normalizes the relationships used by student enrollment,
faculty workload, examinations, and attendance.

```text
Department → Course → Semester → Subject
                     ↘ Student enrollment
Faculty ↔ Subject assignment
Academic session + Subject + Faculty → Timetable entry
```

Administrators manage all academic routes under `/api/v1/academic`:

- `POST` / `GET` departments, courses, semesters, subjects, and sessions
- `POST` faculty-subjects to assign a faculty member to a subject
- `POST` / `GET` timetable

The migration maps existing Student and Faculty text fields to seeded academic
records, then replaces those fields with foreign keys. Student and Faculty API
creation payloads now accept `department_id`; student payloads also require
`course_id` and `semester_id`.
