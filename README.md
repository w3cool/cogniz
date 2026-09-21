# Cogniz

Cogniz 由 Next.js 前端、FastAPI 后端、PostgreSQL 和 Redis 组成。登录后 AI 工作区位于 `/ai`，平台管理后台位于 `/admin`。开发与生产环境的公开域名、端口和容器内部地址分别保存在 `config/compose.dev.env`、`config/compose.prod.env`。

PostgreSQL 和 Redis 使用宿主机目录持久化：开发数据位于 `data/dev/`，生产数据位于 `data/prod/`。可通过对应环境配置中的 `DATA_DIR` 修改根路径。

## 开发环境

```bash
docker compose --env-file config/compose.dev.env -f docker-compose.dev.yaml up --build
```

默认服务地址：

| 服务 | 地址 |
| --- | --- |
| 前端 | `http://localhost:3000` |
| AI 工作区 | `http://localhost:3000/ai` |
| 平台管理后台 | `http://localhost:3000/admin` |
| 后端 | `http://localhost:8000` |
| 前端同域 API | `http://localhost:3000/api` |
| PostgreSQL | `127.0.0.1:5432` |
| Redis | `127.0.0.1:6379` |

修改开发域名或端口时编辑 `config/compose.dev.env`。PostgreSQL 和 Redis 只绑定到本机回环地址；前后端默认允许局域网访问。

## 生产环境

生产环境中只有前端公开发布。Next.js 将同域的 `/api/*` 转发到 Docker 内部的 FastAPI 服务，FastAPI、PostgreSQL 和 Redis 均不映射到宿主机端口。

部署前编辑 `config/compose.prod.env`，至少将 `WEB_DOMAIN`、`WEB_ORIGIN` 和对应的 API 域名改为实际域名。复制生产密码模板并填写密码：

```bash
cp config/compose.prod.secrets.env.example config/compose.prod.secrets.env
docker compose \
  --env-file config/compose.prod.env \
  --env-file config/compose.prod.secrets.env \
  -f docker-compose.prod.yaml up -d --build
```

`docker-compose.prod.yaml` 在 `WEB_PORT` 上提供 HTTP 服务。生产域名的 DNS、HTTPS 证书和 TLS 终止由部署环境的反向代理或入口网关负责，并应将流量转发到该端口。后端公开地址始终为 `WEB_ORIGIN + API_PUBLIC_PATH`，默认是 `https://cogniz.example.com/api`。

## 地址配置

| 变量 | 用途 |
| --- | --- |
| `WEB_DOMAIN` / `WEB_PORT` | 前端公开域名和宿主机端口 |
| `WEB_ORIGIN` | 完整前端来源，用于后端来源校验 |
| `API_DOMAIN` / `API_PORT` | API 对外展示的同域域名和端口 |
| `API_PUBLIC_PATH` | API 同域路径，固定使用 `/api` |
| `API_INTERNAL_HOST` / `API_INTERNAL_PORT` | 前端代理访问后端的 Docker 内部地址 |
| `REDIS_BIND_ADDRESS` / `REDIS_PORT` | Redis 开发环境宿主机监听地址与端口 |
| `DATA_DIR` | PostgreSQL 与 Redis 的宿主机持久化根目录 |

生产数据库密码保存在被 Git 忽略的 `config/compose.prod.secrets.env`，不放入公开地址配置文件。
