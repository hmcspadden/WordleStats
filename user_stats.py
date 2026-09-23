import json
import os

#gets stats of user if it exists, creates new stats otherwise
def get_stats(user:str)-> dict:

    if os.path.exists(filepath(user)):
        with open(filepath(user), "r") as f: #read user stats
            stats = json.load(f)
    else:
        #create_stats(user) #create new stat sheet if one does not exist
        #stats = get_stats(user)
        stats = "No Stats Logged."

    return stats


#writes the stats of the user to the corresponding .json file
def write_stats(user: str, stats: dict):

    with open(filepath(user), "w") as f:
        json.dump(stats, f)


#turns the stats .jsons into prettier text
def check_stats(user: str)-> str:

    stats = get_stats(user)
    
    pretty_stats = "" #create readable str for return
    for stat in stats:
        pretty_stats += f'{stat.title()} {stats[stat]}\n'
    
    return pretty_stats


#creates new stats
def default_stats()-> dict:
    stats = { #default stats
        "played:" : "0",
        "average:" : "0",
        "1/6:" : "0",
        "2/6:" : "0",
        "3/6:" : "0",
        "4/6:" : "0",
        "5/6:" : "0",
        "6/6:": "0",
        "X/6:" : "0"
    }
    return stats


#creates a new stat sheet if one does not already exist
def create_user(user: str):

    if os.path.exists(filepath(user)):
        return

    write_stats(user, default_stats())


#checks if user stat sheet already exists for external use   
def user_exists(user: str)-> bool:

    return os.path.exists(filepath(user))


#creates string for filepath of user
def filepath(user: str)-> str:

    return "./users/" + user + ".json"


#updates existing user stats
def update_stats(user: str, new_stats: dict):

    stats = get_stats(user)
    
    additive_stats = [
        "played:", "1/6:", "2/6:", "3/6:", "4/6:", "5/6:", 
        "6/6:", "X/6:"
    ]

    for stat in stats:
        if stat in additive_stats:
            num = int(stats[stat]) + int(new_stats[stat])
            stats[stat] = str(num)

    num_played = int(stats["played:"])
    total_guesses = 0

    for stat in stats: #calculates average guess
        if stat in additive_stats:
            total_guesses += int(stats[stat]) * additive_stats.index(stat)
    
    if int(stats["played:"]) > 0:
        stats["average:"] = str(total_guesses / num_played)
        
    write_stats(user, stats)


def get_played(user: str)-> int:
    stats = get_stats(user)
    return int(stats["played:"])
    
'''
def get_missed(user: str)-> int:
    stats - get_stats(user)
    return int(stats["missed"])
'''
