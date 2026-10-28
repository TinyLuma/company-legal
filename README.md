# 公司软件政策与条款

按 App 管理的公开 Markdown 仓库。建议仓库名：`company-legal`，默认分支：`main`。
每个 App 一个固定英文目录；每类文档按语言拆分，文件名不带版本号。更新原文件即可保留固定读取地址；历史版本由 Git 记录。

**当前 TinyLuma 为草稿：公司身份、生效日期和正式政策链接已写入正文，实际服务与订阅配置仍待核实，尚不可接入生产。** 发布准备见 [核对说明](docs/tinyluma-release-checklist.md)。本仓库的维护说明也会公开。

## 快速找到 App

| App | 状态 | 文档入口 |
| --- | --- | --- |
| TinyLuma | 草稿 | [全部文档](apps/breastfeeding-timer/README.md) |

程序查找请读 [apps.json](apps.json)。新增 App 时同时更新本表与清单。

公司法定名称、注册地址、公司邮箱，以及政策要支持的语言，见 [company.json](company.json)。填写各政策中的运营主体和联系方式时以该文件为准。各 App 的价格、供应商、数据处理和试用安排仍只看该 App 自己的正文。

## 目录结构

```text
company-legal/
├── README.md                       # App 总入口
├── AGENTS.md                       # 给 AI 的单个 / 批量维护规则
├── apps.json                       # App ID、状态和文档路径
├── company.json                    # 公司法定名称、注册地址、邮箱和支持语言
├── CHANGELOG.md                    # 人可读的变更记录
├── apps/
│   └── breastfeeding-timer/
│       ├── README.md               # 此 App 的文档入口
│       ├── privacy/
│       │   ├── en.md
│       │   ├── zh-CN.md
│       │   ├── es.md
│       │   ├── zh-TW.md
│       │   ├── vi.md
│       │   ├── fil.md
│       │   ├── ko.md
│       │   └── ar.md
│       └── terms/
│           ├── en.md
│           ├── zh-CN.md
│           ├── es.md
│           ├── zh-TW.md
│           ├── vi.md
│           ├── fil.md
│           ├── ko.md
│           └── ar.md
├── docs/
│   ├── github-setup.md              # 上传与代码读取说明
│   ├── maintenance.md               # 修改 / 新增 App / AI 提示示例
│   └── tinyluma-release-checklist.md
└── scripts/
    └── check.py                    # 路径检查及发布前检查，无额外依赖
```

## App 代码如何读取最新版

生产使用前先完成草稿发布核对。公开仓库为 [TinyLuma/company-legal](https://github.com/TinyLuma/company-legal)，默认分支 `main`：

```text
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/privacy/en.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/privacy/zh-CN.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/privacy/es.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/privacy/zh-TW.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/privacy/vi.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/privacy/fil.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/privacy/ko.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/privacy/ar.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/terms/en.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/terms/zh-CN.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/terms/es.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/terms/zh-TW.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/terms/vi.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/terms/fil.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/terms/ko.md
https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/terms/ar.md
```

这些地址返回 Markdown 文本。App 可直接请求并用 Markdown 组件渲染；直接在 WebView 打开不保证渲染成网页。面向用户的正式网页若有需要，可另行配置 GitHub Pages，本包不依赖它。

`main` 指向该分支当前版本，提交更新后地址无需改变；网络/CDN/客户端缓存可能导致短暂延迟，并非即时推送。App 应保存最近一次有效正文，在加载失败时提供兜底；不要向用户展示空白政策。需要对应特定历史版本时，将 `main` 替换成 commit SHA 或发布标签。

也可读取 `https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps.json` 发现路径。接入方应核对 `status` 为 `published`；草稿仍可被公开下载，清单状态不是访问控制。

## 开始使用

1. [创建公开仓库并上传](docs/github-setup.md)。先解压，再上传目录内的文件与文件夹。
2. [补齐 TinyLuma 发布信息](docs/tinyluma-release-checklist.md)，审阅通过后再接入 App。
3. 单改或批改时，让 AI 先读 [AGENTS.md](AGENTS.md) 和 [维护指南](docs/maintenance.md)。

不需要为旧政策复制 `v1/v2/latest` 多套目录，也不需要数据库或构建步骤。
