# API contract

This repository contains the static Ananda AI frontend. The production backend is deployed separately and is not included here.

By default the frontend calls the same origin. A deployment may set the `ananda-api-base` meta value in `dialog/index.html` when the API is hosted elsewhere.

## Endpoints

### `POST /api/dialog`

Request:

```json
{
  "message": "User message",
  "mode": "heart",
  "tempo": "normal",
  "night": false,
  "rhythm": {
    "avgSpeed": 180,
    "length": 12,
    "pauseBeforeSend": 900
  }
}
```

Response must contain a string `reply` or `action` field.

### `POST /api/vision`

Accepts multipart form data with an `image` field. Response:

```json
{"text": "Image description"}
```

### `POST /api/tts`

Request:

```json
{"text": "Text to speak"}
```

Returns playable audio bytes with an appropriate audio content type.

### `POST /api/clear`

Clears any backend session state associated with the current client. The frontend always clears its local browser history independently.

## Error behavior

All endpoints should return a non-2xx status for failures. The frontend validates HTTP status and essential response fields before rendering data.
