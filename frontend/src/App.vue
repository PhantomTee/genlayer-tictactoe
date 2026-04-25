<script setup lang="ts">
import { ref } from 'vue'

const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS;
const board = ref(["", "", "", "", "", "", "", "", ""]);
const statusMessage = ref("Connected to Genlayer: " + contractAddress);

const makeMove = async (index: number) => {
    if (board.value[index] !== "") return;
    board.value[index] = "X"; 
    statusMessage.value = `Move made at square ${index}! Waiting for O...`;
};
</script>

<template>
  <div class="game-container">
    <h1>Genlayer Tic-Tac-Toe</h1>
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
.status { 
  margin-bottom: 30px; 
  font-size: 1.2rem; 
  color: #42b883; 
}
.board { 
  display: grid; 
  grid-template-columns: repeat(3, 120px); 
  grid-gap: 10px; 
  background-color: #2a2a2a; 
  padding: 10px; 
  border-radius: 12px; 
}
.cell { 
  width: 120px; 
  height: 120px; 
  background-color: #1a1a1a; 
  display: flex; 
  justify-content: center; 
  align-items: center; 
  font-size: 4rem; 
  font-weight: bold; 
  cursor: pointer; 
  border-radius: 8px; 
  transition: background-color 0.2s; 
}
.cell:hover { 
  background-color: #3a3a3a; 
}
</style>