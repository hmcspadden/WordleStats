import user_stats

user = "hunter"
#print(user_stats.check_stats(user))

stats = { #default stats
    "username" : user,
    "played" : "10",
    "average" : "0",
    "first" : "1",
    "second" : "2",
    "third" : "3",
    "fourth" : "1",
    "fifth" : "1",
    "sixth": "1",
    "failed" : "1"
}

user_stats.update_stats(user, stats)
print(user_stats.check_stats(user))
print(user_stats.get_played(user))