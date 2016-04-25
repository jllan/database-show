# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify, json, redirect, url_for
from create_app import app
from models import db, Event
from config import PAGE_SIZE, CURRENT_DATE, TABLE_NAME
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@app.route('/')
@app.route('/scan/all/', methods=['GET', 'POST'])
def scan_all():
    if request.method == 'GET':
        #paginate = Event.query.filter(Event.StartDate>'2016-03').order_by(Event.StartDate.asc(), Event.CityName.asc(),Event.ExpoName.asc()).paginate(page, PAGE_SIZE, False)
        #object_list = paginate.items
        #return render_template('base.html', pagination = paginate, page=page, per_page=PAGE_SIZE, events=object_list)
        return render_template('base.html')

"""
获取ajax传过来的参数,根据参数状态进行不同的操作
共有四种操作:搜索数据（直接显示数据等同于搜索关键字全为空），排序，删除数据，更新数据

1.进行搜索(全局搜索)时不需要关心sort,del,update信息,每次进行搜索操作,前端需要把sort_info,del_info,update_info设为'none'
if sort_info='none' and del_info='none' and update_info='none':
    跳转到搜索(search_info)

2.进行排序(全局排序)时不需要关心search,del,update信息,每次进行排序操作,前端需要把search_info,del_info,update_info设为'none'
if sort_info!='none':
    跳转到排序(sort_info)

3.如果是在排序的基础上进行更新操作,执行更新操作后,需要跳转到排序操作;如果是在搜索的基础上进行更新操作,执行更新操作后,需要跳转到搜索操作
if update_info!='none'：
    if sort_info!='none'：
        跳转到更新(update_info, sort_info)
        执行更新操作后跳转到排序(sort_info)
    if sort_info=='none':
        跳转到更新(update_info, search_info)
        执行更新操作后跳转到搜索(search_info)

4.del操作和update操作类似
"""
@app.route('/getargs/')
def getArgs():
    page = request.args.get('Page', 1, type=int)
    search_info = request.args.get('SearchInfo', '', type=str)
    del_info = request.args.get('DelInfo', '', type=str)
    update_info = request.args.get('UpdateInfo', '', type=str)
    sort_info = request.args.get('SortInfo', '', type=str)
    add_info = request.args.get('AddInfo', '', type=str)
    print page, del_info, sort_info, update_info, search_info, add_info
    if del_info=='none' and sort_info=='none' and update_info=='none' and add_info=='none':
        print '进行查找操作'
        return redirect(url_for('search', search_info=search_info, page=page))
    if sort_info!='none' and del_info=='none' and update_info=='none' and add_info=='none':
        print '进行排序操作'
        return redirect(url_for('sort', page=page, sort_info=sort_info))
    if update_info!='none':
        print '进行更新操作'
        update_event(update_info=update_info)
        if sort_info!='none':
            print '更新操作执行完毕，按原样进行排序', sort_info
            return redirect(url_for('sort', page=page, sort_info=sort_info))
        else:
            print '更新操作执行完毕，按原样进行搜索', search_info
            return redirect(url_for('search', page=page, search_info=search_info))
    if del_info!='none':
        print '进行删除操作'
        del_event(del_info=del_info)
        if sort_info!='none':
            print '删除操作执行完毕，按原样进行排序', sort_info
            return redirect(url_for('sort', page=page, sort_info=sort_info))
        else:
            print '删除操作执行完毕，按原样进行搜索', search_info
            return redirect(url_for('search', page=page, search_info=search_info))
    if add_info!='none':
        print '进行添加操作'
        add_event(add_info=add_info)
        if sort_info!='none':
            print '添加操作执行完毕，按原样进行排序', sort_info
            return redirect(url_for('sort', page=page, sort_info=sort_info))
        else:
            print '添加操作执行完毕，按原样进行搜索', search_info
            return redirect(url_for('search', page=page, search_info=search_info))


@app.route('/sort/<sort_info>/<int:page>', methods=['GET', 'POST'])
def sort(sort_info='', page=1):
    #page = request.args.get('Page', 2, type=int)
    #keyword = request.args.get('Keyword', '', type=str)
    #sort = request.args.get('Sort', '', type=str)
    print sort_info, page
    sort_info = sort_info.split('&')
    sort_info = ['' if x=='undefined' else x for x in sort_info]
    keyword = sort_info[0]
    sort = sort_info[1]
    print page, keyword, sort
    print getattr(getattr(Event, keyword),sort)()
    total_num = Event.query.filter().count()
    '''根据变量来调用类对应的属性和方法，这里需要用到python的自省和反射,getattr(obj, attr)将返回obj中名为attr的属性的值'''
    paginate = Event.query.filter(Event.StartDate>CURRENT_DATE).order_by(getattr(getattr(Event,keyword), sort)()).paginate(page, PAGE_SIZE, False)
    #paginate = Event.query.order_by(Event.StartDate.asc(), Event.CityName.asc(),Event.ExpoName.asc()).paginate(page, PAGE_SIZE, False)
    events = []
    pagination = {}
    pagination['total_num'] = total_num
    pagination['num'] = total_num
    pagination['total_pages'] = paginate.pages
    pagination['current_page'] = page
    #pagination['paginate'] = paginate
    events.append(pagination)
    object_list = paginate.items
    for i in object_list:
        event = {}
        event['ID'] = i.ID
        event['Itemid'] = i.Itemid
        event['Sid'] = i.Sid
        event['ExpoName'] = i.ExpoName
        event['UnitCode'] = i.UnitCode
        event['UnitName'] = i.UnitName
        #event['UnitNameEn'] = i.UnitNameEn
        event['CityName'] = i.CityName
        event['StartDate'] = i.StartDate
        event['EndDate']  = i.EndDate
        event['Site'] = i.Site
        event['Exhibitor'] = i.Exhibitor
        event['Visitor'] = i.Visitor
        event['ExpoArea'] = i.ExpoArea
        event['GetDate'] = i.GetDate
        events.append(event)
    return jsonify(result=events)


