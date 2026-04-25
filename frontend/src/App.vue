<script setup lang="ts">
import { ref } from 'vue'

/**
 * ENVIRONMENT & STATE
 */
const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS;
const userAddress = ref("");
const statusMessage = ref("Connect to GenLayer Asimov to start");
const onChainStrategy = ref(""); // 'every-move' or 'end-only'

const board = ref([
  "", "", "",
  "", "", "",
  "", "", ""
]);

const scores = ref({
  player: 0,
  tie: 0,
  computer: 0
});

const isGameOver = ref(false);
const gameResultForChain = ref("");

/**
 * NETWORK CONFIGURATION
 * Pointing to GenLayer Asimov L2 (Chain ID 4221)
 */
const targetNetwork = {
  chainId: '0x107d',
  chainName: 'GenLayer Asimov L2',
  rpcUrls: ['https://rpc.testnet-chain.genlayer.com'],
  blockExplorerUrls: ['https://explorer.testnet-chain.genlayer.com'],
  nativeCurrency: {
    name: 'GEN',
    symbol: 'GEN',
    decimals: 18
  }
};

/**
 * WALLET INTERACTION
 */
const connectWallet = async () => {
  const ethWindow = window as any;
  if (!ethWindow.ethereum) {
    statusMessage.value = "Web3 Wallet not detected!";
    return;
  }

  try {
    const accounts = await ethWindow.ethereum.request({ 
      method: 'eth_requestAccounts' 
    });
    userAddress.value = accounts[0];

    // Ensure user is on Asimov L2
    await ethWindow.ethereum.request({
      method: 'wallet_addEthereumChain',
      params: [targetNetwork],
    });

    statusMessage.value = "Connected to Asimov. Pick your strategy.";
  } catch (error) {
    statusMessage.value = "Connection failed. Please try again.";
  }
};

/**
 * GENLAYER SMART CONTRACT CALL
 * This triggers the actual wallet popup.
 */
const executeOnChainAction = async (actionName: string, params: any) => {
  const ethWindow = window as any;
  statusMessage.value = `Broadcasting ${actionName}...`;

  try {
    // REAL transaction request to your Scoreboard contract
    const txHash = await ethWindow.ethereum.request({
      method: 'eth_sendTransaction',
      params: [{
        from: userAddress.value,
        to: contractAddress,
        data: '0x', // Replace with encoded GenVM call if using full SDK
        value: '0x0'
      }]
    });

    console.log(`Transaction successful: ${txHash}`, params);
    statusMessage.value = "Blockchain confirmed!";
    return true;
  } catch (err) {
    console.error(err);
    statusMessage.value = "Transaction failed. Need GEN gas?";
    return false;
  }
};

/**
 * GAME LOGIC
 */
const makeMove = async (index: number) => {
  if (board.value[index] !== "" || isGameOver.value || !onChainStrategy.value) {
    return;
  }

  // Record Player Move On-Chain if Hardcore
  if (onChainStrategy.value === 'every-move') {
    const ok = await executeOnChainAction("record_move", { index, symbol: "X" });
    if (!ok) return;
  }

  board.value[index] = "X";
  let result = checkWinner(board.value);

  if (result) {
    handleEndGame(result);
    return;
  }

  // Robot Logic
  statusMessage.value = "Robot is deciding...";
  setTimeout(async () => {
    const available = board.value
      .map((val, idx) => (val === "" ? idx : null))
      .filter((val) => val !== null) as number[];

    if (available.length > 0) {
      const choice = available[Math.floor(Math.random() * available.length)];
      
      if (onChainStrategy.value === 'every-move') {
        await executeOnChainAction("record_move", { index: choice, symbol: "O" });
      }

      board.value[choice] = "O";
      let robotResult = checkWinner(board.value);
      if (robotResult) {
        handleEndGame(robotResult);
      } else {
        statusMessage.value = "Your turn! (X)";
      }
    }
  }, 600);
};

const checkWinner = (b: string[]) => {
  const patterns = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // Cols
    [0, 4, 8], [2, 4, 6]             // Diagonals
  ];

  for (let p of patterns) {
    if (b[p[0]] && b[p[0]] === b[p[1]] && b[p[0]] === b[p[2]]) {
      return b[p[0]];
    }
  }
  return b.includes("") ? null : "Tie";
};

const handleEndGame = (winner: string) => {
  isGameOver.value = true;
  if (winner === "X") {
    scores.value.player++;
    gameResultForChain.value = "win";
    statusMessage.value = "You Won!";
  } else if (winner === "O") {
    scores.value.computer++;
    gameResultForChain.value = "loss";
    statusMessage.value = "Robot Won!";
  } else {
    scores.value.tie++;
    gameResultForChain.value = "tie";
    statusMessage.value = "It's a Tie!";
  }
};

const restart = () => {
  board.value = ["", "", "", "", "", "", "", "", ""];
  isGameOver.value = false;
  gameResultForChain.value = "";
  statusMessage.value = "Your turn (X)";
};
</script>

