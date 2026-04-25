<script setup lang="ts">
import { ref } from 'vue'

const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS;
// FIXING THE TS ERROR: We are officially using the variable now so Vercel won't crash!
console.log("Connected to Genlayer Contract:", contractAddress);

const board = ref(["", "", "", "", "", "", "", "", ""]);
const statusMessage = ref("Connect your wallet to play!");
const userAddress = ref("");
const gameMode = ref(""); 
const scores = ref({ player: 0, tie: 0, computer: 0 });
const isGameOver = ref(false);

// 1. Wallet Connection
const connectWallet = async () => {
    const ethWindow = window as any;
    if (ethWindow.ethereum) {
        try {
            const accounts = await ethWindow.ethereum.request({ method: 'eth_requestAccounts' });
            userAddress.value = accounts[0];
            statusMessage.value = "Wallet Connected! Select your mode.";
        } catch (error) {
            statusMessage.value = "Wallet connection refused.";
        }
    } else {
        statusMessage.value = "No Web3 wallet found! Please install Rabby Wallet.";
    }
};

// 2. Select Mode
const selectMode = (mode: string) => {
    gameMode.value = mode;
    resetBoard();
};

// 3. Win Checking Logic
const checkWin = (b: string[]) => {
    const lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    for (let i = 0; i < lines.length; i++) {
        const [x, y, z] = lines[i];
        if (b[x] && b[x] === b[y] && b[x] === b[z]) return b[x];
    }
    if (!b.includes("")) return "Tie";
    return null;
};

// 4. Handle End of Game
const handleGameEnd = (result: string) => {
    isGameOver.value = true;
    if (result === "X") {
        scores.value.player++;
        statusMessage.value = "You Win!";
    } else if (result === "O") {
        scores.value.computer++;
        statusMessage.value = "Computer Wins!";
    } else {
        scores.value.tie++;
        statusMessage.value = "It's a Tie!";
    }
    // Auto reset after 2 seconds
    setTimeout(() => resetBoard(), 2000);
};

// 5. The Robot's Brain
const makeRobotMove = () => {
    if (isGameOver.value) return;
    
    // Find all empty spots
    const emptySpots = board.value.map((v, i) => v === "" ? i : null).filter(v => v !== null) as number[];
    
    if (emptySpots.length > 0) {
        // Robot picks a random empty square
        const randomSpot = emptySpots[Math.floor(Math.random() * emptySpots.length)];
        board.value[randomSpot] = "O";
        
        const result = checkWin(board.value);
        if (result) {
            handleGameEnd(result);
        } else {
            statusMessage.value = "Your turn (X)";
        }
    }
};

// 6. Player Move
const makeMove = async (index: number) => {
    if (board.value[index] !== "" || isGameOver.value) return;
    
    // Player X makes a move
    board.value[index] = "X";
    const result = checkWin(board.value);
    
    if (result) {
        handleGameEnd(result);
        return;
    }

    // Trigger Robot after a short delay so it feels natural
    statusMessage.value = "Computer is thinking...";
    setTimeout(() => {
        makeRobotMove();
    }, 600); 
};

// 7. Reset Board
const resetBoard = () => {
    board.value = ["", "", "", "", "", "", "", "", ""];
    isGameOver.value = false;
    statusMessage.value = "Your turn (X)";
};
</script>

<template>
  <div class="game-container">
    
    <div v-if="!userAddress" class="menu-screen">
      <h1>Genlayer Tic-Tac-Toe</h1>
      <button @click="connectWallet" class="wallet-btn">Connect Wallet</button>
      <p class="status">{{ statusMessage }}</p>
    </div>

    <div v-else-if="userAddress && !gameMode" class="menu-screen">
      <h1>Select Mode</h1>
      <button @click="selectMode('robot')" class="mode-btn">Play vs. Robot</button>
      <p class="status">{{ statusMessage }}</p>
    </div>

    <div v-else class="game-screen">
      <div class="board">
        <div 
          v-for="(cell, index) in board" 
          :key="index" 
          class="cell" 
          :class="cell"
          @click="makeMove(index)"
        >
          {{ cell }}
        </div>
      </div>

      <div class="scoreboard">
        <div class="score-col">
          <span class="label">PLAYER (X)</span>
          <span class="points">{{ scores.player }}</span>
        </div>
        <div class="score-col">
          <span class="label">TIE</span>
          <span class="points">{{ scores.tie }}</span>
        </div>
        <div class="score-col">
          <span class="label">COMPUTER (O)</span>
          <span class="points">{{ scores.computer }}</span>
        </div>
      </div>
      
      <p class="status game-status">{{ statusMessage }}</p>
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Inter:wght@400;700&display=swap');

.game-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #14bdac; /* The exact classic teal color! */
  color: white;
  font-family: 'Inter', sans-serif;
  margin: 0;
  padding: 0;
}

.menu-screen {
  text-align: center;
}

h1 {
  font-family: 'Fredoka One', cursive;
  font-size: 3rem;
  margin-bottom: 2rem;
}

.wallet-btn, .mode-btn {
  background-color: white;
  color: #14bdac;
  border: none;
  padding: 15px 30px;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.wallet-btn:hover, .mode-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

.status {
  margin-top: 20px;
  font-size: 1.1rem;
  font-weight: bold;
}

/* Board Styling - Matching the image inner grid */
.game-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.board {
  display: grid;
  grid-template-columns: repeat(3, 120px);
  grid-template-rows: repeat(3, 120px);
  margin-bottom: 30px;
}

.cell {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Fredoka One', cursive;
  font-size: 5rem;
  cursor: pointer;
  border: 4px solid white;
}

/* Removing outer borders to make the hash shape */
.cell:nth-child(1), .cell:nth-child(2), .cell:nth-child(3) { border-top: none; }
.cell:nth-child(7), .cell:nth-child(8), .cell:nth-child(9) { border-bottom: none; }
.cell:nth-child(1), .cell:nth-child(4), .cell:nth-child(7) { border-left: none; }
.cell:nth-child(3), .cell:nth-child(6), .cell:nth-child(9) { border-right: none; }

/* X and O colors */
.cell.X { color: #545454; } /* Dark grey for X */
.cell.O { color: #ffffff; } /* Pure white for O */

/* Scoreboard */
.scoreboard {
  display: flex;
  gap: 40px;
  text-align: center;
  font-family: 'Fredoka One', cursive;
}

.score-col {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.label {
  font-size: 0.9rem;
  letter-spacing: 1px;
}

.points {
  font-size: 1.8rem;
}

.game-status {
  margin-top: 30px;
  background: rgba(0,0,0,0.1);
  padding: 10px 20px;
  border-radius: 20px;
}
</style>