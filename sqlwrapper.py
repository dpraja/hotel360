import psycopg2
import json
import datetime

def dbput(sql):
    try:
      con = psycopg2.connect(user='akvwghpxnyalss',password='bc0080c7c0f0b55e162582666cf6b39227c6160e2759dbb0d7f28d58190952cd',host='ec2-54-235-146-184.compute-1.amazonaws.com',port='5432',database='dfbvc8j8egd076')
      cur = con.cursor()
    except psycopg2.Error :
       return (json.dumps({'Status': 'Failure','Message':'DB connection Error'}, sort_keys=True, indent=4))
    cur.execute(sql)
    con.commit()
    return sql
def dbget(sql):
     try:
      con = psycopg2.connect(user='akvwghpxnyalss',password='bc0080c7c0f0b55e162582666cf6b39227c6160e2759dbb0d7f28d58190952cd',host='ec2-54-235-146-184.compute-1.amazonaws.com',port='5432',database='dfbvc8j8egd076')
      cur = con.cursor()
     except psycopg2.Error :
       return (json.dumps({'Status': 'Failure','Message':'DB connection Error'}, sort_keys=True, indent=4))
     cur.execute(sql)
  
     def serialize(obj):
        if isinstance(obj, datetime.date):
       
               return obj.__str__()

        if isinstance(obj, datetime.time):
               return obj.__str__()
        # Let the base class default method raise the TypeError
       


    
     columns = cur.description
     result = [{columns[index][0]:column for index, column in enumerate(value)}   for value in cur.fetchall()]
     fresult= json.dumps(result,indent=3,default=serialize)
     #print(result)
     #print(fresult)
     return(fresult)
     #return(json.dumps({'Status': 'Success', 'StatusCode': '200','ReturnValue': fresult ,'ReturnCode':'RRTS'}, sort_keys=True, indent=4, default=myconverter))
def Dict2Str(dictin,joiner=','):
    # make dict to str, with the format key='value'
    #tmpstr=''
    tmplist=[]
    for k,v in dictin.items():
        # if v is list, so, generate 
        # "k in (v[0], v[1], ...)"
        if isinstance(v, (list, tuple)):
            tmp = str(k)+' in ('+ ','.join(map(lambda x:'\''+str(x)+'\'',v)) +') '
        else:
            tmp = str(k)+'='+'\''+str(v)+'\''
        tmplist.append(' '+tmp+' ')
    return joiner.join(tmplist)
def gen_insert(table,dicts):
    '''
    >>> kdict = {'name':'lin','age':22} 
    >>> geninsertsql('persons',kdict)
    insert into person (name,age) values ('lin',22)
    '''
    sql = 'insert into %s '%table
    ksql = []
    vsql = []
    for k,v in dicts.items():
        ksql.append(str(k))
        vsql.append('\''+str(v)+'\'')
    sql += ' ('+','.join(ksql)+') '
    sql += ' values ('+','.join(vsql)+')'
    #return sql
    return(dbput(sql))

def gen_select(table,keys="*",conddicts=None):
    if isinstance(keys, (tuple,list)):
        keys=','.join(map(str,keys))
    sql = 'select %s '%keys
    sql += ' from %s '%table
    if conddicts:
        sql += ' where %s '%Dict2Str(conddicts,'and')
    print (sql)
    return (dbget(sql))
def gen_update(table,dicts,conddicts):
    # conddicts maybe the Condition, in sql, where key='value' or key in (value)
    # dicts are the values to update
    sql = ''
    sql += 'update %s '%table
    sql += ' set %s'%Dict2Str(dicts)
    sql += ' where %s'%Dict2Str(conddicts,'and')
    print(sql)
    return(dbput(sql))
    
def gensql(imp,*args, **kwds):
    if imp == "insert":
        return gen_insert(*args, **kwds)
    elif imp == "update":
        return gen_update(*args, **kwds)
    elif imp == "select":
        return gen_select(*args, **kwds)
    else:
        return None  

