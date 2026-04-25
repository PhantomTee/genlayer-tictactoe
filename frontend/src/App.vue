<script setup lang="ts">
import { ref } from 'vue'

const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS;
const board = ref(["", "", "", "", "", "", "", "", ""]);
const statusMessage = ref("Connect an EVM wallet to play!");
const userAddress = ref("");
const onChainStrategy = ref(""); 
const scores = ref({ player: 0, tie: 0, computer: 0 });
const isGameOver = ref(false);
const showFaucetLink = ref(false); // New state to show faucet button
const gameResultForChain = ref(""); 

const targetNetwork = {
    chainId: '0x107d', 
    chainName: 'GenLayer Asimov L2',
    rpcUrls: ['https://rpc.testnet-chain.genlayer.com'], 
    blockExplorerUrls: ['https://explorer.testnet-chain.genlayer.com'],
    nativeCurrency: { name: 'GEN', symbol: 'GEN', decimals: 18 },
};

const connectWallet = async () => {
    const ethWindow = window as any;
    if (!ethWindow.ethereum) { statusMessage.value = "No wallet found!"; return; }
    try {
        const accounts = await ethWindow.ethereum.request({ method: 'eth_requestAccounts' });
        userAddress.value = accounts[0];
        const currentChainId = await ethWindow.ethereum.request({ method: 'eth_chainId' });
        if (currentChainId !== targetNetwork.chainId) {
            await ethWindow.ethereum.request({
                method: 'wallet_addEthereumChain',
                params: [targetNetwork],
            });
        }
        statusMessage.value = "Connected! Select Strategy.";
    } catch (e) { statusMessage.value = "Connection failed."; }
};

const sendToGenLayer = async (action: string, data: any) => {
    statusMessage.value = `Broadcasting ${action} to GenLayer...`;
    showFaucetLink.value = false;
    try {
        // Simulation of contract call
        await new Promise(r => setTimeout(r, 1500)); 
        return true;
    } catch (e: any) {
        if (e.message?.includes('insufficient funds') || e.code === -32000) {
            statusMessage.value = "Transaction failed: Insufficient gas!";
            showFaucetLink.value = true;
        } else {
            statusMessage.value = "Transaction failed or rejected.";
        }
        return false;
    }
};

const makeMove = async (i: number) => {
    if (board.value[i] || isGameOver.value || !onChainStrategy.value) return;

    if (onChainStrategy.value === 'every-move') {
        const success = await sendToGenLayer("record_move", [i, "X"]);
        if (!success) return;
    }

    board.value[i] = "X";
    let res = checkWin(board.value);
    if (res) return endGame(res);

    statusMessage.value = "Robot thinking...";
    setTimeout(async () => {
        const spots = board.value.map((v, idx) => v === "" ? idx : null).filter(v => v !== null) as number[];
        if (spots.length > 0) {
            const robotChoice = spots[Math.floor(Math.random() * spots.length)] as number;
            if (onChainStrategy.value === 'every-move') await sendToGenLayer("record_move", [robotChoice, "O"]);
            board.value[robotChoice] = "O";
            let r = checkWin(board.value);
            if (r) endGame(r); else statusMessage.value = "Your turn!";
        }
    }, 600);
};

const checkWin = (b: string[]) => {
    const lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    for (let l of lines) {
        if (b[l[0]] && b[l[0]] === b[l[1]] && b[l[0]] === b[l[2]]) return b[l[0]];
    }
    return b.includes("") ? null : "Tie";
};

const endGame = (r: string) => {
    isGameOver.value = true;
    if (r === "X") { scores.value.player++; gameResultForChain.value = "win"; statusMessage.value = "You Won!"; }
    else if (r === "O") { scores.value.computer++; gameResultForChain.value = "loss"; statusMessage.value = "Robot Won!"; }
    else { scores.value.tie++; gameResultForChain.value = "tie"; statusMessage.value = "Tie!"; }
};

const resetBoard = () => {
    board.value = ["", "", "", "", "", "", "", "", ""];
    isGameOver.value = false;
    gameResultForChain.value = "";
    showFaucetLink.value = false;
    statusMessage.value = "Your turn!";
};

