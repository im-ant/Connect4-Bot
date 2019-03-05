##
# The MCST agent
# References for algorithm overview:
#   http://mcts.ai/about/
#   https://towardsdatascience.com/monte-carlo-tree-search-158a917a8baa
##
import numpy as np
import random
import copy
import APIConnectFour as C4


class MctsTreeNode:
    # Attributes
    Board = None
    IsPlayerTurn = True
    Children = None
    TotalUtility = 0
    TotalVisits = 0

    def __init__(self, board, isPlayerTurn):
        self.IsPlayerTurn = isPlayerTurn
        self.Board = copy.deepcopy(board)



class CFAgent:
    # Attributes
    MyTile = None
    OpponentTile = None
    BoardWidth = 0
    boardHeight = 0

    # Initialize
    def __init__(self, myTile, oppoTile, boardWidth, boardHeight):
        self.MyTile = myTile
        self.OpponentTile = oppoTile
        self.BoardWidth = boardWidth
        self.boardHeight = boardHeight

    # Agent decides what move to play next given board position
    def decideMove(self, board):
        ## Initialize current search tree ##
        TreeRoot = MctsTreeNode(board, isPlayerTurn=True)

        ## Monte-Carlo Tree Search until budget runs out ##
        iters = 0
        iterMax = 300
        while(iters < iterMax):
            self.McTreeSeach(TreeRoot)
            iters += 1

        ## Select best move from current root node ##
        cUtils = [c.TotalUtility if c is not None else 0 for c in TreeRoot.Children ]
        cVisits = [c.TotalVisits if c is not None else 1 for c in TreeRoot.Children]
        cVals = [ float(u)/float(v) for u, v in zip(cUtils, cVisits)]

        # Return index of best move
        print("Agent move values:")
        print(cVals)
        return cVals.index(max(cVals))


    ##
    # Monte-Carlo Tree Search
    ##
    def McTreeSeach(self, node):
        # If leaf, Expand
        if node.Children is None:
            cUtility, cVisits = self.expandMCTree(node)
            return cUtility, cVisits

        # Select most promising children and recurse
        bestChildNode = self.getPromisingChild(node)
        cUtility, cVisits = self.McTreeSeach(bestChildNode)

        ## Back-propr to accumulate statistics ##
        node.TotalUtility += cUtility
        node.TotalVisits += cVisits

        return cUtility, cVisits



    ##
    # Given a leaf node, expand children
    ##
    def expandMCTree(self, curNode):
        # If terminal, return win, lose or tie with 1 visit
        if C4.isWinner(curNode.Board, self.MyTile):
            curNode.TotalUtility = 1
            curNode.TotalVisits = 1
            return curNode.TotalUtility, curNode.TotalVisits
        if C4.isWinner(curNode.Board, self.OpponentTile):
            curNode.TotalUtility = -1
            curNode.TotalVisits = 1
            return curNode.TotalUtility, curNode.TotalVisits
        if C4.isBoardFull(curNode.Board):
            curNode.TotalUtility = 0
            curNode.TotalVisits = 1
            return curNode.TotalUtility, curNode.TotalVisits

        # Initialize children for nodes
        curNode.Children = [None] * self.BoardWidth
        # What is the action tile of the current node?
        curTile = self.MyTile if curNode.IsPlayerTurn else self.OpponentTile
        # Iterate through possible moves from current node and rollout
        for moveIdx in range(len(curNode.Children)):
            # If move not valid, keep the move as None
            if not C4.isValidMove(curNode.Board, moveIdx):
                continue

            # If valid, construct the new board with move made
            dupeBoard = copy.deepcopy(curNode.Board)
            C4.makeMove(dupeBoard, curTile, moveIdx)
            curNode.Children[moveIdx] = MctsTreeNode(dupeBoard, not curNode.IsPlayerTurn)

            # Rollout simulated plays
            simUtility = self.rollout(copy.deepcopy(dupeBoard), not curNode.IsPlayerTurn)
            # Update statistics
            curNode.Children[moveIdx].TotalUtility += simUtility
            curNode.Children[moveIdx].TotalVisits += 1
            curNode.TotalUtility += simUtility
            curNode.TotalVisits += 1

        return curNode.TotalUtility, curNode.TotalVisits


    ##
    # Rollout to simulate the game from current node using Default Policy
    ##
    def rollout(self, board, isPlayerTurn):
        # If terminal, return state
        if C4.isWinner(board, self.MyTile):
            return 1
        if C4.isWinner(board, self.OpponentTile):
            return -1
        if C4.isBoardFull(board):
            return 0

        # Initialize current tile and random move
        curTile = self.MyTile if isPlayerTurn else self.OpponentTile
        allowableMoves = [mIdx for mIdx in range(self.BoardWidth) if C4.isValidMove(board, mIdx)]
        randMove = random.choice(allowableMoves)

        # Play move and recurse
        C4.makeMove(board, curTile, randMove)
        return self.rollout(board, not isPlayerTurn)


    ##
    # Use the Tree Policy to get the most promising children
    ##
    def getPromisingChild(self, node):
        # Allowable indeces
        validChildren = [c for c in node.Children if c is not None]

        ## Upper confidence tree evaluation ##
        # Exploration constant
        EXP_CONS = np.sqrt(2)

        # Initialize value for each valid children
        QArr = [0.0] * len(validChildren)
        # Compute value
        for i, c in enumerate(validChildren):
            # Compute value of going to this children
            Q_child = np.divide(c.TotalUtility, c.TotalVisits)
            # Compute exploration value
            unSqrtExp = np.divide( np.log(node.TotalVisits) , c.TotalVisits )
            # Compute the overall value
            QArr[i] = Q_child + np.multiply(EXP_CONS, np.sqrt(unSqrtExp))

        # Temp return
        #return random.choice(validChildren)

        # Return best value
        return validChildren[ np.argmax(QArr) ]
