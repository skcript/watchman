# COMMON FOR ALL FUNCTIONS DEFINED HERE
# Accepts path as input
# For create, destroy actions, this function is called with src path
# For move actions, this function is called twice for src and dest path

def ratelimit(path):
    "Ratelimits API calls by returning a unique string based on path"
    return path.split("/")[0]

def prevent(path):
    "Prevents API call from being made by returning a True or False"
    return False
