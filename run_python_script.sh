#!/bin/bash

# 获取用户输入的用户名
read -r -p "请输入校园网账号(目前仅支持CMCC):" user_account
# 获取用户输入的密码（-s参数表示不回显密码）
read -r -s -p "请输入校园网密码:" user_password
# 获取当前用户和用户组
current_user=$(whoami)
current_group=$(id -gn)
# 指定Python脚本的绝对路径
python_script_path=$(readlink -f "main.py")


# 创建Systemd服务配置文件，并传递用户名和密码给Python脚本
cat <<EOF > /etc/systemd/system/NJUPTWlanAutoLogin.service
[Unit]
Description=NJUPT Wlan Auto Login

[Service]
Type=simple
ExecStart=/usr/bin/python3 $python_script_path "$user_account" "$user_password"
Restart=always
RestartSec=3
User=$current_user
Group=$current_group

[Install]
WantedBy=default.target
EOF

# 重新加载Systemd服务
systemctl daemon-reload
# 启用并启动服务
systemctl enable NJUPTWlanAutoLogin.service
systemctl start NJUPTWlanAutoLogin.service

