## 说明 | [English](https://github.com/waynia/Chat-GUI/blob/main/readme.md)

这个工具是一个使用flask实现的简易GUI对话界面，虽然还未整合OpenAI的知识库查询功能，但已经具备了一切基础。该GUI界面可以实现如下效果：

1）第一次打开界面，用户需要输入自己的OpenAI API Key，程序会将其保存在Cookie中，并向用户提供了一种删除该Key的方式。程序会调用OpenAI的函数对API Key的有效性进行验证，确保该Key可用。

2）在API Key有效的前提下，epub文件上传按钮可见，用户点击按钮或拖放epub文件到GUI界面，程序会将文件上传到uploads文件夹中，然后在后台生成一个与上传文件名称相同的csv文件。生成csv文件的函数是parse_book，该函数体内部无任何具体的执行代码，下一步需要在此调用分析epub文件、并生成embedding的函数。

3）程序会判断uploads文件夹下是否有csv文件，如果有的情况下，会让聊天对话框可见，此时用户可以在输入框中输入任何文字，然后程序会在后台调用process_input函数遍历uploads文件夹下的所有csv文件，然后对输入文字进行分析。分析部分无任何具体的执行代码，下一步需要在此调用计算用户输入的embedding，并从csv中检索similarity数值最高的记录的函数。

4）程序尚未实现对用户对话的保留以及memory功能。

![image](https://user-images.githubusercontent.com/49633741/228503581-f4750198-e5b5-4fd0-9556-b029fe1e3ff3.png)
