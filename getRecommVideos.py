import connectorSSHMySQL as msql
import json
import webbrowser


def cid2bid(cid):
    try:
        sql_query = """select bvid from Vinfo where cid="{cid}" order by cid;""".format(
            cid=cid)
        sql_result = msql.SSHMysql("bilibili", sql_query)
        return sql_result[0][0]
    except:
        return ""


def bid2cid(bid):
    try:
        sql_query = """select cid from Vinfo where bvid="{bid}" order by cid;""".format(
            bid=bid)
        sql_result = msql.SSHMysql("bilibili", sql_query)
        return sql_result[0][0]
    except:
        return ""


def getAdviseList(bid):
    cid = bid2cid(bid)
    ans = []
    sql_query = """SELECT Vinfo.bvid, T.r
        FROM
        (SELECT * FROM (( SELECT cid_a AS cid_0, cid_b AS cid_x, r FROM comment_wordfreq_relation WHERE cid_a = "{cid}" ) UNION
        ( SELECT cid_b AS cid_0, cid_a AS cid_x, r FROM comment_wordfreq_relation WHERE cid_b = "{cid}" )) AS ta 
        ORDER BY
	    r DESC) as T, Vinfo WHERE T.cid_x=Vinfo.cid;""".format(cid=cid)
    sql_result = msql.SSHMysql("bilibili", sql_query)
    cnt = 5
    for i in sql_result:
        ans += [{"bvid": i[0], "r": i[1]}]
        cnt -= 1
        if cnt <= 0:
            break
    return ans


advise_list = getAdviseList("BV12h411h7JR")
print(json.dumps(advise_list))
for i in advise_list:
    webbrowser.open("https://www.bilibili.com/video/{bid}".format(bid=i["bvid"]))