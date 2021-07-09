import json
from json import decoder

with open("ciku/sqlr.txt","w",encoding="utf-8") as rsql:
    with open("ciku/sqlquery.txt","w",encoding="utf-8") as fsql:
        def sqlfileprint(str):
            fsql.write(str)
            fsql.write("\n")
        with open("ciku/ciku.json", "r", encoding="utf-8") as f:
            ciku=json.load(f)['RECORDS']
            f.close()
        sqlfileprint("""SELECT
            cid,""")
        for i in ciku:
            sqlfileprint("	n{id} / danmuTotalLength AS f{id},".format(id=i["id"]))
        sqlfileprint("""FROM
            (
            SELECT
                Danmu.cid,
                sum(
                LENGTH( Danmu.text )) AS danmuTotalLength,""")
        for i in ciku:
            sqlfileprint("""  sum(locate("{word}", Danmu.text ) > 0) AS n{id}, """.format(word=i["word"],id=i["id"]))
        sqlfileprint("""	FROM
                Danmu 
            GROUP BY
            Danmu.cid 
            ) AS T;""")
        
        for i in ciku:
            rsql.write("a.f{id}*b.f{id}+\n".format(id=i["id"]))
