# Ananda AI

Ananda AI is a calm, presence-oriented web interface for dialogue. The project emphasizes deliberate interaction, clear modes, local browser history, and a restrained visual design.

Русское описание находится ниже.

## Repository status

This repository currently contains the **static frontend only**:

- HTML, CSS, and JavaScript interface;
- Heart, Silence, and Guide interaction modes;
- browser speech recognition when supported;
- local conversation history using `localStorage`;
- frontend integrations for dialogue, vision, text-to-speech, and session clearing.

The production API is deployed separately and is not present in this repository. Its expected endpoints are documented in [API_CONTRACT.md](API_CONTRACT.md).

## Run locally

The informational pages work with any static web server:

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000>.

The dialogue page requires a compatible backend. Without one, the interface loads and local features work, but dialogue, image analysis, TTS, and backend session clearing report a connection error.

By default API calls use the same origin. For a separate API host, set the value of this tag in `dialog/index.html`:

```html
<meta name="ananda-api-base" content="https://api.example.com">
```

The backend must then allow requests from the frontend origin.

## Checks

Requirements: Python 3.11+ and Node.js 18+.

```bash
python scripts/check_site.py
```

The checker validates:

- local links and assets;
- duplicate HTML IDs;
- page metadata;
- inline JavaScript syntax;
- absence of deployment copies such as `var/www`.

GitHub Actions runs the same check for pull requests and changes to `main`.

## Privacy

- Conversation history displayed by the frontend is stored in the browser's `localStorage`.
- Messages, rhythm metadata, and uploaded images are sent to the configured API when the corresponding feature is used.
- Browser speech recognition may be implemented by the browser vendor and is not controlled by this repository.
- Actual server retention and third-party AI processing depend on the separately deployed backend.

Do not describe a deployment as collecting no data unless its backend and infrastructure have been verified accordingly.

## Structure

- `index.html` — landing page.
- `dialog/index.html` — main dialogue interface.
- `about/`, `modes/`, `silence/` — supporting pages.
- `API_CONTRACT.md` — frontend/backend integration contract.
- `scripts/check_site.py` — dependency-free static integrity checks.

## License

MIT. See [LICENSE](LICENSE).

---

## Русский

Ananda AI — спокойный веб-интерфейс для диалога, построенный вокруг присутствия, ритма и тишины.

В этом репозитории находится только статический frontend. Production backend развёрнут отдельно и сюда не включён. Поэтому после обычного запуска статического сервера доступны страницы, режимы, локальная история и браузерное распознавание речи, но AI-диалог, анализ изображений и озвучка требуют совместимого API.

Frontend сохраняет отображаемую историю в `localStorage`, однако при использовании AI-функций сообщения, данные о ритме и изображения передаются настроенному серверу. Политика хранения на сервере зависит от отдельной backend-реализации.

Основные принципы проекта:

- уважение к человеку;
- отсутствие манипулятивных механик;
- возможность молчания и медленного взаимодействия;
- прозрачность обработки данных;
- минимальный и спокойный интерфейс.
