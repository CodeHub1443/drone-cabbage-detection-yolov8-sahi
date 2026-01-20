import os

def check_paths(ENGINE_PATH:str, VIDEO_PATH:str, SRT_PATH:str)->None:
    '''
    checks if the given paths exists
    '''

    for path in [ENGINE_PATH, VIDEO_PATH, SRT_PATH]:
        if not os.path.exists(path):
            print(f"Path does not exist: {path}")
            exit(1)
        else:
            print(f"Path exists: {path}")
