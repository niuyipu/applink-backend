from pathlib import Path

class SecurityValidator:
    @staticmethod
    def validate_filename(filename):
        forbidden_chars = {'/', '\\', ':', '*', '?', '"', '<', '>', '|'}
        if any(char in filename for char in forbidden_chars):
            return False
        return filename.endswith('.exe')  # 仅限Windows可执行文件

    #@staticmethod
    '''
    def check_whitelist(filename):
        with open('allowed_executables.txt', 'r') as f:
            allowed = [line.strip().lower() for line in f.readlines()]
        return filename.lower() in allowed
    '''