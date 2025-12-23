# Dual-Robot Autonomous Chess Player (RoboDK + Python + Stockfish)

**Live demo:** https://youtu.be/VXk2BCppK2I

This repository contains a fully functional **autonomous chess playing system** simulated in RoboDK. Two collaborative robots play a complete chess game against each other using a standard chess engine (Stockfish) and Python motion logic. The system handles piece detection, pick-and-place operations, captures, and turn-based play — all in simulation.

---

## Overview

This project integrates:

- **RoboDK** for robot simulation and motion execution  
- **Python** for control logic and robot sequencing  
- **Stockfish** (UCI engine) for chess intelligence  
- **python-chess** for move validation and game state management  

The result is a system where two robot arms play a full game of chess without human intervention, using geometric pose calculations and inverse kinematics instead of physics simulation.

---

## Demo

Watch the simulated chess game in action:  
▶️ https://youtu.be/VXk2BCppK2I

---

## Features

- Dual robot setup with independent workspaces  
- Chessboard square-to-pose mapping and robot motion planning  
- Real-time capture detection and piece removal  
- Engine-driven game logic (Stockfish)  
- Safe intermediate moves and collision-aware motion sequencing

---

## Requirements

Before running this project:

1. **RoboDK** (simulation environment)
2. Python 3.7+
3. RoboDK Python API installed
4. Stockfish engine executable on your system
5. `python-chess` library

## How It Works

1. The game loop requests moves from Stockfish via UCI
2. python-chess interprets the move and identifies captures
3. Robot executes pick/place motion for each move
4. Captured pieces are moved to designated graveyard zones
5. The game continues until checkmate/stalemate

## Limitations

1. This is a simulation-only project (RoboDK)
2. No advanced collision avoidance beyond basic motion logic
3. Assumes ideal piece detection within threshold

## About the Author
Mechanical Engineering Student
