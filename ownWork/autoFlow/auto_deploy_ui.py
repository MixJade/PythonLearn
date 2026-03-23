# coding=utf-8
# @Time    : 2026/3/23 13:48
# @Software: PyCharm
import json
import os
import sys
from typing import Optional

import paramiko


class FrontendProjectDeployer:
    """前端项目自动部署工具（打包文件夹并部署到远程服务器）"""

    def __init__(
            self,
            # 本地配置
            local_zip_path: str,
            local_dir_name: str,
            # 远程服务器配置
            remote_host: str,
            remote_port: int,
            remote_user: str,
            remote_password: Optional[str],
            remote_ssh_key: Optional[str],
            remote_target_dir: str
    ):
        # 本地配置
        self.local_zip_path = local_zip_path
        # 远程服务器配置
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.remote_user = remote_user
        self.remote_password = remote_password
        self.remote_ssh_key = remote_ssh_key
        self.remote_target_dir = remote_target_dir
        self.remote_zip_path = f"{remote_target_dir}/{local_dir_name}.zip"
        self.remote_unzip_dir = f"{remote_target_dir}/{local_dir_name}"
        # SSH 客户端
        self.ssh_client = None

    def check_local_zip_exists(self) -> bool:
        """检查本地文件夹是否存在，不存在则终止程序"""
        print(f"\n=== 检查本地文件夹是否存在 ===")
        if os.path.exists(self.local_zip_path):
            print(f"✅ 本地Zip文件存在: {self.local_zip_path}")
            return True
        else:
            print(f"❌ 错误：本地Zip文件不存在 - {self.local_zip_path}")
            print("程序终止！")
            exit(1)

    def connect_ssh(self) -> bool:
        """建立 SSH 连接"""
        print(f"\n=== 连接远程服务器 {self.remote_host} ===")
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 支持密码或 SSH 密钥登录
            if self.remote_ssh_key:
                private_key = paramiko.RSAKey.from_private_key_file(self.remote_ssh_key)
                self.ssh_client.connect(
                    hostname=self.remote_host,
                    port=self.remote_port,
                    username=self.remote_user,
                    pkey=private_key,
                    timeout=10
                )
            else:
                self.ssh_client.connect(
                    hostname=self.remote_host,
                    port=self.remote_port,
                    username=self.remote_user,
                    password=self.remote_password,
                    timeout=10
                )

            print(f"✅ SSH 连接成功！")
            return True

        except Exception as e:
            print(f"❌ SSH 连接失败: {str(e)}")
            self.ssh_client = None
            return False

    def execute_remote_command(self, command: str, timeout: int = 30) -> tuple[bool, str, str]:
        """执行远程命令"""
        print(command)
        if not self.ssh_client:
            return False, "", "未建立 SSH 连接"
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=timeout)
            stdout_str = stdout.read().decode('utf-8', errors='ignore')
            stderr_str = stderr.read().decode('utf-8', errors='ignore')

            # 检查命令执行状态
            exit_status = stdout.channel.recv_exit_status()
            success = exit_status == 0

            return success, stdout_str, stderr_str

        except Exception as e:
            return False, "", f"命令执行异常: {str(e)}"

    def clean_remote_files(self) -> bool:
        """清理远程服务器目标目录下的旧文件"""
        if not self.ssh_client:
            print("❌ 错误：未建立 SSH 连接")
            return False

        print(f"\n=== 清理远程服务器旧文件 ===")
        try:
            # 删除旧的文件夹和zip包
            clean_commands = [
                f"rm -rf {self.remote_unzip_dir}",
                f"rm -rf {self.remote_zip_path}"
            ]

            for cmd in clean_commands:
                success, stdout, stderr = self.execute_remote_command(cmd)
                if success:
                    print(f"执行命令成功: {cmd}")
                    if stdout:
                        print(f"输出: {stdout.strip()}")
                else:
                    print(f"⚠️ 执行命令可能失败: {cmd}")
                    print(f"错误信息: {stderr.strip()}")

            return True

        except Exception as e:
            print(f"❌ 清理远程文件异常: {str(e)}")
            return False

    def upload_zip(self) -> bool:
        """上传 ZIP 文件到远程服务器指定目录"""
        if not self.ssh_client:
            print("❌ 错误：未建立 SSH 连接")
            return False

        print(f"\n=== 上传 ZIP 文件到 {self.remote_host}:{self.remote_target_dir} ===")
        try:
            # 创建 SFTP 客户端
            sftp = self.ssh_client.open_sftp()

            # 上传文件
            sftp.put(self.local_zip_path, self.remote_zip_path)
            sftp.close()

            print(f"✅ ZIP 文件上传成功！")
            print(f"本地路径: {self.local_zip_path}")
            print(f"远程路径: {self.remote_zip_path}")
            return True

        except Exception as e:
            print(f"❌ 文件上传失败: {str(e)}")
            return False

    def unzip_remote_file(self) -> bool:
        """远程服务器解压ZIP包"""
        if not self.ssh_client:
            print("❌ 错误：未建立 SSH 连接")
            return False

        print(f"\n=== 解压远程服务器上的 ZIP 文件 ===")
        try:
            unzip_cmd = f"unzip -o {self.remote_zip_path} -d {self.remote_target_dir}"
            success, stdout, stderr = self.execute_remote_command(unzip_cmd, timeout=60)

            if success:
                print(f"✅ 解压命令执行成功！")
                print(f"解压输出: {stdout.strip()}")
                return True
            else:
                print(f"❌ 执行解压命令失败: {stderr.strip()}")
                return False

        except Exception as e:
            print(f"❌ 解压文件异常: {str(e)}")
            return False

    def close_ssh(self):
        """关闭 SSH 连接"""
        if self.ssh_client:
            self.ssh_client.close()
            print(f"\n✅ SSH 连接已关闭")

    def deploy(self) -> bool:
        """完整部署流程"""
        try:
            # 1. 检查本地zip是否存在（不存在直接终止）
            self.check_local_zip_exists()

            # 2. 建立 SSH 连接
            if not self.connect_ssh():
                return False

            # 3. 清理远程服务器旧文件
            if not self.clean_remote_files():
                self.close_ssh()
                return False

            # 4. 上传 ZIP 文件
            if not self.upload_zip():
                self.close_ssh()
                return False

            # 5. 解压远程ZIP文件
            if not self.unzip_remote_file():
                self.close_ssh()
                return False

            print(f"\n=== 部署完成！===")
            return True

        finally:
            # 确保关闭连接
            self.close_ssh()