@app.route('/search/<search_info>/', methods=['GET','POST'])
@app.route('/search/<search_info>/<int:page>', methods=['GET','POST'])
def search(search_info='', page=1):
    expo_name, city_name, start_date, sid, itemid, unit_code, unit_name='','','','','','',''
    print search_info, page
    if search_info != 'none':
        search_info = ['' if x=='undefined' else x for x in search_info.split('&')]
        print search_info
        expo_name = search_info[0]
        start_date = search_info[1]
        city_name = search_info[2]
        sid = search_info[3]
        itemid = search_info[4]
        unit_name = search_info[5]
        unit_code = search_info[6]
        print expo_name, city_name, start_date, sid, itemid, unit_code, unit_name
    try:
        total_num = Event.query.filter().count()
        num = Event.query.filter(Event.StartDate>CURRENT_DATE, Event.ExpoName.like('%'+expo_name+'%'), Event.CityName.like('%'+city_name+'%'), Event.UnitName.like('%'+unit_name+'%'), Event.StartDate.like('%'+start_date+'%')).count()
        paginate = Event.query.filter(Event.StartDate>CURRENT_DATE, Event.ExpoName.like('%'+expo_name+'%'), Event.CityName.like('%'+city_name+'%'), Event.UnitName.like('%'+unit_name+'%'), Event.StartDate.like('%'+start_date+'%'), Event.Sid.like('%'+sid+'%'), Event.Itemid.like('%'+itemid+'%')).order_by(Event.StartDate.asc(), Event.CityName.asc(),Event.ExpoName.asc()).paginate(page, PAGE_SIZE, False)
        #paginate = Event.query.all().paginate(page, PAGE_SIZE, False)
    except Exception,e:
        print 'Error:',e
        result = '未找到数据'
        return render_template('back.html', result=result)
    else:
        print paginate.pages
        if not paginate.pages:
            result = '未找到数据'
            result = json.dumps(result)
            return render_template('back.html', result=result)
        else:
            print '共%s页数据,当前%s页'%(paginate.pages,page)
            events = []
            pagination = {'total_num':total_num, 'num':num, 'total_pages':paginate.pages, 'current_page':page, 'per_page':PAGE_SIZE}
            events.append(pagination)
            object_list = paginate.items
            for i in object_list:
                event = {}
                event['ID'] = i.ID
                event['Itemid'] = i.Itemid
                event['Sid'] = i.Sid
                event['ExpoName'] = i.ExpoName
                event['UnitCode'] = i.UnitCode
                event['UnitName'] = i.UnitName
                #event['UnitNameEn'] = i.UnitNameEn
                event['CityName'] = i.CityName
                event['StartDate'] = i.StartDate
                event['EndDate']  = i.EndDate
                event['Site'] = i.Site
                event['Exhibitor'] = i.Exhibitor
                event['Visitor'] = i.Visitor
                event['ExpoArea'] = i.ExpoArea
                event['GetDate'] = i.GetDate
                events.append(event)
            return jsonify(result=events)     #返回数据到ajax


@app.route('/delete/<del_info>/', methods=['GET','POST'])
def del_event(del_info=''):
    event_ids = del_info.split('&')
    print event_ids
    for event_id in event_ids:
        print event_id
        print '准备删除ID为%s的数据'%event_id
        #db.session.execute('delete from eventlist_201603_only where ID=%s'%event_id)
        del_result = Event.query.filter(Event.ID == event_id).delete()
        print del_result
        if del_result:
            db.session.commit()
            print 'ID为%s的数据已删除'%event_id
        else:
            print 'ID为%s的数据删除失败'%event_id
    return


@app.route('/update/<update_info>', methods=['GET', 'POST'])
def update_event(update_info=''):
    print update_info
    update_info = ['' if x=='undefined' else x for x in update_info.split('&')]
    print update_info
    event_id = update_info[0]
    keyword = update_info[1]
    value = update_info[2]
    print event_id, keyword, value
    try:
        db.session.execute('update %s set %s="%s" where ID=%s'%(TABLE_NAME, keyword, value, event_id))
        p = Event.query.get(event_id)
        #getattr(p, keyword) = value
        #print p.ExpoName
    except Exception, e:
        print 'Error:', e
        result = u'修改失败'
        print result
        return
    else:
        db.session.commit()
        print '修改ID为%s的%s的值为%s'%(event_id, keyword, value)
        return


@app.route('/add/<add_info>/', methods=['POST'])
def add_event(add_info=''):
    print add_info
    add_info = ['' if x=='undefined' else x for x in add_info.split('&')]
    print add_info
    itemid = add_info[0]
    sid = add_info[1]
    expo_name = add_info[2]
    unit_code = add_info[3]
    unit_name = add_info[4]
    city_name = add_info[5]
    start_date = add_info[6]
    end_date = add_info[7]
    site = add_info[8]
    exhibitor = add_info[9]
    visitor = add_info[10]
    expo_area = add_info[11]
    get_date = add_info[12]
    print itemid, sid, expo_name, unit_code, unit_name, city_name, start_date, end_date, site, exhibitor, visitor, expo_area, get_date
    new_event = Event(itemid, sid, expo_name, unit_code, unit_name, city_name, start_date, end_date, site, exhibitor, visitor, expo_area)
    result = db.session.add(new_event)
    db.session.commit()
    return


if __name__ == '__main__':
  app.run(host='0.0.0.0', port = 8080, debug=True)