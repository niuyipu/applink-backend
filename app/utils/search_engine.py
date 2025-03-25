import os
import threading
import queue
import platform
import time
from pathlib import Path

class ThreadedSearcher:
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.found = False
        self.result_path = None
        self.lock = threading.Lock()
        self.search_queue = queue.Queue()
        self.threads = []

    def _search_worker(self, target_file):
        while not self.found and not self.search_queue.empty():
            try:
                dir_path = self.search_queue.get_nowait()
            except queue.Empty:
                return

            try:
                for entry in os.scandir(dir_path):
                    if self.found:
                        return
                    if entry.is_file() and entry.name.lower() == target_file:
                        with self.lock:
                            self.found = True
                            self.result_path = entry.path
                        return
                    elif entry.is_dir():
                        self.search_queue.put(entry.path)
            except (PermissionError, FileNotFoundError):
                continue

    def search(self, filename):
        """线程安全搜索可执行文件"""
        start_time = time.time()
        target_file = filename.lower()
        
        # 构建安全的搜索路径
        search_roots = self._get_search_roots()
        valid_roots = [root for root in search_roots if root and os.path.exists(root)]
        
        if not valid_roots:
            return None

        # 初始化队列
        for root in valid_roots:
            self.search_queue.put(root)

        # 启动线程
        thread_count = min(os.cpu_count() * 2, 8)  # 最多8个线程
        self.threads = [
            threading.Thread(target=self._search_worker, args=(target_file,))
            for _ in range(thread_count)
        ]
        
        for thread in self.threads:
            thread.start()

        # 等待结果
        while time.time() - start_time < self.timeout:
            if self.found:
                break
            time.sleep(0.1)

        # 清理
        self.found = True
        for thread in self.threads:
            thread.join()

        return self.result_path

    def _get_search_roots(self):
        """获取平台特定的搜索根目录"""
        if platform.system() == 'Windows':
            return list(set([
                os.environ.get('ProgramFiles', 'C:\\Program Files'),
                os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Roaming'),
                os.environ.get('SystemRoot', 'C:\\Windows'),
                'C:\\',
                os.path.expanduser('~')
            ]))
        else:
            return [
                '/usr/bin',
                '/usr/local/bin',
                '/opt',
                os.path.expanduser('~/.local/bin'),
                os.path.expanduser('~/Applications')
            ]