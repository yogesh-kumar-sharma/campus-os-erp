# Role-Based Access Control

The API defines three seeded, persistent roles:

| Role | Access |
| --- | --- |
| `admin` | Full administrative access and role assignment |
| `faculty` | Attendance, marks, and student access in later modules |
| `student` | Personal profile, attendance, results, and fees in later modules |

New public registrations are assigned the `student` role. The role catalog and
role assignment route are admin-only:

```text
GET   /api/v1/roles
PATCH /api/v1/roles/users/{user_id}
```

After running migrations, bootstrap the first administrator locally or through
the deployment secret manager:

```bash
python -m app.utils.create_admin \
  --email admin@example.edu \
  --full-name "ERP Administrator" \
  --password "use-a-unique-strong-password"
```

Use `require_roles(RoleName.ADMIN)` (or the appropriate role set) on all new
protected routes. The database migration seeds a Student role for existing
accounts, preserving data during deployment.
