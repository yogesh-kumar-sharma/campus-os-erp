# Authentication API

All routes are versioned under `/api/v1/auth`. Protected routes use the
`Authorization: Bearer <access_token>` header.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/register` | Register an account |
| POST | `/login` | Get access and refresh tokens |
| POST | `/refresh` | Rotate a refresh token |
| POST | `/logout` | Revoke a refresh token |
| POST | `/forgot-password` | Request reset instructions |
| POST | `/reset-password` | Set a new password using reset token |
| POST | `/change-password` | Change the current account password |
| GET | `/me` | Get the authenticated account |

Example login request:

```json
{"email":"student@example.edu","password":"strong-password"}
```

Successful login response:

```json
{"access_token":"<jwt>","refresh_token":"<jwt>","token_type":"bearer"}
```

Refresh tokens are stored only as SHA-256 fingerprints, rotated upon use, and
revoked on logout or any password change. Password-reset requests return a
generic message to prevent account enumeration, and successful resets invalidate
previous reset tokens. Connect the service hand-off in
`AuthService.request_password_reset` to the selected email provider before
production deployment.
