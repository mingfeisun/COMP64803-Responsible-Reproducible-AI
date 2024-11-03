import pickle
import numpy as np 

class headsandtails: 
    def __init__(self, heads=0, tails=0): 
        self.heads = heads 
        self.tails = tails 

    def iter_heads(self, n_heads):
        self.heads += n_heads 

    def iter_tails(self, n_tails): 
        self.tails += n_tails 

    def flip_coin(self, N):
        heads = np.random.binomial(N, 0.5)
        tails = N - heads 

        self.iter_heads(heads)
        self.iter_tails(tails)
     
game = headsandtails()
game.flip_coin(20)

# Here we save the game as a pickle byte stream
save_file = "sudo_files/sudo_game_scores.bin"
with open(save_file, 'wb') as f: 
    pickle.dump(game, f) 

# Reloading the saved pickle file saved to a different variable name
with open(save_file, 'rb') as f:
    saved_game = pickle.load(f)

# Showing that the type is the object that it was originally constructed as
# Essentially we have reconstructed the object using the pickle class
print(type(saved_game))
print(saved_game.__dict__)

# Now we can continue the game from our save file 
saved_game.flip_coin(10)
print(saved_game.__dict__)


pass 
# How about if we update and modify our game, because we reconstruct
# the object using pickle loads will it contain the new method and attributes?
class headsandtails: 
    def __init__(self, heads=0, tails=0, total_flips=0): 
        self.heads = heads 
        self.tails = tails 
        self.total_flips = total_flips

    def iter_heads(self, n_heads):
        self.heads += n_heads 

    def iter_tails(self, n_tails): 
        self.tails += n_tails 

    def count_flips(self): 
        self.total_flips = self.heads + self.tails
        return self.total_flips

    def flip_coin(self, N):
        heads = np.random.binomial(N, 0.5)
        tails = N - heads 

        self.iter_heads(heads)
        self.iter_tails(tails)

modified_game = headsandtails()
modified_game.flip_coin(20)
modified_game.count_flips

print(f'This is our modified game {modified_game.__dict__}')

print('Loading original game with new game class')
with open(save_file, 'rb') as f:
    saved_game = pickle.load(f)

print('Counting flips from our original game')
saved_game.count_flips

print(f'This is our original games state {saved_game.__dict__}') 
assert isinstance(saved_game, headsandtails)

# As we can see, the state of the old game means that even though it is constructed
# using our redefined class, it does not contain the methods and attributes
# we would expect! 

# To resolve this we can use the copyreg module
import copyreg 

# In this case, we define a rule for how to pickle the object attributes
# This is not that complicated we just pass the game state dict
def pickle_game(game_state): 
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs, )

# Here we define how to unpickle the object, as can be seen
# We ask it to call the headsandtails class that's instantiated 
# in the game
def unpickle_game_state(kwargs): 
    return headsandtails(**kwargs) 

copyreg.pickle(headsandtails, pickle_game)

with open(save_file, 'wb') as f: 
    pickle.dump(saved_game, f) 

with open(save_file, 'rb') as f:
    saved_game = pickle.load(f)

# Now when we save the game state, and reload it 
# it will be constructed with the new attributes
print(f'Original game {saved_game.__dict__}')


