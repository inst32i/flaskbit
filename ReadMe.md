
# 本地环境安装
1. 安装mysql5.5以上,并运行sql文件，生成数据库manifoldb  用户名root,密码 mysqladmin
2. 安装虚拟环境virtualenv , pip install virtualenv and then input :source venv/bin/activate
3. 安装python依赖库，在项目根目录下运行  pip install -r requirements.txt,if still have error in moudle, please use pip install <moudle_name>
4. import manifoldb.sql to databases in mysql;
5. 启动项目 python flaskunit
6. 用浏览器打开  localhost:5000
  