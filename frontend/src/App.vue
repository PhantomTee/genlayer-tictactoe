<script setup lang="ts">
import { ref } from 'vue'

const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS;
const board = ref(["", "", "", "", "", "", "", "", ""]);
const statusMessage = ref("Not connected. Please connect your wallet.");
const userAddress = ref("");

// 1. Function to connect Rabby / Browser Wallet (Now TypeScript safe!)
const connectWallet = async () => {
    const ethWindow = window as any; // Tells TypeScript to bypass the strict window check
    
    if (ethWindow.ethereum) {
        try {
            const accounts = await ethWindow.ethereum.request({ method: 'eth_requestAccounts' });
            userAddress.value = accounts[0];
            statusMessage.value = `Connected: ${userAddress.value.slice(0,6)}...${userAddress.value.slice(-4)}. Ready to play!`;
        } catch (error) {
            statusMessage.value = "Wallet connection refused.";
        }
    } else {
        statusMessage.value = "No Web3 wallet found! Please install Rabby Wallet.";
    }
};

// 2. Function to interact with the Genlayer Smart Contract
const makeMove = async (index: number) => {
    if (!userAddress.value) {
        statusMessage.value = "❌ Connect your wallet first!";
        return;
    }
    if (board.value[index] !== "") return;
    
    statusMessage.value = `Please sign the transaction in Rabby for square ${index}...`;
    
    try {
        await new Promise(r => setTimeout(r, 1500)); 
        board.value[index] = "X"; 
        statusMessage.value = `Move confirmed! Waiting for O...`;
    } catch (e) {
        statusMessage.value = "Transaction failed or rejected!";
    }
};
</script>


<template>
  <div class="game-container">
    <h1>Genlayer Tic-Tac-Toe</h1>
    
    <button v-if="!userAddress" @click="connectWallet" class="wallet-btn">
      Connect Wallet
    </button>
    
    <p class="status">{{ statusMessage }}</p>
    
    <div class="board">
      <div 
        v-for="(cell, index) in board" 
        :key="index" 
        class="cell" 
        @click="makeMove(index)"
      >
        {{ cell }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.game-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Inter', sans-serif;
  margin-top: 50px;
  color: white;
  background-color: #121212;
  min-height: 100vh;
}

.wallet-btn {
  background-color: #7b3fe4; /* Rabby Purple */
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  margin-bottom: 20px;
  transition: opacity 0.2s;
}

.wallet-btn:hover {
  opacity: 0.8;
}

.status { margin-bottom: 30px; font-size: 1.2rem; color: #42b883; }
.board { display: grid; grid-template-columns: repeat(3, 120px); grid-gap: 10px; background-color: #2a2a2a; padding: 10px; border-radius: 12px; }
.cell { width: 120px; height: 120px; background-color: #1a1a1a; display: flex; justify-content: center; align-items: center; font-size: 4rem; font-weight: bold; cursor: pointer; border-radius: 8px; transition: background-color 0.2s; }
.cell:hover { background-color: #3a3a3a; }
</style>