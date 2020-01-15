### fakemail 说明

你有一个域名或者二级域名，想用email注册很多账号，那么fakemail可以立刻让你拥有无数email邮箱地址，并收取验证邮件！

- 零配置，一键启动
- 无需事先配置收件地址，只要是你域名下的邮件全部自动收到
- 提供web界面接收验证码
- 提供API方式接收验证码



### API

- /email/{email}/{type}  获取email地址收到的最近一封邮件内容，格式为type(text|html)。里面如果含有验证码，你需要自己解析哦。




### Web UI
- /   显示全部邮件，按照日期从最近到最久
- /detail/{id}/{type} 显示这个邮件的详细内容,type:text|html
- /delete/{email}  删除发送到email地址的邮件



### email解析库
- https://pypi.org/project/mail-parser/
