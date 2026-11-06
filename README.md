# Shoes

A small, local-only showcase for shoes you have worn. The app uses:

- **Python** for a standard-library HTTP server and the in-code shoe collection.
- **TypeScript** for the frontend, compiled into `dist/`.
- No database, authentication, uploads, or external services.

## Run it

```bash
npm install
npm run build
python3 app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

`npm run dev` also builds the TypeScript and starts the Python server.

## Add your own shoes

Edit the `SHOES` list in [`app.py`](./app.py). Each entry supports:

- `brand`, `model`, `colorway`, and `category`
- `price` and `currency`
- `purchaseYear` and optional `wornSince`
- `rating` from 0 to 5
- `comments`
- `details`, a list of short tags
- optional `imageUrl` for a remote image URL

The current image area intentionally falls back to a typographic placeholder, so the scaffold works without uploading or storing images.
