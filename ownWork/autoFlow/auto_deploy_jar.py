# coding=utf-8
import json
import os
import sys
from typing import Optional, List
import paramiko


class JarDeployer:
    """JAR包部署工具：上传前执行命令 → 上传文件 → 上传后执行命令"""

    def __init__(
            self,
            # 远程服务器配置
            remote_host: str,
            remote_port: int,
            remote_user: str,
            remote_password: Optional[str],
            remote_ssh_key: Optional[str],
            # 上传前执行的命令
            pre_upload_commands: List[str],
            # 上传文件配置
            local_jar_path: str,
            remote_jar_path: str,
            # 上传后执行的命令
            post_upload_commands: List[str]
    ):
        # 本地配置
        self.local_jar_path = local_jar_path
        self.jar_file_name = os.path.basename(local_jar_path)  # 自动提取文件名
        # 远程配置
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.remote_user = remote_user
        self.remote_password = remote_password
        self.remote_ssh_key = remote_ssh_key
        self.remote_jar_path = remote_jar_path
        # 命令配置
        self.pre_upload_commands = pre_upload_commands or []
        self.post_upload_commands = post_upload_commands or []
        # SSH客户端
        self.ssh_client = None

    def check_local_jar(self) -> bool:
        """检查本地文件是否存在"""
        print(f"\n=== 检查本地文件 ===")
        if os.path.exists(self.local_jar_path):
            print(f"✅ 本地文件存在: {self.local_jar_path}")
            return True
        else:
            print(f"❌ 本地文件不存在: {self.local_jar_path}")
            sys.exit(1)

    def connect_ssh(self) -> bool:
        """建立SSH连接"""
        print(f"\n=== 连接远程服务器 {self.remote_host} ===")
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.remote_ssh_key:
                private_key = paramiko.RSAKey.from_private_key_file(self.remote_ssh_key)
                self.ssh_client.connect(
                    hostname=self.remote_host, port=self.remote_port, username=self.remote_user,
                    pkey=private_key, timeout=10
                )
            else:
                self.ssh_client.connect(
                    hostname=self.remote_host, port=self.remote_port, username=self.remote_user,
                    password=self.remote_password, timeout=10
                )
            print(f"✅ SSH连接成功")
            return True
        except Exception as e:
            print(f"❌ SSH连接失败: {str(e)}")
            self.ssh_client = None
            return False

    def execute_remote_commands(self, commands: List[str], stage: str) -> bool:
        """批量执行远程命令"""
        if not self.ssh_client:
            print(f"❌ {stage}：未建立SSH连接")
            return False
        if not commands:
            print(f"⚠️ {stage}：无待执行命令，跳过")
            return True

        print(f"\n=== {stage} ===")
        full_cmd = "\n".join(commands)
        try:
            print(full_cmd)
            print("=== end ===\n")
            stdin, stdout, stderr = self.ssh_client.exec_command(full_cmd, timeout=60)
            exit_status = stdout.channel.recv_exit_status()
            stdout_str = stdout.read().decode('utf-8', errors='ignore').strip()
            stderr_str = stderr.read().decode('utf-8', errors='ignore').strip()

            if exit_status == 0:
                if stdout_str:
                    print(f"✅ 命令执行成功，输出：\n{stdout_str}")
                else:
                    print(f"✅ 命令执行成功（无输出）")
                return True
            else:
                print(f"❌ 命令执行失败，错误：\n{stderr_str}")
                return False
        except Exception as e:
            print(f"❌ {stage}执行异常: {str(e)}")
            return False

    def upload_jar(self) -> bool:
        """上传JAR文件到远程服务器"""
        if not self.ssh_client:
            print(f"❌ 上传文件：未建立SSH连接")
            return False

        print(f"\n=== 上传JAR文件 ===")
        try:
            sftp = self.ssh_client.open_sftp()
            # 上传文件
            sftp.put(self.local_jar_path, self.remote_jar_path)
            sftp.close()
            print(f"✅ 文件上传成功")
            print(f"本地路径：{self.local_jar_path}")
            print(f"远程路径：{self.remote_jar_path}")
            return True
        except Exception as e:
            print(f"❌ 文件上传失败: {str(e)}")
            return False

    def close_ssh(self):
        """关闭SSH连接"""
        if self.ssh_client:
            self.ssh_client.close()
            print(f"\n✅ SSH连接已关闭")

    def deploy(self) -> bool:
        """核心部署流程：上传前命令 → 上传文件 → 上传后命令"""
        try:
            # 1. 检查本地文件
            self.check_local_jar()
            # 2. 建立SSH连接
            if not self.connect_ssh():
                return False
            # 3. 执行上传前命令（如停止旧进程）
            if not self.execute_remote_commands(self.pre_upload_commands, "执行上传前命令"):
                return False
            # 4. 上传JAR文件
            if not self.upload_jar():
                return False
            # 5. 执行上传后命令（如启动新进程）
            if not self.execute_remote_commands(self.post_upload_commands, "执行上传后命令"):
                return False

            print(f"\n🎉 部署流程全部完成！")
            return True
        finally:
            self.close_ssh()


def load_config(json_path):
    """加载JSON配置文件"""
    if not os.path.exists(json_path):
        print(f"❌ 配置文件不存在: {json_path}")
        sys.exit(1)
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config_load = json.load(f)
        # 校验必填参数
        required = ["local_jar_path", "remote_jar_path", "pre_upload_commands", "post_upload_commands", "remote"]
        for key in required:
            if key not in config_load:
                print(f"❌ 配置文件缺少必填项: {key}")
                sys.exit(1)
        return config_load
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ 使用示例：python auto_deploy_jar.py cm_xxx_jar_config.json")
        sys.exit(1)

    # 加载配置
    config = load_config(sys.argv[1])
    remote_config = config["remote"]

    # 创建部署器并执行部署
    deployer = JarDeployer(
        # 远程服务器配置
        remote_host=remote_config["remote_host"],
        remote_port=remote_config["remote_port"],
        remote_user=remote_config["remote_user"],
        remote_password=remote_config.get("remote_password"),
        remote_ssh_key=remote_config.get("remote_ssh_key"),
        # 上传前命令
        pre_upload_commands=config.get("pre_upload_commands", []),
        # 上传文件路径
        local_jar_path=config["local_jar_path"],
        remote_jar_path=config.get("remote_jar_path"),
        # 上传后命令
        post_upload_commands=config.get("post_upload_commands", [])
    )

    if not deployer.deploy():
        print("\n❌ 部署流程执行失败！")
        sys.exit(1)
