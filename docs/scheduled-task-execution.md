# 定时任务执行机制

实现入口：前端 `/ai/scheduled-tasks`，后端 `/v1/scheduled-tasks`，调度进程为现有 API 容器中的 `maintenance`。

参考 DeerFlow 源码快照 `5ecc1c2ac2de624af354bc515d5cb04f80df226c`：

- [调度服务](https://github.com/bytedance/deer-flow/blob/5ecc1c2ac2de624af354bc515d5cb04f80df226c/backend/app/scheduler/service.py)：到期入队与执行容量分离、队列超时、启动恢复。
- [运行仓库](https://github.com/bytedance/deer-flow/blob/5ecc1c2ac2de624af354bc515d5cb04f80df226c/backend/packages/harness/deerflow/persistence/scheduled_task_runs/sql.py)：数据库并发预算、租约与过期抢占恢复。
- [调度配置](https://github.com/bytedance/deer-flow/blob/5ecc1c2ac2de624af354bc515d5cb04f80df226c/backend/packages/harness/deerflow/config/scheduler_config.py)：全局及单用户并发、排队超时。

本项目沿用 PostgreSQL 原始 SQL、Taskiq 和已有 Run/outbox；每轮新建普通对话或在当前用户已有对话中添加新轮次，再经现有 Agent、Skill、Tool 执行链完成。未引入 DeerFlow 的 LangGraph、ORM 或新容器服务。

## 流程

1. 到期扫描或手动试运行在任务行锁下创建轮次，保存提示词、每轮目标、智能体、对话模式及目标对话、思考深度、名称和语言快照。手动接口返回 `202` 和等待启动的记录。
2. 调度周期先恢复失效租约、同步原始 Run 的完成状态并使排队超时的轮次失败，再处理到期任务和等待队列。
3. 启动认领在共享数据库预算锁下检查全局/单用户并发，发放 UUID token 和 120 秒启动租约。各用户轮流获得扫描机会。
4. 创建对话或追加已有对话、创建 Agent Run/outbox、关联轮次在同一事务中完成。持有任务及轮次锁，重新检查 token、租约、账号和暂停状态；部分失败全部回滚。
5. outbox 交给现有 Taskiq Worker，执行阶段继续使用既有执行 token、租约、恢复和证据快照。定时任务的启动租约不会中断长时间的 Agent 执行。

状态为 `queued → launching → launched → completed / failed / cancelled`；暂停或重叠的自动轮次为 `skipped`。接口可按原始 Agent Run 将已启动轮次显示为排队、运行或完成状态，不必等待下一次维护扫描。

## 行为约定

| 场景 | 结果 |
| --- | --- |
| 同一任务仍在排队、启动或执行 | 手动试运行返回 409；到期自动轮次记录为跳过 |
| 全局或单用户执行槽已满 | 轮次保留队列，不丢失，不占启动槽 |
| 临时启动异常 | 安全错误码持久化，退避重试，默认最多 3 次 |
| 模型/Agent 配置不可用 | 启动失败可见，不无限重试；修复后可重新试运行 |
| 排队超过 1 小时 | 失败并保留 `queue_timeout` 记录 |
| 维护进程启动中断 | 租约失效后恢复；旧 token 无法覆盖新认领 |
| 暂停任务 | 取消未启动自动轮次，已启动轮次继续；允许手动试运行 |
| 修改提示词 | 不改变已经排队的提示词快照 |
| 漏过多次计划 | 合并补跑一次，下一次恢复未来计划 |
| 删除活跃任务 | 返回 409，避免丢失活跃执行的追踪和并发计数 |
| 对话重新生成 | 任务记录仍关联最初 Run，不改写原状态和 tokens |
| 浏览器关闭 | 不影响后端执行；页面刷新仅用于读取状态 |

Cron 使用五段数字表达式和 IANA 时区，UTC 存储。不存在的夏令时时刻跳过；回拨时重复的本地时刻对应两次真实 UTC 时间。日期不可达的计划返回 422。

配置、初始化和检查命令见 [后端部署说明](../cogniz-api/docs/deployment.md)。统一的 `001_initial_schema.sql` 直接创建任务配置、运行历史、租约、Run 关联、心跳及累计运行次数字段；新任务从 0 次开始，不再逐次改表或从历史记录回填。

## 新建和编辑

表单参考 [DeerFlow 任务编辑器](https://github.com/bytedance/deer-flow/blob/5ecc1c2ac2de624af354bc515d5cb04f80df226c/frontend/src/components/workspace/scheduled-tasks/task-form-dialog.tsx)，统一用于 `/ai/scheduled-tasks` 的新建和编辑。

- 运行时间：每小时（分钟 0–59）、每天、工作日、每周、每月（日期 1–31）、仅一次、自定义五段 Cron。没有对应日期的月份自动跳过。可选择 IANA 时区，并通过 `/v1/scheduled-tasks/preview-schedule` 预览最近三次实际 UTC 运行时刻的本地显示。
- 日期按所选时区解释。单次运行及结束时间以 UTC 保存；本地输入遇到夏令时缺失或重复时刻会返回 422，避免默默选择错误偏移。API 也接受明确包含偏移的 ISO 日期。未修改的日期保留原偏移，编辑标题不会改动排期。
- 可选每轮目标（最长 2000 字符）：写入 TaskSpec.goal 及 acceptance_criteria，通过现有 Agent 规划、执行与验收流程处理；任务指令仍作为该轮对话的用户内容。设置目标必须使用新对话。
- 安全上限：累计自动启动次数（1–10000，空白不限制）和结束时间（空白不限制）。次数在成功提交 Run/outbox 时原子加一，手动试运行、跳过及启动失败不计入。Agent 启动后失败也计入。修改上限不会清零已用次数；到达任一上限停止未启动自动轮次，已开始的运行继续。结束任务仍可手动试运行。
- 高级选项：默认智能体沿用自动路由，或选择平台启用的注册智能体。所选智能体仍受平台工具、技能和预算策略约束；需要结构化输入的智能体会验证指令是否提供足够信息。
- 在已有对话中运行：只能使用当前用户的对话 ID，会带入其历史。忙碌时回到队列，5 秒后检查，等待不消耗启动重试次数，原始排队超时仍有效。成功时关联新增轮次自己的 Run，历史 tokens 不会混入任务记录；目标对话已删除则明确失败。
- 单次任务到期入队即清除下一次排期，结束后标记已结束。仅修改标题、指令、上限等配置不会重新执行；需要再次自动运行时设置新的未来运行时间并启用。
- PATCH 省略字段保持原值；显式 `null` 清空目标、次数/时间上限、智能体或目标对话。所有运行内容在入队时快照；修改表单不改变已排队的指令和执行配置，但安全上限与暂停状态仍在启动前重新检查。

表单在弹窗内部显示错误，内容可以滚动，顶部标题与底部保存/取消按钮保持可见；中文简体、香港繁体和英文同步支持。任务列表区分启用、暂停和已结束，并在详情中显示目标、对话模式及上限。
