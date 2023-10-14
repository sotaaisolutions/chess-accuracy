import chess.pgn
import chess.engine
import pandas as pd
import traceback
import pgnhelper.app

eco = r'/home/rohit/Desktop/python3.11envs/venv311/pgnhelper-main/eco/eco.pgn'

def addopening(file):
    outputname ='out.pgn'
    a = pgnhelper.app.PgnHelper(
    'addeco',
    inpgnfn=file,
    outpgnfn= outputname,
    inecopgnfn=eco)
    a.start()
    return outputname


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
        outputname = 'chess.csv'
        df.to_csv('chess.csv')
        return outputname
    except:
        df = pd.DataFrame(gamedata)
        print(df)
        df.to_csv('chess.csv')
        traceback.print_exception()

def winfunc(row):
    if row['color'] == 'white':
        if row['Result'] == '1-0':
            return True
        else:
            return False
    if row['color'] == 'black':
        if row['Result'] == '0-1':
            return True
        else:
            return False


def losefunc(row):
    if row['color'] == 'white':
        if row['Result'] == '0-1':
            return True
        else:
            return False
    if row['color'] == 'black':
        if row['Result'] == '1-0':
            return True
        else:
            return False


def drawfunc(row):
    if row['Result'] == '1/2-1/2':
        return True
    else:
        return False


def calculations(file):
    df = pd.read_csv(file)
    whitecolumns = ['Opening','Date', 'White', 'Black','Result', 'WhiteElo', 'BlackElo', 'TimeControl', 'Termination', 'white_blunder', 'white_accuracy','no_white_moves']
    white = df [whitecolumns]
    newcols= ['Opening','Date', 'Player', 'Opponent','Result', 'PlayerElo', 'OpponentElo', 'TimeControl', 'Termination', 'blunder', 'accuracy','no__moves']
    white.columns = newcols
    white['color'] ='white'
    blackcolumns = ['Opening','Date', 'White', 'Black','Result', 'WhiteElo', 'BlackElo', 'TimeControl', 'Termination', 'black_blunder','black_accuracy','no_black_moves']
    black = df[blackcolumns]
    newcolumns = ['Opening','Date', 'Opponent', 'Player','Result', 'OpponentElo', 'PlayerElo', 'TimeControl', 'Termination', 'blunder', 'accuracy', 'no__moves']
    black.columns = newcolumns
    black['color'] = 'black'
    total =pd.concat([white,black])
    total['win'] = total.apply(lambda x: winfunc(x), axis =1)
    total['lose'] = total.apply(lambda x: losefunc(x), axis =1)
    total['draw'] = total.apply(lambda x: drawfunc(x), axis =1)
    counts = total.Player.value_counts()
    total = total[total.Player==counts.index[0]]
    return total

def calculate_performance_rating(df):
    K = 32  # K-factor. You may need to adjust this based on the specific context or tournament rules.
    total_score = 0
    total_expected_score = 0
    total_opponent_rating = 0
    
    for row in df.itertuples():
        opponent_rating = row.OpponentElo
        player_rating = row.PlayerElo
        total_opponent_rating += row.OpponentElo
        S = 0  # Score for a loss
        if row.win:
            S = 1  # Score for a win
        elif row.draw:
            S = 0.5  # Score for a draw
        
        total_score += S
        
        E = 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))  # Expected score
        total_expected_score += E
    
    num_games = len(df)
    R_avg = total_opponent_rating / num_games if num_games > 0 else 0
    performance_rating = R_avg + K * (total_score - total_expected_score)
    
    return performance_rating

def output_calculations(file):
    total = calculations(file)
    # print(total)
    output_dict = {}
    output_dict['total-winloss'] = total.groupby('Player').sum()[['win','lose','draw']].sort_values('win',ascending=False)
    output_dict['timecontrol-winloss'] = total.groupby('TimeControl').sum()[['win','lose','draw']].sort_values('win',ascending=False)
    output_dict['color-winloss'] = total.groupby('color').sum()[['win','lose','draw']].sort_values('win',ascending=False)
    table = total.groupby('Player').sum()[['no__moves','blunder']]
    table['acc'] = 1-table.blunder/table.no__moves
    output_dict['total-accuracy'] = table.copy()
    table =total.groupby('TimeControl').sum()[['no__moves','blunder']]
    table['acc'] = 1-table.blunder/table.no__moves
    output_dict['tc-accuracy']= table.copy()
    table = total.groupby('color').sum()[['no__moves','blunder']]
    table['acc'] = 1-table.blunder/table.no__moves
    output_dict['color-accuracy']= table.copy()
    output_dict['opening-winloss'] = total.groupby(['color','Opening']).sum()[['win','lose','draw']].sort_values('win',ascending=False)
    output_dict['date-winloss'] = total.groupby(['Date']).sum()[['win','lose','draw']]
    # print(output_dict)
    with pd.ExcelWriter("output.xlsx") as writer:
        for key in output_dict:
            output_dict[key].to_excel(writer, sheet_name=key, index=True)







