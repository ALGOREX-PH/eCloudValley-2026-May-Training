# Setup Guide — Read this BEFORE Day 1

We have only 6 hours together. Please complete this setup **before you arrive on Day 1** so we can spend the time building agents instead of debugging environments.

> **Estimated time:** 10–15 minutes on a clean laptop.

If you get stuck on any step, message the speaker — we'd rather solve it now than during the workshop.

---

## 1. Install Python 3.11+

### Windows

1. Download the installer from <https://www.python.org/downloads/windows/>
2. Run the installer
3. **Tick "Add python.exe to PATH"** at the bottom of the first screen
4. Click **Install Now**

Verify:

```powershell
python --version
# Should print: Python 3.11.x  or  Python 3.12.x
```

### macOS

```bash
brew install python@3.12
python3 --version
```

### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3-pip
python3 --version
```

---

## 2. Install Git

- **Windows:** <https://git-scm.com/download/win>
- **macOS:** `brew install git`
- **Linux:** `sudo apt install git`

Verify: `git --version`

---

## 3. Clone the training repo

Pick a folder you can find again:

```bash
# Windows (PowerShell)
cd $HOME\Documents
git clone <repo-url-shared-by-speaker> eCloudValley-Training
cd eCloudValley-Training

# macOS / Linux
cd ~
git clone <repo-url-shared-by-speaker> eCloudValley-Training
cd eCloudValley-Training
```

---

## 4. Create a virtual environment & install dependencies

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> If you see `running scripts is disabled on this system` on Windows, run PowerShell as Administrator once and execute:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

The install should take 1–3 minutes.

---

## 5. Configure your OpenAI API key

The speaker emailed you a workshop API key (a string starting with `sk-...`). Paste it into your local `.env` file:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` in a text editor and replace the placeholder:

```
OPENAI_API_KEY=sk-your-actual-key-here
```

> The workshop key is rate-limited and budget-capped. **Do not commit the `.env` file to git** (it's already in `.gitignore`). Do not share the key.

---

## 6. Run the smoke test

```bash
python labs/day1/lab1_first_agent/starter.py
```

You should see streaming text from the agent. If you do, you're ready for class. 🎉

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'agno'` | The venv isn't activated. Re-run the activate command from step 5. |
| `Authentication error` from OpenAI | Your `.env` key is wrong or has trailing spaces. Re-copy from the speaker's email. |
| `RateLimitError` | The workshop key has limits — try again in 30 sec, or message the speaker. |
| `python: command not found` (macOS) | Use `python3` instead of `python` everywhere. |
| Nothing prints on Windows | Make sure you ran the script in the activated venv terminal, not in a fresh window. |
| `Set-ExecutionPolicy ... script disabled` (Windows) | Re-run step 4's PowerShell exec policy fix in an admin shell. |

---

## What to bring on the day

- Your laptop, **fully charged** + charger
- The `.env` file populated with your key
- The repo cloned and `pip install` already run
- A power adapter if your laptop uses an unusual plug
- An open mind and questions — this is a workshop, not a lecture
