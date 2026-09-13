# 持久化数据

Docker Compose 将服务数据保存在此目录：

```text
data/
├── dev/
│   ├── postgres/
│   └── redis/
└── prod/
    ├── postgres/
    └── redis/
```

实际数据目录已被 Git 忽略。路径由 `config/compose.dev.env` 和
`config/compose.prod.env` 中的 `DATA_DIR` 配置。
