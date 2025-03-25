from flask import redirect, abort, request, jsonify
from app import app
from app.utils.search_engine import ThreadedSearcher
from app.utils.validator import SecurityValidator
import os
import subprocess

@app.route('/launch/<filename>/<path:fallback_url>')
def launch(filename, fallback_url):
    try:
        
        searcher = ThreadedSearcher(timeout=5)
        exe_path = searcher.search(filename)

        if exe_path:
            # 使用非阻塞方式启动程序
            if os.name == 'nt':
                os.startfile(exe_path)
            else:
                subprocess.Popen([exe_path], shell=False)
            
            # 返回立即响应的空页面
            return '''
                <html>
                    <head>
                        <script>
                            // 立即关闭窗口（适用于弹窗场景）
                            window.close();
                            
                            // 或返回原页面（适用于非弹窗场景）
                            setTimeout(function(){
                                window.history.back();
                            }, 500); // 500ms延迟确保程序启动
                        </script>
                    </head>
                    <body></body>
                </html>
            ''', 200, {'Content-Type': 'text/html'}

        else:
            return redirect(fallback_url, code=302)

    except Exception as e:
        return jsonify(
            status="error",
            message=str(e)
        ), 500
    
#1.0
'''
@app.route('/launch/<filename>/<path:fallback_url>')
def launch(filename, fallback_url):
    # 安全验证
    if not SecurityValidator.validate_filename(filename):
        abort(400, "非法文件名格式")
    #whitelist
    
    if not SecurityValidator.check_whitelist(filename):
        abort(403, "未授权的可执行文件")
    

    # 搜索并执行
    searcher = ThreadedSearcher(timeout=5)
    exe_path = searcher.search(filename)

    if exe_path:
        try:
            # 启动应用程序
            if os.name == 'nt':
                os.startfile(exe_path)
            else:
                subprocess.Popen([exe_path], shell=False)
            
            # 返回自动返回脚本
            return f
                <script>
                    // 可选：添加启动成功提示
                    alert("成功启动 {filename}");
                    // 保持当前页面
                    window.location.href = document.referrer; 
                </script>
            , 200
        except Exception as e:
            return f"启动失败: {str(e)}", 500
    else:
        return redirect(fallback_url, code=302)

@app.errorhandler(500)
def handle_500(e):
    return "服务器内部错误，请检查日志", 500
'''