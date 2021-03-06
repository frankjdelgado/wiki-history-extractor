from db_connector import RevisionDB
import datetime

class QueryHandler(object):
    data={}
    #function which get the quantity of revisions

    #tested
    @classmethod
    def filter_by_user(self,values):
        #values is a list composed by 1 value, the user name to filter by
        data={'user':values[0]}
        return data
    
    @classmethod
    def filter_by_tag(self,values):
        #values is a list composed by 1 value, the tag to filter by
        #NOTE: if necesary, it can be added a functionality to filter by multiple tags with logical OR, AND, XOR, etc.
        data={'tags':values[0]}
        return data

    @classmethod
    def filter_by_size(self,values):
        #values is a list composed by 2 values, the size to filter by, and the order of filtering
        # when the order is greater than 0, it will return the revisions which size are greater than the argument
        # when the order is lesser than 0, it will return the revisions which size are lesser than the argument
        # if the order is 0, it will return the revisions which size are exactly as the argument
        if values[1] > 0:
            data={'size': {'$gt': values[0]} }
        elif values[1] < 0:
            data={'size': {'$lt': values[0]} }
        else:
            data={'size':values[0] }
        return data

    @classmethod
    def filter_by_date(self,values):
        date_format = '%Y-%m-%d'
        #values is a list composed by 1 or 2 values: 
        # date arguments must be in format: YYYY-MM-DD
        # 1 value: one date. It will return the revisions made that date.
        # 2 values: two dates. It will return the revisions made between those dates, inclusive
        # 2 values: one date and one integer. 
        # If the integer is -1: It will return the revisions made from the first revision until the date.
        # If the integer is 1: It will return the revisions made from the date until the last revision.
        # the strptime convert the string arguments into datetime datatype
        if len(values) == 1:
            date_i=datetime.datetime.strptime(values[0],date_format)
            #it is used 2 dates to extract the revision for the whole day, from 0:0 to 23:59
            date_f=date_i.replace(hour=23,minute=59,second=59)
            data={'timestamp': {'$gte':date_i , '$lte':date_f} }
            return data
        elif len(values) == 2:
            #if the second argument is a date:
            if values[1] != 1 and values[1] != -1 :
                date_i=datetime.datetime.strptime(values[0],date_format)
                date_f=datetime.datetime.strptime(values[1],date_format)
                #the date values are adjusted to take into account the day until 23:59
                date_f=date_f.replace(hour=23,minute=59,second=59)
                data={'timestamp': {'$gte':date_i , '$lte':date_f} }
                return data
            else:
                if values[1] == 1:
                    date=datetime.datetime.strptime(values[0],date_format)
                    data={'timestamp': {'$gte':date} }
                    return data
                else:
                    date=datetime.datetime.strptime(values[0],date_format)
                    #the date values are adjusted to take into account the day until 23:59
                    date=date.replace(hour=23,minute=59,second=59)
                    data={'timestamp': {'$lte':date} }
                    return data

    @classmethod
    #the filter allows multiple filters, based on the attribute argument
    # 1111 - 0000 -> 1 on . 0 off
    # 1XXX apply user filter
    # X1XX apply tag filter
    # XX1X apply size filter
    # XXX1 apply date filter 
    def filter_by(self,attribute,values):
        token=attribute
        query={}
        valueslist=values
        option=False
        if token / 1000 == 1:
            query.update(self.filter_by_user(valueslist))
            del valueslist[0]
            option=True
        token= token % 1000 
        if token / 100 == 1:
            query.update(self.filter_by_tag(values))
            del valueslist[0]
            option=True
        token= token % 100 
        if token / 10 == 1:
            query.update(self.filter_by_size(values))
            del valueslist[0]
            del valueslist[0]
            option=True
        token= token % 10 
        if token == 1:
            query.update(self.filter_by_date(values))
            option=True
        if option==False:
            print 'Wrong Filter Option'
            return ''
        else:
            return query
        
    @classmethod
    def get_count(self,filter_by_attribute,values):
        data=self.filter_by(filter_by_attribute,values)
        if data!='':
            return RevisionDB.count(data)

    @classmethod
    #1 for user,2 for tag, 3 for size
    #besides the values required to filter(eg: username for user filtering, size and order for size filtering), it requires 2 values, as with date filtering for 2 dates-interval
    def get_avg(self,filter_by_attribute,values):
        # the filter to set avg is converted in a code with date filtering included
        code=2
        if filter_by_attribute==1:
            code=1001
        elif filter_by_attribute==2:
            code=101
        elif filter_by_attribute==3:
            code=11
        else:
            code=2
        data=self.filter_by(code,values)
        date_format = '%Y-%m-%d'
        #the dates are extracted and it is calculated the number of days with the .days function (datetime.timedelta library)
        date_i=datetime.datetime.strptime(values[len(values)-2],date_format)
        date_f=datetime.datetime.strptime(values[len(values)-1],date_format)
        days=(date_f-date_i).days
        if data!='':
            res= RevisionDB.count(data)
            return res/(days*1.0)

    @classmethod
    #function that gets the mode for an attribute, for now it works with users and size, because tags are mostly empty
    #and date formats needs to be updated in the database(extractor)
    def get_mode(self,filter_by_attribute):
        #it is created the projection for the query
        projection={'_id':0}
        attribute=''
        if filter_by_attribute==1:
            projection.update({'user':1})
            attribute='user'
        elif filter_by_attribute==2:
            projection.update({'size':1})
            attribute='size'
#        elif filter_by_attribute==3:
#            projection.update({'tags':1})
#            attribute='tags'
#        elif filter_by_attribute==4:
#            projection.update({'timestamp':1})
#            attribute='timestamp'
        else:
            projection=''
        
        if projection!='':
            revisions=RevisionDB.find_query(projection)
            valueslist=[]
            repetitionslist=[]
            #after collect the projected revisions, it is checked which values appears most,
            #adding them to a list, and keeping track of their appearances on another list
            for rev in revisions:
                if not (rev[attribute] in valueslist) :
                    valueslist.append(rev[attribute])
                    repetitionslist.append(1)
                else:
                    position= valueslist.index(rev[attribute])
                    repetitionslist[position]=repetitionslist[position]+1
            
            # it is calculated the value most repeated
            maxi=max(repetitionslist)
            mode=[]
            i=0
            #it is created a list with all values tied as mode
            for r in repetitionslist:
                if r==maxi:
                    if isinstance(valueslist[i],unicode) :
                    #in case of string, it is converted from unicode
                        mode.append(str(valueslist[i]))
                    else:
                        mode.append(valueslist[i])
                i=i+1
            return mode
    

    @classmethod
    #test method for inserting formatted timestamps
    def insert_dates(self):
        RevisionDB.insert_date()
        

