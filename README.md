# ⭕️❌ GenLayer Tic-Tac-Toe: On-Chain AI Gaming

Welcome to **GenLayer Tic-Tac-Toe**, a fully decentralized, AI-powered variation of the classic game built on the [GenLayer](https://genlayer.com) blockchain. 

Unlike traditional deterministic EVM smart contracts, this game utilizes GenLayer's **GenVM**. Written entirely in Python, the game logic is processed through Optimistic Democracy Consensus (ODC), allowing the contract to potentially leverage LLMs for opponent logic, dynamic trash-talking, or complex state evaluations.

## ✨ Features
* **Python-Native Smart Contracts:** Built using GenVM's strict typed Python environment (`u32`, `Address`, `TreeMap`).
* **Asynchronous Gameplay:** Frontend integrated with `genlayer-js` to gracefully handle AI node consensus polling and leader rotations.
* **Fully Localized Testing:** Pre-configured for `studionet` deployment using local Docker execution to bypass testnet congestion.

---

## 🛠 Prerequisites

Before you begin, ensure you have the following installed:
* **Node.js** (v20+ recommended)
* **Docker Desktop** (Running in the background)
* **Python 3.8+**
* An API Key from an LLM provider (e.g., [Heurist](https://heurist.ai), OpenAI, or Anthropic)

---

## 🚀 Installation & Setup

### 1. Install the GenLayer CLI
Avoid the `maxBuffer` crashes by installing globally and initializing carefully:

npm install -g genlayer@latest
2. Clone the Repository
Bash
git clone [https://github.com/PhantomTee/genlayer-tictactoe.git](https://github.com/YOUR_USERNAME/genlayer-tictactoe.git)
cd genlayer-tictactoe
3. Start the Local Blockchain (studionet)
We recommend developing on studionet to ensure instant execution and to use your own LLM API keys without dealing with public testnet LEADER TIMEOUTs.

Bash
# Set network to local
genlayer network set studionet

# Initialize the environment (Input your LLM API key when prompted)
genlayer init

# Start the simulator
genlayer up
(Note: If Docker times out building the Postgres database, simply run genlayer up again).

📜 Contract Deployment
Your game logic lives inside contracts/TicTacToe.py. To deploy it to your local network:

Create a local deployer account:

Bash
```
genlayer account create --name game-deployer
genlayer account use game-deployer
```
Deploy the Python contract:

Bash
```
genlayer deploy --contract contracts/TicTacToe.py
```
Save the Contract Address output by the terminal! You will need it for the frontend.

🖥 Frontend Integration
The frontend is built with Vue.js and uses the genlayer-js SDK to communicate with the GenVM. Because GenLayer reaches consensus via LLMs, transactions are inherently asynchronous.

Navigate to the frontend directory:

Bash
cd frontend
npm install
Configure your environment variables:
Create a .env file in the frontend folder and add your deployed contract address:

Code snippet
VITE_CONTRACT_ADDRESS=0xYOUR_COPIED_CONTRACT_ADDRESS
Start the development server:

Bash
```
npm run dev
```
💡 Note on Transaction Polling
If you migrate this project to the public testnet-asimov, be aware that public AI nodes can get congested. The frontend genClient.waitForTransactionReceipt is intentionally configured with a long polling interval (retries: 120, interval: 5000) to handle validator rotations gracefully. Do not lower these values if deploying to public testnets!

🤝 Contributing
Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingAI)

Commit your Changes (git commit -m 'Add some AmazingAI')

Push to the Branch (git push origin feature/AmazingAI)

Open a Pull Request

📄 License
Distributed under the MIT License. See ```LICENSE``` for more information.
