# Github Webhook Deployment Manager

A tool that automates the deployment updates for Node.js projects using GitHub webhooks. This tool triggers git commands (`git fetch`, `git merge`, etc.) and the `pm2 restart` command to keep your application up-to-date with minimal intervention required.

---

## Environment Variables

Read the file `env.sample` to understand each environment variable. The Telegram environment variables are optional and are used to send notifications via a Telegram Bot.

Create a new `.env` file and configure the required environment variables.

---

## Installation

Clone this repository:

```bash
git clone https://github.com/ordenada/github-webhook-deployment-manager.git
cd github-webhook-deployment-manager
```

You can use the `install.sh` script to prepare the virtual environment. The packages in the `requirements.txt` files are required. Install them with the command `pip install -r requirements.txt`.

---

## Run

Start the webhook service:

```bash
python main.py
```

You can use PM2 to keep this process running.

---

## Usage

1. Configure a webhook in your GitHub repository:

   - Payload URL: `http://<HOST>:<PORT>/webhook`
   - Content Type: `application/json`
   - Secret: Match the `SECRET` value in your `.env` file.

2. Push updates to your repository. The tool will:

   - Fetch and merge the latest changes.
   - Restart the Node.js application using PM2.
   - Optionally send a Telegram notification about the deployment status.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