<template>
  <main class="app-wrapper">
    
    <header class="top-nav" v-if="userAddress">
      <div class="user-pill">
        {{ userAddress.substring(0, 6) }}...{{ userAddress.slice(-4) }}
      </div>
      <a 
        href="https://testnet-faucet.genlayer.foundation" 
        target="_blank" 
        class="faucet-button"
      >
        Get GEN Gas ↗
      </a>
    </header>

    <section class="main-content">
      <h1 class="title">GenLayer <br> Tic-Tac-Toe</h1>

      <div v-if="!userAddress" class="view-box">
        <button class="primary-button" @click="connectWallet">
          Connect Wallet
        </button>
        <p class="status-text">{{ statusMessage }}</p>
      </div>

      <div v-else-if="!onChainStrategy" class="view-box">
        <h2 class="sub-title">Select On-Chain Mode</h2>
        <div class="strategy-grid">
          <button class="strat-card" @click="onChainStrategy = 'every-move'">
            <span class="strat-name">Hardcore</span>
            <span class="strat-desc">Every move = Real Transaction</span>
          </button>
          
          <button class="strat-card" @click="onChainStrategy = 'end-only'">
            <span class="strat-name">Casual</span>
            <span class="strat-desc">Only result saved on-chain</span>
          </button>
        </div>
      </div>

      <div v-else class="view-box">
        <div class="game-board">
          <div 
            v-for="(cell, i) in board" 
            :key="i" 
            class="grid-cell" 
            :class="cell"
            @click="makeMove(i)"
          >
            {{ cell }}
          </div>
        </div>

        <div class="score-display">
          <div class="score-item">
            <label>PLAYER</label>
            <var>{{ scores.player }}</var>
          </div>
          <div class="score-item">
            <label>TIES</label>
            <var>{{ scores.tie }}</var>
          </div>
          <div class="score-item">
            <label>ROBOT</label>
            <var>{{ scores.computer }}</var>
          </div>
        </div>

        <p class="status-text">{{ statusMessage }}</p>

        <footer class="game-controls" v-if="isGameOver">
          <button 
            v-if="onChainStrategy === 'end-only' && gameResultForChain"
            class="save-button"
            @click="executeOnChainAction('record_match', [userAddress, gameResultForChain])"
          >
            Record Win On-Chain
          </button>
          <button class="outline-button" @click="restart">
            Play Again
          </button>
        </footer>
      </div>
    </section>
  </main>
</template>

<style scoped>
/**
 * ROBUST CSS ARCHITECTURE
 */

.app-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #14bdac;
  color: #ffffff;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  position: relative;
  padding: 20px;
  box-sizing: border-box;
}

/* NAVBAR */
.top-nav {
  position: absolute;
  top: 20px;
  width: 100%;
  max-width: 500px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-sizing: border-box;
}

.user-pill {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 6px 14px;
  border-radius: 30px;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.faucet-button {
  background-color: #2a2a2a;
  color: white;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 30px;
  transition: opacity 0.2s;
}

.faucet-button:hover {
  opacity: 0.8;
}

/* MAIN CONTENT */
.main-content {
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.title {
  font-size: 2.8rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 2rem;
  text-transform: uppercase;
  letter-spacing: -1px;
}

.sub-title {
  margin-bottom: 20px;
  font-weight: 700;
}

/* BUTTONS */
.primary-button {
  background-color: #ffffff;
  color: #14bdac;
  border: none;
  padding: 18px 36px;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.strategy-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.strat-card {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid #ffffff;
  border-radius: 15px;
  padding: 20px;
  color: #ffffff;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  transition: all 0.2s;
}

.strat-card:hover {
  background: #ffffff;
  color: #14bdac;
}

.strat-name {
  font-size: 1.3rem;
  font-weight: 800;
}

.strat-desc {
  font-size: 0.85rem;
  opacity: 0.8;
}

/* GAME BOARD - HARDCODED GRID */
.game-board {
  display: grid;
  grid-template-columns: repeat(3, 100px);
  grid-template-rows: repeat(3, 100px);
  margin: 0 auto 30px;
  width: 300px;
  height: 300px;
}

.grid-cell {
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4.5rem;
  font-weight: 900;
  cursor: pointer;
  border: 5px solid #ffffff;
  box-sizing: border-box;
}

/* Inner Grid Lines */
.grid-cell:nth-child(1), .grid-cell:nth-child(2), .grid-cell:nth-child(3) { border-top: none; }
.grid-cell:nth-child(7), .grid-cell:nth-child(8), .grid-cell:nth-child(9) { border-bottom: none; }
.grid-cell:nth-child(1), .grid-cell:nth-child(4), .grid-cell:nth-child(7) { border-left: none; }
.grid-cell:nth-child(3), .grid-cell:nth-child(6), .grid-cell:nth-child(9) { border-right: none; }

.grid-cell.X { color: #545454; }
.grid-cell.O { color: #f2ebd3; }

/* SCOREBOARD */
.score-display {
  display: flex;
  justify-content: space-between;
  background: rgba(0, 0, 0, 0.08);
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 20px;
}

.score-item {
  display: flex;
  flex-direction: column;
}

.score-item label {
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 1px;
}

.score-item var {
  font-size: 1.8rem;
  font-style: normal;
  font-weight: 900;
}

.status-text {
  font-weight: 700;
  min-height: 1.5em;
  margin-bottom: 20px;
}

/* CONTROLS */
.game-controls {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.save-button {
  background-color: #2a2a2a;
  color: #ffffff;
  border: none;
  padding: 14px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
}

.outline-button {
  background: transparent;
  border: 2px solid #ffffff;
  color: #ffffff;
  padding: 10px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
}

/* RESPONSIVENESS */
@media (max-width: 420px) {
  .game-board {
    grid-template-columns: repeat(3, 85px);
    grid-template-rows: repeat(3, 85px);
    width: 255px;
    height: 255px;
  }
  .grid-cell {
    width: 85px;
    height: 85px;
    font-size: 3.5rem;
  }
  .title {
    font-size: 2.2rem;
  }
}
</style>