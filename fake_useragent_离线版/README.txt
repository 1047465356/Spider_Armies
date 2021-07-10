
# 安装
pip install fake_useragent

# fake_useragent 离线版的作用
1.部分网站有UA反爬，原理是检测请求头是否带真实浏览器参数，这时可以使用模拟浏览器请求头实现绕过

2.使用fake_useragent库有时需要联网下载浏览器文件，往往很难下载到正确文件
这时使用fake_useragent离线版，相对来说比较稳定，免去更新和下载出错的带来的麻烦

# 注意事项
建议py文件和json文件放在同级目录
或者修改path，可以设置绝对路径或者相对路径
