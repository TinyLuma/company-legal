# 上传到 GitHub 与读取

## 浏览器上传

1. 在 GitHub 新建仓库，建议名称 `company-legal`，选择 **Public**，使用 `main` 分支。无需另外生成 README 或许可证。
2. 解压 ZIP。打开其中的 `company-legal` 文件夹。
3. 在新仓库的上传入口（空仓库通常有 uploading an existing file 链接，已有仓库为 **Add file → Upload files**）上传该文件夹**里面的内容**，保留子目录。
4. 提交前确认仓库顶层直接是 `README.md`、`apps.json`、`apps/` 等，而不是多嵌套一层 `company-legal/`。
5. 输入提交说明，例如 `Initialize company policy repository`，提交到 `main`。
6. 打开文件核对目录和正文。TinyLuma 完成发布核对前，只将它当作公开草稿，App 不使用它作为生效政策。

不要只上传 ZIP 文件本身；那样无法按上述固定路径逐份读取政策。

如果 GitHub 中目录结构不正确，可使用 GitHub Desktop 把解压后的内容复制到克隆的仓库根目录，再提交并推送。

官方上传说明：<https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository>

## 链接的区别

| 用途 | URL 格式 |
| --- | --- |
| 在 GitHub 中阅读 | `https://github.com/TinyLuma/company-legal/blob/main/apps/breastfeeding-timer/privacy/en.md` |
| App 下载 Markdown | `https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps/breastfeeding-timer/privacy/en.md` |
| 程序发现所有文档路径 | `https://raw.githubusercontent.com/TinyLuma/company-legal/main/apps.json` |

公开仓库为 [TinyLuma/company-legal](https://github.com/TinyLuma/company-legal)，默认分支为 `main`。其他语言把路径末尾的 `en.md` 换成对应文件名。

## JavaScript 读取示例

```js
const owner = 'TinyLuma';
const repo = 'company-legal';
const base = `https://raw.githubusercontent.com/${owner}/${repo}/main/`;

async function loadPolicy() {
  const response = await fetch(`${base}apps/breastfeeding-timer/privacy/en.md`);
  if (!response.ok) throw new Error(`Policy request failed: ${response.status}`);
  const markdown = await response.text();
  if (!markdown.trim()) throw new Error('Policy is empty');
  return markdown; // 交给 Markdown 渲染组件；如支持 HTML，进行安全过滤。
}
```

这个示例只展示下载。生产代码还应处理超时、离线、缓存和错误，并在上线前确认政策已发布。不要把 GitHub Token 放进 App：公开文件无需读取凭证。

更新 `main` 后，固定 URL 会随分支内容更新，但缓存可能延迟。不要每秒轮询；按应用的合理刷新策略拉取。需要保留某用户当时阅读/接受的版本时，可记录对应提交标识，必要时通过该 commit SHA 读取，不能仅记录会变化的 `main` URL。
