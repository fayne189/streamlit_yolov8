# README.md

## 介绍

该项目提供了一个用户友好的基于Streamlit的交互界面，用于YOLOv8目标检测模型。我想利用这个项目对个人现阶段的一些技能和专业知识做个简单的总结，并用一个系列的博客来记录和分享项目的开发过程及其中涉及的机器视觉知识。如果你对此感兴趣，欢迎去[我的博客](https://fayne189.github.io/index.html)阅读系列文章，并与我交流。

简单介绍这个应用，它利用目标检测模型开发智慧监控应用，例如感兴趣区域、电子围栏、车流量统计和行人计数等功能。我计划将这个项目分为3个阶段进行开发：

- 可视化模型推理结果：Yolov8模型+Streamlit前端界面
- 实现几何图形间的交互条件逻辑：使用Shapely库构建几何图形，并设置条件逻辑
- 可自定义逻辑及条件触发行为：使用界面自定义智慧监控应用

我将使用3个标签来标识这些阶段，分别是Base（基础）、Advanced（高级）和Final（最终）。

## 安装

### 安装依赖包

使用以下命令安装所需的依赖包：

```
pip install ultralytics
pip install streamlit
# 或者
pip install -r requirements.txt
```

### 在Docker上运行

推荐使用Visual Studio Code的Dev Containers功能来运行项目：

1. 按下`Ctrl + Shift + P`
2. 选择"`Dev Containers: Reopen on Container`"
3. 完成，VS Code将根据项目根目录中的Dockerfile运行一个容器

或者，自己构建Docker镜像：

```
docker build -t ${imagename} .
```

然后，在容器内运行streamlit命令：

```
streamlit run app.py
```

## 开发计划

- [x]  多种计算机视觉任务，包括检测、分割、分类和姿态估计等
- [x]  可视化模型推理结果
- [x]  实时模型交互、配置和视频帧选择
- [ ]  可定义画面上的几何图形，点，线，面
- [ ]  可定义几何图形与目标Bouding Box间的交互条件逻辑
- [ ]  可定义条件满足时触发的行为