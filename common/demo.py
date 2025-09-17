import pandas as pd

def add_https_to_links(file_path, link_column, output_file):
    """
    读取表格中的链接列，为缺少https前缀的链接添加https://
    
    参数:
        file_path: 输入表格文件路径（支持xlsx, csv等格式）
        link_column: 包含链接的列名
        output_file: 处理后的文件保存路径
    """
    # 根据文件后缀选择合适的读取方法
    if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("不支持的文件格式，请使用xlsx、xls或csv格式")
    
    # 检查链接列是否存在
    if link_column not in df.columns:
        raise ValueError(f"表格中未找到名为 '{link_column}' 的列")
    
    # 定义函数：为链接添加https://前缀（如果缺少）
    def add_https(link):
        # 处理空值
        if pd.isna(link):
            return link
        
        # 转换为字符串
        link_str = str(link).strip()
        
        # 检查是否已包含http或https前缀
        if link_str.startswith(('http://', 'https://')):
            return link_str
        # 检查是否是相对路径或IP地址，添加https://
        else:
            return f'https://{link_str}'
    
    # 应用函数处理链接列
    df[link_column] = df[link_column].apply(add_https)
    
    # 保存处理后的表格
    if output_file.endswith('.xlsx') or output_file.endswith('.xls'):
        df.to_excel(output_file, index=False)
    elif output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    else:
        raise ValueError("不支持的输出文件格式，请使用xlsx、xls或csv格式")
    
    print(f"处理完成！共处理 {len(df)} 条记录，结果已保存至 {output_file}")
    return df

if __name__ == "__main__":
    # 示例用法
    input_file = "/Users/didi/Downloads/内蒙古机房映射.xlsx"    # 输入表格文件
    link_col = "B"            # 链接所在的列名
    output_file = "processed_links.xlsx"  # 输出文件
    
    # 执行处理
    result_df = add_https_to_links(input_file, link_col, output_file)
    
    # 显示前5条处理结果
    print("\n处理后的前5条链接：")
    print(result_df[link_col].head())
