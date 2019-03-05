##
# Simulating a game of connect 4 with agents
##

import APIConnectFour as C4
import Agent as Ag

print('Four-In-A-Row')
print()

## Default board dimensions (also need to change the API) ##
BOARDWIDTH = 7
BOARDHEIGHT = 6

## Game Setting ##
# 'Human_v_Agent' or 'Agent_v_Computer'
GameType = 'Human_v_Agent'


## Agent Settings ##
# How many iteration of MCTS to run per move
MCTS_ITERS = 500
# Verbosity of agent and game states
VERBOSITY = True
# Default tile when playing against computer
DE_AGENT_TILE = 'O'


###
# Agent against the default AI of the game
###
def agentDefaultPlay(verbose=True):
    # Initialize tiles of default play
    humanTile = DE_AGENT_TILE
    computerTile = 'X' if DE_AGENT_TILE=='O' else 'O'

    # Initialize game
    mainBoard = C4.getNewBoard()
    turn = 'human' if DE_AGENT_TILE=='O' else 'computer'

    # Initialize Agent
    Agent = Ag.CFAgent(humanTile, computerTile, BOARDWIDTH, BOARDHEIGHT, mctsIters=MCTS_ITERS)

    ## Start game ##
    while True:
        if turn == 'human':
            if verbose:
                C4.drawBoard(mainBoard)
            move = Agent.decideMove(mainBoard, verbose=verbose)
            C4.makeMove(mainBoard, humanTile, move)
            if C4.isWinner(mainBoard, humanTile):
                winner = 'agent'
                break
            turn = 'computer'
        else:
            if verbose:
                C4.drawBoard(mainBoard)
                print('The computer is thinking...')
            move = C4.getComputerMove(mainBoard, computerTile)
            C4.makeMove(mainBoard, computerTile, move)
            if C4.isWinner(mainBoard, computerTile):
                winner = 'computer'
                break
            turn = 'human'

        if C4.isBoardFull(mainBoard):
            winner = 'tie'
            break

    ## Game outcome ##
    C4.drawBoard(mainBoard)
    print('Winner is: %s' % winner)


###
# Agent against human play
###
def agentHumanPlay(verbose=True):
    ## Initialization ##
    # Decide who to go first
    humanTile, computerTile = C4.enterHumanTile()
    turn = 'human' if humanTile=='O' else 'computer'
    print('The %s player will go first.' % (turn))
    mainBoard = C4.getNewBoard()

    # Initialize agent
    Agent = Ag.CFAgent(computerTile, humanTile, BOARDWIDTH, BOARDHEIGHT, mctsIters=MCTS_ITERS)

    ## Start game ##
    while True:
        if turn == 'human':
            C4.drawBoard(mainBoard)
            move = C4.getHumanMove(mainBoard)
            C4.makeMove(mainBoard, humanTile, move)
            if C4.isWinner(mainBoard, humanTile):
                winner = 'human'
                break
            turn = 'computer'
        else:
            C4.drawBoard(mainBoard)
            print('The agent is thinking...')
            move = Agent.decideMove(mainBoard, verbose=verbose)
            C4.makeMove(mainBoard, computerTile, move)
            if C4.isWinner(mainBoard, computerTile):
                winner = 'agent'
                break
            turn = 'human'

        if C4.isBoardFull(mainBoard):
            winner = 'tie'
            break

    ## Game outcome ##
    C4.drawBoard(mainBoard)
    print('Winner is: %s' % winner)




def main():
    # Human against agent
    if GameType == 'Human_v_Agent':
        agentHumanPlay(verbose=VERBOSITY)
    elif GameType == 'Agent_v_Computer':
        agentDefaultPlay(verbose=VERBOSITY)


if __name__ == '__main__':
    main()
