# PAE Bird — LibreOffice Extension

## What this is
A LibreOffice Calc `.oxt` extension that adds 5 polynomial algebra functions powered by the Railway-hosted PAE API.

## Build
```bash
bash build.sh   # produces PAEBird.oxt (~8KB)
```

## Files
| File | Purpose |
|------|---------|
| `META-INF/manifest.xml` | Declares all components to LibreOffice |
| `CalcAddins.xcu` | Registers PAE_SOLVE/EXPAND/FACTOR/DIFFERENTIATE/INTEGRATE as calc functions |
| `Addons.xcu` | Adds "Tools → PAE Bird Settings…" menu item |
| `python/pae_bird.py` | UNO Python add-in — XAddIn implementation, HTTP calls to Railway |
| `PaeBird/Module1.xba` | Basic macro — InputBox settings dialog, reads/writes `~/.config/paebird/key.txt` |
| `PaeBird/PaeBird.xlb` | Basic library descriptor |

## Free / Paid tier
- **Free key** hardcoded in `pae_bird.py`: `pae-free-public-2026`
  - Railway rate-limits this key to **50 calls/day per IP** via `freeTierLimiter` in `PAE-API/index.js`
  - Railway env var required: `PAE_FREE_KEY=pae-free-public-2026`
- **Paid key**: user pastes via Tools → PAE Bird Settings, stored at `~/.config/paebird/key.txt`
- Registration/upgrade page: `pae-bird-landing/register.html`

## API backend
- Repo: `PAE-API/index.js` (Railway, same as Google Sheets)
- URL: `https://pae-api-production.up.railway.app`
- Auth: `x-api-key` header
- Endpoints: POST `/solve`, `/expand`, `/factor`, `/differentiate`, `/integrate`

## TODO before publishing
1. Set `PAE_FREE_KEY=pae-free-public-2026` in Railway env and redeploy
2. Upload `PAEBird.oxt` to GitHub Releases (or similar), update download link in `index.html` (`href="#"` placeholder near bottom of libreoffice section)
3. Submit to https://extensions.libreoffice.org
4. Add payment processor (Stripe/Gumroad) and update `register.html` upgrade button

## Install (user-facing)
Extensions → Extension Manager → Add → select PAEBird.oxt → restart Calc
