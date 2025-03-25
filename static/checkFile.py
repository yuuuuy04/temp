import os
from pathlib import Path
from datetime import datetime

def check_file_in_data(file_name, select):
    """
    检查上级目录中的 data 文件夹是否存在指定文件，并根据 select 参数返回相关信息。
    
    :param file_name: 要检查的文件名（包括扩展名）
    :param select: 操作模式 ('mytime' 或 'isexist')
    :return: 根据 select 参数返回相应信息
    """
    try:
        # 获取当前文件的绝对路径、所在目录及上一级目录
        current_file_path = Path(__file__).resolve()
        parent_dir = current_file_path.parent.parent
        # 构建 data 文件夹和目标文件的完整路径
        data_dir = parent_dir / 'data'
        target_file_path = data_dir / file_name
        
        # 检查 data 文件夹和目标文件是否存在
        if data_dir.exists() and target_file_path.exists():
            if select == 'mytime':
                stat_info = target_file_path.stat()
                creation_time = stat_info.st_birthtime if hasattr(stat_info, 'st_birthtime') else os.path.getctime(target_file_path)
                creation_time_readable = datetime.fromtimestamp(creation_time)
                current_time = datetime.now()
                delta = current_time - creation_time_readable
                return delta.days  # 返回天数差
            elif select == 'isexist':
                return 'exist'  # 文件存在标志
            else:
                raise ValueError("未知的选择方式")
        else:
            return 'notExist' if select == 'isexist' else 'notExist'  # 如果是 isexist 则返回False，否则返回None
    except Exception as e:
        print(f"发生错误: {e}")
        return e  # 发生错误时返回错误