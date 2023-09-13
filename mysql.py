import pymysql.cursors

db_settings = {
  "host" : 'ichef2-readonly-for-external.cm3pmmqhwbdv.ap-northeast-1.rds.amazonaws.com',
  "port" : 3306,
  "user" : 'ichef_prod',
  "password" : 'apmZpPAKGL9Zo6cjNs8crvWwu8uFdxZQtwnTJ9qh',
  "db" : "ichef_prod" ,
  "charset" : "utf8"
}

db_settings = {
  "host" : 'report-psql-production-readonly3-for-external.cm3pmmqhwbdv.ap-northeast-1.rds.amazonaws.com',
  "port" : 5432,
#   "user" : 'ichef_prod',
#   "password" : 'apmZpPAKGL9Zo6cjNs8crvWwu8uFdxZQtwnTJ9qh',
  "db" : "mongo2psql_prod" ,
  "charset" : "utf8",
  "connect_timeout" : 60
}

try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)
    print("連線成功")
except Exception as ex: # 出現意外時印出
    print(ex)


mysql -h ichef2-readonly-for-external.cm3pmmqhwbdv.ap-northeast-1.rds.amazonaws.com -P 3306 -u ichef_prod -p ichef_prod
mysql -h report-psql-production-readonly3-for-external.cm3pmmqhwbdv.ap-northeast-1.rds.amazonaws.com -P 5432 -u ichef_prod -p ichef_postgres_prod