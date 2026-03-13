# Neomma

[English](readme.md) | **简体中文**

Neomma 是一款音乐伴奏生成器，类似电子琴中的伴奏功能。它可以根据用户输入的包含和弦和 MMA 指令的文件，生成 MIDI 伴奏音轨供独奏者或歌手使用。Neomma 内置了大量伴奏模板，用户也可以自行编写模板

Neomma 基于 [MMA—Musical MIDI Accompaniment](https://www.mellowood.ca/mma/)

## 安装

首先安装 [Python](https://www.python.org/)，然后在命令行中运行：

```cmd
git clone https://github.com/oxygen-dioxide/neomma
cd neomma
pip install .
```

## 使用

首先编写 mma 文件（文本文件，声明了歌曲的速度、所使用的伴奏模板和每个小节的和弦，格式参见 [mma 文档](https://www.mellowood.ca/mma/online-docs/html/tut/node3.html)）

然后在命令行中运行：
```cmd
neomma <.mma 文件路径>
```

midi 文件会输出到 mma 文件同一文件夹下。

## 开发计划
本仓库致力于让 MMA 现代化。目前，Neomma 与原版 MMA 相比有以下区别：

- 支持使用 pip 安装
