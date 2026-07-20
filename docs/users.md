# User Profile API

All endpoints require a bearer access token. Administrators may retrieve and
search all accounts; all users manage their own profile.

| Method | Endpoint | Access |
| --- | --- | --- |
| GET | `/api/v1/users/me` | Current user |
| PATCH | `/api/v1/users/me` | Current user |
| POST | `/api/v1/users/me/profile-picture` | Current user |
| POST | `/api/v1/users/me/deactivate` | Current user, password confirmation |
| GET | `/api/v1/users` | Admin |
| GET | `/api/v1/users/{user_id}` | Admin |

Profile updates accept `full_name`, `phone`, and `address`. The list endpoint
supports `offset`, `limit` (maximum 100), and `search` across name and email.

Profile images accept JPEG, PNG, and WebP only, and are stored under the
configured `STORAGE_PATH` using server-generated names. The API stores a
relative reference rather than serving the storage directory directly. Module 14
will extend this storage abstraction to student and faculty documents.