def load_config_from_json(json_path):
    """从JSON文件加载配置参数"""
    try:
        # 检查JSON文件是否存在
        if not os.path.exists(json_path):
            print(f"❌ 错误：JSON配置文件不存在 - {json_path}")
            sys.exit(1)

        # 读取并解析JSON文件
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 校验必要参数是否存在
        required_fields = [
            "local_zip_path", "local_dir_name", "remote_host", "remote_port",
            "remote_user", "remote_target_dir"
        ]
        for field in required_fields:
            if field not in config:
                print(f"❌ 错误：JSON配置文件缺少必要参数 - {field}")
                sys.exit(1)

        return config
    except json.JSONDecodeError as e:
        print(f"❌ 错误：JSON配置文件格式错误 - {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误：加载JSON配置文件失败 - {str(e)}")
        sys.exit(1)


# ==================== 主程序 ====================
if __name__ == "__main__":
    # 检查命令行参数数量（只需要传入JSON文件路径）
    if len(sys.argv) != 2:
        print("❌ 参数错误！正确用法：")
        print("python 自动部署前端项目.py <json_config_file_path>")
        print("示例：python 自动部署前端项目.py deploy_config.json")
        sys.exit(1)

    # 获取JSON配置文件路径并加载配置
    json_config_path = sys.argv[1]
    config = load_config_from_json(json_config_path)

    # 创建部署器并执行部署
    deployer = FrontendProjectDeployer(
        local_zip_path=config["local_zip_path"],
        local_dir_name=config["local_dir_name"],
        remote_host=config["remote_host"],
        remote_port=config["remote_port"],
        remote_user=config["remote_user"],
        remote_password=config.get("remote_password"),  # 可选参数
        remote_ssh_key=config.get("remote_ssh_key"),  # 可选参数
        remote_target_dir=config["remote_target_dir"]
    )

    if deployer.deploy():
        print("\n🎉 整体部署流程执行成功！")
    else:
        print("\n❌ 整体部署流程执行失败！")
        exit(1)
