# xiaolanshu

> 以下抄自xc的readme

- 可能得要求python3.8以上的版本
- 不要在本地pip，在虚拟环境中pip
  - 及时更新requirements.txt，保证项目可运行
- 项目无关的生成文件记得添加进 .gitignore
- 当然直接跑是跑不了的，要开发记得找我要config文件（这个我还没做，目前配置信息先不急着填进去，我18，19号内完成）

## git 规范 （啊啊这个我目前还没太熟，我们可以笨一点手动合并先）

- 创建自己的分支

```bash
git branch xxxx; git checkout xxxx
# or
git checkout -b xxxx
```

- 每一次完成自己的更改之后，需要先变基到主分支上(保证主分支是线性的)，再发起push -f (如果push不上，就加上 force 选项)
  - 如果发现变基的时候有冲突，那就是有两个人的工作冲突了，修改了相同的代码。

```bash
git rebase main
git push -f
```

- 然后在 GitHub 上创建 pull request，可 merge 的条件是
  - 有一人审核通过
  - 且提交是线性的

## 主分支使用说明

- 首先创建项目文件夹，并在项目文件夹下加载python的虚拟环境

```bash
mkdir your_project; cd your_project

virtualenv venv
# or
python -m venv venv
```

- 进入虚拟环境

```bash
source venv/bin/activate
# win下进入虚拟环境
call venv/script/activate.bat
```

- 安装依赖

```bash
pip install -r requirements.txt
```