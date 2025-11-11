# BodaNet Dev Journal

## 2025-11-11

**Goal:** bootstrap a modular Django backend for boda-boda operations (fare lookup, stand queueing, trusted riders) using Django + DRF.

### What I did

- Created Django project `bodanet/`.
- Created apps: `core`, `fare`, `queueing`, `trusted`.
- Configured `rest_framework` in `INSTALLED_APPS`.
- Implemented a custom user model in `core.models.User` with `is_rider` and `phone`.
- Added `Stand` model in `core` with `name`, `code`, and optional coordinates.
- Wired URLs:
  - `/admin/`
  - `/api/ping/` (health check)
- Created `fare` app model `FareRule` for origin/destination stand pairs with min/max/recommended fares.
- Exposed endpoint: `GET /api/fare/?origin=USA-RIVER&destination=MAJI-YA-CHAI`
  - Tested successfully — returned correct fare JSON.
- Created `queueing` app with `StandSession` model to represent riders checked into a stand.
- Exposed queue endpoints:
  - `POST /api/queue/join/` — rider joins a stand (initially took `rider_id`, later switched to using `request.user`)
  - `POST /api/queue/next/` — dispatch next available rider from a stand, supports `trusted_only`
- Created basic `trusted.RiderProfile` model (one-to-one to user) with `is_trusted` flag to support trusted-only queries.
- Verified that joining the queue via browsable API works:
  - Response example:

    ```json
    {
      "id": 4,
      "rider_username": "dkomics",
      "stand_code": "USA-RIVER",
      "joined_at": "2025-11-11T19:38:20.674913Z",
      "active": true
    }
    ```

### Notes / Decisions

- We chose to modularize early: `core`, `fare`, `queueing`, `trusted` as separate apps.
- We set `AUTH_USER_MODEL = "core.User"` on day 1 to avoid painful refactors later.
- For now, browser tests rely on Django session auth (login via `/admin/`), but plan to add JWT for mobile clients.
- `fare` returns stand codes, not numeric IDs — easier for mobile/USSD.
- Queue join now uses `request.user` → safer than sending arbitrary `rider_id`.

### To do (next)

- Add endpoint to list available stands: `GET /api/stands/`
- Register `RiderProfile` in admin and test `/api/queue/next/` with `trusted_only=true`
- Add JWT auth (djangorestframework-simplejwt) for Flutter/mobile use
- Add basic validation to prevent duplicate active sessions for the same rider/stand
- Consider seeding common stands in Arusha (USA River, Maji ya Chai, Leganga, Tengeru)
- Write minimal README about project purpose

---
