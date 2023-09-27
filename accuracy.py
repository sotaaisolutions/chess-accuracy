import chess.pgn
import chess.engine
import pandas as pd
import traceback


def accuracy(file, stockfish, blunder_threshold = -100,analysis_time = 0.1):
    gamedata = []
    try:
        with open(file) as pgn_file:
            
            game = chess.pgn.read_game(pgn_file)

            
            
            while game:
                
                with chess.engine.SimpleEngine.popen_uci(stockfish) as engine:
                    
                    board = game.board()
                    i = 1
                    white_evals= []
                    black_evals = []

                    
                    for move in game.mainline_moves():
                        engine.configure({"Contempt": 0})
                        
                        board.push(move)
                        

                        
                        fen_str = board.fen()
                        # print(fen_str)  
                        board = chess.Board(fen_str)

                        
                        info = engine.analyse(board, chess.engine.Limit(time=analysis_time))

                        
                        evaluation = info["score"].relative.score(mate_score=10000)
                        # print("Evaluation:", evaluation)
                        if i % 2 == 1:
                            black_evals.append(evaluation)
                        else:
                            white_evals.append(evaluation)
                        i = i + 1
                evals_white_perspective =  [-1*(black_evals[i//2]) if i % 2 == 0 else white_evals[i // 2] for i in range(len(white_evals)+len(black_evals)) ]
                
                blunder_count = 0
                game_dict = dict(game.headers)
                no_white_moves = 0
                for i in range(1, len(evals_white_perspective)):

                    if evals_white_perspective[i-1]>-500 and evals_white_perspective[i-1]<500:
                        if i % 2 == 0:
                            no_white_moves = no_white_moves +1
                        if evals_white_perspective[i] - evals_white_perspective[i - 1] < blunder_threshold:
                        
                            blunder_count += 1
                            # print(evals_white_perspective[i],evals_white_perspective[i - 1] )

                
                game_dict['white_blunder'] = blunder_count
                
                if len(white_evals)>0:
                    game_dict['white_accuracy'] = 1-blunder_count/no_white_moves
                
                blunder_count = 0
                no_black_moves = 0
                for i in range(1, len(evals_white_perspective)):
                    if evals_white_perspective[i-1]>-500 and evals_white_perspective[i-1]<500:
                        if i % 2 == 1:
                            no_black_moves  = no_black_moves +1
                        if evals_white_perspective[i] - evals_white_perspective[i - 1] > -blunder_threshold:
                        
                            blunder_count += 1
                            # print(evals_white_perspective[i],evals_white_perspective[i - 1] )
                
                if len(black_evals)>0:
                    game_dict['black_accuracy'] = 1-blunder_count/no_black_moves
                game_dict['black_blunder']= blunder_count
                game_dict['no_black_moves'] = no_black_moves
                game_dict['no_white_moves'] = no_white_moves
                gamedata.append(game_dict)
                print(game_dict)
                
                game = chess.pgn.read_game(pgn_file)

        df = pd.DataFrame(gamedata)
        print(df)
        df.to_csv('chess.csv')
    except:
        df = pd.DataFrame(gamedata)
        print(df)
        df.to_csv('chess.csv')
        traceback.print_exception()
