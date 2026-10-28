# 维护指南

## 改一个 App

打开 `apps/<app-id>/`，修改对应 `privacy` 或 `terms` 下的语言文件，然后检查其他语言和相关条款，更新清单日期及变更记录。固定文件名不变。

可以直接交给 AI：

> 先读 AGENTS.md。仅修改 tinyluma，把隐私联系邮箱改为我提供的新邮箱（在这里填写），同步中英文及相关出现位置。不要改变条款含义。更新清单和变更记录，运行检查并给我看 diff。

## 批量改多个 App

> 先读 AGENTS.md 和 apps.json。把 tinyluma、另一个已登记的 App 的支持邮箱改为我提供的新邮箱（在这里填写）。逐 App 查找中英文所有相关位置并修改，保留各 App 的其他差异，更新变更记录并检查。不要修改未指定 App。

> 先读 AGENTS.md。检查清单中全部 App，列出每个 App 的隐私联系邮箱及文件位置；把符合指定旧邮箱的出现位置统一替换为我提供的新邮箱，中英文一起核对，不要修改其他公司身份或订阅配置。完成后展示逐 App 的变更摘要。

把示例中的值换成实际值即可。全公司信息变更仍需逐份正文落盘，不依赖公共模板动态拼接，保证每个 App 的政策可单独读取。

## 新增 App

1. 确定固定 App ID，例如 `new-app`。在 `apps/new-app/` 下建立 `README.md`、`privacy/zh-CN.md`、`privacy/en.md`、`terms/zh-CN.md`、`terms/en.md`；实际仅有的语言/文档按需登记。
2. 使用该 App 已确认的政策正文；不要直接复用 TinyLuma 的业务事实。
3. 在 `apps.json` 的 `apps` 数组新增条目，填写 `id`、`name`、`status`、`source_version`、`source_date`、`effective_date`、`updated_at` 和 `documents`。没有来源版本/日期时前两项可用 null；未确认生效日期使用 null，状态用 `draft`。
4. 更新根 README 的 App 导航表。检查 `python3 scripts/check.py`。
5. 业务审阅完成、日期和占位符已确认后，状态改为 `published`，执行 `python3 scripts/check.py --release --app new-app`。

## 更新与历史

普通编辑的结构检查：

```bash
python3 scripts/check.py
python3 scripts/check.py --app tinyluma
```

发布前检查（当前包因草稿和占位符应失败）：

```bash
python3 scripts/check.py --release --app tinyluma
```

单 App 提交例子，先检查 diff，确认只包含本次修改：

```bash
git diff
git add apps/tinyluma apps.json CHANGELOG.md
git commit -m "Update TinyLuma policies"
git push origin main
```

新增 App 或导航变更时，也要提交 README 等对应文件。批量更新可在同一个提交中加入所有明确修改的 App；不需要逐个仓库切换。

草稿变更应放在独立分支；不要把未审阅正文直接覆盖生产 `main`。首次建仓目前全部为草稿，确认后再让 App 接入。

用 Git 查看旧版本，避免维护重复历史文件；如需回滚，检查目标内容仍符合实际业务后，以新提交恢复，保留历史记录。
