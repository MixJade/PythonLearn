# Python读取配置文件

> 2024年2月12日14:26:31

Python自身并没有自带的配置文件，但Python常常使用`.ini`，`.json`或`.yaml`格式的文件作为配置文件。你也可以直接创建一个Python文件，将数据库的配置写成Python的变量或者字典。

如果要使用.ini文件，可以使用Python内置的`configparser`模块来读取和修改.ini文件：

例如，你的.ini文件内容为：

```ini
[mysql]
host = 127.0.0.1
user = root
password = mypassword
database = test
```

你可以这样读取.ini文件中的内容：

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

host = config['mysql']['host']
user = config['mysql']['user']
password = config['mysql']['password']
database = config['mysql']['database']
```

如果要使用.json文件，可以使用Python内置的`json`模块来读取和修改.json文件：

例如，你的.json文件内容为：

```json
{
    "mysql": {
        "host": "127.0.0.1",
        "user": "root",
        "password": "mypassword",
        "database": "test"
    }
}
```

你可以这样读取.json文件中的内容：

```python
import json

with open('config.json', 'r') as f:
    config = json.load(f)

host = config['mysql']['host']
user = config['mysql']['user']
password = config['mysql']['password']
database = config['mysql']['database']
```

如果要使用.yaml文件，可以使用`pyyaml`包（你需要另外安装这个包）来读取和修改.yaml文件：

例如，你的.yaml文件内容为：

```yaml
mysql:
  host: 127.0.0.1
  user: root
  password: mypassword
  database: test
```

你可以这样读取.yaml文件中的内容：

```python
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

host = config['mysql']['host']
user = config['mysql']['user']
password = config['mysql']['password']
database = config['mysql']['database']
```