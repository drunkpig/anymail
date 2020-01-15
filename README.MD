

### API
- /email/{type}/{email}  获取email地址收到的最近一封邮件内容，格式为type(text|html)




### page
- /list/   显示全部邮件，按照日期从最近到最久
- /detail/{id}/{type} 显示这个邮件的详细内容,type:text|html
- /delete/{email}  删除发送到email地址的邮件



### email解析库
- https://pypi.org/project/mail-parser/
