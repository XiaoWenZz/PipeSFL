# 根据 csvs/no_corr 和 csvs/corr 生成对比图片
# 1. 读取 csvs/no_corr 和 csvs/corr
# 2. 生成对比图片
# 3. 保存到 output/images

import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_comparison(no_corr_file, corr_files, output_file):
    # 加载 no_corr 文件数据
    no_corr_data = pd.read_csv(no_corr_file, header=None).squeeze()
    # 确定是 client 还是 server 文件
    if 'Client' in no_corr_file:
        y_label = 'Train Acc'
        title_prefix = 'train_acc_ep'
    else:
        y_label = 'Test Acc'
        title_prefix = 'test_acc_ep'

    # 提取 ep, dp, dr 值
    ep_value = no_corr_file.split('_ep')[1].split('_')[0]
    dp_value = no_corr_file.split('_dp')[1].split('_')[0]
    dr_value = no_corr_file.split('_dr')[1].split('_')[0]

    epochs = range(len(no_corr_data))

    # 绘制 no_corr 数据
    plt.plot(epochs, no_corr_data, label='No Corr')

    # 绘制 corr 数据
    for corr_file in corr_files:
        corr_data = pd.read_csv(corr_file, header=None).squeeze()
        cr_value = corr_file.split('_cr')[1].split('_')[0]
        plt.plot(epochs, corr_data, label=f'Corr (cr={cr_value})')

    # 生成标题
    title = f'{title_prefix}{ep_value}_dp{dp_value}_dr{dr_value}'
    # 设置图表属性
    plt.xlabel('Epochs')
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)

    # 保存图表
    plt.savefig(output_file)
    plt.close()


# 定义文件夹路径
no_corr_folder = 'csvs/no_corr'
corr_folder = 'csvs/corr'
output_folder = 'imgs'

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取 no_corr 文件夹下的所有文件
no_corr_files = [f for f in os.listdir(no_corr_folder) if f.endswith('.csv')]

# 处理每个 no_corr 文件
for no_corr_file in no_corr_files:
    # 构建 no_corr 文件的完整路径
    no_corr_file_path = os.path.join(no_corr_folder, no_corr_file)
    # 提取 ep, dp, dr 值
    ep_value = no_corr_file.split('_ep')[1].split('_')[0]
    dp_value = no_corr_file.split('_dp')[1].split('_')[0]
    dr_value = no_corr_file.split('_dr')[1].split('_')[0]
    client_or_server = 'Client' if 'Client' in no_corr_file else 'Server'

    # 查找对应的 corr 文件
    corr_files = []
    corr_file_prefix = f'{client_or_server}_Acc_Corr_ep{ep_value}_dp{dp_value}_dr{dr_value}_cr'
    for f in os.listdir(corr_folder):
        if f.startswith(corr_file_prefix) and f.endswith('.csv'):
            corr_files.append(os.path.join(corr_folder, f))

    # 生成标题和文件名
    if client_or_server == 'Client':
        title = f'train_acc_ep{ep_value}_dp{dp_value}_dr{dr_value}'
    else:
        title = f'test_acc_ep{ep_value}_dp{dp_value}_dr{dr_value}'
    output_file = os.path.join(output_folder, f'{title}.png')

    # 绘制对比图
    plot_comparison(no_corr_file_path, corr_files, output_file)


