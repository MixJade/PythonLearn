# Python查看库的依赖关系

> 2024年5月25日16:26:01

1. **下载pipdeptree**

```bash
pip install pipdeptree
```

2. **查看所有依赖numpy的包**

```shell
pipdeptree --reverse --packages numpy
```

输出结果(这些包依赖numpy)：

```bash
numpy==1.26.3
├── contourpy==1.2.0 [requires: numpy>=1.20,<2.0]
│   └── matplotlib==3.8.2 [requires: contourpy>=1.0.1]
├── matplotlib==3.8.2 [requires: numpy>=1.21,<2]
├── pandas==2.2.0 [requires: numpy>=1.22.4,<2]
└── pyarrow==15.0.2 [requires: numpy>=1.16.6,<2]
```

3. **查看pandas依赖的所有包**

```bash
pipdeptree --packages pandas
```

输出结果(Pandas依赖这些包)：

```bash
pandas==2.2.0
├── numpy [required: >=1.22.4,<2, installed: 1.26.3]
├── python-dateutil [required: >=2.8.2, installed: 2.8.2]
│   └── six [required: >=1.5, installed: 1.16.0]
├── pytz [required: >=2020.1, installed: 2023.3.post1]
└── tzdata [required: >=2022.7, installed: 2023.4]
```

