import os

def check_paths(ENGINE_PATH: str, VIDEO_PATH: str, SRT_PATH: str) -> None:
    '''
    checks if the given paths exists. 
    Required: ENGINE_PATH, VIDEO_PATH, SRT_PATH
    '''
    # Required files
    for path in [ENGINE_PATH, VIDEO_PATH, SRT_PATH]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Required path does not exist: {path}")
        else:
            print(f"Path exists: {path}")
