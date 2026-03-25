# coding=utf-8
# @Time    : 2026/3/23 13:48
# @Software: PyCharm
import json
import os
import sys
from typing import Optional, List

import paramiko


class JavaProjectDeployer:
    """Java 项目自动部署工具（跳过打包，直接部署指定JAR包）"""

    def __init__(
            self,
            # 本地配置 - 固定JAR包路径
            local_jar_path: str,
            # 远程服务器配置
            remote_host: str,
            remote_port: int,
            remote_user: str,
            remote_password: Optional[str],
            remote_ssh_key: Optional[str],
            remote_target_dir: str,
            # Java 进程配置
            jar_file_name: str,
            execute_commands: List[str]
    ):
        # 本地JAR包配置
        self.local_jar_path = local_jar_path
        self.jar_file_name = jar_file_name
        # 远程服务器配置
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.remote_user = remote_user
        self.remote_password = remote_password
        self.remote_ssh_key = remote_ssh_key
        self.remote_target_dir = remote_target_dir
        self.remote_jar_path = f"{remote_target_dir}/{jar_file_name}"
        # 新增：待执行命令
        self.execute_commands = execute_commands
        # SSH 客户端
        self.ssh_client = None

    def check_local_jar_exists(self) -> bool:
        """检查本地JAR文件是否存在，不存在则终止程序"""
        print(f"\n=== 检查本地JAR文件是否存在 ===")
        if os.path.exists(self.local_jar_path):
            print(f"✅ 本地JAR文件存在: {self.local_jar_path}")
            return True
        else:
            print(f"❌ 错误：本地JAR文件不存在 - {self.local_jar_path}")
            print("程序终止！")
            exit(1)  # 直接终止程序

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

    def stop_remote_jar_process(self) -> bool:
        """远程服务器停止指定JAR包进程（单行命令直接kill相关进程）"""
        if not self.ssh_client:
            print("❌ 错误：未建立 SSH 连接")
            return False

        print(f"\n=== 停止远程服务器上的 {self.jar_file_name} 进程 ===")
        try:
            # 压缩为单行命令：直接查找并kill相关进程
            stop_cmd = f"PID=$(ps -ef | grep java | grep {self.jar_file_name} | grep -v grep | awk '{{print $2}}') && [ -n \"$PID\" ] && (kill -9 $PID && sleep 2) || true"

            success, stdout, stderr = self.execute_remote_command(stop_cmd)

            if success:
                print(f"进程检查/停止命令执行成功")
                return True
            else:
                print(f"❌ 执行停止进程命令失败: {stderr}")
                return False

        except Exception as e:
            print(f"❌ 停止进程异常: {str(e)}")
            return False

    def start_remote_jar_process(self) -> bool:
        """远程服务器执行配置中的待执行命令数组"""
        if not self.ssh_client:
            print("❌ 错误：未建立 SSH 连接")
            return False

        print(f"\n=== 执行远程服务器待执行命令 ===")
        if not self.execute_commands:
            print("⚠️ 未配置待执行命令，跳过执行")
            return True

        try:
            # 把所有命令用 \n 拼接成 1 条完整命令
            full_command = "\n".join(self.execute_commands)
            # 一次执行所有命令
            success, stdout, stderr = self.execute_remote_command(full_command)
            if success:
                if stdout:
                    print(f"✅ 所有命令执行完成，输出：\n{stdout.strip()}")
                else:
                    print("✅ 所有命令执行成功（无输出）")
                return True
            else:
                print(f"❌ 命令执行失败: {stderr}")
                return False
        except Exception as e:
            print(f"❌ 执行待执行命令异常: {str(e)}")
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

    def upload_jar(self) -> bool:
        """上传 JAR 文件到远程服务器指定目录"""
        if not self.ssh_client:
            print("❌ 错误：未建立 SSH 连接")
            return False

        print(f"\n=== 上传 JAR 文件到 {self.remote_host}:{self.remote_target_dir} ===")
        try:
            # 创建 SFTP 客户端
            sftp = self.ssh_client.open_sftp()

            # 上传文件
            sftp.put(self.local_jar_path, self.remote_jar_path)
            sftp.close()

            print(f"✅ JAR 文件上传成功！")
            print(f"本地路径: {self.local_jar_path}")
            print(f"远程路径: {self.remote_jar_path}")
            return True

        except Exception as e:
            print(f"❌ 文件上传失败: {str(e)}")
            return False

    def close_ssh(self):
        """关闭 SSH 连接"""
        if self.ssh_client:
            self.ssh_client.close()
            print(f"\n✅ SSH 连接已关闭")

    def deploy(self) -> bool:
        """完整部署流程"""
        try:
            # 1. 检查本地JAR文件是否存在（不存在直接终止）
            self.check_local_jar_exists()

            # 2. 建立 SSH 连接
            if not self.connect_ssh():
                return False

            # 3. 停止远程服务器上的指定进程
            if not self.stop_remote_jar_process():
                self.close_ssh()
                return False

            # 4. 上传 JAR 文件
            if not self.upload_jar():
                self.close_ssh()
                return False

            # 5. 执行待执行命令
            if not self.start_remote_jar_process():
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
            "local_jar_path", "remote_host", "remote_port", "remote_user",
            "remote_target_dir", "jar_file_name",
            "execute_commands"  # 新增：校验待执行命令配置
        ]
        for field in required_fields:
            if field not in config:
                print(f"❌ 错误：JSON配置文件缺少必要参数 - {field}")
                sys.exit(1)

        # 校验execute_commands是数组类型
        if not isinstance(config["execute_commands"], list):
            print(f"❌ 错误：execute_commands 必须是数组类型")
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
        print("python 自动部署jar包.py <json_config_file_path>")
        print("示例：python 自动部署jar包.py deploy_config.json")
        sys.exit(1)

    # 获取JSON配置文件路径并加载配置
    json_config_path = sys.argv[1]
    config = load_config_from_json(json_config_path)

    # 创建部署器并执行部署
    deployer = JavaProjectDeployer(
        local_jar_path=config["local_jar_path"],
        remote_host=config["remote_host"],
        remote_port=config["remote_port"],
        remote_user=config["remote_user"],
        remote_password=config.get("remote_password"),  # 可选参数
        remote_ssh_key=config.get("remote_ssh_key"),  # 可选参数
        remote_target_dir=config["remote_target_dir"],
        jar_file_name=config["jar_file_name"],
        execute_commands=config["execute_commands"]  # 新增：传入待执行命令
    )
    if deployer.deploy():
        print("\n🎉 整体部署流程执行成功！")
    else:
        print("\n❌ 整体部署流程执行失败！")
        exit(1)