const openFaucet = () => {
  window.open('https://testnet-faucet.genlayer.foundation', '_blank');
};
</script>

<template>
  <div class="app">
    <div class="container">
      <h1 class="logo">GenLayer Tic-Tac-Toe</h1>

      <div v-if="!userAddress">
        <button class="btn main-btn" @click="connectWallet">Connect EVM Wallet</button>
        <p class="status-msg">{{ statusMessage }}</p>
      </div>

      <div v-else-if="!onChainStrategy" class="strategy-box">
        <h3>Choose On-Chain Strategy</h3>
        <div class="strategy-options">
          <button class="opt-btn" @click="onChainStrategy = 'every-move'">
            <strong>Hardcore</strong>
            <span>Every move recorded</span>
          </button>
          <button class="opt-btn" @click="onChainStrategy = 'end-only'">
            <strong>Casual</strong>
            <span>Only result recorded</span>
          </button>
        </div>
      </div>

      <div v-else>
        <div class="board">
          <div v-for="(v, i) in board" :key="i" class="cell" :class="v" @click="makeMove(i)">{{ v }}</div>
        </div>
        <div class="scores">
          <div class="score-card">PLAYER <span>{{ scores.player }}</span></div>
          <div class="score-card">TIE <span>{{ scores.tie }}</span></div>
          <div class="score-card">ROBOT <span>{{ scores.computer }}</span></div>
        </div>
        
        <p class="status-msg">{{ statusMessage }}</p>
        
        <button v-if="showFaucetLink" @click="openFaucet" class="faucet-btn">
          Get Testnet GEN (Faucet)
        </button>

        <div v-if="isGameOver" class="game-actions">
          <button v-if="onChainStrategy === 'end-only' && gameResultForChain" 
                  @click="sendToGenLayer('record_match', gameResultForChain)" class="save-btn">Save Result to Chain</button>
          <button class="reset-btn" @click="resetBoard">New Game</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app { min-height: 100vh; background: #14bdac; color: white; display: flex; justify-content: center; align-items: center; font-family: 'Inter', sans-serif; }
.container { width: 100%; max-width: 450px; text-align: center; padding: 20px; }
.logo { font-size: 2.5rem; margin-bottom: 2rem; font-weight: 800; }
.btn { background: white; color: #14bdac; border: none; padding: 16px 32px; border-radius: 50px; font-weight: bold; cursor: pointer; }
.strategy-options { display: flex; flex-direction: column; gap: 15px; }
.opt-btn { background: rgba(255,255,255,0.1); border: 2px solid white; color: white; padding: 15px; border-radius: 12px; cursor: pointer; display: flex; flex-direction: column; }
.board { display: grid; grid-template-columns: repeat(3, 1fr); margin: 30px auto; width: 300px; height: 300px; }
.cell { border: 4px solid white; display: flex; justify-content: center; align-items: center; font-size: 4rem; font-weight: bold; cursor: pointer; }
.cell:nth-child(1), .cell:nth-child(2), .cell:nth-child(3) { border-top: none; }
.cell:nth-child(7), .cell:nth-child(8), .cell:nth-child(9) { border-bottom: none; }
.cell:nth-child(1), .cell:nth-child(4), .cell:nth-child(7) { border-left: none; }
.cell:nth-child(3), .cell:nth-child(6), .cell:nth-child(9) { border-right: none; }
.cell.X { color: #545454; }
.scores { display: flex; justify-content: space-between; margin-top: 20px; background: rgba(0,0,0,0.05); padding: 15px; border-radius: 15px; }
.score-card { display: flex; flex-direction: column; font-size: 0.8rem; }
.status-msg { margin: 15px 0; font-weight: 600; }

.faucet-btn { background: #ffcc00; color: #000; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; margin-bottom: 10px; }
.game-actions { display: flex; flex-direction: column; gap: 10px; }
.save-btn { background: #2a2a2a; color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; }
.reset-btn { background: transparent; border: 1px solid white; color: white; padding: 8px; border-radius: 8px; cursor: pointer; }
</style>